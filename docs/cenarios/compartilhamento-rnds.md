# Cenário: Compartilhamento via RNDS

## Descrição

Publicar dado clínico na **Rede Nacional de Dados em Saúde** ou consumir
dado dela para apresentar ao profissional de saúde. O cenário envolve
padrões técnicos (FHIR), autenticação institucional (ICP-Brasil) e
governança (Decreto 12.560/2025).

Cobre:

- Estabelecimento que **publica** laudo/vacina/atendimento.
- Sistema que **consulta** histórico do paciente.
- Mapeamento de identificadores (CPF/CNS ↔ *resources* FHIR).
- Registro local do envio/consulta.

## Riscos

| Risco | Consequência |
|---|---|
| Publicar sem certificado do estabelecimento | RNDS rejeita; mas se aceitar por bug, dado sem autenticidade |
| Consultar CPF sem finalidade declarada | Viola Decreto 12.560/2025 e Decreto 10.046/2019 |
| Replicar em local dataset baixado da RNDS sem base legal | Viola LGPD Art. 7º e Art. 46 |
| Usar padrão FHIR desatualizado | Quebra de integração |
| Não registrar envio/consulta localmente | Sem evidência para auditoria |

## Normas aplicáveis

- [Decreto 12.560/2025 (RNDS)](../normas/ms-datasus/rnds-12560-2025.md).
- [Portaria 3.232/2024 (SUS Digital)](../normas/ms-datasus/sus-digital-3232-2024.md).
- [ESD28 (Portaria 1.434/2020)](../normas/ms-datasus/esd28-1434-2020.md).
- [Decreto 10.046/2019 (governança de compartilhamento)](../normas/apf-seguranca/README.md).
- [LGPD Art. 11 II "b" e "c"](../normas/lgpd/README.md).

## Requisitos mínimos

### Para publicar (estabelecimento → RNDS)

- [ ] Certificado digital **ICP-Brasil A1/A3** do estabelecimento (CNES).
- [ ] Adapter FHIR R4 aderente ao catálogo do MS.
- [ ] Tabela local `rnds_outbox` com status (`pending`, `sent`, `failed`,
      `acked`) e resposta da RNDS.
- [ ] Retry com *backoff* exponencial e *dead-letter*.
- [ ] Registro local do envio — quem, quando, qual recurso, resposta.
- [ ] Monitoramento de fila e alerta de falha.

### Para consumir (profissional consulta RNDS via sistema local)

- [ ] Autenticação do profissional via gov.br ou federação institucional
      com vínculo ao CPF.
- [ ] Campo **finalidade** da consulta registrado (ex.: "atendimento
      emergencial", "continuidade de cuidado").
- [ ] Token de acesso com escopo mínimo.
- [ ] Trilha local: `rnds_query` com usuário, CPF consultado mascarado,
      finalidade, timestamp, recursos consultados.
- [ ] Cache local com retenção curta e limpa; sem replicação persistente
      sem justificativa.

## Padrão de implementação

### Outbox de publicação

```python
# NOTE: atende Decreto 12.560/2025 - rastreabilidade de envio a RNDS.
class RNDSOutboxItem(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pendente"),
        ("sent", "Enviado"),
        ("acked", "Confirmado"),
        ("failed", "Falha"),
    ]
    resource_type = models.CharField(max_length=64)  # ex.: "Observation"
    resource_id = models.CharField(max_length=64)
    payload_hash = models.CharField(max_length=64)  # sha256 do body
    status = models.CharField(max_length=16, choices=STATUS_CHOICES)
    last_error = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

Enviar por job assíncrono (Celery/RQ) com idempotência via
`payload_hash`.

### Registro de consulta

```python
class RNDSQuery(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    patient_cpf_masked = models.CharField(max_length=20)  # '***.***.***-12'
    purpose = models.CharField(max_length=128)  # finalidade declarada
    resources_requested = models.JSONField(default=list)
    response_status = models.IntegerField()
    ip = models.GenericIPAddressField()
    created_at = models.DateTimeField(auto_now_add=True)
```

## Armadilhas comuns

- **"Cache da RNDS para agilizar"** — replicação silenciosa viola modelo
  federado.
- **Consultar "todos os exames do CPF"** sem finalidade — viola menor
  privilégio e governança.
- **Publicar em homolog da RNDS com dado real** — homolog é homolog, use
  sintético.

## Como testar conformidade

1. **Test** de outbox: publicação com falha → fica em `failed`, re-tentativa
   move para `sent` quando RNDS responder 200.
2. **Test** de idempotência: reenvio do mesmo payload gera nova tentativa
   mas não duplica recurso (*hash* confere).
3. **Test** de trilha: cada consulta à RNDS cria `RNDSQuery` com
   `purpose` não vazio.
4. **Scan** de logs: nenhum CPF em claro nos logs de envio/consulta.

## Versão consultada

Este cenário **não substitui** a documentação oficial da RNDS, que muda
com frequência. Consulte sempre:

- <https://rnds-guia.saude.gov.br/>
- Catálogos FHIR do MS.
- Termo de adesão do estabelecimento.
