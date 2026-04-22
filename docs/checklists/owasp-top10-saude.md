# Checklist — OWASP Top 10 (2021) aplicado a saúde digital

Versão enxuta do Top 10 OWASP 2021 com notas específicas do domínio de
saúde.

## A01 — Broken Access Control

- [ ] Autorização **server-side** em cada endpoint (ver
      [cenário RBAC](../cenarios/autorizacao-rbac.md)).
- [ ] Verificação de **propriedade do recurso** (usuário só vê o que é
      dele ou da sua unidade).
- [ ] Sem *IDOR*: IDs sequenciais + ausência de verificação = vaza
      prontuário alheio.
- [ ] `deny by default` em rotas novas.

## A02 — Cryptographic Failures

- [ ] **TLS ≥1.2**, cifra forte, HSTS.
- [ ] Hash de senha PBKDF2/Argon2/bcrypt.
- [ ] Criptografia em repouso para dado sensível.
- [ ] Sem chave hardcoded no repositório.
- [ ] Gestão de chaves (KMS/cofre) documentada.

## A03 — Injection

- [ ] ORM com parâmetros (Django ORM já protege).
- [ ] Sem concatenação de string em SQL.
- [ ] Validação de input com *allow list* onde possível.
- [ ] *Output encoding* no template (Django escapa por padrão — não
      use `|safe` com input do usuário).

## A04 — Insecure Design

- [ ] Cenários em [`docs/cenarios/`](../cenarios/) aplicados antes de
      codar.
- [ ] Limite de recurso (rate limit, paginação, *timeout*).
- [ ] Verificação de **finalidade** em consultas a dado sensível (em
      auditoria ANPD, "por que esse usuário viu esse CPF?" é pergunta
      padrão).

## A05 — Security Misconfiguration

- [ ] `DEBUG = False` em produção.
- [ ] `ALLOWED_HOSTS` restrito.
- [ ] Headers de segurança (`X-Content-Type-Options`, `X-Frame-Options`,
      `Referrer-Policy`, `Content-Security-Policy`).
- [ ] Mensagem de erro genérica para cliente (detalhe só em log interno).
- [ ] Versões de dependência atualizadas.

## A06 — Vulnerable and Outdated Components

- [ ] `pip-audit` / `safety` no CI.
- [ ] Renovate/Dependabot ativo.
- [ ] Framework e runtime suportados (Python ≥3.11, Django ≥5).

## A07 — Identification and Authentication Failures

- [ ] Ver [cenário de autenticação](../cenarios/autenticacao.md).
- [ ] Bloqueio após N tentativas.
- [ ] Rotação de ID de sessão em login.
- [ ] Sem credencial compartilhada de serviço.

## A08 — Software and Data Integrity Failures

- [ ] CI/CD com verificação de assinatura/hash de artefato.
- [ ] Sem `curl | bash` em dockerfile.
- [ ] Dependências com *pin* (requirements com versão fixa, `uv.lock`,
      `poetry.lock`).

## A09 — Security Logging and Monitoring Failures

- [ ] Ver [cenário de auditoria](../cenarios/auditoria.md).
- [ ] Alerta para eventos críticos (tentativa massiva de login, acesso
      admin fora do horário).
- [ ] Logs **sem** dado sensível em claro.

## A10 — Server-Side Request Forgery (SSRF)

- [ ] Requisições externas com *allow list* de domínios.
- [ ] Sem fetch de URL arbitrária fornecida pelo usuário.
- [ ] Metadados do cloud provider (ex.: `169.254.169.254`) bloqueados em
      *egress*.

---

## OWASP ASVS v4 — mapeamento resumido

| ASVS | Tema | Cenário correspondente |
|---|---|---|
| V2 | Autenticação | [autenticação](../cenarios/autenticacao.md) |
| V3 | Session management | idem |
| V4 | Access control | [RBAC](../cenarios/autorizacao-rbac.md) |
| V5 | Validação/sanitização | [auto-cadastro](../cenarios/auto-cadastro-publico.md) |
| V7 | Error handling / logging | [auditoria](../cenarios/auditoria.md) |
| V8 | Data protection | [dado sensível](../cenarios/armazenamento-dado-sensivel.md) |
| V9 | Communication | HTTPS/TLS |
| V10 | Malicious code | SAST no CI |
| V11 | Business logic | [auto-cadastro](../cenarios/auto-cadastro-publico.md) |
