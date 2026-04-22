# flask-auth-lgpd-compliant (stub)

**Status:** stub — implementação futura.

Este diretório reserva o espaço para um template Flask equivalente ao
[`django-auth-lgpd-compliant`](../django-auth-lgpd-compliant/).

Enquanto não houver implementação, consulte o exemplo Django como
referência conceitual e aplique os mesmos princípios em Flask:

## Equivalências Flask ↔ Django

| Django | Flask equivalente |
|---|---|
| `AbstractBaseUser` + `PermissionsMixin` | `flask-login` + modelo SQLAlchemy com `cpf` como coluna única |
| `UserManager.create_user` | *service layer* Python (`create_user()`) |
| `django.contrib.auth.hashers.PBKDF2` | `werkzeug.security.generate_password_hash` (PBKDF2 padrão, já atende NGS1.02.02) |
| `AUTH_PASSWORD_VALIDATORS` | `password-strength` ou validação custom (NGS1.02.03) |
| Signals `user_logged_in` etc. | blinker signals do Flask ou eventos diretos no endpoint |
| Middleware `AuditContextMiddleware` | `before_request` handler |
| `django-ratelimit` | `flask-limiter` |
| `TermsAcceptanceMiddleware` | `before_request` que redireciona via `url_for` |

## O que preservar ao portar

- CPF como *identifier* único, com validação de DV server-side.
- Hash PBKDF2/Argon2 (werkzeug oferece PBKDF2 por padrão).
- Captura de IP considerando `X-Forwarded-For` (via `werkzeug.middleware.proxy_fix.ProxyFix`).
- Cookie de sessão com `SESSION_COOKIE_SECURE = True`,
  `SESSION_COOKIE_HTTPONLY = True`, `SESSION_COOKIE_SAMESITE = "Strict"`
  em Flask config.
- HSTS via reverse proxy ou `flask-talisman`.
- Trilha de auditoria em tabela `audit_login_event` com os mesmos campos
  (ver `audit/models.py` do exemplo Django).
- Middleware de aceite de termo de uso (flask-login + redirect).

## Contribuições bem-vindas

Um PR implementando este stub é excelente contribuição. Mantenha os
comentários `# NOTE: atende ...` em cada arquivo para preservar a
rastreabilidade normativa.
