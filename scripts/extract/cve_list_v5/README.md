Cybersecurity Datalake Project

README - BRANCH POC/CVE-LIST-V5

Extraction and Proof of Concept Documentation

---

### 1. Source Identification

The primary data source for this branch is the CVE List V5, maintained by the CVE Project. This repository serves as the official global record of Common Vulnerabilities and Exposures, utilizing the CVE JSON 5.0 record format to provide structured and machine-readable security data.

**Link:** https://github.com/CVEProject/cvelistV5
**Authentication:** No authentication, API keys, or tokens are required to access this public repository.

### 2. Configuration and Environment

This extraction module is designed for high-volume public data retrieval. As the source does not require credentials or restricted access, no .env file is required for the execution of this specific script. All necessary configurations are handled internally within the extraction logic.

### 3. Script Execution

To perform the data extraction and generate the consolidated dataset, follow the steps below from the project's root directory:

1. Create a virtual environment, activate it, and install required packages:
```
python3 -m venv .venv
```
```
source ./.venv/bin/activate
```
2. Install the required packages:
```
pip install -r requirements.txt
```
3. Execute the extraction script: 
```
python scripts/extract/cve_extractor.py
```

### 4. Technical Extraction Details

The extraction process is optimized to handle the massive scale of the CVE Project repository, which contains hundreds of thousands of individual records. The script follows these technical stages:

- **Download:** The script retrieves the official main.zip archive directly from the GitHub repository's main branch to ensure the most up-to-date data.
- **Extraction:** The archive is unpacked into a temporary local directory named cvelist_temp.
- **Consolidation:** The script recursively traverses the directory structure to locate and process over 250,000 individual JSON files.
- **Memory Management:** To prevent memory overflow, the records are consolidated into a single JSONL (JSON Lines) file. This format allows for efficient line-by-line processing in downstream ETL stages.
- **Cleanup:** Upon successful consolidation, the script automatically deletes the cvelist_main.zip file and the cvelist_temp directory to free up disk space.
- **Output Path:** The final consolidated file is stored at `datalake/raw/cve_list_v5/cve_data.jsonl`.

### 5. Structure and Limitations

#### 5.1 Relevant Columns (CVE JSON 5.0)

The extracted data follows the CVE JSON 5.0 schema. The following fields are prioritized for the Datalake integration:

- `cveMetadata.cveId`
  - The unique identifier for the vulnerability (Primary Key).


- `cveMetadata.datePublished`
  - The timestamp indicating when the CVE record was first published.


- `containers.cna.title`
  - A short, descriptive title of the vulnerability.


- `containers.cna.descriptions`
  - Comprehensive technical details regarding the nature of the flaw.


- `containers.cna.affected`
  - Data regarding the vendor, product, and specific version ranges impacted.


- `containers.cna.problemTypes`
  - Classification of the weakness, typically mapped to CWE IDs.


- `containers.cna.references`
  - A collection of external links to advisories, patches, and exploits.


#### 5.2 Updates and Limits

The CVE List V5 is updated continuously, with new records and updates pushed to GitHub approximately every 7 minutes. Due to the sheer volume of data, the JSONL format is essential for maintaining system stability during the transformation and analysis phases, as it avoids the need to load the entire multi-gigabyte dataset into active memory.
