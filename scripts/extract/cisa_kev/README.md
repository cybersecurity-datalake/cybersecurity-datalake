Cybersecurity Datalake Project
README - BRANCH POC/CISA-KEV
Extraction and Proof of Concept Documentation

---

## 1. Source Identification

### 1.1 Source/API Name
CISA KEV (Known Exploited Vulnerabilities) - Catalog of Actively Exploited Vulnerabilities.

### 1.2 Documentation Link
[https://www.cisa.gov/known-exploited-vulnerabilities-catalog](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)

### 1.3 Authentication
No API key or any form of authentication is required to access the public data from this source.

---

## 2. Configuration and Environment

### 2.1 Environment Variables
It is not necessary to configure a `.env` file for this specific extraction, as the source does not require credentials or access tokens.

---

## 3. Script Execution

### 3.1 Execution Instructions
First, create a virtual environment, activate it, and install required packages:
```
python3 -m venv .venv
```
```
source ./.venv/bin/activate
```
Then, install the required packages:
```
pip install -r requirements.txt
```
The extraction script was developed in Python and uses libraries for data download, validation, and persistence. Ensure that the dependencies listed in the project's `requirements.txt` are installed.

### 3.2 Command Example
To execute the extraction and initial PoC processing, use the command below from the project root:

```bash
python scripts/extract/cisa_kev_poc.py
```

---

## 4. Technical Extraction Details

### 4.1 Data and Processing Explanation
The script performs the automated download of the official JSON file maintained by CISA. After the download, the system executes the following steps:

1. **Validation:** Verifies schema integrity and the presence of mandatory fields.
2. **Quality:** Generates a quality report (metadata) containing record counts and null value verification.
3. **Persistence:** Saves data in multiple formats to ensure compatibility with the next Datalake layers.

### 4.2 Storage and Formats
- **Saving location:** Files are automatically stored in the `datalake/raw/cisa_kev/` directory.
- **Downloaded file:** The script consumes the original JSON file from CISA.
- **Output formats:** Data is converted and saved locally in **CSV**, **JSON**, and **Parquet**.
- **Decompression:** Not necessary, as the file is provided in flat format.
- **File size:** Small (approximately a few MBs), allowing fast in-memory processing.

---

## 5. Structure and Limitations

### 5.1 Relevant Columns
The following columns were identified as fundamental to the Datalake core:
- `cveID`: Unique vulnerability identifier (Primary key).
- `vendorProject`: Company or project responsible for the software.
- `product`: Name of the affected product.
- `dateAdded`: Date the vulnerability was added to the active exploitation catalog.
- `knownRansomwareCampaignUse`: Indicator of known use in Ransomware campaigns.
- `vulnerabilityName`: Descriptive title of the flaw.
- `shortDescription`: Technical summary of the vulnerability.

### 5.2 Update and Limits
- **Periodic update:** Yes, the database is continuously updated by CISA as new exploitations are confirmed.
- **Known limitations:** There is no strict rate-limit for the public endpoint. The source does not use pagination, providing all data in a single consolidated file.
