# django-auth-lgpd-compliant

Template de referência Django para sistema de saúde digital no Brasil com:

- **Auth por CPF** com validação de DV (PNIIS / SBIS NGS1.03.09).
- **Bloqueio após N tentativas** (SBIS NGS1.02.13).
- **Hash PBKDF2** padrão Django (SBIS NGS1.02.02).
- **Política de senha 8/1/1** (SBIS NGS1.02.03).
- **Trilha de auditoria** com IP, UA, tipo de evento, UTC
  (Marco Civil Art. 15 / SBIS NGS1.07).
- **Cookies seguros**, HSTS, SSL redirect
  (LGPD Art. 46 / SBIS NGS1.02.23 / NGS1.05.01).
- **Termo de uso versionado** com aceite forçado no 1º acesso
  (SBIS NGS1.11.01 / LGPD Art. 6º VI).
- **Mascaramento de CPF** em logs.

## Estrutura

```
django-auth-lgpd-compliant/
├── requirements.txt
├── manage.py
├── config/
│   └── settings.py           # configs SECURE_*, AUTH_PASSWORD_VALIDATORS, LOGIN_MAX_ATTEMPTS
├── accounts/
│   ├── models.py             # User custom com CPF, validacao DV, lock
│   ├── managers.py
│   ├── admin.py
│   ├── forms.py              # LoginForm, RegisterForm
│   └── views.py              # login com rate limit
├── audit/
│   ├── models.py             # LoginEvent append-only
│   ├── middleware.py         # captura IP/UA
│   └── signals.py            # handlers de eventos de auth
└── terms/
    ├── models.py             # TermsVersion, TermsAcceptance
    └── middleware.py         # forca aceite no primeiro acesso
```

## Validade

- **Python ≥3.11**.
- **Django ≥5.0**.
- Código é sintaticamente válido. **Não foi otimizado para rodar** — é
  template. Faltam `__init__.py`, migrations, URLs completas, templates
  HTML. Os arquivos presentes são os que concentram decisões de
  conformidade.

## Checklist SBIS mapeado

Cada arquivo tem comentários `# NOTE: atende ...` que apontam o requisito.
Use o [checklist SBIS NGS1](../../docs/checklists/sbis-ngs1-estagio1.md)
para fazer a rastreabilidade no seu projeto.

## Como adaptar para seu projeto

1. Copie as pastas `accounts/`, `audit/` e `terms/` como apps do seu
   Django.
2. Configure `INSTALLED_APPS`, `AUTH_USER_MODEL = 'accounts.User'`,
   `MIDDLEWARE` (adicionando `audit.middleware.AuditContextMiddleware` e
   `terms.middleware.TermsAcceptanceMiddleware`).
3. Adote as *settings* de segurança de `config/settings.py` no seu
   `production.py`.
4. Rode migrations, crie grupos (`admin`, `profissional`, etc.) via data
   migration.
5. Publique o termo de uso inicial via management command (ver
   `terms/models.py` — comentário).
