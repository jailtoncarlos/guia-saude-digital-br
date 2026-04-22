"""Validadores de CPF para uso em models, forms e views.

NOTE: atende PNIIS (Portaria GM/MS 589/2015) e SBIS NGS1.06.03
(validacao de entrada).
"""
from __future__ import annotations

import re

CPF_INVALID_SEQUENCES = frozenset(str(d) * 11 for d in range(10))


def normalize_cpf(raw: str | None) -> str:
    """Mantem apenas digitos. String vazia se entrada None."""
    return re.sub(r"\D", "", raw or "")


def is_valid_cpf(cpf: str) -> bool:
    """Valida comprimento, sequencia e digitos verificadores.

    Aceita CPF com ou sem mascara, desde que seja normalizado antes.
    """
    cpf = normalize_cpf(cpf)
    if len(cpf) != 11 or cpf in CPF_INVALID_SEQUENCES:
        return False

    def _digit(base: str) -> int:
        total = sum(int(d) * w for d, w in zip(base, range(len(base) + 1, 1, -1)))
        rest = total % 11
        return 0 if rest < 2 else 11 - rest

    return int(cpf[9]) == _digit(cpf[:9]) and int(cpf[10]) == _digit(cpf[:10])


def mask_cpf(cpf: str) -> str:
    """Retorna CPF mascarado como ***.***.***-XX, seguro para log e UI.

    NOTE: atende LGPD Art. 46 - minimizacao em log.
    """
    cpf = normalize_cpf(cpf)
    if len(cpf) != 11:
        return "***"
    return f"***.***.***-{cpf[-2:]}"
