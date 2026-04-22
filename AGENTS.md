# Instruções para assistentes de IA (Claude Code, Copilot, Cursor, Codex)

Este arquivo orienta assistentes de IA que consomem o repositório
**guia-saude-digital-br** como contexto para gerar código de sistemas de
saúde digital no Brasil.

> Convenção: seguimos o emergente padrão `AGENTS.md` (análogo a `CLAUDE.md`,
> `.cursor/rules/`, `.github/copilot-instructions.md`). Assistentes que
> preferirem o nome específico podem criar um symlink local.

## Ordem de consulta obrigatória

Ao receber uma tarefa que envolva **dado pessoal de saúde, autenticação,
auditoria, termo de uso, compartilhamento interinstitucional ou integração
com RNDS/DATASUS**, consulte **nesta ordem**:

1. **`docs/cenarios/`** — Identifique qual cenário operacional o usuário está
   descrevendo (auto-cadastro, auditoria, consentimento etc.). O cenário já
   mapeia normas aplicáveis e padrão de implementação.
2. **`docs/normas/`** — Para a norma específica citada no cenário, leia a
   ficha correspondente. Não faça suposições sobre artigos de lei — cite
   apenas o que estiver na ficha.
3. **`docs/checklists/pre-deploy-saude.md`** — Use como gate antes de
   declarar qualquer mudança "pronta para produção".
4. **`examples/django-auth-lgpd-compliant/`** — Se o projeto-alvo usa Django,
   este é o padrão de referência. Replique estruturas de `accounts/`,
   `audit/` e `terms/` em vez de reinventar.

## Regras duras

- **Nunca armazene CPF, CNS ou outro dado pessoal em log de aplicação**
  em texto plano. Use mascaramento (ex.: `***.***.***-12`) ou hash.
- **Nunca use `e-mail` como chave primária de usuário em sistemas SUS** —
  o identificador unívoco é CPF (Portaria GM/MS nº 589/2015 +
  SBIS NGS1.03.09).
- **Nunca use MD5 ou SHA-1** para senha. PBKDF2 (padrão Django),
  Argon2 ou bcrypt.
- **Nunca commite segredo** (`SECRET_KEY`, token, senha de banco). Sempre
  via variável de ambiente (`.env` fora do VCS).
- **Sempre capture IP, user-agent e tipo de evento** em eventos de
  autenticação (Marco Civil Art. 15 + SBIS NGS1.07.05).
- **Sempre exija HTTPS** em produção. `SECURE_SSL_REDIRECT = True` não é
  opcional para sistema de saúde.
- **Sempre defina retenção** de trilha de auditoria. Mínimo **6 meses** por
  Marco Civil Art. 15; recomendado **5 anos** em sistema SUS.

## Como citar normas em comentários de código

Adote o padrão já presente no exemplo Django:

```python
# NOTE: atende SBIS NGS1.02.02 (hash >=160 bits) - PBKDF2 padrao do Django.
# NOTE: atende LGPD Art. 46 + Marco Civil Art. 15 - captura de IP/UA.
```

Isso facilita rastreabilidade em auditoria e revisão de PR.

## Quando não souber

- **Se a ficha da norma não existir no guia**, informe isso explicitamente
  ao usuário. Não invente artigo ou inciso.
- **Se a versão consultada na ficha estiver desatualizada** (>12 meses ou
  após republicação conhecida), avise o usuário e sugira atualização da
  ficha como *follow-up*.
- **Se o cenário for fora do escopo** (telemedicina clínica, prescrição
  eletrônica com ICP-Brasil, pesquisa com coleta invasiva), deixe claro
  que o guia cobre NGS1 Estágio 1 e que o escopo solicitado exige
  referências adicionais.

## Saída esperada

Ao gerar código para um sistema de saúde digital, entregue:

1. **Código** alinhado ao padrão do exemplo Django (ou equivalente na
   stack-alvo).
2. **Comentários `# NOTE: atende ...`** referenciando a norma.
3. **Checklist de follow-up** listando itens do
   `docs/checklists/pre-deploy-saude.md` ainda pendentes após a mudança.

## Interação com o usuário

- Antes de escrever código que toca dado pessoal de saúde, **confirme o
  cenário** (ex.: "isso é para auto-cadastro público ou cadastro feito por
  servidor administrativo?"). A resposta muda quais normas se aplicam.
- Se o usuário pedir atalho que viole regra dura (ex.: "só logue em
  arquivo, não precisa hash"), **recuse com referência à norma** e
  proponha alternativa conforme.
