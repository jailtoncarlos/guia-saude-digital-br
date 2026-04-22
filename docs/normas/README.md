# Normas

Fichas das normas aplicáveis a sistemas de saúde digital no Brasil,
organizadas por eixo. Cada ficha segue o padrão descrito em
[`../../CONTRIBUTING.md`](../../CONTRIBUTING.md#padrão-de-ficha-de-norma).

## Eixos

| Eixo | Pasta | O que cobre |
|---|---|---|
| LGPD | [`lgpd/`](./lgpd/) | Lei 13.709/2018 aplicada a sistemas de saúde |
| Marco Civil | [`marco-civil/`](./marco-civil/) | Lei 12.965/2014 — Art. 15 (guarda de logs) |
| SBIS/CFM | [`sbis-cfm/`](./sbis-cfm/) | Certificação S-RES, NGS1 Estágio 1 |
| MS/DATASUS | [`ms-datasus/`](./ms-datasus/) | PNIIS, ESD28, SUS Digital, RNDS, Cloud MS, POSIC |
| ANPD | [`anpd/`](./anpd/) | Resoluções 19/2024 e 30/2025, Guia Poder Público 2024 |
| APF/Segurança | [`apf-seguranca/`](./apf-seguranca/) | PNSI (Decreto 9.637/2018), IN GSI/PR nº 1/2020 |
| Pesquisa/Inaep | [`pesquisa-inaep/`](./pesquisa-inaep/) | Lei 14.874/2024 + Decreto 12.651/2025; Res. CNS 738/2024 |

## Matriz cenário × normas

Consulte também a visão cruzada em
[`../cenarios/`](../cenarios/): cada cenário operacional já aponta para
as fichas das normas aplicáveis.

| Cenário | Normas principais |
|---|---|
| Autenticação | LGPD Art. 6º VII; Marco Civil Art. 15; PNSI; IN GSI/PR 1/2020; SBIS NGS1.02; OWASP ASVS V2 |
| RBAC / gestão de usuários | LGPD Art. 6º X; SBIS NGS1.03; OWASP ASVS V4 |
| Auditoria de acessos | LGPD Art. 6º VII/X, 15, 46; Marco Civil Art. 15; Decreto 10.046/2019; PNSI; IN GSI/PR 1/2020; SBIS NGS1.07 |
| Auto-cadastro público | LGPD Art. 6º VI (transparência), 9º; SBIS NGS1.06.03 (validação); OWASP ASVS V11 |
| Dado pessoal sensível | LGPD Art. 5º II, 11, 46; Res. ANPD 30/2025; Guia ANPD Poder Público |
| Compartilhamento RNDS | Decreto 12.560/2025; Portaria 3.232/2024; ESD28; Decreto 10.046/2019 |
| Consentimento | LGPD Art. 7º/8º/11; Guia ANPD Poder Público |
| Termo de uso do servidor | SBIS NGS1.11.01; LGPD Art. 6º VI |
| Uso em pesquisa (futuro) | Lei 14.874/2024 + Decreto 12.651/2025; Res. CNS 738/2024 |
