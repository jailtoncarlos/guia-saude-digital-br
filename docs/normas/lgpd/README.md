# LGPD — Lei nº 13.709/2018 aplicada a sistemas de saúde

## Identificação

- **Nome:** Lei Geral de Proteção de Dados Pessoais.
- **Base legal:** Lei nº 13.709, de 14 de agosto de 2018.
- **Link oficial:** <https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm>
- **Vigência:** desde 18/09/2020 (sanções administrativas desde 01/08/2021).
- **Regulador:** ANPD — Autoridade Nacional de Proteção de Dados.

## Objeto e sujeitos

Regula o tratamento de dados pessoais por pessoa natural ou jurídica, de
direito público ou privado, incluindo meios digitais. Em saúde digital,
aplica-se integralmente porque **dado de saúde é dado pessoal sensível**
(Art. 5º, II).

Sujeitos-chave:

- **Controlador** — define propósito e meios (geralmente o órgão/empresa que
  opera o sistema).
- **Operador** — trata dados em nome do controlador (pode ser o fornecedor
  de software, cloud provider etc.).
- **Encarregado (DPO)** — ponto de contato entre controlador, titulares e
  ANPD.
- **Titular** — pessoa natural a quem os dados se referem (paciente,
  servidor, cidadão).

## Artigos-chave aplicados a sistemas de saúde

### Art. 5º, II — Dado pessoal sensível

Define dado pessoal sensível como dado sobre origem racial/étnica,
convicção religiosa, opinião política, filiação a sindicato, **dado
referente à saúde ou à vida sexual**, dado genético e biométrico.

**Prático:** qualquer campo de prontuário, diagnóstico, laudo, procedimento,
exame, medicamento, histórico clínico é sensível. Tratamento exige base
legal específica do Art. 11 (não basta consentimento genérico).

### Art. 6º — Princípios

Relevantes para sistemas de saúde:

- **VI — Transparência:** informação clara sobre finalidade, forma e
  duração do tratamento. Implica **termo de uso + política de privacidade**
  acessíveis antes do cadastro.
- **VII — Segurança:** medidas técnicas e administrativas aptas a proteger
  os dados de acessos não autorizados. Casa com Art. 46 e Marco Civil Art. 15.
- **X — Responsabilização e prestação de contas:** o controlador deve
  demonstrar adoção de medidas eficazes. **Trilha de auditoria** é artefato
  central.

### Art. 7º, Art. 8º, Art. 11 — Bases legais e consentimento

- Em sistemas **do poder público** (SUS, SES, SMS), a base legal usual é o
  **cumprimento de obrigação legal** (Art. 7º, II) ou **execução de
  políticas públicas** (Art. 7º, III), **não** consentimento.
- Em sistemas **privados** (operadoras, laboratórios), pode ser
  execução de contrato (Art. 7º, V) ou consentimento específico e
  destacado (Art. 8º).
- Para **dado sensível** (Art. 11), o consentimento, quando usado, deve
  ser **específico e destacado** para cada finalidade. No poder público,
  aplicam-se as hipóteses de tratamento compartilhado do Art. 11, II, "b"
  e "c".

### Art. 15 — Término do tratamento

O tratamento deve terminar quando a finalidade se esgotar. Na prática:

- Ter **política de retenção** e procedimento de anonimização/eliminação.
- O Marco Civil Art. 15 impõe **guarda mínima de 6 meses** de registros de
  acesso — prevalece quando há conflito (retenção ≥ 6 meses para logs).
- Em sistemas SUS, retenção de prontuário segue CFM Res. 1.821/2007 (≥20
  anos em papel ou permanente em digital) — prevalece sobre "esgotamento"
  genérico da LGPD.

### Art. 46 — Segurança

Obriga adoção de medidas técnicas e administrativas. **Não lista
tecnologias específicas** — mas a ANPD considera "inadequadas" soluções
sem:

- Autenticação forte (ver SBIS NGS1.02).
- Controle de acesso baseado em papéis (ver SBIS NGS1.03).
- Criptografia em trânsito (TLS ≥1.2) e em repouso para dado sensível.
- Trilha de auditoria (ver SBIS NGS1.07).
- Plano de resposta a incidentes.

## Implicações técnicas

1. **Termo de uso e política de privacidade** obrigatórios no primeiro
   acesso. Versionados. Registrar aceite com data, IP e versão.
   → ver [`../../cenarios/consentimento.md`](../../cenarios/consentimento.md).
2. **Identificação unívoca** do usuário (CPF em SUS) para responsabilização.
   → ver [`../ms-datasus/pniis-589-2015.md`](../ms-datasus/pniis-589-2015.md).
3. **Minimização** — não colete campo que não tem finalidade declarada.
4. **Trilha de auditoria** com IP, user-agent, evento, timestamp UTC.
   → ver [`../../cenarios/auditoria.md`](../../cenarios/auditoria.md).
5. **Direitos do titular** (Art. 18) — expor endpoints/processos para
   acesso, correção, portabilidade, eliminação, anonimização.
6. **Incidente de segurança** (Art. 48) — comunicar ANPD e titulares
   afetados em prazo razoável (a Res. ANPD 15/2024 detalha).

## Armadilhas comuns

- **"Consentimento resolve tudo."** Errado em poder público — a base legal
  é outra. E mesmo no privado, consentimento para dado sensível exige
  **especificidade** por finalidade; não vale "aceito os termos" genérico.
- **Logar CPF em texto plano** em arquivo de log. Viola minimização e
  segurança. Use mascaramento ou hash.
- **Usar e-mail como chave** em sistema SUS. E-mail não é identificador
  unívoco; cidadão pode não ter ou trocar. Usar CPF (ver SBIS NGS1.03.09).
- **Retenção indefinida** de logs "por garantia". Viola Art. 15 —
  mantenha apenas o necessário e justifique.
- **Esquecer o Art. 46 em ambiente de homologação.** Dado de saúde em
  homolog/staging deve ser **sintético ou anonimizado**. Nunca espelhar
  produção sem tratamento.

## Referências cruzadas

- Cenários:
  [auth](../../cenarios/autenticacao.md),
  [auditoria](../../cenarios/auditoria.md),
  [auto-cadastro](../../cenarios/auto-cadastro-publico.md),
  [dado sensível](../../cenarios/armazenamento-dado-sensivel.md),
  [consentimento](../../cenarios/consentimento.md).
- Normas relacionadas:
  [Marco Civil Art. 15](../marco-civil/README.md),
  [Res. ANPD 30/2025](../anpd/resolucao-30-2025.md),
  [Guia ANPD Poder Público](../anpd/guia-poder-publico-2024.md),
  [SBIS NGS1.11.01](../sbis-cfm/README.md).
- Checklists:
  [LGPD mínimo viável](../../checklists/lgpd-minimo-viavel.md).

## Versão consultada

- Texto da lei conforme Planalto em 2026-04-22, consolidado até Lei
  14.010/2020 e alterações posteriores até 13.853/2019 (criação da ANPD)
  e alterações da LC 192/2022 (isenções fiscais da ANPD; não impactam o
  conteúdo substantivo).
