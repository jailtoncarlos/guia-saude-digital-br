# Checklist — LGPD mínimo viável para sistema de saúde

Itens que **todo** sistema de saúde digital precisa endereçar antes do
primeiro deploy, independentemente de porte.

## Base legal e transparência

- [ ] **Base legal declarada** para cada finalidade (Art. 7º / Art. 11).
      Em sistema SUS, tipicamente Art. 7º II/III e Art. 11 II "b"/"c".
- [ ] **Política de privacidade** publicada, acessível sem login,
      explicando finalidades, base legal, retenção, direitos do titular.
- [ ] **Termo de uso** publicado e aceito no 1º acesso
      (ver [cenário de consentimento](../cenarios/consentimento.md)).
- [ ] **DPO/Encarregado** com nome, cargo e contato publicados.

## Identidade e acesso

- [ ] **Identificador unívoco** (CPF em SUS — ver
      [PNIIS](../normas/ms-datasus/pniis-589-2015.md)).
- [ ] **Senha** com hash ≥160 bits.
- [ ] **RBAC** — papéis definidos e aplicados server-side.
- [ ] **Menor privilégio** na conexão da aplicação com o banco.

## Segurança

- [ ] **HTTPS** obrigatório (`SECURE_SSL_REDIRECT`, HSTS).
- [ ] **Cookie de sessão** `Secure`, `HttpOnly`, `SameSite`.
- [ ] **Segredo fora do VCS** — `.env` no `.gitignore`.
- [ ] **Criptografia em repouso** do banco / volume.
- [ ] **Rate limit** em rotas sensíveis (login, cadastro, reset).

## Dado e minimização

- [ ] Inventário de campos por finalidade (**não coletar por comodidade**).
- [ ] Dado sensível em **schema separado**.
- [ ] Log de aplicação **sem CPF em claro** (mascarar ou hash).
- [ ] Homologação com dado **sintético ou anonimizado**.

## Trilha de auditoria

- [ ] `LoginEvent` (ou equivalente) com IP, UA, timestamp UTC, usuário,
      tipo de evento.
- [ ] **Append-only** — ACL que nega UPDATE/DELETE para a aplicação.
- [ ] **Retenção ≥6 meses** (Marco Civil Art. 15).
- [ ] **Exportação** possível para CSV/JSON com metadados.

## Direitos do titular (LGPD Art. 18)

- [ ] Canal documentado de solicitação (e-mail do DPO + formulário).
- [ ] Prazo interno de **15 dias** para responder.
- [ ] Procedimento de **correção** de dado cadastral.
- [ ] Procedimento de **anonimização/eliminação** quando cabível.
- [ ] Procedimento de **portabilidade** (ex.: export em JSON).

## Incidentes (LGPD Art. 48)

- [ ] **Runbook de incidente** no repositório.
- [ ] Canal ETIR/COSEGI (se APF) ou DPO (se privado).
- [ ] **Template** de notificação ANPD e titulares.
- [ ] **Prazo** definido internamente (ANPD: 3 dias úteis quando
      provável risco relevante — Res. 15/2024).

## Operador e fornecedor

- [ ] **Contrato** com cláusulas LGPD para cada operador.
- [ ] **Transferência internacional** sob CPC ou outro mecanismo do Art.
      33 se aplicável
      (ver [Res. ANPD 19/2024](../normas/anpd/resolucao-19-2024.md)).
- [ ] **Cláusula de auditoria** e fim de contrato (devolução /
      eliminação).

---

Use junto com [`pre-deploy-saude.md`](./pre-deploy-saude.md).
