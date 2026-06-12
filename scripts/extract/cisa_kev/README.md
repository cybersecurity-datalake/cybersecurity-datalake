Projeto Datalake de Cibersegurança

README - BRANCH POC/CISA-KEV

Documentação de Extração e Prova de Conceito

---

## 1. Identificação da Fonte

### 1.1 Nome da Fonte/API
CISA KEV (Known Exploited Vulnerabilities) - Catálogo de Vulnerabilidades Exploradas Ativamente.

### 1.2 Link da Documentação
[https://www.cisa.gov/known-exploited-vulnerabilities-catalog](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)

### 1.3 Autenticação
Não é necessária chave de API ou qualquer forma de autenticação para o acesso aos dados públicos desta fonte.

---

## 2. Configuração e Ambiente

### 2.1 Variáveis de Ambiente
Não é necessário configurar arquivo `.env` para esta extração específica, uma vez que a fonte não exige credenciais ou tokens de acesso.

---

## 3. Execução do Script

### 3.1 Instruções de Execução
O script de extração foi desenvolvido em Python e utiliza bibliotecas para download, validação e persistência de dados. Certifique-se de que as dependências listadas no `requirements.txt` do projeto estejam instaladas.

### 3.2 Exemplo de Comando
Para executar a extração e o processamento inicial da PoC, utilize o comando abaixo a partir da raiz do projeto:

```bash
python scripts/extract/cisa_kev_poc.py
```

---

## 4. Detalhes Técnicos da Extração

### 4.1 Explicação dos Dados e Processamento
O script realiza o download automatizado do arquivo JSON oficial mantido pela CISA. Após o download, o sistema executa as seguintes etapas:
1. **Validação:** Verifica a integridade do esquema e a presença de campos obrigatórios.
2. **Qualidade:** Gera um relatório de qualidade (metadados) contendo contagem de registros e verificação de valores nulos.
3. **Persistência:** Salva os dados em múltiplos formatos para garantir compatibilidade com as próximas camadas do Datalake.

### 4.2 Armazenamento e Formatos
- **Local de salvamento:** Os arquivos são armazenados automaticamente no diretório `datalake/raw/cisa_kev/`.
- **Arquivo baixado:** O script consome o arquivo JSON original da CISA.
- **Formatos de saída:** O dado é convertido e salvo localmente em **CSV**, **JSON** e **Parquet**.
- **Descompactação:** Não é necessária, pois o arquivo é fornecido em formato plano.
- **Tamanho do arquivo:** Pequeno (aproximadamente alguns MBs), permitindo processamento rápido em memória.

---

## 5. Estrutura e Limitações

### 5.1 Colunas Relevantes
As seguintes colunas foram identificadas como fundamentais para o núcleo do Datalake:
- `cveID`: Identificador único da vulnerabilidade (Chave primária).
- `vendorProject`: Empresa ou projeto responsável pelo software.
- `product`: Nome do produto afetado.
- `dateAdded`: Data em que a vulnerabilidade foi adicionada ao catálogo de exploração ativa.
- `knownRansomwareCampaignUse`: Indicador de uso conhecido em campanhas de Ransomware.
- `vulnerabilityName`: Título descritivo da falha.
- `shortDescription`: Resumo técnico da vulnerabilidade.

### 5.2 Atualização e Limites
- **Atualização periódica:** Sim, a base é atualizada continuamente pela CISA conforme novas explorações são confirmadas.
- **Limitações conhecidas:** Não há rate-limit estrito para o endpoint público. A fonte não utiliza paginação, fornecendo todos os dados em um arquivo único consolidado.
