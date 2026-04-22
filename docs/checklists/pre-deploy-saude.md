# Checklist — Pré-deploy de sistema de saúde digital

Gate final antes de qualquer go-live que envolva dado pessoal ou
sensível em produção.

## Documentação vinculante

- [ ] Política de privacidade **publicada** em URL estável.
- [ ] Termo de uso **publicado** e versionado.
- [ ] DPO/Encarregado identificado com contato publicado.
- [ ] Runbook de incidente no repositório.

## Código e infraestrutura

- [ ] `DEBUG = False`.
- [ ] `ALLOWED_HOSTS` restrito ao domínio de produção.
- [ ] `SECURE_SSL_REDIRECT = True`, HSTS ≥1 ano.
- [ ] Cookie de sessão `Secure`, `HttpOnly`, `SameSite`.
- [ ] `SECRET_KEY` e credenciais **fora** do VCS (cofre / env var).
- [ ] TLS ≥1.2 no endpoint público.
- [ ] Certificado válido (A+ no Qualys SSL Labs recomendado).
- [ ] Backup automático + **teste de restore** no último mês.
- [ ] Monitoramento e alerta para logs de aplicação.

## Banco de dados

- [ ] Usuários segregados (`app_writer`, `app_reader`, `auditor`,
      `admin`).
- [ ] `GRANT` restrito por schema.
- [ ] Trilha de auditoria com ACL append-only.
- [ ] `log_statement != 'all'` em Postgres.
- [ ] Criptografia em repouso.

## Autenticação e autorização

- [ ] Hash de senha ≥160 bits.
- [ ] Política 8/1/1.
- [ ] Bloqueio após N tentativas.
- [ ] Inatividade encerra sessão.
- [ ] RBAC server-side.
- [ ] Ao menos 1 admin ativo (invariante).

## Dados

- [ ] Homologação com dado sintético/anonimizado.
- [ ] Log de aplicação sem CPF/senha em claro.
- [ ] Exportação/portabilidade testada.

## LGPD / regulatório

- [ ] RIPD/DPIA documentado (se tratamento de alto risco).
- [ ] Contrato com operadores (cloud, fornecedores) com cláusulas LGPD.
- [ ] Transferência internacional sob CPC se aplicável.
- [ ] Base legal de cada finalidade documentada.

## Auditoria (SBIS NGS1.07)

- [ ] `LoginEvent` com IP/UA/UTC.
- [ ] Tela de consulta com filtros.
- [ ] Exportação com metadados institucionais.

## Pesquisa (se aplicável)

- [ ] CAAE de cada projeto registrado.
- [ ] Dataset de pesquisa via view pseudonimizada.
- [ ] Retenção ≥5 anos (Res. CNS 738/2024).

## Cloud / MS (se aplicável)

- [ ] Região Brasil contratualmente garantida.
- [ ] Cláusula de auditoria pelo órgão.
- [ ] Export em formato aberto ao fim do contrato.

---

## Como aplicar este checklist no CI

Sugestão de automação (não obrigatório):

```yaml
# .github/workflows/pre-deploy.yml
name: pre-deploy
on:
  pull_request:
    branches: [main]
jobs:
  lint-settings:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Block DEBUG=True in production settings
        run: |
          ! grep -R "^DEBUG = True" config/settings/production.py
      - name: Check SECURE_SSL_REDIRECT
        run: grep -q "SECURE_SSL_REDIRECT = True" config/settings/production.py
```

Integrar com `bandit`, `pip-audit`, `semgrep` conforme a stack.
