# dash-audit-trail-minimal (stub)

**Status:** stub — implementação futura.

Este diretório reserva o espaço para um template mínimo de dashboard em
**Plotly Dash** com trilha de auditoria já implementada desde o primeiro
request.

## Escopo planejado

- App Dash + Flask por trás (`dash.Dash(__name__, server=flask_app)`).
- Middleware Flask (`before_request`) populando contexto de auditoria
  (IP/UA — mesma lógica de
  [`django-auth-lgpd-compliant/audit/middleware.py`](../django-auth-lgpd-compliant/audit/middleware.py)).
- Flask-Login com usuário por CPF.
- Tabela `login_event` em Postgres (mesmo schema do exemplo Django).
- Layout Dash com:
  - Callback de `login_success` que grava trilha e exibe último acesso.
  - Filtros de consulta à trilha (período, tipo de evento).
- `dcc.Store` **não** armazena dado sensível — só identificadores e
  metadados.

## Motivação

Muitos dashboards em saúde pública no Brasil são Dash + Postgres. Esses
projetos frequentemente ignoram trilha de auditoria ("é só um
dashboard"), o que viola Marco Civil Art. 15 e SBIS NGS1.07 quando o
dashboard expõe dado identificável.

Este template virá para encurtar o *time-to-compliance* em projetos Dash.

## Contribuições bem-vindas

Siga as diretrizes de
[`../../CONTRIBUTING.md`](../../CONTRIBUTING.md). Mantenha comentários
`# NOTE: atende ...` apontando a norma.
