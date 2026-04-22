# Guia Orientativo ANPD — Tratamento de Dados pelo Poder Público (2024)

## Identificação

- **Nome:** Guia Orientativo para o Tratamento de Dados Pessoais pelo
  Poder Público.
- **Publicação:** ANPD, 2024 (atualização da versão anterior de 2022).
- **Link oficial:** <https://www.gov.br/anpd/pt-br/documentos-e-publicacoes>
- **Regulador:** ANPD.

## Objeto e sujeitos

Orienta órgãos e entidades da administração pública (União, estados, DF,
municípios, autarquias, fundações, empresas públicas, sociedades de
economia mista) na aplicação da LGPD.

**Não é norma vinculante**, mas é o documento prático mais relevante para
sistemas SUS. Em fiscalização, a ANPD confrontará o operador com o guia.

## Pontos-chave para sistemas de saúde pública

### Bases legais no poder público

O guia reforça que, em regra, **consentimento não é a base adequada** para
tratamento pelo Poder Público. Bases adequadas:

- **Art. 7º, II** — cumprimento de obrigação legal ou regulatória.
- **Art. 7º, III** — execução de políticas públicas previstas em lei,
  regulamento, contrato, convênio ou instrumento congênere.
- **Art. 11, II, "b" e "c"** — para dado sensível em contexto de
  tratamento compartilhado para política pública de saúde.

**Prático:** um sistema de vigilância em saúde (ex.: SISCAN) opera sob
obrigação legal do SUS. Cidadão "retirar consentimento" não interrompe o
tratamento — porque não há consentimento em jogo. O que o cidadão tem é
**direito a informação, acesso e correção**.

### Direitos do titular

O guia orienta sobre como estruturar canais para exercer os direitos do
Art. 18 no setor público:

- **Atendimento presencial e digital** — prever ambos quando possível.
- **Prazo de resposta** — 15 dias prorrogáveis.
- **Identificação segura** do titular para evitar fraude.
- **Encarregado (DPO)** com contato publicado.

### RIPD / DPIA

Relatório de Impacto à Proteção de Dados Pessoais. O guia:

- **Não** obriga para todo tratamento — só para alto risco.
- Dado **sensível de saúde em escala** atinge o gatilho de alto risco.
- Template sugerido na própria publicação.

### Incidentes

- Notificar ANPD e titulares afetados em prazo razoável (a Res. 15/2024
  detalha — 3 dias úteis para ANPD quando provável risco relevante).
- Runbook de incidente, canal no site, contato do DPO.

## Implicações técnicas

1. **Publicar base legal** explicitamente na política de privacidade (não
   escrever "com base em consentimento" quando não for).
2. **Expor endpoints/formulários** para os direitos do Art. 18.
3. **Elaborar RIPD** para o sistema — documento vivo, revisto a cada
   grande mudança.
4. **Treinar equipe** para reconhecer incidente e acionar o runbook.
5. **Publicar DPO** — nome, cargo, e-mail de contato.

## Armadilhas comuns

- **Copiar política de privacidade de e-commerce** — base legal errada.
- **Exigir consentimento** para operação que é obrigação legal — gera
  confusão com titular e risco de a ANPD entender que foi adotada base
  inadequada.
- **Esquecer portabilidade** — Art. 18, V. Em sistema público, o canal
  mais comum é o próprio cidadão pedir via e-SIC.

## Referências cruzadas

- [LGPD](../lgpd/README.md).
- [Res. ANPD 30/2025](./resolucao-30-2025.md).
- [Checklist LGPD mínimo viável](../../checklists/lgpd-minimo-viavel.md).
- [Cenário: consentimento](../../cenarios/consentimento.md).

## Versão consultada

- Guia Orientativo ANPD, versão 2024. Consulta em 2026-04-22.
