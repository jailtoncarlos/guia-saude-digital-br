# Certificação SBIS/CFM — Manual de Certificação de S-RES

## Identificação

- **Nome:** Manual de Certificação para Sistemas de Registro Eletrônico em
  Saúde (S-RES).
- **Mantenedores:** Sociedade Brasileira de Informática em Saúde (SBIS) e
  Conselho Federal de Medicina (CFM).
- **Versão de referência do guia:** Requisitos v5.2, de 10/11/2021,
  categoria **Segurança da Informação**.
- **Link oficial:** <https://sbis.org.br/certificacao/>
- **Nível coberto:** **NGS1 Estágio 1 — Essencial** (mínimos para aderência
  à legislação). NGS2 exige certificado digital ICP-Brasil e está **fora
  do escopo** deste guia.

## Objeto e sujeitos

Define requisitos para sistemas que coletam, armazenam e processam
Registro Eletrônico em Saúde. Se aplica a sistemas analíticos de dados de
saúde que **não se enquadram** em PEP (Prontuário Eletrônico), Telessaúde,
Receita Digital ou SADT — nesses casos existem categorias específicas.

## Requisitos-chave do NGS1 Estágio 1

Agrupados por família. O checklist completo com matriz issue-commit está
em [`../../checklists/sbis-ngs1-estagio1.md`](../../checklists/sbis-ngs1-estagio1.md).

### NGS1.01 — Controle de versão do software

- **NGS1.01.01** — Exibição de versão do software ao usuário.

### NGS1.02 — Identificação e autenticação

- **NGS1.02.01** — Método de autenticação (senha + identificador unívoco).
- **NGS1.02.02** — Proteção de parâmetros: hash de senha **≥160 bits**
  (PBKDF2 padrão Django, Argon2, bcrypt atendem).
- **NGS1.02.03** — Qualidade mínima da senha: ≥8 caracteres, ≥1
  maiúscula, ≥1 numérico (política "8/1/1").
- **NGS1.02.04** — Forçar troca periódica (recomendação; avaliar contra
  NIST SP 800-63 que desaconselha expiração automática sem motivo).
- **NGS1.02.06** — Geração inicial pelo administrador + troca forçada no
  primeiro login.
- **NGS1.02.08** — Troca pelo próprio usuário autenticado.
- **NGS1.02.11** — Nova senha diferente da atual e da anterior (manter
  histórico mínimo).
- **NGS1.02.12** — "Esqueci minha senha" por canal previamente registrado
  (e-mail do cadastro).
- **NGS1.02.13** — Bloqueio após N tentativas falhas consecutivas
  (recomendado 5). Desbloqueio por tempo ou por administrador.
- **NGS1.02.15** — Informação do último login após autenticação bem
  sucedida.
- **NGS1.02.16** — Mensagem genérica em falha de login (não revelar se é
  usuário ou senha que errou).
- **NGS1.02.17** — Impedir memorização de credenciais pelo navegador
  (`autocomplete="off"` / `new-password`).
- **NGS1.02.20** — Bloqueio/encerramento por inatividade (sessão).
- **NGS1.02.23** — Segurança contra roubo de sessão (cookie `Secure`,
  `HttpOnly`, `SameSite`; HTTPS; rotação de ID em login).

### NGS1.03 — Autorização e controle de acesso

- **NGS1.03.01** — Impedir acesso por pessoas não autorizadas.
- **NGS1.03.02** — Perfis mínimos (RBAC).
- **NGS1.03.07** — Múltiplos perfis por usuário (pode ficar em escopo
  futuro).
- **NGS1.03.08** — Gerenciamento de usuários via aplicação (não via SQL
  direto).
- **NGS1.03.09** — **Identidade única e responsabilização (CPF)**. Um CPF
  = um usuário. Sem compartilhamento.
- **NGS1.03.10** — Pelo menos 1 administrador ativo sempre (invariante de
  sistema).

### NGS1.04 — Disponibilidade

- **NGS1.04.01–05** — Backup e restauração do RES. Frequência e retenção
  definidas em procedimento.

### NGS1.05 — Comunicação

- **NGS1.05.01** — HTTPS + autenticação do servidor (certificado válido).
- **NGS1.05.02** — Processamento server-side (não confiar em lógica só no
  cliente).

### NGS1.06 — Segurança de dados

- **NGS1.06.01** — Uso de SGBD (não arquivo plano).
- **NGS1.06.03** — Validação de dados de entrada.

### NGS1.07 — Auditoria

- **NGS1.07.01** — Auditoria contínua.
- **NGS1.07.02** — Proteção dos registros contra alteração.
- **NGS1.07.03** — Eventos registrados (autenticação, gestão de usuário,
  troca de senha, consulta a dado sensível).
- **NGS1.07.05** — Campos obrigatórios: **IP, usuário, tipo de evento,
  data/hora**.
- **NGS1.07.06** — Privacidade do paciente na trilha (para sistemas de
  PEP; em sistemas analíticos frequentemente N/A).
- **NGS1.07.07** — Tela de consulta com filtros (período, usuário, tipo).
- **NGS1.07.08** — Exportação com metadados institucionais.

### NGS1.08 — Documentação

- **NGS1.08.01** — Manuais de uso, instalação, configuração.
- **NGS1.08.11** — Recomendações de configurações de segurança.
- **NGS1.08.12** — Histórico de alterações (release notes / CHANGELOG).

### NGS1.09 — Tempo

- **NGS1.09.01** — NTP server-side.
- **NGS1.09.03** — Registro de tempo com fuso **UTC** em trilha
  (PostgreSQL `TIMESTAMP WITH TIME ZONE`).

### NGS1.11 — Privacidade

- **NGS1.11.01** — Concordância com termo de uso no primeiro acesso.
  Registro versionado do aceite.

### NGS1.12 — Integridade

- **NGS1.12.01** — Regras de correção de dados (aplicável a sistemas com
  escrita em RES). Em sistema read-only sobre dataset externo, frequentemente
  **N/A** — justificar no checklist.

## Implicações técnicas

O exemplo Django em
[`examples/django-auth-lgpd-compliant/`](../../../examples/django-auth-lgpd-compliant/)
foi construído endereçando os itens acima. Cada arquivo traz comentários
`# NOTE: atende SBIS NGS1.XX.YY` nos pontos relevantes.

## Armadilhas comuns

- **Hash MD5/SHA-1** para senha — não atende NGS1.02.02. PBKDF2 do Django
  atende.
- **Permitir e-mail como USERNAME_FIELD** em S-RES — contraria NGS1.03.09
  (responsabilização) e PNIIS.
- **Trilha em mesmo schema/credencial da aplicação** com permissão DELETE
  — viola NGS1.07.02. Configure role separada somente-INSERT para app, e
  role-auditor somente-SELECT.
- **Timestamp em fuso local** — NGS1.09.03 pede UTC. Em PostgreSQL use
  `TIMESTAMP WITH TIME ZONE` e configure `TIME_ZONE = 'UTC'` no Django.
- **Mensagem "usuário não encontrado" vs "senha incorreta"** — permite
  enumeração. NGS1.02.16 exige mensagem genérica.
- **Marcar NGS1.12.01 como atendido sem escrita** — em sistema read-only
  marque N/A com justificativa, não "atendido".

## Referências cruzadas

- Cenários:
  [autenticação](../../cenarios/autenticacao.md),
  [autorização RBAC](../../cenarios/autorizacao-rbac.md),
  [auditoria](../../cenarios/auditoria.md).
- Checklist: [SBIS NGS1 Estágio 1](../../checklists/sbis-ngs1-estagio1.md).
- Exemplo: [Django auth LGPD-compliant](../../../examples/django-auth-lgpd-compliant/).

## Versão consultada

- Manual de Certificação SBIS/CFM, Requisitos v5.2 de 10/11/2021,
  categoria Segurança da Informação. Consulta em 2026-04-22 via
  <https://sbis.org.br/certificacao/>.
