# Cenários operacionais

Cada cenário parte de uma situação concreta do desenvolvimento de sistema
de saúde digital e mapeia:

1. Descrição do cenário.
2. Riscos jurídicos e de segurança.
3. Normas aplicáveis (com links).
4. Requisitos mínimos (checklist inline).
5. Exemplo de implementação (preferencialmente Django).
6. Como testar conformidade.

Use os cenários **antes** de mergulhar nas fichas de normas — eles já
agregam a leitura multiatributo ("para fazer X, preciso de Y, Z, W").

## Índice

| Cenário | Quando usar |
|---|---|
| [Autenticação](./autenticacao.md) | Todo sistema que exige login |
| [Autorização / RBAC](./autorizacao-rbac.md) | Sistema com mais de um perfil de usuário |
| [Auditoria](./auditoria.md) | Todo sistema de saúde digital |
| [Auto-cadastro público](./auto-cadastro-publico.md) | Cidadão cria a própria conta (vs. admin cadastra) |
| [Armazenamento de dado sensível](./armazenamento-dado-sensivel.md) | Persistir CPF, diagnóstico, exame etc. |
| [Compartilhamento via RNDS](./compartilhamento-rnds.md) | Publicar ou consumir dado na RNDS |
| [Consentimento](./consentimento.md) | Termo de uso, consentimento específico, TCLE |
