"""Signals do Django transformados em LoginEvent.

NOTE: atende SBIS NGS1.07.03 - eventos de autenticacao e gestao.

Plugue este modulo via `apps.py`:

    class AuditConfig(AppConfig):
        default_auto_field = "django.db.models.BigAutoField"
        name = "audit"
        def ready(self):
            from audit import signals  # noqa: F401
"""
from __future__ import annotations

import logging
from typing import Any

from django.contrib.auth import get_user_model
from django.contrib.auth.signals import (
    user_logged_in,
    user_logged_out,
    user_login_failed,
)
from django.dispatch import receiver
from django.http import HttpRequest

from accounts.validators import mask_cpf
from audit.models import EventType, FailureReason, LoginEvent

logger = logging.getLogger("audit")
User = get_user_model()


def _ctx(request: HttpRequest | None) -> dict[str, Any]:
    if request is None:
        return {"ip": None, "user_agent": "", "session_key": ""}
    return dict(getattr(request, "audit_context", {})) or {
        "ip": None,
        "user_agent": "",
        "session_key": "",
    }


@receiver(user_logged_in)
def on_user_logged_in(sender, request, user, **kwargs):  # type: ignore[no-untyped-def]
    ctx = _ctx(request)
    LoginEvent.objects.create(
        user=user,
        event_type=EventType.LOGIN_SUCCESS,
        ip=ctx.get("ip") or None,
        user_agent=ctx.get("user_agent", ""),
        session_key=ctx.get("session_key", ""),
    )
    # Atualiza info de ultimo login e reseta contador. NOTE: NGS1.02.15 / 02.13.
    user.update_last_login_info(ctx.get("ip"), ctx.get("user_agent"))
    user.reset_failed_logins()
    logger.info("login_success cpf=%s ip=%s", mask_cpf(user.cpf), ctx.get("ip"))


@receiver(user_logged_out)
def on_user_logged_out(sender, request, user, **kwargs):  # type: ignore[no-untyped-def]
    if user is None:
        return
    ctx = _ctx(request)
    LoginEvent.objects.create(
        user=user,
        event_type=EventType.LOGOUT,
        ip=ctx.get("ip") or None,
        user_agent=ctx.get("user_agent", ""),
        session_key=ctx.get("session_key", ""),
    )


@receiver(user_login_failed)
def on_user_login_failed(sender, credentials, request, **kwargs):  # type: ignore[no-untyped-def]
    ctx = _ctx(request)
    cpf_raw = credentials.get("username") or credentials.get("cpf") or ""
    # Se o chamador nao mascarou antes, mascara agora. NOTE: LGPD Art. 46.
    if cpf_raw and "*" not in cpf_raw:
        cpf_masked = mask_cpf(cpf_raw)
    else:
        cpf_masked = cpf_raw

    user = None
    reason = FailureReason.INVALID_CREDENTIALS
    # Tenta resolver user para vincular evento (sem expor CPF em claro).
    if cpf_raw and "*" not in cpf_raw:
        user = User.objects.filter(cpf=cpf_raw).first()
        if user and not user.is_active:
            reason = FailureReason.USER_INACTIVE
        elif user and user.is_locked:
            reason = FailureReason.USER_LOCKED

    LoginEvent.objects.create(
        user=user,
        cpf_attempted=cpf_masked[:20],
        event_type=EventType.LOGIN_FAILURE,
        failure_reason=reason,
        ip=ctx.get("ip") or None,
        user_agent=ctx.get("user_agent", ""),
        session_key=ctx.get("session_key", ""),
    )
    logger.info(
        "login_failure cpf=%s ip=%s reason=%s",
        cpf_masked,
        ctx.get("ip"),
        reason,
    )
