#!/usr/bin/env python
"""Django manage.py do template de referencia.

Nada de especial aqui - padrao do Django. O valor do template esta nos
apps `accounts`, `audit` e `terms`, e no `config/settings.py`.
"""
import os
import sys


def main() -> None:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Django nao esta instalado ou nao esta disponivel no PYTHONPATH."
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
