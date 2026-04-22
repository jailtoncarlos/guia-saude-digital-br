# Cenário: Autorização / RBAC

## Descrição

Implementar controle de acesso baseado em **papéis** em um sistema de
saúde digital, garantindo que cada usuário só acesse o que é compatível
com sua função.

Cobre:

- Modelo de papéis (administrador, profissional, gestor, etc.).
- Decoradores/guards de acesso em views, endpoints e filas.
- Princípio do menor privilégio.
- Revisão periódica de acesso.
- Pelo menos 1 administrador ativo sempre.

## Riscos

| Risco | Consequência |
|---|---|
| Verificação de permissão apenas no frontend | *Privilege escalation* trivial; viola SBIS NGS1.03 e OWASP A01 |
| Papel "admin" atribuído a muitos usuários | *Blast radius* enorme em incidente; viola menor privilégio |
| Conta administrativa sem rotação / sem MFA | Alvo preferencial em ataque credencial |
| Remover último admin acidentalmente | Sistema inacessível administrativamente |
| Usuário com perfil vencido mantém acesso | Violação do princípio de menor privilégio |

## Normas aplicáveis

- [LGPD Art. 6º X (responsabilização), Art. 46](../normas/lgpd/README.md).
- [SBIS NGS1.03 (autorização) e NGS1.03.10 (ao menos 1 admin)](../normas/sbis-cfm/README.md).
- [PNSI / IN GSI/PR nº 1/2020](../normas/apf-seguranca/README.md).
- OWASP ASVS V4 / Top 10 A01 (broken access control).

## Requisitos mínimos

- [ ] Modelo de papéis em banco (tabela `roles`/`groups`).
- [ ] Autorização **sempre server-side** — nunca confiar em flag frontend.
- [ ] Papéis mínimos para o domínio (ex.: `admin`, `profissional`, `gestor`,
      `auditor`).
- [ ] Menor privilégio: cada papel tem só as permissões que usa.
- [ ] Invariante "1 admin ativo" — bloquear remoção do último admin.
- [ ] Trilha registra concessão/revogação de permissão.
- [ ] Revisão periódica trimestral (documentada).
- [ ] `locked_until` ou `is_active=False` não apaga usuário — mantém
      responsabilização histórica.

## Exemplo de implementação (Django)

Django fornece o sistema `Group`/`Permission` nativo; use-o antes de
reinventar. Esquema sugerido:

```python
# NOTE: atende SBIS NGS1.03.02 / NGS1.03.08 - perfis geridos pela aplicacao.
ADMIN_GROUP = "admin"
PROFISSIONAL_GROUP = "profissional"
GESTOR_GROUP = "gestor"
AUDITOR_GROUP = "auditor"  # so leitura da trilha
```

Decorator para views:

```python
from functools import wraps
from django.core.exceptions import PermissionDenied


def require_group(*allowed_groups):
    """Restringe view aos papeis informados.

    NOTE: atende SBIS NGS1.03.01 - autorizacao server-side.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            if not request.user.is_authenticated:
                raise PermissionDenied
            user_groups = set(request.user.groups.values_list("name", flat=True))
            if not user_groups.intersection(allowed_groups):
                raise PermissionDenied
            return view_func(request, *args, **kwargs)
        return _wrapped
    return decorator
```

Invariante de ao menos 1 admin (em `accounts/models.py` ou signal):

```python
from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver


# NOTE: atende SBIS NGS1.03.10 - ao menos 1 administrador ativo.
def ensure_system_admin_invariant(user, action: str):
    from django.contrib.auth.models import Group
    admin_group = Group.objects.get(name=ADMIN_GROUP)
    active_admins = admin_group.user_set.filter(is_active=True).exclude(pk=user.pk)
    if not active_admins.exists():
        raise ValueError(
            f"Operacao {action} removeria o ultimo administrador ativo. "
            "Promova outro usuario a admin antes."
        )
```

## Como testar conformidade

1. **Unit test** do decorator: chamadas sem grupo → `PermissionDenied`.
2. **Test** de invariante admin:
   - Tentar desativar último admin → erro.
   - Tentar remover do grupo admin o último admin → erro.
3. **Fuzz** de rotas: para cada endpoint protegido, garantir que
   requisição sem sessão retorne 302/401 e requisição com sessão de perfil
   inadequado retorne 403.
4. **Revisão trimestral** — dashboard/listagem de usuários com data de
   última revisão e botão "marcar como revisado".
5. **Logs de concessão/revogação** — cada mudança de grupo gera evento
   na trilha.
