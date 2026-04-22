# Exemplos de código

Templates de referência para diferentes stacks. Cada exemplo é
**autoexplicativo** e traz comentários `# NOTE: atende SBIS NGS1.XX.YY /
LGPD Art. ZZ` nos pontos relevantes.

| Exemplo | Status | Stack |
|---|---|---|
| [django-auth-lgpd-compliant](./django-auth-lgpd-compliant/) | Completo | Django ≥5 / PostgreSQL |
| [flask-auth-lgpd-compliant](./flask-auth-lgpd-compliant/) | Stub | Flask — implementação futura |
| [dash-audit-trail-minimal](./dash-audit-trail-minimal/) | Stub | Plotly Dash — implementação futura |

## Licença dos exemplos

Todo código em `examples/` é distribuído sob **Apache-2.0**. Ver
[`../LICENSE`](../LICENSE) e [`../LICENSE-CODE`](../LICENSE-CODE).

## Como usar

Os exemplos **não** são para rodar como está — são esqueletos didáticos
focados em modelar o *design* correto. Ao iniciar um projeto:

1. Leia o `README.md` do exemplo.
2. Copie a **estrutura** de apps/models, não o *settings* completo (que é
   específico por ambiente).
3. Adapte ao seu contexto mantendo os comentários `# NOTE: atende ...` —
   são a rastreabilidade para SBIS e ANPD.
