# guia-saude-digital-br

Guia aberto e prático de conformidade para desenvolvimento de **sistemas de
saúde digital no Brasil**. Autoridade curada, não enciclopédia: cada norma
vira uma ficha focada em *como aplicar em código*.

> **Status:** MVP em construção. Conteúdo em revisão contínua. Contribuições
> são bem-vindas — veja [`CONTRIBUTING.md`](./CONTRIBUTING.md).

## Para quem é este guia

1. **Pessoas desenvolvedoras** que iniciam ou evoluem sistemas de saúde
   digital (SUS, operadoras, laboratórios, pesquisa clínica) e precisam de
   um ponto de partida já cotejado com LGPD, ANPD, SBIS/CFM, MS/DATASUS e
   OWASP.
2. **Assistentes de IA** (Claude Code, Copilot, Cursor) que podem consumir
   este repositório como contexto para gerar código aderente *por padrão*.
   Veja [`AGENTS.md`](./AGENTS.md) e
   [`ai/system-prompts/`](./ai/system-prompts/).

## Como usar

- **Começando um projeto?** Leia
  [`docs/checklists/pre-deploy-saude.md`](./docs/checklists/pre-deploy-saude.md)
  e os cenários em [`docs/cenarios/`](./docs/cenarios/). Eles apontam,
  para cada situação operacional (auto-cadastro, auditoria, consentimento
  etc.), quais normas se aplicam e como resolvê-las em código.
- **Procurando uma norma específica?** Vá direto a
  [`docs/normas/`](./docs/normas/).
- **Certificação SBIS NGS1 Estágio 1?** Use
  [`docs/checklists/sbis-ngs1-estagio1.md`](./docs/checklists/sbis-ngs1-estagio1.md)
  como matriz de rastreabilidade.
- **Stack Django?** Veja o template de referência em
  [`examples/django-auth-lgpd-compliant/`](./examples/django-auth-lgpd-compliant/)
  com autenticação por CPF, trilha de auditoria e aceite de termo de uso.

## Índice

### Conceitos
- [`docs/00-glossario.md`](./docs/00-glossario.md)

### Normas (por eixo)
- [`docs/normas/lgpd/`](./docs/normas/lgpd/) — LGPD focada em saúde
- [`docs/normas/marco-civil/`](./docs/normas/marco-civil/) — Marco Civil da Internet
- [`docs/normas/sbis-cfm/`](./docs/normas/sbis-cfm/) — Certificação SBIS/CFM
- [`docs/normas/ms-datasus/`](./docs/normas/ms-datasus/) — MS / DATASUS / RNDS
- [`docs/normas/anpd/`](./docs/normas/anpd/) — Resoluções e guias da ANPD
- [`docs/normas/apf-seguranca/`](./docs/normas/apf-seguranca/) — Segurança na APF
- [`docs/normas/pesquisa-inaep/`](./docs/normas/pesquisa-inaep/) — Pesquisa com seres humanos

### Cenários práticos
- [`docs/cenarios/autenticacao.md`](./docs/cenarios/autenticacao.md)
- [`docs/cenarios/autorizacao-rbac.md`](./docs/cenarios/autorizacao-rbac.md)
- [`docs/cenarios/auditoria.md`](./docs/cenarios/auditoria.md)
- [`docs/cenarios/auto-cadastro-publico.md`](./docs/cenarios/auto-cadastro-publico.md)
- [`docs/cenarios/armazenamento-dado-sensivel.md`](./docs/cenarios/armazenamento-dado-sensivel.md)
- [`docs/cenarios/compartilhamento-rnds.md`](./docs/cenarios/compartilhamento-rnds.md)
- [`docs/cenarios/consentimento.md`](./docs/cenarios/consentimento.md)

### Checklists
- [`docs/checklists/sbis-ngs1-estagio1.md`](./docs/checklists/sbis-ngs1-estagio1.md)
- [`docs/checklists/lgpd-minimo-viavel.md`](./docs/checklists/lgpd-minimo-viavel.md)
- [`docs/checklists/owasp-top10-saude.md`](./docs/checklists/owasp-top10-saude.md)
- [`docs/checklists/pre-deploy-saude.md`](./docs/checklists/pre-deploy-saude.md)

### Templates
- [`templates/termo-de-uso.md.tpl`](./templates/termo-de-uso.md.tpl)
- [`templates/politica-de-privacidade.md.tpl`](./templates/politica-de-privacidade.md.tpl)

### Exemplos de código
- [`examples/django-auth-lgpd-compliant/`](./examples/django-auth-lgpd-compliant/) — completo
- [`examples/flask-auth-lgpd-compliant/`](./examples/flask-auth-lgpd-compliant/) — stub
- [`examples/dash-audit-trail-minimal/`](./examples/dash-audit-trail-minimal/) — stub

### IA
- [`AGENTS.md`](./AGENTS.md) — instruções para Claude Code / Copilot / Cursor
- [`ai/system-prompts/`](./ai/system-prompts/) — prompts para revisão/auditoria
- [`ai/knowledge-packs/normas-index.yml`](./ai/knowledge-packs/normas-index.yml) — índice YAML consumível por LLM

## Escopo

| Inclui | Não inclui |
|---|---|
| Lei federal, decreto, portaria, resolução com impacto em código | Normas estaduais/municipais específicas |
| SBIS/CFM NGS1 Estágio 1 | NGS2 (certificado ICP-Brasil) |
| LGPD, Marco Civil, PNSI, PNIIS, RNDS, ANPD, OWASP | CFM resoluções de telessaúde clínica (fora do recorte aqui) |
| Exemplo Django completo | Frameworks frontend proprietários |

## Limitações

- **Não é assessoria jurídica.** É material de apoio técnico. Decisões de
  conformidade devem envolver advogado/DPO da instituição.
- **Normas mudam.** Cada ficha registra a versão consultada; o leitor deve
  validar vigência antes de usar.
- **Autoridade curada, não enciclopédia.** Quando uma norma for irrelevante
  para o recorte "sistemas de saúde digital", ela não entra — por design.

## Licença

- Código (`examples/`, `templates/`, `ai/knowledge-packs/`): **Apache-2.0**.
- Conteúdo editorial (demais arquivos): **CC BY 4.0**.

Detalhes em [`LICENSE`](./LICENSE).

## Contribuindo

Veja [`CONTRIBUTING.md`](./CONTRIBUTING.md) e
[`CODE_OF_CONDUCT.md`](./CODE_OF_CONDUCT.md).

## Autor

Mantenedor: [@jailtoncarlos](https://github.com/jailtoncarlos). Issues e
pull requests são o caminho preferido para correções, sugestões de novas
normas e novos cenários.
