# Resolução CD/ANPD nº 19/2024 — Transferência Internacional de Dados

## Identificação

- **Nome:** Regulamento de Transferência Internacional de Dados.
- **Base legal:** Resolução CD/ANPD nº 19/2024.
- **Link oficial:** <https://www.gov.br/anpd/pt-br>
- **Regulador:** ANPD.

## Objeto e sujeitos

Regulamenta as hipóteses de transferência internacional de dados pessoais
previstas nos Arts. 33 a 36 da LGPD. Relevante para sistemas de saúde
digital que usem:

- **Provedores de nuvem global** com processamento fora do Brasil.
- **Ferramentas de análise** (BI, analytics) com infraestrutura no
  exterior.
- **APIs de IA** hospedadas em outros países.
- **Suporte técnico terceirizado** com acesso remoto a dados do país sede.

## Mecanismos admitidos

A LGPD e a Resolução 19/2024 admitem:

1. **Decisão de adequação** da ANPD (lista de países — em construção).
2. **Cláusulas-Padrão Contratuais (CPC)** publicadas pela ANPD.
3. **Cláusulas contratuais específicas** submetidas à ANPD.
4. **Normas corporativas globais** aprovadas pela ANPD.
5. **Selos, certificados, códigos de conduta** aprovados pela ANPD.
6. **Cooperação jurídica internacional**, garantia da vida etc. (hipóteses
   legais específicas).

Para o dia-a-dia de TI, o caminho usual é **CPC** ou **cláusulas
específicas**. Sem um desses, transferência é **irregular**.

## Implicações técnicas

1. **Inventariar fluxos internacionais** — toda API, SDK, plugin,
   *tracker* que envie dado a país estrangeiro entra no inventário.
2. **Registrar no RIPD/DPIA** — mapear transferência, finalidade, base
   legal e mecanismo.
3. **Evitar transferência quando possível** — em saúde, preferir região
   Brasil do provedor ou *self-hosting*.
4. **Se inevitável, firmar CPC** — incluir no contrato com o operador.
5. **Minimização extra** — pseudonimizar/agregar antes de enviar.

## Armadilhas comuns

- **SDK de analytics no front-end** — enviar hit para servidor no exterior
  com identificador que permite vincular ao CPF = transferência
  internacional de dado sensível (se o contexto for saúde). Regra: **não
  usar** analytics 3rd-party em páginas autenticadas de saúde sem
  pseudonimização e CPC.
- **Modelo de IA em API externa** com envio do texto do prontuário = risco
  extremo. Mesmo com CPC, pondere se a finalidade justifica.
- **Suporte remoto do fornecedor** acessando produção — é transferência
  (acesso à distância configura tratamento internacional).

## Referências cruzadas

- [LGPD Arts. 33–36](../lgpd/README.md).
- [Cloud MS (Portaria 7.678/2025)](../ms-datasus/cloud-7678-2025.md).
- [Res. ANPD 30/2025 (prioridades 2026–2027)](./resolucao-30-2025.md).

## Versão consultada

- Referência bibliográfica em 2026-04-22. Conferir publicação oficial na
  ANPD.
