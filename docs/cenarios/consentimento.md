# Cenário: Consentimento, Termo de Uso e TCLE

## Descrição

Três instrumentos diferentes, frequentemente confundidos:

| Instrumento | Quando usar | Base normativa |
|---|---|---|
| **Termo de Uso** do sistema | Todo usuário, no primeiro acesso | SBIS NGS1.11.01 + LGPD Art. 6º VI |
| **Consentimento LGPD** específico | Quando a base legal é consentimento (Art. 7º I / Art. 8º / Art. 11 I) | LGPD |
| **TCLE** — Termo de Consentimento Livre e Esclarecido | Participação em pesquisa | Lei 14.874/2024 + Res. CNS 738/2024 |

Este cenário cobre os três.

## Riscos

| Risco | Consequência |
|---|---|
| Tratar "aceite do termo de uso" como base legal LGPD | Erro de base — termo de uso é contrato de serviço, não consentimento |
| Consentimento genérico "aceito tudo" para dado sensível | Viola LGPD Art. 11 — exige especificidade |
| Não versionar o termo | Impossível provar qual texto o usuário aceitou |
| Não permitir revogação de consentimento | Viola LGPD Art. 8º §5º |
| TCLE em sistema assistencial por engano | Confunde base legal do tratamento |

## Normas aplicáveis

- [LGPD Art. 6º VI, Art. 7º, Art. 8º, Art. 11](../normas/lgpd/README.md).
- [Guia ANPD Poder Público 2024](../normas/anpd/guia-poder-publico-2024.md).
- [SBIS NGS1.11.01](../normas/sbis-cfm/README.md).
- [Lei 14.874/2024 (TCLE)](../normas/pesquisa-inaep/lei-14874-2024.md).
- [Res. CNS 738/2024 (bancos de dados em pesquisa)](../normas/pesquisa-inaep/resolucao-cns-738-2024.md).

## Termo de Uso

### Requisitos mínimos

- [ ] Exibido no primeiro acesso, antes de qualquer uso do sistema.
- [ ] Texto versionado (`TermsVersion` com `version`, `text`,
      `created_at`).
- [ ] Aceite registrado (`TermsAcceptance` com `user`, `terms_version`,
      `accepted_at`, `ip`).
- [ ] Nova versão → usuário é redirecionado ao aceite no próximo login.
- [ ] Usuário pode baixar o texto aceito (PDF / cópia do Markdown).

Ver [`templates/termo-de-uso.md.tpl`](../../templates/termo-de-uso.md.tpl)
e o middleware em
[`examples/django-auth-lgpd-compliant/terms/middleware.py`](../../examples/django-auth-lgpd-compliant/terms/middleware.py).

### Distinção importante

Aceitar termo de uso **não é** dar consentimento LGPD. O termo diz "como o
sistema funciona e quais são seus deveres"; a base legal do tratamento
vem separada (obrigação legal / política pública / consentimento
específico).

## Consentimento LGPD específico

Quando usado:

- Sistema privado sem outra base legal adequada.
- Tratamento adicional à finalidade principal (marketing, analytics com
  dado identificável).
- Dado sensível sem hipótese do Art. 11 II aplicável.

### Requisitos mínimos

- [ ] **Específico por finalidade** — "aceito receber notificação sobre
      vacinação" é diferente de "aceito compartilhamento com fornecedor X".
- [ ] **Destacado** — não pode ser cláusula enterrada em termo de uso.
- [ ] **Granular** — um checkbox por finalidade.
- [ ] **Revogável a qualquer tempo**, sem ônus (Art. 8º §5º).
- [ ] Registro versionado do consentimento (data, IP, texto, finalidade).

### Modelo de dados sugerido

```python
class ConsentPurpose(models.Model):
    code = models.CharField(max_length=64, unique=True)
    description = models.TextField()
    is_sensitive = models.BooleanField(default=False)


class Consent(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    purpose = models.ForeignKey(ConsentPurpose, on_delete=models.PROTECT)
    granted = models.BooleanField()  # False = revogado
    version = models.CharField(max_length=16)
    ip = models.GenericIPAddressField()
    created_at = models.DateTimeField(auto_now_add=True)
```

Cada mudança cria **nova linha** — tabela é append-only, permite histórico.

## TCLE — Termo de Consentimento Livre e Esclarecido

Aplicável **apenas** em sistema de pesquisa. Características:

- **Por projeto** (CAAE) — não é termo de uso do sistema.
- Aprovado por CEP / Inaep antes de ser exibido.
- **Participante pode retirar consentimento** — desde que os dados não
  tenham sido anonimizados irreversivelmente.
- Retenção **mínima 5 anos** (Res. CNS 738/2024).

Ver [`docs/normas/pesquisa-inaep/`](../normas/pesquisa-inaep/).

## Como testar conformidade

1. **Test** de termo de uso: nova versão criada → usuário é redirecionado
   para aceite; sem aceite, view principal retorna 302.
2. **Test** de consentimento específico: marcar finalidade A não marca
   finalidade B.
3. **Test** de revogação: `Consent.granted=False` não apaga histórico —
   cria nova linha.
4. **UI test**: consentimento **não** pode ser pré-marcado
   (pré-preenchimento = vicia o consentimento, segundo orientação ANPD).
5. **Test** de TCLE: TCLE associado a `research.project` (CAAE) e
   identificador do participante, não ao `User` geral.
