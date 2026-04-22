"""Manager customizado para o User que usa CPF como USERNAME_FIELD."""
from __future__ import annotations

from typing import Any

from django.contrib.auth.models import BaseUserManager

from accounts.validators import is_valid_cpf, normalize_cpf


class UserManager(BaseUserManager):
    """Cria usuario com CPF normalizado e validado.

    NOTE: atende PNIIS + SBIS NGS1.03.09 (identificador unico por CPF).
    """

    use_in_migrations = True

    def _create_user(self, cpf: str, password: str | None, **extra: Any):
        cpf = normalize_cpf(cpf)
        if not cpf:
            raise ValueError("CPF e obrigatorio.")
        if not is_valid_cpf(cpf):
            raise ValueError("CPF invalido.")

        email = extra.pop("email", "")
        email = self.normalize_email(email) if email else ""

        user = self.model(cpf=cpf, email=email, **extra)
        user.set_password(password)  # NOTE: atende SBIS NGS1.02.02 via PBKDF2.
        user.save(using=self._db)
        return user

    def create_user(self, cpf: str, password: str | None = None, **extra: Any):
        extra.setdefault("is_staff", False)
        extra.setdefault("is_superuser", False)
        return self._create_user(cpf, password, **extra)

    def create_superuser(self, cpf: str, password: str | None = None, **extra: Any):
        extra.setdefault("is_staff", True)
        extra.setdefault("is_superuser", True)
        extra.setdefault("is_active", True)
        if extra.get("is_staff") is not True:
            raise ValueError("Superusuario precisa de is_staff=True.")
        if extra.get("is_superuser") is not True:
            raise ValueError("Superusuario precisa de is_superuser=True.")
        return self._create_user(cpf, password, **extra)
