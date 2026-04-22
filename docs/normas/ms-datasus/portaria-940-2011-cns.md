---
title: Portaria GM/MS nº 940/2011 — Cartão Nacional de Saúde (CNS)
tipo: portaria
orgao: Ministério da Saúde — Gabinete do Ministro
ano: 2011
url_oficial: https://bvsms.saude.gov.br/bvs/saudelegis/gm/2011/prt0940_28_04_2011.html
escopo: "Regulamenta o Sistema Cartão Nacional de Saúde (CNS). Define o CNS como identificador único do usuário do SUS em todos os sistemas de informação em saúde."
aplicavel_a_saude_digital: alta
---

# Portaria GM/MS nº 940, de 28 de abril de 2011

> Regulamenta o Sistema Cartão Nacional de Saúde (Sistema Cartão).

## Objeto e quem está sujeito

Estabelece o **Cartão Nacional de Saúde (CNS)** como identificador unívoco do usuário do SUS. **Todo sistema de informação em saúde** — seja do MS, estadual, municipal ou de prestador privado que atende o SUS — deve adotar o CNS como chave para identificar pacientes e profissionais.

## Artigos-chave aplicados a sistemas de saúde digital

### Art. 2º — Natureza do CNS

O CNS é:
- **Unívoco por pessoa** — cada cidadão recebe um número único.
- **Nacional** — válido em todo o território.
- **Integrado** — amarra atendimentos em qualquer unidade do SUS ao mesmo indivíduo.

### Art. 3º — Obrigatoriedade de uso

Determina o uso do CNS:
- No cadastramento de usuários, profissionais e estabelecimentos de saúde.
- Na identificação de procedimentos ambulatoriais e hospitalares (vinculação com APAC, AIH, etc.).
- No registro de atendimentos clínicos.

### Art. 4º — Profissionais de saúde

Profissionais de saúde também têm CNS próprio — usado para identificar autoria em laudos, prescrições, assinaturas digitais em sistemas.

### Art. 7º — Interoperabilidade

Sistemas de informação em saúde devem ser **capazes de capturar, armazenar e exportar o CNS** em qualquer operação. O CNS é a chave-raiz da interoperabilidade no SUS.

## Relação com CPF

CNS e CPF **coexistem**:

- **CNS** = identificador **setorial** (SUS).
- **CPF** = identificador **universal** do cidadão no Brasil (Receita Federal, gov.br).

Sistemas modernos em saúde devem **capturar ambos** quando possível:
- **CPF** como identidade cívica de profissionais que operam o sistema (alinhado à Lei 14.129/2021).
- **CNS** como chave de integração com o SUS (alinhado a esta portaria e à Portaria MS 2.073/2011).

## Implicações técnicas

- Modelos de usuário (operadores, gestores, profissionais) devem ter campo **`cns`** ao lado de `cpf`.
- Modelos de paciente devem ter `cns` obrigatório (quando disponível), `cpf` complementar.
- Em IdP (ex.: Keycloak), `cns` é atributo declarativo do usuário, exposto como claim no token.
- Interoperabilidade com RNDS, e-SUS, SISCAN, APAC, SIH — todos usam CNS como chave.

## Armadilhas comuns

- Usar CPF no lugar de CNS para atendimento: viola a portaria. CPF é opcional/complementar; CNS é o primário para o tratamento clínico.
- Confundir CNS do paciente com CNS do profissional: são tabelas diferentes, contextos diferentes.
- Não persistir o CNS em histórico — perde-se capacidade de linkage longitudinal.

## Referências cruzadas

- [Portaria MS 2.073/2011](portaria-2073-2011.md) — padrões de interoperabilidade (CNS + CPF como chaves).
- [ESD28 — Portaria 1.434/2020](esd28-1434-2020.md) — saúde digital.
- [RNDS — Decreto 12.560/2025](rnds-12560-2025.md) — Rede Nacional de Dados em Saúde (CNS como chave federada).
- [Lei 14.129/2021](../apf-seguranca/lei-14129-2021.md) — Governo Digital (CPF como identidade civil).

## Histórico e atualizações

- 2011-04-28: publicação original.
- Atualizações incorporadas em portarias subsequentes do Ministério da Saúde.
- Regulamentação complementar pelo DATASUS.
