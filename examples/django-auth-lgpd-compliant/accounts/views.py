"""Views de autenticacao e cadastro.

Concentram a logica de bloqueio, rate limit e captura de contexto de
trilha. A trilha em si e gravada via signals em `audit.signals`.
"""
from __future__ import annotations

import logging

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.signals import user_login_failed
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from accounts.forms import CPFLoginForm, RegisterForm
from accounts.validators import mask_cpf

try:
    from django_ratelimit.decorators import ratelimit
except ImportError:  # pragma: no cover - dependencia opcional em import-time
    def ratelimit(*a, **k):  # type: ignore[no-redef]
        def deco(view):
            return view
        return deco

logger = logging.getLogger("audit")
User = get_user_model()


# NOTE: atende SBIS NGS1.02.13 + OWASP ASVS V2 - rate limit em /login.
@ratelimit(key="ip", rate="10/m", method="POST", block=True)
def login_view(request: HttpRequest) -> HttpResponse:
    form = CPFLoginForm(request, data=request.POST or None)

    if request.method == "POST":
        cpf = form.data.get("username", "")  # ainda nao limpo se form invalido
        cpf_norm = cpf.strip()

        # Tenta localizar o usuario para checar lock antes de authenticate().
        user_obj = User.objects.filter(cpf=cpf_norm).first()
        if user_obj and user_obj.is_locked:
            messages.error(request, "Conta temporariamente bloqueada. Tente mais tarde.")
            logger.info(
                "login_blocked cpf=%s ip=%s",
                mask_cpf(cpf_norm),
                getattr(request, "audit_context", {}).get("ip"),
            )
            return render(request, "accounts/login.html", {"form": form}, status=403)

        if form.is_valid():
            user = form.get_user()
            # Reset de contador e update de last_login_* ocorre via signal.
            login(request, user)
            messages.success(request, _last_login_banner(user))
            if user.must_change_password:
                return redirect("accounts:password_change")
            return redirect(settings.LOGIN_REDIRECT_URL)

        # Falha autenticada (form invalido). Disparamos signal manualmente
        # com credenciais mascaradas. NOTE: atende Marco Civil Art. 15.
        user_login_failed.send(
            sender=login_view,
            credentials={"cpf": mask_cpf(cpf_norm)},
            request=request,
        )
        # Incrementa contador se o CPF existe.
        if user_obj:
            user_obj.register_failed_login()

    return render(request, "accounts/login.html", {"form": form})


def _last_login_banner(user) -> str:
    """Mensagem com info do ultimo login. NOTE: atende SBIS NGS1.02.15."""
    if user.last_login_ip or user.last_login:
        return (
            f"Ultimo acesso: {user.last_login or 'N/A'}"
            f" a partir de {user.last_login_ip or 'IP desconhecido'}."
        )
    return "Primeiro acesso registrado."


# NOTE: atende cenario de auto-cadastro publico.
@ratelimit(key="ip", rate="5/h", method="POST", block=True)
def register_view(request: HttpRequest) -> HttpResponse:
    form = RegisterForm(data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        logger.info(
            "user_created cpf=%s ip=%s",
            mask_cpf(user.cpf),
            getattr(request, "audit_context", {}).get("ip"),
        )
        messages.success(request, "Cadastro realizado. Verifique seu e-mail para continuar.")
        return redirect("accounts:login")
    return render(request, "accounts/register.html", {"form": form})
