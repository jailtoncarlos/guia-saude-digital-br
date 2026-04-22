# Cenário: Armazenamento de dado pessoal sensível

## Descrição

Persistir dado pessoal sensível (diagnóstico, procedimento, exame, CPF/CNS
vinculado) de forma que atenda LGPD, SBIS e boas práticas OWASP.

Cobre:

- Onde guardar (SGBD, não arquivo).
- Como guardar (minimização, pseudonimização quando útil).
- Criptografia em repouso.
- Controle de acesso ao schema.
- Log de acesso a dado sensível.

## Riscos

| Risco | Consequência |
|---|---|
| CSV com dado sensível no filesystem da aplicação | Vazamento trivial em incidente; viola LGPD Art. 46 |
| Schema único para tudo | Qualquer SQL injection expõe tudo |
| Credencial única app ↔ banco com privilégios totais | *Blast radius* extremo |
| Log de query com valor de parâmetro | Dado sensível no `postgresql.log` |
| Dado de produção replicado em homolog | Vazamento por ambiente menor |
| Sem criptografia de volume em repouso | Roubo de disco = vazamento |

## Normas aplicáveis

- [LGPD Art. 5º II, Art. 11, Art. 46](../normas/lgpd/README.md).
- [SBIS NGS1.06.01](../normas/sbis-cfm/README.md) (uso de SGBD).
- [Cloud MS (Portaria 7.678/2025)](../normas/ms-datasus/cloud-7678-2025.md).
- [POSIC/MS](../normas/ms-datasus/posic-ms.md).
- [Res. ANPD 30/2025](../normas/anpd/resolucao-30-2025.md) (prioridade
  2026–2027).
- OWASP Top 10 A02 (cryptographic failures), A04 (insecure design).

## Requisitos mínimos

- [ ] Persistência em **SGBD** (PostgreSQL/MySQL), não em CSV/JSON no FS.
- [ ] **Schema separado** para dado sensível (`clinical.`) vs. dado
      operacional (`app.`, `audit.`).
- [ ] **Usuários de banco** segregados: `app_reader`, `app_writer`,
      `app_admin`, `auditor`, `etl`. Cada um com permissões mínimas.
- [ ] **Criptografia em repouso** no volume (TDE do Postgres ou disco
      criptografado do provedor).
- [ ] **TLS ≥1.2** entre app e banco.
- [ ] `log_statement = 'none'` ou `'ddl'` no Postgres de produção (nunca
      `'all'` em produção — vaza parâmetros).
- [ ] **Masking em log de aplicação** — nunca CPF/diagnóstico em claro.
- [ ] **Homologação com dado sintético** ou anonimizado.
- [ ] **Evento `sensitive_data_access`** na trilha (usuário, CPF
      mascarado, timestamp, finalidade quando aplicável).
- [ ] **Retenção** documentada por tipo de dado (prontuário = regra CFM
      1.821/2007; trilha = ≥6 meses Marco Civil, 5 anos recomendado).

## Padrões de modelagem

### Separação de schemas

```
clinical.   -- dado sensivel de saude (exames, laudos, diagnosticos)
personal.   -- dado pessoal identificador (nome, email, endereco)
app.        -- dado operacional (sessoes, preferencias)
audit.      -- trilha de auditoria (append-only)
research.   -- vistas pseudonimizadas para pesquisa (ver Res. CNS 738/2024)
```

### Pseudonimização para dataset analítico

```sql
-- NOTE: atende LGPD Art. 12 (dado anonimizado) parcial (pseudonimizacao,
-- reversivel); adequar ao proposito do dataset.
CREATE MATERIALIZED VIEW research.exam_result AS
SELECT
    encode(digest(e.patient_cpf || :salt, 'sha256'), 'hex') AS patient_pid,
    e.exam_type,
    e.result_code,
    date_trunc('month', e.collected_at) AS collected_month,
    e.cnes_code
FROM clinical.exam e;
```

Salt armazenado fora do cluster de banco — em cofre.

### Mascaramento em logs

```python
import re

CPF_RE = re.compile(r"\b(\d{3})\.?(\d{3})\.?(\d{3})-?(\d{2})\b")


def mask_cpf(text: str) -> str:
    """Substitui CPFs em string por ***.***.***-XX.

    NOTE: atende LGPD Art. 46 - minimizacao em log.
    """
    return CPF_RE.sub(lambda m: f"***.***.***-{m.group(4)}", text)
```

Aplicar em `Formatter` de logging customizado.

## Como testar conformidade

1. **Scan** de produção em staging: `grep -rE '[0-9]{11}' logs/` — esperar
   zero resultado em logs de aplicação.
2. **Test** de ACL de banco: tentar `SELECT * FROM clinical.exam` com
   credencial `app_writer` limitada → autorizado; com `auditor` →
   negado (só `audit.*`).
3. **Test** de extração: exportar dataset para pesquisa → ler via
   `research.*`, nunca direto do `clinical.*`.
4. **Test** de ambiente: varredura de produção→homolog não replica CPF.
5. **Audit**: `SELECT pg_ls_dir('pg_log')` em produção — nenhum log de
   query com dado em claro.
