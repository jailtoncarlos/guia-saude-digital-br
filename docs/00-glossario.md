# Glossário

Termos e siglas recorrentes no guia, com foco em como impactam decisões de
desenvolvimento.

## A

**ANPD** — Autoridade Nacional de Proteção de Dados. Autarquia responsável
por fiscalizar a LGPD, emitir resoluções e guias orientativos. Relevante em
saúde digital por resoluções específicas sobre dado sensível, transferência
internacional e poder público.

**APF** — Administração Pública Federal. Abrange órgãos da União. Sistemas
de saúde digital operados por MS, DATASUS, SES estaduais e secretarias
municipais podem ter obrigações específicas (PNSI, IN GSI/PR).

**ASVS** — *Application Security Verification Standard* (OWASP). Padrão de
verificação de segurança em aplicações. Relevante para o guia: V2
(autenticação), V4 (controle de acesso), V7 (logging), V11 (lógica de
negócio).

## C

**CNES** — Cadastro Nacional de Estabelecimentos de Saúde. Identificador
unívoco de unidade de saúde no SUS. Usado como chave em sistemas de
vigilância, SIA/SIH, RNDS.

**CNS** — Cartão Nacional de Saúde. Identificador do cidadão no SUS. Em
paralelo ao CPF, pode aparecer como identificador em integrações DATASUS.
A PNIIS (Portaria 589/2015) privilegia o uso do CPF como identificador
unívoco principal, mas o CNS segue operacional.

**CPF** — Cadastro de Pessoas Físicas. Identificador oficial do cidadão
brasileiro. Em sistemas SUS, é o **USERNAME_FIELD recomendado** (ver
SBIS NGS1.03.09 e PNIIS). Requer validação de dígito verificador.

**CC BY 4.0** — Creative Commons Attribution 4.0 International. Licença de
conteúdo editorial adotada neste guia.

## D

**DATASUS** — Departamento de Informática do SUS. Responsável por sistemas
nacionais (e-SUS APS, SISCAN, SINAN, SIH/SIA, CNES, RNDS).

**DPO** — *Data Protection Officer* / Encarregado de Proteção de Dados.
Figura prevista na LGPD. Deve ser consultado em decisões de tratamento de
dado sensível.

## E

**e-SUS APS** — Sistema de Informação em Saúde para a Atenção Básica.
Referência de stack Django + PostgreSQL em saúde digital governamental.

**ESD28** — Estratégia de Saúde Digital 2020–2028, instituída pela
Portaria GM/MS nº 1.434/2020.

## F

**FHIR** — *Fast Healthcare Interoperability Resources*. Padrão HL7 de
interoperabilidade adotado pela RNDS.

## I

**ICP-Brasil** — Infraestrutura de Chaves Públicas Brasileira. Base de
certificados digitais reconhecidos pelo ITI. Exigida em assinatura de
prescrições eletrônicas e no NGS2 da SBIS (**fora do escopo** deste guia).

**Inaep** — Instância Nacional de Ética em Pesquisa. Sucessora da CONEP
(conforme Lei 14.874/2024 + Decreto 12.651/2025).

**IN GSI/PR** — Instrução Normativa do Gabinete de Segurança Institucional
da Presidência da República. A IN nº 1/2020 define controles mínimos em
sistemas da APF.

## L

**LGPD** — Lei Geral de Proteção de Dados Pessoais (Lei 13.709/2018).
Base geral para qualquer sistema que trate dado pessoal. Dado de saúde é
**dado pessoal sensível** (Art. 5º, II).

## N

**NGS1 / NGS2** — Níveis de garantia de segurança no manual de certificação
SBIS/CFM. NGS1 cobre requisitos essenciais (aderência à legislação); NGS2
exige certificado digital ICP-Brasil (fora do escopo deste guia).

**NIST SP 800-63** — Publicação do *National Institute of Standards and
Technology* dos EUA sobre identidade digital. Referência internacional
para níveis de garantia de autenticação (IAL/AAL).

## O

**OWASP** — *Open Worldwide Application Security Project*. Comunidade cujos
artefatos mais relevantes aqui: **Top 10** e **ASVS**.

## P

**PBKDF2** — *Password-Based Key Derivation Function 2*. Função de
derivação padrão do Django para armazenar senhas. Atende SBIS NGS1.02.02
(hash ≥160 bits) quando configurada com SHA-256 e iterações adequadas.

**PNIIS** — Política Nacional de Informação e Informática em Saúde
(Portaria GM/MS nº 589/2015).

**PNSI** — Política Nacional de Segurança da Informação (Decreto
9.637/2018).

**POSIC/MS** — Política de Segurança da Informação e Comunicações do
Ministério da Saúde. Aplicável a sistemas operados pelo MS/DATASUS.

## R

**RBAC** — *Role-Based Access Control*. Controle de acesso baseado em
papéis/perfis. Modelo preferencial em saúde digital (SBIS NGS1.03).

**RES** — Registro Eletrônico em Saúde. Termo guarda-chuva para prontuário
eletrônico e similares. S-RES = Sistema de Registro Eletrônico em Saúde.

**RNDS** — Rede Nacional de Dados em Saúde. Plataforma federada de
intercâmbio de dados de saúde, regulada pelo Decreto 12.560/2025.

## S

**SBIS** — Sociedade Brasileira de Informática em Saúde. Em parceria com o
CFM, mantém o manual de certificação de S-RES.

**SUS Digital** — Programa instituído pela Portaria GM/MS nº 3.232/2024
com três eixos: cultura, soluções e interoperabilidade.

## T

**TLS** — *Transport Layer Security*. Exigido (≥1.2) em qualquer sistema
de saúde digital (SBIS NGS1.05.01, OWASP ASVS V9).

## U

**UTC** — *Coordinated Universal Time*. Padrão de fuso horário para
timestamps em trilha de auditoria (SBIS NGS1.09.03).
