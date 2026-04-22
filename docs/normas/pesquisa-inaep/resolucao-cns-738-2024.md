# Resolução CNS nº 738/2024 (republicada em 2025)

## Identificação

- **Nome:** Dispõe sobre uso, armazenamento e transferência de bancos de
  dados em pesquisa com seres humanos.
- **Base legal:** Resolução CNS nº 738/2024, republicada em 2025.
- **Link oficial:** <https://conselho.saude.gov.br/resolucoes-cns>
- **Regulador:** Conselho Nacional de Saúde (CNS); em articulação com Inaep.

## Objeto e sujeitos

Regula o tratamento de **bancos de dados** em pesquisa com seres humanos:
constituição, uso secundário, transferência entre instituições,
armazenamento e retenção.

## Pontos-chave para sistemas de dados

### Rastreabilidade em transferências

Toda transferência de dataset entre instituições de pesquisa precisa ser
**registrada** com:

- Instituição origem e destino.
- Pesquisador responsável.
- Finalidade / projeto CAAE.
- Data.
- Conformidade LGPD (base legal).

### Armazenamento mínimo de 5 anos

Dataset de pesquisa e seus metadados (incluindo TCLE e trilha de acesso)
devem ser mantidos por **pelo menos 5 anos** após o término do projeto,
para permitir auditoria ética.

### Segurança e pseudonimização

- Armazenar dataset **pseudonimizado por padrão**.
- Tabela de mapeamento (ID-pesquisa ↔ identificadores diretos) em
  repositório separado, com acesso restrito ao pesquisador responsável.
- Criptografia em repouso.
- Trilha de acesso.

## Implicações técnicas

1. **Schema de pesquisa separado** — `research.*` diferente de `clinical.*`.
2. **View pseudonimizada** — visão sobre dados assistenciais que substitui
   CPF/CNS por ID de pesquisa.
3. **Export autorizado** — procedimento que gera pacote de export com
   metadados (instituição, CAAE, finalidade, hash do conteúdo).
4. **Retenção configurável ≥5 anos** para artefatos de pesquisa.
5. **Log de acesso** a dataset de pesquisa com CAAE e finalidade no campo.

## Armadilhas comuns

- **Enviar CSV bruto por e-mail** entre pesquisadores — comum, **viola** a
  Resolução. Usar repositório institucional com registro.
- **Pseudonimização apenas por "apagar CPF"** — dado de saúde com atributos
  combinados reidentifica. Avaliar k-anonymity ou agregação.
- **Descartar dataset ao fim do projeto** — **não**. Manter ≥5 anos.

## Referências cruzadas

- [Lei 14.874/2024](./lei-14874-2024.md).
- [LGPD](../lgpd/README.md).
- [Res. ANPD 30/2025](../anpd/resolucao-30-2025.md).

## Versão consultada

- Referência bibliográfica em 2026-04-22; conferir texto republicado em
  2025 no CNS.
