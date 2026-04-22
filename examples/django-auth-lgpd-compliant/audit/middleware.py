"""Middleware que popula request.audit_context com IP e User-Agent.

NOTE: atende Marco Civil Art. 15 + SBIS NGS1.07.05.

Lida com proxy reverso via X-Forwarded-For. Configure TRUSTED_PROXIES
no settings para validar o primeiro IP da cadeia.
"""
from __future__ import annotations

import ipaddress
from typing import Callable

from django.conf import settings
from django.http import HttpRequest, HttpResponse


class AuditContext(dict):
    """dict leve com atributos estilo attr access."""

    def __getattr__(self, item: str):
        try:
            return self[item]
        except KeyError as exc:
            raise AttributeError(item) from exc


def _trusted_proxy_cidrs() -> list[ipaddress.IPv4Network | ipaddress.IPv6Network]:
    cidrs: list = []
    for raw in getattr(settings, "TRUSTED_PROXIES", []) or []:
        try:
            cidrs.append(ipaddress.ip_network(raw, strict=False))
        except ValueError:
            continue
    return cidrs


def _is_trusted(ip: str) -> bool:
    try:
        addr = ipaddress.ip_address(ip)
    except ValueError:
        return False
    return any(addr in net for net in _trusted_proxy_cidrs())


def get_client_ip(request: HttpRequest) -> str:
    """Retorna IP do cliente considerando proxy confiavel.

    Regra: se REMOTE_ADDR e trusted proxy, usa o primeiro IP do
    X-Forwarded-For; caso contrario, usa REMOTE_ADDR (XFF e spoofavel
    quando nao vem de proxy confiavel).
    """
    remote = request.META.get("REMOTE_ADDR", "") or ""
    xff = request.META.get("HTTP_X_FORWARDED_FOR", "") or ""

    if xff and _is_trusted(remote):
        first = xff.split(",")[0].strip()
        if first:
            return first
    return remote


class AuditContextMiddleware:
    """Injeta request.audit_context com ip/user_agent/session_key."""

    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        ua = (request.META.get("HTTP_USER_AGENT", "") or "")[:512]
        session_key = ""
        session = getattr(request, "session", None)
        if session is not None:
            session_key = session.session_key or ""

        request.audit_context = AuditContext(
            ip=get_client_ip(request),
            user_agent=ua,
            session_key=session_key,
        )
        return self.get_response(request)
