# README.md - Cybersecurity Datalake

---

## 1. TÍTULO E DESCRIÇÃO

### 🛡️ Cybersecurity Datalake

**Descrição:**  
O Cybersecurity Datalake é um projeto acadêmico voltado à coleta, transformação e análise de dados de cibersegurança provenientes de múltiplas fontes públicas e gratuitas. O objetivo é construir uma base de dados consolidada para análise de vulnerabilidades, ameaças e tendências no ecossistema de cibersegurança.

---

## 2. VISÃO GERAL

### 📌 O que é o projeto?

O Cybersecurity Datalake é um projeto de engenharia de dados que busca integrar informações de vulnerabilidades, exploits e ameaças de fontes como CISA KEV, CVE List V5, EPSS, NVD, GitHub Advisories, Shodan e VirusTotal.

### 🎯 Por que foi criado?

Com o aumento constante de ameaças cibernéticas, a capacidade de analisar dados de vulnerabilidades em tempo real se torna essencial para a tomada de decisão em segurança. Este projeto visa consolidar esses dados em uma única estrutura organizada, deixando-os prontos pra análises e insights.

### 🎯 Objetivos principais

- Coletar dados de múltiplas fontes de cibersegurança
- Transformar e enriquecer os dados para análise
- Criar uma estrutura de dados organizada (camadas Bronze, Silver e Gold)
- Gerar relatórios e insights sobre vulnerabilidades e tendências

### 🏗️ Arquitetura em alto nível

```
Fontes de Dados
    ↓
Scripts de Extração
    ↓
Camada Bronze (Dados Brutos)
    ↓
Scripts de Transformação
    ↓
Camada Silver (Dados Transformados)
    ↓
Scripts de Análise
    ↓
Camada Gold (Dados para Análise)
```

---

## 3. FUNCIONALIDADES

- ✅ **Coleta de dados de múltiplas fontes** (CISA KEV, CVE List V5, EPSS, NVD, GitHub Advisories, Shodan, VirusTotal)
- ✅ **Transformação e enriquecimento** (normalização, limpeza, junção de dados)
- ✅ **Armazenamento em camadas** (Bronze, Silver, Gold)
- ✅ **Análise e relatórios** (exportação para CSV, Parquet, JSON e visualizações)

---

## 4. ARQUITETURA

### 🔄 Fluxo de Dados

```
Fontes Externas
    ↓
scripts/extract/
    ↓
datalake/raw/ (Bronze)
    ↓
scripts/transform/
    ↓
datalake/processed/ (Silver)
    ↓
scripts/load/
    ↓
datalake/analytics/ (Gold)
```

### 📁 Estrutura de Pastas

```
cybersecurity-datalake/
├── scripts/
│   ├── extract/
│   ├── transform/
│   ├── load/
│   ├── utils/
│   └── orchestration/
├── config/
├── datalake/
│   ├── raw/
│   ├── processed/
│   └── analytics/
├── logs/
├── tests/
├── notebooks/
├── docs/
├── deployment/
├── .env
├── config.yaml
├── requirements.txt
├── .gitignore
└── README.md
```

### 🛠️ Tecnologias Utilizadas

- **Python 3.12+**
- **Pandas / Polars** – Manipulação de dados
- **PyArrow** – Exportação em Parquet
- **Requests / CISA-KEV** – Extração de dados
- **YAML / Dotenv** – Configuração e variáveis de ambiente
- **Git / GitHub** – Controle de versão e colaboração

---

## 5. PRÉ-REQUISITOS

- Python 3.12 ou superior
- Git
- Acesso à internet (para download de dados)
- Conhecimento básico de Python e análise de dados

---

## 6. INSTALAÇÃO

### 🚀 Clonar o repositório

```bash
git clone https://github.com/cybersecurity-datalake/cybersecurity-datalake.git
cd cybersecurity-datalake
```

### 🐍 Criar ambiente virtual

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

### 📦 Instalar dependências

```bash
pip install -r requirements.txt
```

### 🔐 Configurar variáveis de ambiente

Crie um arquivo `.env` na raíz do projeto e preencha com suas credenciais (se necessário):

```bash
touch .env  # Linux/Mac
# ou
New-Item .env  # Windows
```

---

## 7. CONFIGURAÇÃO

### 📄 Arquivo `config.yaml`

Contém configurações como caminhos de diretórios, URLs de fontes de dados e parâmetros de execução.

### 🔐 Variáveis de Ambiente (`.env`)

Exemplo:

```bash
SHODAN_API_KEY=seu_api_key_aqui
VT_API_KEY=seu_api_key_aqui
GITHUB_TOKEN=seu_token_aqui
LOG_LEVEL=INFO
ENVIRONMENT=dev
```

### 🔐 Credenciais de API

Para fontes como Shodan e VirusTotal, é necessário configurar as respectivas chaves de API no `.env`.

---

## 8. COMO USAR

### 🚀 Executar scripts de extração

```bash
python scripts/extract/extract_cisa_kev.py
```

### 🔄 Executar transformações

```bash
python scripts/transform/transform_kev.py
```

### 📊 Gerar relatórios

```bash
python scripts/load/load_to_analytics.py
```

### 🧪 Exemplo de uso

```bash
# Extrair dados do CISA KEV
python scripts/extract/extract_cisa_kev.py

# Transformar e enriquecer
python scripts/transform/transform_kev.py

# Gerar relatório de análise
python scripts/load/load_to_analytics.py
```

---

## 9. ESTRUTURA DO PROJETO

| Pasta | Função |
|-------|--------|
| `scripts/extract/` | Scripts de coleta de dados |
| `scripts/transform/` | Scripts de transformação e enriquecimento |
| `scripts/load/` | Scripts de carregamento para análise |
| `scripts/utils/` | Funções auxiliares |
| `scripts/orchestration/` | Orquestração do pipeline |
| `config/` | Arquivos de configuração |
| `datalake/raw/` | Dados brutos (camada Bronze) |
| `datalake/processed/` | Dados transformados (camada Silver) |
| `datalake/analytics/` | Dados prontos para análise (camada Gold) |
| `logs/` | Logs de execução |
| `tests/` | Testes automatizados |
| `notebooks/` | Jupyter notebooks para análise |
| `docs/` | Documentação do projeto |
| `deployment/` | Arquivos para deploy (Docker, Kubernetes) |

---

## 10. FONTES DE DADOS

| Fonte | Descrição | Acesso |
|-------|-----------|--------|
| **CISA KEV** | Vulnerabilidades ativamente exploradas | Público |
| **CVE List V5** | Lista oficial de vulnerabilidades | Público |
| **EPSS** | Previsão de exploração de CVEs | Público |
| **NVD** | Banco de dados de vulnerabilidades do NIST | Público |
| **GitHub Advisories** | Vulnerabilidades em projetos de código aberto | Público |
| **Shodan** | Inventário de dispositivos expostos | API pública (limitada) |
| **VirusTotal** | Análise de malware e IOCs | API pública (limitada) |

---

## 11. FLUXO DE TRABALHO

### 🧑‍💻 Como contribuir

1. Clone o repositório
2. Crie uma branch para sua feature: `git checkout -b feature/nome-da-feature`
3. Faça alterações e commits
4. Faça push da branch: `git push origin feature/nome-da-feature`
5. Crie um Pull Request (PR) no GitHub

### 🔄 Branches e Pull Requests

- `main`: Branch principal (protegida)
- `feature/*`: Branches para desenvolvimento de novas funcionalidades
- `hotfix/*`: Branches para correções urgentes

### 📝 Convenção de commits

Use a [Convenção de Commit do Angular](https://www.conventionalcommits.org/) para padronizar os commits:

```
feat: adicionar script de extração CVE List V5
fix: corrigir erro de importação
docs: atualizar README.md
```

---

## 12. TROUBLESHOOTING

### ❌ Erro: `Invalid username or token`

**Solução:** Use um **Personal Access Token (PAT)** ou configure **SSH** no Git.

### ❌ Erro: `ModuleNotFoundError`

**Solução:** Certifique-se de ter instalado as dependências com `pip install -r requirements.txt`.

### ❌ Erro: `Permission denied`

**Solução:** Execute com `sudo` ou como administrador.

### ❌ Erro: `ConnectionError`

**Solução:** Verifique sua conexão com a internet e tente novamente.

---

## 13. DOCUMENTAÇÃO

- 📚 [Documentação do CISA KEV](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)
- 📚 [CVE List V5 Schema](https://cveproject.github.io/cve-schema/)
- 📚 [EPSS Documentation](https://www.first.org/epss/)
- 📚 [NVD API](https://nvd.nist.gov/vuln/data-feeds)
- 📚 [GitHub Security Advisories API](https://docs.github.com/en/code-security/supply-chain-security/getting-started-with-the-dependabot-api)
- 📚 [Shodan API](https://www.shodan.io/api)
- 📚 [VirusTotal API](https://developers.virustotal.com/reference)

---

### 🔗 Links Úteis

- [GitHub do Projeto](https://github.com/cybersecurity-datalake/cybersecurity-datalake)
- [Documentação do Projeto](docs/)
- [Notebooks de Análise](notebooks/)
