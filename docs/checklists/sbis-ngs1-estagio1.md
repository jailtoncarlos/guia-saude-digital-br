# Checklist — SBIS NGS1 Estágio 1 (Essencial)

Reaproveita a matriz de rastreabilidade do Manual de Certificação de S-RES
(Requisitos v5.2, categoria Segurança da Informação) no recorte **NGS1
Estágio 1**.

Para cada requisito, indique status (`⬜ pendente`, `🟡 parcial`, `✅ atendido`,
`N/A justificado`). Ver [ficha da SBIS](../normas/sbis-cfm/README.md)
para descrição completa.

## NGS1.01 — Controle de versão

| ID | Título | Status |
|---|---|---|
| NGS1.01.01 | Exibição de versão do software | ⬜ |

## NGS1.02 — Identificação e autenticação

| ID | Título | Status |
|---|---|---|
| NGS1.02.01 | Método de autenticação (identificador + senha) | ⬜ |
| NGS1.02.02 | Proteção de parâmetros (hash ≥160 bits) | ⬜ |
| NGS1.02.03 | Qualidade mínima da senha (8/1/1) | ⬜ |
| NGS1.02.04 | Troca periódica | ⬜ |
| NGS1.02.06 | Geração pelo admin + troca forçada | ⬜ |
| NGS1.02.08 | Troca pelo próprio usuário | ⬜ |
| NGS1.02.11 | Nova senha ≠ atual e anterior | ⬜ |
| NGS1.02.12 | "Esqueci minha senha" por canal registrado | ⬜ |
| NGS1.02.13 | Bloqueio após N tentativas | ⬜ |
| NGS1.02.15 | Info do último login pós-autenticação | ⬜ |
| NGS1.02.16 | Mensagem genérica em login inválido | ⬜ |
| NGS1.02.17 | Impedir memorização de credenciais | ⬜ |
| NGS1.02.20 | Bloqueio/encerramento por inatividade | ⬜ |
| NGS1.02.23 | Segurança contra roubo de sessão | ⬜ |

## NGS1.03 — Autorização e controle de acesso

| ID | Título | Status |
|---|---|---|
| NGS1.03.01 | Impedir acesso por não autorizados | ⬜ |
| NGS1.03.02 | Perfis mínimos (RBAC) | ⬜ |
| NGS1.03.07 | Múltiplos perfis por usuário | ⬜ |
| NGS1.03.08 | Gerenciamento de usuários via aplicação | ⬜ |
| NGS1.03.09 | Identidade única (CPF) | ⬜ |
| NGS1.03.10 | Pelo menos 1 admin ativo | ⬜ |

## NGS1.04 — Disponibilidade

| ID | Título | Status |
|---|---|---|
| NGS1.04.01 | Procedimento de backup definido | ⬜ |
| NGS1.04.02 | Execução periódica | ⬜ |
| NGS1.04.03 | Retenção definida | ⬜ |
| NGS1.04.04 | Testes de restauração | ⬜ |
| NGS1.04.05 | Armazenamento segregado | ⬜ |

## NGS1.05 — Comunicação

| ID | Título | Status |
|---|---|---|
| NGS1.05.01 | HTTPS + autenticação do servidor | ⬜ |
| NGS1.05.02 | Processamento server-side | ⬜ |

## NGS1.06 — Segurança de dados

| ID | Título | Status |
|---|---|---|
| NGS1.06.01 | Uso de SGBD | ⬜ |
| NGS1.06.03 | Validação de dados de entrada | ⬜ |

## NGS1.07 — Auditoria

| ID | Título | Status |
|---|---|---|
| NGS1.07.01 | Auditoria contínua | ⬜ |
| NGS1.07.02 | Proteção dos registros | ⬜ |
| NGS1.07.03 | Eventos registrados | ⬜ |
| NGS1.07.05 | Campos obrigatórios (IP, usuário, tipo, data/hora) | ⬜ |
| NGS1.07.06 | Privacidade do paciente na trilha | ⬜ |
| NGS1.07.07 | Tela de consulta com filtros | ⬜ |
| NGS1.07.08 | Exportação com metadados institucionais | ⬜ |

## NGS1.08 — Documentação

| ID | Título | Status |
|---|---|---|
| NGS1.08.01 | Manuais de uso/instalação/config | ⬜ |
| NGS1.08.11 | Recomendações de configurações de segurança | ⬜ |
| NGS1.08.12 | Histórico de alterações (CHANGELOG) | ⬜ |

## NGS1.09 — Tempo

| ID | Título | Status |
|---|---|---|
| NGS1.09.01 | NTP server-side | ⬜ |
| NGS1.09.03 | Registro de tempo em UTC | ⬜ |

## NGS1.11 — Privacidade

| ID | Título | Status |
|---|---|---|
| NGS1.11.01 | Concordância com termo de uso no 1º acesso | ⬜ |

## NGS1.12 — Integridade

| ID | Título | Status |
|---|---|---|
| NGS1.12.01 | Regras de correção de dados | ⬜ |

---

**Dica:** salve uma cópia deste checklist dentro do repositório do seu
projeto (ex.: `docs/compliance/sbis-ngs1.md`) e preencha com o PR/commit
que atende cada item. Isso é o artefato de rastreabilidade pedido na
auditoria SBIS.
