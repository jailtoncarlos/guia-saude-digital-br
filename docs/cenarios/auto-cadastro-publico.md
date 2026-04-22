# Cenário: Auto-cadastro público

## Descrição

Um sistema web público de saúde permite que o **cidadão crie sua própria
conta** (sem cadastro prévio por servidor administrativo). Exemplos:
acompanhar exames, agendar consulta, consentir em compartilhamento.

Este cenário difere de sistema corporativo interno (servidor do SUS) em
pelo menos três pontos:

1. **Base legal LGPD** pode ser **consentimento** ou política pública
   (varia; verificar).
2. **Risco de abuso** — bot criando contas em massa, *credential stuffing*.
3. **Transparência obrigatória** — termo de uso e política de privacidade
   antes do cadastro.

## Riscos

| Risco | Consequência |
|---|---|
| Aceitar qualquer string como CPF | Lixo em base de produção |
| Cadastro sem termo de uso / sem política de privacidade | Viola LGPD Art. 6º VI |
| Sem CAPTCHA ou rate limit | Bot cria milhares de contas |
| E-mail não verificado | Identidade não confiável |
| "Primeira senha = CPF" ou sequência previsível | Violação grave NGS1.02 + LGPD Art. 46 |
| Exibir "CPF já cadastrado" | Enumeração de base |

## Normas aplicáveis

- [LGPD Art. 6º VI (transparência), Art. 46, Art. 11 (dado sensível)](../normas/lgpd/README.md).
- [PNIIS (Portaria 589/2015) — CPF](../normas/ms-datasus/pniis-589-2015.md).
- [SBIS NGS1.02 e NGS1.06.03 (validação de entrada)](../normas/sbis-cfm/README.md).
- [SBIS NGS1.11.01 (aceite de termo no 1º acesso)](../normas/sbis-cfm/README.md).
- [Guia ANPD Poder Público 2024](../normas/anpd/guia-poder-publico-2024.md).
- OWASP ASVS V11 (business logic) / Top 10 A04 (insecure design).

## Requisitos mínimos

- [ ] **Termo de uso** e **política de privacidade** exibidos e aceitos
      antes do cadastro. Registrar versão, IP, data/hora do aceite.
- [ ] Validação de **DV do CPF** e rejeição de sequências repetidas.
- [ ] Verificação de **e-mail** por link/código antes de ativar conta.
- [ ] **CAPTCHA** ou rate limit em `/cadastro` (por IP; ex.: 5/hora).
- [ ] Senha definida pelo usuário (nunca gerada a partir de CPF).
- [ ] Política de qualidade (≥8/1/1 — ver [cenário de autenticação](./autenticacao.md)).
- [ ] Resposta genérica mesmo quando CPF já existe ("Verifique seu e-mail
      para continuar") — não revelar existência.
- [ ] Trilha do cadastro (`user_created`, com IP/UA).

## Exemplo de implementação (Django)

Ver [`examples/django-auth-lgpd-compliant/`](../../examples/django-auth-lgpd-compliant/):

- `accounts/forms.py` — `RegisterForm` com validador de CPF e checagem de
  aceite de termos.
- `accounts/views.py` — view `RegisterView` com rate limit e fluxo de
  confirmação por e-mail.
- `terms/models.py` e `terms/middleware.py` — `TermsVersion` e
  `TermsAcceptance`, com middleware que força aceite no primeiro acesso.

Validador de CPF (conceitual, detalhes no exemplo):

```python
import re

INVALID_CPF_SEQUENCES = {str(d) * 11 for d in range(10)}


def validate_cpf(cpf_raw: str) -> str:
    """Normaliza e valida CPF. Lanca ValueError se invalido.

    NOTE: atende PNIIS / SBIS NGS1.06.03 (validacao de entrada).
    """
    cpf = re.sub(r"\D", "", cpf_raw or "")
    if len(cpf) != 11 or cpf in INVALID_CPF_SEQUENCES:
        raise ValueError("CPF invalido")

    def _dv(base: str) -> int:
        total = sum(int(d) * w for d, w in zip(base, range(len(base) + 1, 1, -1)))
        rest = total % 11
        return 0 if rest < 2 else 11 - rest

    if int(cpf[9]) != _dv(cpf[:9]) or int(cpf[10]) != _dv(cpf[:10]):
        raise ValueError("CPF invalido")
    return cpf
```

## Como testar conformidade

1. **Unit test** do validador: DV válido, inválido, sequência repetida,
   string vazia, com máscara.
2. **Test** de fluxo: cadastro com termo de uso não aceito → bloqueia
   submit.
3. **Test** de fluxo: cadastro submetido → cria `TermsAcceptance` e
   `LoginEvent` de criação.
4. **Test** de enumeração: tentativa de cadastrar CPF já existente →
   resposta igual à do sucesso ("verifique seu e-mail"); nenhuma
   *password reset* é enviada ao usuário real sem clique adicional.
5. **Test** de rate limit: 10 tentativas do mesmo IP → 429.
