# APF e Segurança da Informação

Fichas de normas de segurança da informação aplicáveis à Administração
Pública Federal — e, por equivalência prática, a sistemas públicos em
todos os níveis.

| Ficha | Norma | Tema |
|---|---|---|
| [PNSI](./pnsi-9637-2018.md) | Decreto nº 9.637/2018 | Política Nacional de Segurança da Informação |
| [IN GSI/PR nº 1/2020](./in-gsi-1-2020.md) | IN GSI/PR nº 1/2020 | Controles mínimos de segurança em sistemas da APF |

## Decreto 10.046/2019 (governança de compartilhamento)

Não ganhou ficha separada porque seu impacto de código se manifesta
principalmente via RNDS e via procedimentos administrativos. Resumo:

- Institui o **Cadastro Base do Cidadão** e governança de compartilhamento
  entre órgãos da APF.
- Exige **rastreabilidade** de quem acessou qual dado — casa com trilha de
  auditoria já exigida por LGPD, Marco Civil e SBIS NGS1.07.
- Exige **finalidade declarada** no pedido de compartilhamento.

Para desenvolvedor: se o sistema se conecta a outro órgão federal (SUS,
Receita Federal, CAGED etc.) via barramento, **registre finalidade e
identificação do consumidor** em cada chamada. Isso é exigido.

Ficha completa do Decreto 10.046/2019 fica no *backlog* (contribuições
bem-vindas via PR).
