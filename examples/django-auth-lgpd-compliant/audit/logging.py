"""Formatter de logging que mascara CPF antes da emissao.

NOTE: atende LGPD Art. 46 - nunca logar CPF em texto plano.
"""
from __future__ import annotations

import logging
import re

CPF_RE = re.compile(r"\b(\d{3})\.?(\d{3})\.?(\d{3})-?(\d{2})\b")


def _mask_cpfs(text: str) -> str:
    return CPF_RE.sub(lambda m: f"***.***.***-{m.group(4)}", text)


class MaskingFormatter(logging.Formatter):
    """Aplica mascara de CPF em cada mensagem formatada."""

    def format(self, record: logging.LogRecord) -> str:
        base = super().format(record)
        return _mask_cpfs(base)
