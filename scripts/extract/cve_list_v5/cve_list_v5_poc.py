import os
import zipfile
import json
import logging
import requests
import shutil
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

URL = "https://github.com/CVEProject/cvelistV5/archive/refs/heads/main.zip"
ZIP_FILE = "cvelist_main.zip"
EXTRACT_DIR = "cvelist_temp"
OUTPUT_DIR = Path("datalake/raw/cve_list_v5")
OUTPUT_FILE = OUTPUT_DIR / "cve_data.jsonl"

def process_cve_data():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    logging.info(f"Downloading {URL}...")
    response = requests.get(URL, stream=True)
    with open(ZIP_FILE, 'wb') as f:
        shutil.copyfileobj(response.raw, f)
    
    logging.info("Extracting files...")
    with zipfile.ZipFile(ZIP_FILE, 'r') as zip_ref:
        zip_ref.extractall(EXTRACT_DIR)
    
    logging.info("Processing JSON files and writing to JSONL...")
    count = 0
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as outfile:
        for root, _, files in os.walk(EXTRACT_DIR):
            for file in files:
                if file.endswith('.json'):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            outfile.write(json.dumps(data) + '\n')
                            count += 1
                            if count % 25000 == 0:
                                logging.info(f"Processed {count} records...")
                    except Exception as e:
                        logging.error(f"Error processing {file_path}: {e}")
    
    logging.info("Cleaning up temporary files...")
    os.remove(ZIP_FILE)
    shutil.rmtree(EXTRACT_DIR)
    logging.info(f"Done! Total records: {count}. Saved to {OUTPUT_FILE}")

if __name__ == '__main__':
    process_cve_data()