"""Trilha de auditoria - append-only.

NOTE: atende SBIS NGS1.07 + Marco Civil Art. 15 + LGPD Art. 46.

Em producao, alem do model Django:
- Conceder apenas INSERT na tabela para a credencial da aplicacao.
- Conceder SELECT apenas para credencial separada do auditor.
- Nao permitir UPDATE/DELETE - ver docs/cenarios/auditoria.md para SQL.
"""
from __future__ import annotations

from django.conf import settings
from django.db import models


class EventType(models.TextChoices):
    LOGIN_SUCCESS = "login_success", "Login com sucesso"
    LOGIN_FAILURE = "login_failure", "Tentativa de login com falha"
    LOGIN_BLOCKED = "login_blocked", "Tentativa em conta bloqueada"
    LOGOUT = "logout", "Logout"
    SESSION_EXPIRED = "session_expired", "Sessao encerrada por inatividade"
    PASSWORD_CHANGE = "password_change", "Senha alterada pelo usuario"
    PASSWORD_RESET_REQUEST = "password_reset_request", "Solicitacao de reset de senha"
    USER_CREATED = "user_created", "Usuario criado"
    USER_UPDATED = "user_updated", "Usuario atualizado"
    USER_DEACTIVATED = "user_deactivated", "Usuario desativado"
    ROLE_GRANTED = "role_granted", "Permissao concedida"
    ROLE_REVOKED = "role_revoked", "Permissao revogada"
    SENSITIVE_DATA_ACCESS = "sensitive_data_access", "Acesso a dado sensivel"
    DATA_EXPORT = "data_export", "Exportacao de dados"
    AUDIT_TRAIL_VIEW = "audit_trail_view", "Consulta a trilha de auditoria"


class FailureReason(models.TextChoices):
    INVALID_CREDENTIALS = "invalid_credentials", "Credenciais invalidas"
    USER_INACTIVE = "user_inactive", "Usuario inativo"
    USER_LOCKED = "user_locked", "Usuario bloqueado"
    OTHER = "other", "Outro"


class LoginEvent(models.Model):
    """Evento de autenticacao / gestao de usuario.

    NOTE: atende SBIS NGS1.07.05 - campos obrigatorios
    (IP, usuario, tipo, data/hora).
    """

    # Pode ser NULL em login_failure quando o CPF nao existe no banco.
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="login_events",
    )
    cpf_attempted = models.CharField(
        max_length=20,  # mascarado, ex. '***.***.***-12'
        blank=True,
        help_text="CPF mascarado tentado (para pre-autenticacao).",
    )
    event_type = models.CharField(max_length=32, choices=EventType.choices, db_index=True)
    failure_reason = models.CharField(
        max_length=32,
        choices=FailureReason.choices,
        blank=True,
    )
    ip = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=512, blank=True)
    session_key = models.CharField(max_length=40, blank=True)
    extra = models.JSONField(default=dict, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = "evento de auditoria"
        verbose_name_plural = "eventos de auditoria"
        indexes = [
            models.Index(fields=["event_type", "created_at"]),
            models.Index(fields=["user", "created_at"]),
        ]

    def __str__(self) -> str:
        return f"{self.event_type} @ {self.created_at.isoformat()}"

    def save(self, *args, **kwargs) -> None:  # type: ignore[override]
        # Proibir UPDATE - append only. NOTE: atende SBIS NGS1.07.02.
        if self.pk is not None:
            raise ValueError("LoginEvent e append-only; UPDATE nao permitido.")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):  # type: ignore[override]
        raise ValueError("LoginEvent e append-only; DELETE nao permitido.")
