"""Settings de producao focadas em conformidade para saude digital.

Este arquivo consolida as decisoes cobertas em
`docs/cenarios/autenticacao.md` e `docs/checklists/pre-deploy-saude.md`.

Leitura obrigatoria antes de adaptar:
- docs/normas/lgpd/README.md (Art. 46 - medidas de seguranca)
- docs/normas/marco-civil/README.md (Art. 15 - trilha)
- docs/normas/sbis-cfm/README.md (NGS1 Estagio 1)
- docs/normas/apf-seguranca/in-gsi-1-2020.md (controles APF)
"""
from __future__ import annotations

import os
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover
    load_dotenv = None

BASE_DIR = Path(__file__).resolve().parent.parent

if load_dotenv is not None:
    load_dotenv(BASE_DIR / ".env")


def _env_bool(name: str, default: bool) -> bool:
    raw = os.environ.get(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


def _env_int(name: str, default: int) -> int:
    raw = os.environ.get(name)
    if raw is None or not raw.strip():
        return default
    return int(raw)


# --------------------------------------------------------------------------- #
# Basico
# --------------------------------------------------------------------------- #

SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]  # NOTE: atende LGPD Art. 46 - segredo fora do VCS.
DEBUG = _env_bool("DJANGO_DEBUG", default=False)
ALLOWED_HOSTS = [h.strip() for h in os.environ.get("DJANGO_ALLOWED_HOSTS", "").split(",") if h.strip()]

# --------------------------------------------------------------------------- #
# Apps
# --------------------------------------------------------------------------- #

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Template apps (este repo).
    "accounts",
    "audit",
    "terms",
]

# --------------------------------------------------------------------------- #
# Middleware
#
# Ordem importa. O AuditContextMiddleware precisa estar apos
# AuthenticationMiddleware para ter request.user. O TermsAcceptanceMiddleware
# vem depois para redirecionar somente usuarios autenticados.
# --------------------------------------------------------------------------- #

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",

    "audit.middleware.AuditContextMiddleware",        # NOTE: atende Marco Civil Art. 15 + SBIS NGS1.07.05.
    "terms.middleware.TermsAcceptanceMiddleware",     # NOTE: atende SBIS NGS1.11.01.
]

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

# --------------------------------------------------------------------------- #
# Banco de dados
# --------------------------------------------------------------------------- #

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ["DB_NAME"],
        "USER": os.environ["DB_USER"],
        "PASSWORD": os.environ["DB_PASSWORD"],
        "HOST": os.environ.get("DB_HOST", "localhost"),
        "PORT": os.environ.get("DB_PORT", "5432"),
        "OPTIONS": {
            "sslmode": os.environ.get("DB_SSLMODE", "require"),  # NOTE: TLS entre app e banco.
        },
        "CONN_MAX_AGE": 60,
    }
}

# --------------------------------------------------------------------------- #
# Autenticacao
# --------------------------------------------------------------------------- #

AUTH_USER_MODEL = "accounts.User"
LOGIN_URL = "accounts:login"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = LOGIN_URL

# NOTE: atende SBIS NGS1.02.03 (qualidade minima 8/1/1).
# Reforcado por validator custom em accounts.validators (nao versionado
# aqui para nao expandir o exemplo; o template aponta a ideia).
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {"min_length": 8},
    },
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# NOTE: atende SBIS NGS1.02.02 - PBKDF2 com SHA-256 (>=160 bits).
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]

# NOTE: atende SBIS NGS1.02.13 - bloqueio apos N tentativas.
LOGIN_MAX_ATTEMPTS = _env_int("LOGIN_MAX_ATTEMPTS", default=5)
LOGIN_LOCKOUT_MINUTES = _env_int("LOGIN_LOCKOUT_MINUTES", default=15)

# --------------------------------------------------------------------------- #
# Sessao / cookies
# --------------------------------------------------------------------------- #

# NOTE: atende SBIS NGS1.02.23 - protecao contra roubo de sessao.
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Strict"
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True

# NOTE: atende SBIS NGS1.02.20 - inatividade.
SESSION_COOKIE_AGE = _env_int("SESSION_COOKIE_AGE_SECONDS", default=30 * 60)
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_SAVE_EVERY_REQUEST = True  # renova TTL a cada request autenticada

# --------------------------------------------------------------------------- #
# Transporte / HTTPS
# --------------------------------------------------------------------------- #

# NOTE: atende SBIS NGS1.05.01 + LGPD Art. 46.
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = _env_int("SECURE_HSTS_SECONDS", default=31_536_000)  # 1 ano
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = "same-origin"
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

X_FRAME_OPTIONS = "DENY"

# --------------------------------------------------------------------------- #
# Proxy reverso confiavel (para captura correta de IP)
# --------------------------------------------------------------------------- #

# NOTE: AuditContextMiddleware usa essa lista para validar X-Forwarded-For.
# Configure com o CIDR do seu proxy/load balancer.
TRUSTED_PROXIES = [
    p.strip() for p in os.environ.get("TRUSTED_PROXIES", "").split(",") if p.strip()
]

# --------------------------------------------------------------------------- #
# Tempo / timezone
# --------------------------------------------------------------------------- #

# NOTE: atende SBIS NGS1.09.03 - armazenar em UTC.
TIME_ZONE = "UTC"
USE_TZ = True

# --------------------------------------------------------------------------- #
# I18N
# --------------------------------------------------------------------------- #

LANGUAGE_CODE = "pt-br"
USE_I18N = True

# --------------------------------------------------------------------------- #
# Static / media
# --------------------------------------------------------------------------- #

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --------------------------------------------------------------------------- #
# Logging - trilha rotacionada; nunca CPF/senha em claro.
# --------------------------------------------------------------------------- #

LOG_DIR = Path(os.environ.get("DJANGO_LOG_DIR", BASE_DIR / "logs"))
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "masked": {
            # O formatter real vive em audit.logging.MaskingFormatter e
            # aplica mask_cpf() no output antes de escrever.
            "()": "audit.logging.MaskingFormatter",
            "format": "%(asctime)s %(levelname)s %(name)s %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "masked",
        },
        "audit_file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": str(LOG_DIR / "audit.log"),
            "when": "D",
            "backupCount": int(os.environ.get("AUDIT_LOG_RETENTION_DAYS", "365")),
            "formatter": "masked",
        },
    },
    "loggers": {
        "audit": {
            "handlers": ["console", "audit_file"],
            "level": "INFO",
            "propagate": False,
        },
        "django.security": {
            "handlers": ["console", "audit_file"],
            "level": "INFO",
            "propagate": False,
        },
        "django": {
            "handlers": ["console"],
            "level": os.environ.get("DJANGO_LOG_LEVEL", "INFO"),
        },
    },
}
