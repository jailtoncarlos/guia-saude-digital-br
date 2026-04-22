"""AppConfig que registra os signals de auditoria."""
from __future__ import annotations

from django.apps import AppConfig


class AuditConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "audit"

    def ready(self) -> None:
        # import com efeito colateral: registrar receivers.
        from audit import signals  # noqa: F401
