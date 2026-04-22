# POSIC/MS — Política de Segurança da Informação e Comunicações do Ministério da Saúde

## Identificação

- **Nome:** POSIC/MS — Política de Segurança da Informação e Comunicações
  do Ministério da Saúde.
- **Mantida por:** COSEGI — Comitê de Segurança da Informação do MS.
- **Vincula:** sistemas desenvolvidos, mantidos ou hospedados pelo MS e
  suas entidades vinculadas.

## Objeto e sujeitos

Alinha a segurança da informação do MS à PNSI (Decreto 9.637/2018) e à IN
GSI/PR nº 1/2020. Aplica-se a servidores, colaboradores, terceirizados e
fornecedores que operem com ativos de informação do MS.

## Diretrizes relevantes para desenvolvedor

- **Classificação da informação** (pública, interna, restrita,
  confidencial) — projetos em saúde lidam tipicamente com "restrita" ou
  "confidencial".
- **Controle de acesso** com princípio do menor privilégio (RBAC) e
  revisões periódicas de acesso.
- **Gestão de credenciais** — não reaproveitamento, troca obrigatória em
  desligamento.
- **Gestão de incidentes** — canal COSEGI; prazo de reporte.
- **Homologação de software** antes de produção.
- **Cópia de segurança** periódica, testada, segregada.
- **Segurança no desenvolvimento** — ciclo que inclui análise de código
  estática, revisão de dependências, testes de segurança (SAST/DAST).

## Implicações técnicas

1. **Alinhar o CI/CD** a passos de SAST (ex.: Bandit, Semgrep) e checagem
   de dependências (ex.: `pip-audit`, `safety`).
2. **Variáveis sensíveis** em cofre (HashiCorp Vault, AWS Secrets Manager,
   SOPS). Nunca em `.env` comitado.
3. **Homologação** — ambiente com dado **sintético/anonimizado**. Nunca
   espelhar produção sem tratamento.
4. **Runbook de incidente** no repositório, com contatos COSEGI e DPO.
5. **Revisão de acesso** trimestral documentada.

## Armadilhas comuns

- **Credencial compartilhada de serviço** — um único usuário de banco para
  app, admin e BI. Viola menor privilégio.
- **Ambiente de homologação com dado real** — comum e grave.
- **Não registrar ato de homologação** — POSIC exige evidência.

## Referências cruzadas

- [PNSI (Decreto 9.637/2018)](../apf-seguranca/pnsi-9637-2018.md).
- [IN GSI/PR nº 1/2020](../apf-seguranca/in-gsi-1-2020.md).
- [Cloud MS (Portaria 7.678/2025)](./cloud-7678-2025.md).

## Versão consultada

- Descrição genérica; a POSIC vigente e seus anexos específicos do MS
  devem ser consultados com o COSEGI / equipe de SI do órgão.
