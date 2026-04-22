# Contribuindo

Obrigado pelo interesse em contribuir com o **guia-saude-digital-br**. Este
guia é mantido de forma aberta e se beneficia de revisão técnica e jurídica
contínua da comunidade.

## Tipos de contribuição bem-vindos

1. **Correção de erro normativo** — artigo citado incorretamente, link
   oficial quebrado, norma revogada, interpretação equivocada. *Prioridade máxima.*
2. **Atualização de vigência** — uma norma foi alterada, republicada ou
   revogada.
3. **Nova ficha de norma** dentro do recorte "sistemas de saúde digital no
   Brasil".
4. **Novo cenário** prático (ex.: integração FHIR, envio para e-SUS APS,
   laudo digital assinado etc.).
5. **Melhorias no exemplo Django** ou novos exemplos (Flask, FastAPI,
   Dash).
6. **Melhorias nos system prompts** e no knowledge-pack YAML consumido por
   LLMs.

## O que **não** aceitamos

- Cópia integral do texto de leis/portarias — a licença CC BY não se
  estende a obras oficiais, e o guia é uma *interpretação curada*. Sempre
  citar e linkar a fonte oficial.
- Conteúdo jurídico sem referência verificável.
- Expansão para fora do recorte "saúde digital no Brasil" (ex.: LGPD em
  e-commerce, ISO 27001 genérica sem conexão com saúde).

## Padrão de ficha de norma

Cada ficha em `docs/normas/.../*.md` segue **exatamente** esta estrutura:

1. **Identificação** — nome oficial, base legal, ano, link gov.br (ou
   órgão equivalente).
2. **Objeto e sujeitos** — o que a norma regula e a quem se aplica.
3. **Artigos-chave aplicados a sistemas de saúde** — apenas o relevante,
   com interpretação prática. Não copiar lei inteira.
4. **Implicações técnicas** — o que o código precisa fazer, com
   referência a cenários/exemplos.
5. **Armadilhas comuns** — erros frequentes observados em projetos.
6. **Referências cruzadas** — links para outras fichas, cenários,
   checklists.
7. **Versão consultada** — data e versão.

## Padrão de cenário

1. Descrição do cenário operacional.
2. Riscos jurídicos e de segurança.
3. Normas aplicáveis (com links para as fichas).
4. Requisitos mínimos (checklist inline).
5. Exemplo de implementação (preferencialmente Django).
6. Como testar conformidade.

## Padrão de commits

Mensagens em português, no imperativo, seguindo *conventional commits*
simplificado:

```
docs(normas): corrige artigo citado em lgpd/README.md
docs(cenarios): adiciona cenário de assinatura digital ICP-Brasil
feat(examples): adiciona exemplo Flask com auditoria
fix(checklists): corrige link quebrado em sbis-ngs1-estagio1.md
```

**Não incluir co-autoria automática de LLM** nos commits. Se usou IA na
pesquisa, cite na descrição do PR, não no commit.

## Fluxo de PR

1. Abra uma issue antes se a mudança for grande (>200 linhas ou nova
   seção inteira).
2. Faça fork, crie branch `docs/<tema>` ou `feat/<tema>`.
3. Rode uma revisão de links (futuramente um workflow fará isso
   automaticamente — veja
   [`docs/checklists/pre-deploy-saude.md`](./docs/checklists/pre-deploy-saude.md)).
4. Abra PR com descrição do impacto normativo ("esta mudança altera
   interpretação de X porque...").
5. Aguarde revisão — prazo alvo: 7 dias.

## Revisão de interpretação jurídica

Fichas que alteram *interpretação* (não só tipografia) devem receber, além
da revisão técnica, validação por alguém com leitura direta da norma.
Prefira citar o artigo e o link oficial a parafrasear de memória.

## Código de conduta

Veja [`CODE_OF_CONDUCT.md`](./CODE_OF_CONDUCT.md).
