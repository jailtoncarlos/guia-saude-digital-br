# System prompts para IA

System prompts prontos para uso em **Claude, Copilot, Cursor, assistentes
internos** — com foco em revisão de código e auditoria de sistemas de
saúde digital no Brasil.

| Prompt | Uso |
|---|---|
| [code-review-lgpd.md](./code-review-lgpd.md) | Revisar PR focando em LGPD/SBIS/OWASP antes de aprovar |
| [audit-assistant.md](./audit-assistant.md) | Auxiliar em preparação para auditoria SBIS/ANPD |

## Como usar

1. Copie o conteúdo do prompt.
2. Cole como **system prompt** no seu assistente.
3. Forneça o diff/código/documento como `user message`.
4. O assistente responderá no formato estruturado pedido.

Os prompts referenciam o conteúdo deste repositório. Se o assistente
tiver acesso ao filesystem (Claude Code, Cursor), forneça este repo como
contexto para maximizar a utilidade.

## Knowledge pack

Além dos prompts, há o índice YAML consumível por LLM em
[`../knowledge-packs/normas-index.yml`](../knowledge-packs/normas-index.yml)
— útil para *retrieval* sem precisar passar o repo inteiro no contexto.
