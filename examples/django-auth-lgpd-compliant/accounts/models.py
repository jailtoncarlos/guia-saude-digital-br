"""User customizado com CPF como identificador unico.

Este modelo concentra decisoes de conformidade mapeadas em:
- docs/normas/ms-datasus/pniis-589-2015.md
- docs/normas/sbis-cfm/README.md (NGS1.02, NGS1.03)
- docs/normas/lgpd/README.md (Art. 46)
"""
from __future__ import annotations

from datetime import timedelta
from typing import Any

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from accounts.managers import UserManager
from accounts.validators import is_valid_cpf, normalize_cpf


class User(AbstractBaseUser, PermissionsMixin):
    """Usuario com CPF como identificador unico e politicas de bloqueio.

    NOTE: atende SBIS NGS1.03.09 (identidade unica) e PNIIS.
    """

    cpf = models.CharField(
        max_length=11,
        unique=True,
        db_index=True,
        help_text="CPF normalizado (somente digitos). Validacao de DV em save().",
    )
    email = models.EmailField(blank=True)
    full_name = models.CharField(max_length=255, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)

    # Bloqueio por tentativas. NOTE: atende SBIS NGS1.02.13.
    failed_login_attempts = models.PositiveIntegerField(default=0)
    locked_until = models.DateTimeField(null=True, blank=True)

    # Exibir ao proximo login bem sucedido. NOTE: atende SBIS NGS1.02.15.
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    last_login_user_agent = models.CharField(max_length=512, blank=True)

    # Forcar troca de senha no primeiro acesso. NOTE: atende SBIS NGS1.02.06.
    must_change_password = models.BooleanField(default=False)

    USERNAME_FIELD = "cpf"
    REQUIRED_FIELDS = ["email"]

    objects = UserManager()

    class Meta:
        verbose_name = "usuario"
        verbose_name_plural = "usuarios"

    def __str__(self) -> str:
        # Nao expor CPF completo em __str__. NOTE: atende LGPD Art. 46.
        from accounts.validators import mask_cpf
        return f"User({mask_cpf(self.cpf)})"

    def clean(self) -> None:
        self.cpf = normalize_cpf(self.cpf)
        if not is_valid_cpf(self.cpf):
            raise ValidationError({"cpf": "CPF invalido."})
        super().clean()

    def save(self, *args: Any, **kwargs: Any) -> None:
        self.cpf = normalize_cpf(self.cpf)
        super().save(*args, **kwargs)

    # ----------------------------------------------------------------------- #
    # Politicas de seguranca
    # ----------------------------------------------------------------------- #

    @property
    def is_locked(self) -> bool:
        """Retorna True se a conta esta bloqueada no momento."""
        return bool(self.locked_until and self.locked_until > timezone.now())

    def register_failed_login(self) -> None:
        """Incrementa contador e bloqueia se atingir o limite.

        NOTE: atende SBIS NGS1.02.13.
        """
        self.failed_login_attempts = (self.failed_login_attempts or 0) + 1
        max_attempts = getattr(settings, "LOGIN_MAX_ATTEMPTS", 5)
        if self.failed_login_attempts >= max_attempts:
            lockout_minutes = getattr(settings, "LOGIN_LOCKOUT_MINUTES", 15)
            self.locked_until = timezone.now() + timedelta(minutes=lockout_minutes)
        self.save(update_fields=["failed_login_attempts", "locked_until"])

    def reset_failed_logins(self) -> None:
        """Chamar apos login bem sucedido."""
        self.failed_login_attempts = 0
        self.locked_until = None
        self.save(update_fields=["failed_login_attempts", "locked_until"])

    def update_last_login_info(self, ip: str | None, user_agent: str | None) -> None:
        """Persiste IP/UA do login atual para exibir no proximo.

        NOTE: atende SBIS NGS1.02.15.
        """
        self.last_login_ip = ip or None
        self.last_login_user_agent = (user_agent or "")[:512]
        self.save(update_fields=["last_login_ip", "last_login_user_agent"])
