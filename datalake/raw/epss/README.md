# EPSS (Exploit Prediction Scoring System)

## Descrição

O EPSS (Exploit Prediction Scoring System) é um sistema que estima a probabilidade de uma vulnerabilidade ser explorada nos próximos 30 dias.

A base fornece scores para vulnerabilidades identificadas por CVEs, permitindo priorizar correções com base no risco de exploração.

---

## Fonte dos Dados

Repositório oficial:

https://github.com/empiricalsec/epss_scores

Documentação oficial:

https://www.first.org/epss/

---

## Formato da Base

Formato: CSV

Exemplo:

```csv
cve,epss,percentile
CVE-1999-0001,0.01151,0.78141
CVE-1999-0002,0.08201,0.91975
```

---

## Campos Relevantes

### cve

Identificador da vulnerabilidade.

Exemplo:

```
CVE-2024-12345
```

### epss

Probabilidade estimada de exploração da vulnerabilidade.

Valor entre 0 e 1.

### percentile

Posição relativa do score em comparação com as demais vulnerabilidades.

Valor entre 0 e 1.

---

## Como Obter os Dados

1. Acessar o repositório:
   https://github.com/empiricalsec/epss_scores

2. Baixar o arquivo CSV desejado.

3. Colocar o arquivo em:


```
datalake/raw/epss/downloads/
```

---

## Estrutura Utilizada

```text
epss/
├── README.md
├── .gitignore
├── .gitkeep
├── downloads
└── samples/
    └── epss_sample.csv

```

---

## Atualização da Base

A base é atualizada diariamente.

---

## Tamanho da Base

O histórico completo contém milhares de arquivos CSV e pode ocupar centenas de megabytes.

Por esse motivo os arquivos brutos não devem ser versionados no Git.

---

## Versionamento

Arquivos CSV completos não devem ser enviados ao repositório.

Apenas pequenos arquivos de exemplo podem ser armazenados na pasta:

```
samples/
```

---

## Prova de Conceito

Foi desenvolvido um script de prova de conceito para:

- Ler arquivos CSV do EPSS;
- Identificar as colunas disponíveis;
- Exibir estatísticas básicas;
- Demonstrar a consulta dos dados.

Arquivo:

```text
scripts/poc_epss.py
```

---

## Possíveis Integrações

A coluna `cve` permite relacionar esta base com:

- NVD
- CISA KEV
- CVE List v5
- GitHub Advisories

possibilitando análises de priorização de vulnerabilidades.