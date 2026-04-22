# Cenário: Autenticação

## Descrição

Implementar o login de um sistema de saúde digital no Brasil, garantindo
identificação unívoca do usuário, proteção das credenciais, rastreabilidade
e adequação aos padrões SBIS/LGPD/OWASP.

O cenário cobre:

- Escolha do identificador (**CPF** em sistemas SUS).
- Armazenamento seguro da senha.
- Política de qualidade de senha.
- Bloqueio por tentativas e por inatividade.
- Mensagens de erro genéricas.
- Captura de contexto para trilha (IP, UA).

## Riscos

| Risco | Consequência |
|---|---|
| Hash fraco da senha (MD5/SHA-1) | Vazamento permite *offline brute force*; viola SBIS NGS1.02.02 e LGPD Art. 46 |
| Enumerar usuário via mensagem de erro ("senha incorreta" vs "usuário não existe") | Reconhecimento de CPFs válidos; viola SBIS NGS1.02.16 |
| Não bloquear por tentativas | *Brute force online*; viola SBIS NGS1.02.13 |
| Capturar IP errado atrás de proxy | Trilha inválida; viola Marco Civil Art. 15 |
| Cookie sem `Secure`/`HttpOnly`/`SameSite` | Roubo de sessão; viola SBIS NGS1.02.23 |
| Logar CPF/senha em aplicação | Dado pessoal sensível em log; viola LGPD Art. 46 |

## Normas aplicáveis

- [LGPD Art. 6º VII, Art. 46](../normas/lgpd/README.md) — segurança.
- [Marco Civil Art. 15](../normas/marco-civil/README.md) — trilha de acesso.
- [PNIIS — Portaria 589/2015](../normas/ms-datasus/pniis-589-2015.md) —
  identificação unívoca por CPF.
- [SBIS NGS1.02 e NGS1.03.09](../normas/sbis-cfm/README.md) —
  autenticação e responsabilização.
- [PNSI e IN GSI/PR nº 1/2020](../normas/apf-seguranca/README.md) —
  controles de segurança em APF.
- OWASP ASVS V2 / Top 10 A07 (identification and authentication failures).

## Requisitos mínimos

- [ ] Identificador: **CPF** normalizado (sem máscara) como `USERNAME_FIELD`.
- [ ] Validação de DV do CPF no cadastro.
- [ ] Hash de senha PBKDF2 (padrão Django) ou Argon2; **nunca** MD5/SHA-1.
- [ ] Política: ≥8 caracteres, 1 maiúscula, 1 numérico (SBIS NGS1.02.03).
- [ ] Histórico para evitar repetição (SBIS NGS1.02.11).
- [ ] Bloqueio após N tentativas (recomendado 5) com desbloqueio por tempo.
- [ ] Mensagem genérica em falha ("Credenciais inválidas").
- [ ] Exibir último login após autenticação bem sucedida.
- [ ] Cookie de sessão `Secure`, `HttpOnly`, `SameSite='Strict'` (ou `Lax`).
- [ ] Sessão com tempo de inatividade configurável (env).
- [ ] Rotação de ID de sessão no login.
- [ ] Captura de IP (considerando `X-Forwarded-For` só com proxy confiável)
      e `User-Agent` no evento de login.
- [ ] `autocomplete="new-password"` no campo de senha.
- [ ] Trilha de `login_success`, `login_failed`, `logout`,
      `password_change`.

## Exemplo de implementação (Django)

Ver [`examples/django-auth-lgpd-compliant/`](../../examples/django-auth-lgpd-compliant/):

- `accounts/models.py` — `User` com CPF como USERNAME_FIELD, validador
  de DV, política de bloqueio.
- `accounts/views.py` — login com rate limit, mensagem genérica, update
  de `last_login_info` com IP/UA.
- `audit/signals.py` — handlers de `user_logged_in`, `user_logged_out`,
  `user_login_failed`, `password_changed`.
- `audit/middleware.py` — extrai IP/UA de cada request.
- `config/settings.py` — flags de segurança
  (`SESSION_COOKIE_SECURE`, `SECURE_SSL_REDIRECT`, `SECURE_HSTS_SECONDS`,
  `AUTH_PASSWORD_VALIDATORS`).

## Como testar conformidade

1. **Unit test** de validação de CPF (casos: DV válido, DV inválido,
   sequência repetida, string vazia).
2. **Integration test** de login:
   - Sucesso → cria `LoginEvent(event_type='success')`.
   - Falha → cria `LoginEvent(event_type='failure')` e incrementa
     contador.
   - Após N falhas → `locked_until` no futuro, login rejeitado mesmo com
     senha correta.
3. **Verificar mensagem** de erro é idêntica para usuário inexistente e
   senha errada.
4. **Scan do storage de senha** no banco após cadastro — deve começar com
   `pbkdf2_sha256$`.
5. **Header inspection** via `curl -I` em ambiente de staging:
   - `Strict-Transport-Security` presente.
   - Cookie de sessão com `Secure`, `HttpOnly`, `SameSite`.
6. **Teste de rate limit** com `ab` ou `hey`: após N requisições, retorno
   429 ou 403.
7. **Varrer logs** de aplicação: nenhum CPF ou senha em claro.
