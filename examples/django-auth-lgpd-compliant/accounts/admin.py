"""Admin do User - sem expor CPF completo em lista."""
from __future__ import annotations

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from accounts.models import User
from accounts.validators import mask_cpf


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    ordering = ("cpf",)
    list_display = ("masked_cpf", "full_name", "email", "is_active", "is_staff", "last_login")
    search_fields = ("cpf", "email", "full_name")

    fieldsets = (
        (None, {"fields": ("cpf", "password")}),
        ("Pessoal", {"fields": ("full_name", "email")}),
        ("Permissoes", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Bloqueio", {"fields": ("failed_login_attempts", "locked_until", "must_change_password")}),
        ("Ultimo acesso", {"fields": ("last_login", "last_login_ip", "last_login_user_agent", "date_joined")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("cpf", "email", "full_name", "password1", "password2"),
        }),
    )
    readonly_fields = ("last_login", "date_joined", "last_login_ip", "last_login_user_agent")

    @admin.display(description="CPF")
    def masked_cpf(self, obj: User) -> str:
        # NOTE: atende LGPD Art. 46 - minimizacao em exibicao.
        return mask_cpf(obj.cpf)
