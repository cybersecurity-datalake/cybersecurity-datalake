import json
import logging
import os
from datetime import datetime

import pandas as pd
import requests
from tenacity import retry, stop_after_attempt, wait_exponential


class ConfigLoader:
    def __init__(self):
        self.config = {
            "url": "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json",
            "output_dir": "datalake/raw/cisa_kev",
            "formats": ["csv", "json", "parquet"],
        }
        os.makedirs(self.config["output_dir"], exist_ok=True)


class KevExtractor:
    def __init__(self, url):
        self.url = url

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    def fetch_data(self):
        response = requests.get(self.url, timeout=30)
        response.raise_for_status()
        return response.json()


class DataValidator:
    @staticmethod
    def validate(data):
        if not data or "vulnerabilities" not in data:
            raise ValueError("Invalid data structure received from CISA")
        df = pd.DataFrame(data["vulnerabilities"])
        report = {
            "total_records": len(df),
            "missing_values": df.isnull().sum().to_dict(),
            "columns": list(df.columns),
        }
        return df, report


class DataLoader:
    def __init__(self, base_path):
        self.base_path = base_path

    def save(self, df, formats):
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = f"{self.base_path}/cisa_kev_{ts}"
        paths = {}
        if "csv" in formats:
            paths["csv"] = f"{base_name}.csv"
            df.to_csv(paths["csv"], index=False)
        if "json" in formats:
            paths["json"] = f"{base_name}.json"
            df.to_json(paths["json"], orient="records")
        if "parquet" in formats:
            paths["parquet"] = f"{base_name}.parquet"
            df.to_parquet(paths["parquet"])
        return paths


def setup_logging():
    log_file = f"logs/extract_{datetime.now().strftime('%Y%m%d')}.log"
    os.makedirs("logs", exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler(log_file), logging.StreamHandler()],
    )


def main():
    setup_logging()
    logging.info("Starting CISA KEV extraction")
    try:
        cfg = ConfigLoader()
        extractor = KevExtractor(cfg.config["url"])
        raw_data = extractor.fetch_data()

        validator = DataValidator()
        df, report = validator.validate(raw_data)

        loader = DataLoader(cfg.config["output_dir"])
        saved_files = loader.save(df, cfg.config["formats"])

        metadata = {
            "timestamp": str(datetime.now()),
            "files": saved_files,
            "quality": report,
        }
        with open(
            f"{cfg.config['output_dir']}/metadata_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            "w",
        ) as f:
            json.dump(metadata, f, indent=4)

        logging.info(f"Extraction successful. Records: {report['total_records']}")
        return 0
    except Exception as e:
        logging.error(f"Pipeline failed: {str(e)}")
        return 1


if __name__ == "__main__":
    exit(main())
