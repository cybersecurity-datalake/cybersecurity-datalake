# GitHub Advisory Database / GitHub Security Advisories

## Visão Geral

- **Nome da base:** GitHub Advisory Database / GitHub Security Advisories
- **Link da base:** https://github.com/github/advisory-database
- **Tipo de acesso:** clone local de repositório Git com arquivos JSON
- **Precisa de autenticação:** não para o clone público

Esta prova de conceito lê os arquivos JSON do clone local do repositório `github/advisory-database`, opcionalmente copia os JSONs crus para o datalake e gera um CSV achatado com colunas úteis para exploração inicial.

## Configuração do `.env`

Crie o arquivo `scripts/extract/github_advisories/.env` a partir do exemplo:

```bash
cp scripts/extract/github_advisories/.env.example scripts/extract/github_advisories/.env
```

Exemplo de conteúdo:

```env
GITHUB_ADVISORY_DB_PATH=../advisory-database
OUTPUT_BASE_DIR=datalake/raw/github_advisories
COPY_RAW_JSON=true
```

### Variáveis suportadas

- `GITHUB_ADVISORY_DB_PATH`: obrigatório. Pode ser absoluto ou relativo ao diretório raiz do projeto.
- `OUTPUT_BASE_DIR`: opcional. Diretório base para saída. Padrão: `datalake/raw/github_advisories`.
- `COPY_RAW_JSON`: opcional. Quando `true`, copia os JSONs crus para a pasta de saída.

## Instalação das Dependências

```bash
cd <project-root>
python3 -m venv .venv
source .venv/bin/activate
pip install -r scripts/extract/github_advisories/requirements.txt
```

## Execução

```bash
cd <project-root>
python3 -m venv .venv
source .venv/bin/activate
pip install -r scripts/extract/github_advisories/requirements.txt
cp scripts/extract/github_advisories/.env.example scripts/extract/github_advisories/.env
python3 scripts/extract/github_advisories/github_security_advisories_poc.py
```

## Arquivos Gerados

A execução cria a estrutura:

```text
datalake/raw/github_advisories/output/YYYY-MM-DD/
├── github_security_advisories.csv
├── run_metadata.json
└── json/
```

### Descrição dos artefatos

- `github_security_advisories.csv`: saída tabular achatada, com uma linha por advisory JSON.
- `run_metadata.json`: metadados da execução, incluindo contagens, horários e amostra de erros.
- `json/`: cópia opcional dos arquivos JSON crus, preservando a estrutura relativa do clone original.

## Campos Relevantes no Dataset Final

- `source_file`
- `ghsa_id`
- `schema_version`
- `modified`
- `published`
- `withdrawn`
- `summary`
- `details`
- `severity`
- `aliases`
- `cve_ids`
- `cwe_ids`
- `affected_ecosystems`
- `affected_packages`
- `affected_versions`
- `patched_versions`
- `references`
- `database_specific`
- `affected_database_specific`
- `affected_ecosystem_specific`
- `raw_json_copied_path`

## Observações Importantes

- Os arquivos gerados em `datalake/raw` **não devem ser commitados**.
- O script usa apenas biblioteca padrão do Python e `python-dotenv`.
- A cópia dos JSONs crus preserva os caminhos relativos para evitar colisão de nomes.

## Limitações Conhecidas

- A base é grande e pode levar tempo para processar completamente.
- O formato JSON possui campos aninhados e estruturas variáveis.
- Alguns advisories podem ter campos ausentes ou listas vazias.
- O clone local precisa ser atualizado periodicamente com `git pull`.
