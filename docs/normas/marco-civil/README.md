# Marco Civil da Internet — Lei nº 12.965/2014

## Identificação

- **Nome:** Marco Civil da Internet.
- **Base legal:** Lei nº 12.965, de 23 de abril de 2014.
- **Link oficial:** <https://www.planalto.gov.br/ccivil_03/_ato2011-2014/2014/lei/l12965.htm>
- **Regulamento:** Decreto nº 8.771/2016.
- **Vigência:** desde 23/06/2014.

## Objeto e sujeitos

Estabelece princípios, garantias, direitos e deveres para o uso da internet
no Brasil. Define duas figuras relevantes:

- **Provedor de conexão** — quem provê acesso (operadora de telecom).
- **Provedor de aplicação** — quem oferece serviço acessível via internet
  (**sistemas de saúde digital se enquadram aqui**).

## Artigos-chave aplicados a sistemas de saúde

### Art. 15 — Guarda de registros de acesso a aplicações

> "O provedor de aplicações de internet constituído na forma de pessoa
> jurídica e que exerça essa atividade de forma organizada, profissional
> e com fins econômicos deverá manter os respectivos registros de acesso a
> aplicações de internet, sob sigilo, em ambiente controlado e de
> segurança, **pelo prazo de 6 (seis) meses**, nos termos do regulamento."

**Registro de acesso a aplicação** (Art. 5º, VIII) = conjunto de
informações referentes à **data e hora de uso** de uma aplicação, a partir
de um determinado endereço IP.

**Prático para saúde digital:**

- Mesmo sistemas sem "fim econômico" direto (ex.: sistema público SUS) são
  tratados como sujeitos ao Art. 15 na prática, porque a **LGPD Art. 46** e
  a **SBIS NGS1.07** exigem trilha equivalente. Na dúvida, aplique.
- Registro mínimo: **IP, timestamp, identificação da sessão/usuário**.
- Prazo mínimo: **6 meses**. Em saúde, recomenda-se **5 anos** para
  suportar auditoria de prontuário e rastreabilidade administrativa.

### Art. 10 e Art. 13 — Sigilo dos registros

Os registros devem ser armazenados:

- **Em ambiente controlado e de segurança** (Art. 10, §1º).
- Acesso apenas **mediante ordem judicial** ou nos casos previstos em lei
  (Art. 10, §1º e §3º).

**Prático:** a tabela/arquivo de auditoria deve ter:

- Permissões restritas (somente leitura para auditor; escrita só via
  aplicação).
- Backup separado.
- Integridade protegida (hash/assinatura ou append-only).

### Art. 7º, VIII — Informações claras sobre coleta, uso, tratamento e
proteção de dados

Casa com LGPD Art. 6º, VI. Prático: **política de privacidade** com
linguagem clara, acessível antes do cadastro.

## Implicações técnicas

1. **Tabela de auditoria** com IP, user-agent, timestamp UTC, tipo de
   evento, usuário (ou CPF mascarado se auto-cadastro falhou antes de
   autenticar). → ver [`../../cenarios/auditoria.md`](../../cenarios/auditoria.md).
2. **Captura de IP** considerando proxies (`X-Forwarded-For`, `X-Real-IP`).
   Em Django, use
   [`SECURE_PROXY_SSL_HEADER`](https://docs.djangoproject.com/en/stable/ref/settings/#secure-proxy-ssl-header)
   e um middleware que leia o header correto. Exemplo em
   [`examples/django-auth-lgpd-compliant/audit/middleware.py`](../../../examples/django-auth-lgpd-compliant/audit/middleware.py).
3. **Retenção ≥6 meses**. Configure rotação/arquivamento. Não apague antes.
4. **Ambiente controlado** — trilha em banco separado ou schema separado
   com ACL própria; append-only quando possível.
5. **Sigilo** — sem exposição de trilha em logs de aplicação comum. Quem
   consulta a trilha também deve ser registrado na trilha (auditoria da
   auditoria).

## Armadilhas comuns

- **Capturar `REMOTE_ADDR` sem tratar proxy reverso** → IP registrado fica
  sempre sendo o do Nginx/balanceador. Use `X-Forwarded-For` corretamente
  (validando proxies confiáveis, senão é *spoofing*).
- **Apagar logs junto com usuário excluído.** Mesmo após eliminação do
  titular (LGPD Art. 16), é legítimo manter a trilha pelo Art. 15/Art. 16,
  II da LGPD (cumprimento de obrigação legal). Documente.
- **Gravar sessão inteira** (body de request, tokens). Viola minimização.
  Grave só metadados.
- **Fuso local** em vez de UTC. Vira pesadelo em análise forense.

## Referências cruzadas

- Cenários:
  [auditoria](../../cenarios/auditoria.md),
  [autenticação](../../cenarios/autenticacao.md).
- Normas relacionadas:
  [LGPD Art. 15 e 46](../lgpd/README.md),
  [SBIS NGS1.07](../sbis-cfm/README.md).
- Exemplo: [middleware Django de captura de IP/UA](../../../examples/django-auth-lgpd-compliant/audit/middleware.py).

## Versão consultada

- Texto conforme Planalto em 2026-04-22. Decreto 8.771/2016 vigente.
