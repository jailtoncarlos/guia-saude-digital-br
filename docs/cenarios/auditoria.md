# Cenário: Auditoria

## Descrição

Implementar trilha de auditoria em sistema de saúde digital — o que
registrar, onde armazenar, por quanto tempo manter e como expor para
consulta.

Cobre:

- Lista mínima de eventos a registrar.
- Campos obrigatórios por evento.
- Retenção e rotação.
- Proteção dos registros (append-only).
- Consulta filtrada e exportação.

## Riscos

| Risco | Consequência |
|---|---|
| Sem trilha | Viola Marco Civil Art. 15, LGPD Art. 46, SBIS NGS1.07 |
| Trilha editável pela aplicação (UPDATE/DELETE) | Viola SBIS NGS1.07.02 (proteção) |
| Trilha sem IP / sem UA | Dificulta/inviabiliza forense; viola NGS1.07.05 |
| Retenção <6 meses | Viola Marco Civil Art. 15 |
| CPF em texto plano em log de aplicação | Viola LGPD Art. 46 (minimização/segurança) |
| Trilha sem timestamp UTC | Viola SBIS NGS1.09.03 |

## Normas aplicáveis

- [Marco Civil Art. 15](../normas/marco-civil/README.md).
- [LGPD Art. 6º VII/X, Art. 15, Art. 46](../normas/lgpd/README.md).
- [SBIS NGS1.07](../normas/sbis-cfm/README.md).
- [IN GSI/PR nº 1/2020](../normas/apf-seguranca/in-gsi-1-2020.md).
- [Decreto 10.046/2019 (rastreabilidade de compartilhamento)](../normas/apf-seguranca/README.md).
- OWASP ASVS V7 / Top 10 A09 (security logging and monitoring failures).

## Eventos mínimos a registrar

| Evento | Por quê |
|---|---|
| `login_success` | Marco Civil Art. 15; SBIS NGS1.07.03 |
| `login_failure` | Detecção de ataque; NGS1.02.13 |
| `logout` | Encerramento de sessão |
| `session_expired_inactivity` | NGS1.02.20 |
| `password_change` | NGS1.02.08 |
| `password_reset_request` | NGS1.02.12 |
| `user_created` / `user_updated` / `user_deactivated` | NGS1.03.08 |
| `role_granted` / `role_revoked` | Mudança de permissão |
| `sensitive_data_access` | LGPD Art. 46 — acesso a dado sensível |
| `data_export` | LGPD Art. 18, V (portabilidade) + Art. 46 |
| `audit_trail_view` | Auditoria da auditoria |

## Campos obrigatórios por evento

| Campo | Observação |
|---|---|
| `user_id` | Null em `login_failure` quando CPF não existe |
| `cpf_attempted` | Só em eventos pré-autenticação (mascarado em exibição) |
| `event_type` | Enumeração acima |
| `failure_reason` | Opcional em sucesso |
| `ip` | `X-Forwarded-For` tratado, fallback para `REMOTE_ADDR` |
| `user_agent` | Truncado a ~512 chars |
| `session_key` | FK lógica da sessão |
| `created_at` | `TIMESTAMP WITH TIME ZONE` em UTC |

## Requisitos mínimos

- [ ] Tabela `audit_login_event` (ou equivalente) com os campos acima.
- [ ] Captura de IP via middleware que entende proxy reverso.
- [ ] Timestamp em UTC (`TIMESTAMP WITH TIME ZONE`).
- [ ] Credencial de banco da aplicação com permissão **apenas INSERT** na
      tabela de auditoria (UPDATE/DELETE negados via GRANT).
- [ ] Credencial separada para o papel `auditor`, com **apenas SELECT**.
- [ ] Retenção: mínimo 6 meses (Marco Civil); recomendado 5 anos (SUS).
- [ ] Rotação/arquivamento documentado.
- [ ] Tela de consulta com filtros (período, usuário, evento).
- [ ] Exportação CSV/JSON com metadados institucionais (NGS1.07.08).
- [ ] Consulta à trilha **também** gera evento `audit_trail_view`.

## Exemplo de implementação (Django)

Ver [`examples/django-auth-lgpd-compliant/audit/`](../../examples/django-auth-lgpd-compliant/audit/):

- `models.py` — `LoginEvent` com choices de `event_type` e
  `failure_reason`.
- `middleware.py` — `AuditContextMiddleware` que popula
  `request.audit_context` com IP/UA.
- `signals.py` — handlers que criam eventos a partir de sinais do Django
  (`user_logged_in`, `user_logged_out`, `user_login_failed`,
  `password_changed`).

Captura de IP considerando proxy:

```python
def get_client_ip(request) -> str:
    """Retorna IP do cliente considerando proxy reverso confiavel.

    NOTE: atende Marco Civil Art. 15 + SBIS NGS1.07.05.
    Configure TRUSTED_PROXIES no settings.
    """
    xff = request.META.get("HTTP_X_FORWARDED_FOR", "")
    if xff:
        candidates = [ip.strip() for ip in xff.split(",") if ip.strip()]
        if candidates:
            return candidates[0]
    return request.META.get("REMOTE_ADDR", "")
```

## Permissões de banco (PostgreSQL)

Exemplo de `GRANT` para proteger a trilha contra alteração pela aplicação:

```sql
-- NOTE: atende SBIS NGS1.07.02 - protecao dos registros.
CREATE ROLE app_writer LOGIN PASSWORD '...';
CREATE ROLE app_auditor LOGIN PASSWORD '...';

GRANT INSERT ON audit_login_event TO app_writer;
GRANT SELECT ON audit_login_event TO app_writer; -- para exibir "ultimo login"
GRANT SELECT ON audit_login_event TO app_auditor;

REVOKE UPDATE, DELETE, TRUNCATE ON audit_login_event FROM app_writer;
```

Em Django, usar duas conexões (`DATABASES` default e `audit_read`) e
roteador de banco para leitura de trilha pelo auditor.

## Como testar conformidade

1. **Test** de integração: login simulado cria `LoginEvent` com campos
   preenchidos; checar cada campo.
2. **Test** de proxy: `X-Forwarded-For: 1.2.3.4, 5.6.7.8` → IP registrado
   é `1.2.3.4`.
3. **Test** SQL: tentar `UPDATE audit_login_event SET ip='...'` com
   credencial `app_writer` → deve falhar (permission denied).
4. **Test** de retenção: contar registros com `created_at < now() -
   interval '6 months'` — deve haver estratégia clara (rotação ou
   particionamento).
5. **Test** de consulta: acesso à tela de trilha por usuário do grupo
   `auditor` gera `audit_trail_view`.
6. **Scan** de log de aplicação em staging: nenhum CPF em claro, nenhum
   valor de senha, nenhum token.
