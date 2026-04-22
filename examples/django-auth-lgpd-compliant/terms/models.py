"""Termo de uso versionado e aceite do usuario.

NOTE: atende SBIS NGS1.11.01 + LGPD Art. 6o VI (transparencia).

Publique uma nova versao via management command dedicado. Versoes antigas
ficam como referencia historica.
"""
from __future__ import annotations

from django.conf import settings
from django.db import models


class TermsVersion(models.Model):
    """Versao publicada de um termo de uso ou politica."""

    KIND_TERMS_OF_USE = "terms_of_use"
    KIND_PRIVACY_POLICY = "privacy_policy"
    KIND_CHOICES = [
        (KIND_TERMS_OF_USE, "Termo de uso"),
        (KIND_PRIVACY_POLICY, "Politica de privacidade"),
    ]

    kind = models.CharField(max_length=32, choices=KIND_CHOICES, db_index=True)
    version = models.CharField(max_length=32, db_index=True)
    text = models.TextField()
    is_current = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "versao de termo"
        verbose_name_plural = "versoes de termo"
        constraints = [
            models.UniqueConstraint(fields=["kind", "version"], name="uniq_terms_version"),
        ]

    def __str__(self) -> str:
        return f"{self.kind} v{self.version}"

    @classmethod
    def current(cls, kind: str) -> "TermsVersion | None":
        return cls.objects.filter(kind=kind, is_current=True).order_by("-created_at").first()


class TermsAcceptance(models.Model):
    """Registro do aceite de uma versao por um usuario.

    Append-only (analogo ao LoginEvent). Uma nova versao publicada -> novo
    aceite exigido via middleware.
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    terms_version = models.ForeignKey(TermsVersion, on_delete=models.PROTECT)
    accepted_at = models.DateTimeField(auto_now_add=True)
    ip = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=512, blank=True)

    class Meta:
        verbose_name = "aceite de termo"
        verbose_name_plural = "aceites de termo"
        indexes = [
            models.Index(fields=["user", "terms_version"]),
        ]

    def __str__(self) -> str:
        return f"Aceite {self.user_id} -> {self.terms_version_id}"

    def save(self, *args, **kwargs) -> None:  # type: ignore[override]
        if self.pk is not None:
            raise ValueError("TermsAcceptance e append-only; UPDATE nao permitido.")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):  # type: ignore[override]
        raise ValueError("TermsAcceptance e append-only; DELETE nao permitido.")
