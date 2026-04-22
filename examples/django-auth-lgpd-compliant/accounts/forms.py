"""Forms de autenticacao e cadastro."""
from __future__ import annotations

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from accounts.validators import is_valid_cpf, normalize_cpf

User = get_user_model()


class CPFLoginForm(AuthenticationForm):
    """Login form que aceita CPF com ou sem mascara.

    NOTE: atende SBIS NGS1.02.16 - mensagens genericas (herdado de
    AuthenticationForm, que nao diferencia "usuario inexistente" de
    "senha incorreta").
    """

    username = forms.CharField(
        label="CPF",
        max_length=14,  # permite entrada com mascara 000.000.000-00
        widget=forms.TextInput(attrs={
            "autocomplete": "username",
            "inputmode": "numeric",
        }),
    )
    password = forms.CharField(
        label="Senha",
        strip=False,
        widget=forms.PasswordInput(attrs={
            # NOTE: atende SBIS NGS1.02.17 - nao memorizar credenciais.
            "autocomplete": "current-password",
        }),
    )

    def clean_username(self) -> str:
        raw = self.cleaned_data.get("username", "")
        return normalize_cpf(raw)

    error_messages = {
        # NOTE: atende SBIS NGS1.02.16 - mensagem generica.
        "invalid_login": "Credenciais invalidas.",
        "inactive": "Conta inativa. Procure o administrador.",
    }


class RegisterForm(forms.ModelForm):
    """Cadastro publico (auto-cadastro).

    NOTE: atende cenario de auto-cadastro publico
    (docs/cenarios/auto-cadastro-publico.md).
    """

    cpf = forms.CharField(label="CPF", max_length=14)
    password1 = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )
    password2 = forms.CharField(
        label="Confirmar senha",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )
    accept_terms = forms.BooleanField(
        label="Li e aceito o termo de uso e a politica de privacidade.",
        required=True,
    )

    class Meta:
        model = User
        fields = ("cpf", "email", "full_name")

    def clean_cpf(self) -> str:
        cpf = normalize_cpf(self.cleaned_data.get("cpf", ""))
        if not is_valid_cpf(cpf):
            raise ValidationError("CPF invalido.")
        return cpf

    def clean(self) -> dict:
        cleaned = super().clean()
        p1 = cleaned.get("password1")
        p2 = cleaned.get("password2")
        if p1 and p2 and p1 != p2:
            raise ValidationError("As senhas nao conferem.")
        if p1:
            # NOTE: atende SBIS NGS1.02.03 - qualidade minima.
            validate_password(p1)
        return cleaned

    def save(self, commit: bool = True) -> User:
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        # NOTE: auto-cadastro define a propria senha - nao precisa forcar troca.
        user.must_change_password = False
        if commit:
            user.save()
        return user
