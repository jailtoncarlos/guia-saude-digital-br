"""Middleware que exige aceite da versao atual do termo de uso.

NOTE: atende SBIS NGS1.11.01.

Regra:
- Usuario nao autenticado -> passa (login/register cuidam do fluxo).
- Usuario autenticado e ja aceitou a versao atual -> passa.
- Usuario autenticado sem aceite da versao atual -> redireciona para
  /termos/aceitar/, exceto nas rotas isentas.
"""
from __future__ import annotations

from typing import Callable, Iterable

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse

from terms.models import TermsAcceptance, TermsVersion


EXEMPT_VIEW_NAMES: set[str] = {
    "terms:accept",
    "accounts:login",
    "accounts:logout",
    "accounts:register",
    "accounts:password_reset",
    "accounts:password_reset_done",
    "accounts:password_reset_confirm",
}


def _path_exempt(request: HttpRequest, exempt_paths: Iterable[str]) -> bool:
    path = request.path
    return any(path.startswith(p) for p in exempt_paths)


class TermsAcceptanceMiddleware:
    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        self.get_response = get_response
        self.exempt_paths = (
            settings.STATIC_URL or "/static/",
            "/admin/login/",
            "/admin/logout/",
            "/termos/",
        )

    def __call__(self, request: HttpRequest) -> HttpResponse:
        user = getattr(request, "user", None)
        if not user or not user.is_authenticated:
            return self.get_response(request)

        if _path_exempt(request, self.exempt_paths):
            return self.get_response(request)

        current = TermsVersion.current(TermsVersion.KIND_TERMS_OF_USE)
        if current is None:
            # Sem termo configurado - sistema mal configurado, mas nao
            # bloqueamos a navegacao para nao causar loop em setup novo.
            return self.get_response(request)

        has_accepted = TermsAcceptance.objects.filter(
            user=user, terms_version=current,
        ).exists()
        if has_accepted:
            return self.get_response(request)

        try:
            accept_url = reverse("terms:accept")
        except Exception:
            # Rota nao registrada - nao quebrar projeto incompleto.
            return self.get_response(request)

        if request.path == accept_url:
            return self.get_response(request)
        return redirect(accept_url)
