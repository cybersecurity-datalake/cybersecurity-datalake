from __future__ import annotations

import json
import os
from typing import Any

import requests
from dotenv import load_dotenv


BASE_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"


def get_english_description(descriptions: list[dict[str, Any]]) -> str | None:
    for item in descriptions:
        if item.get("lang") == "en":
            return item.get("value")
    return None


def extract_cvss(metrics: dict[str, Any]) -> list[dict[str, Any]]:
    results = []

    for metric_key in ("cvssMetricV40", "cvssMetricV31", "cvssMetricV30", "cvssMetricV2"):
        for metric in metrics.get(metric_key, []):
            cvss_data = metric.get("cvssData", {})

            results.append(
                {
                    "version_group": metric_key,
                    "source": metric.get("source"),
                    "type": metric.get("type"),
                    "version": cvss_data.get("version"),
                    "vector_string": cvss_data.get("vectorString"),
                    "base_score": cvss_data.get("baseScore"),
                    "base_severity": cvss_data.get("baseSeverity"),
                    "exploitability_score": metric.get("exploitabilityScore"),
                    "impact_score": metric.get("impactScore"),
                }
            )

    return results


def extract_weaknesses(weaknesses: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "source": weakness.get("source"),
            "type": weakness.get("type"),
            "descriptions": weakness.get("description", []),
        }
        for weakness in weaknesses
    ]


def extract_references(references: list[dict[str, Any]] | dict[str, Any]) -> list[dict[str, Any]]:
    if isinstance(references, dict):
        references = references.get("referenceData", [])

    return [
        {
            "url": ref.get("url"),
            "source": ref.get("source"),
            "tags": ref.get("tags", []),
        }
        for ref in references
    ]


def normalize_vulnerability(item: dict[str, Any]) -> dict[str, Any]:
    cve = item.get("cve", {})

    return {
        "id": cve.get("id"),
        "source_identifier": cve.get("sourceIdentifier"),
        "published": cve.get("published"),
        "last_modified": cve.get("lastModified"),
        "vuln_status": cve.get("vulnStatus"),
        "description_en": get_english_description(cve.get("descriptions", [])),
        "descriptions": cve.get("descriptions", []),
        "metrics": extract_cvss(cve.get("metrics", {})),
        "weaknesses": extract_weaknesses(cve.get("weaknesses", [])),
        "configurations": cve.get("configurations", []),
        "references": extract_references(cve.get("references", {})),
        "cve_tags": cve.get("cveTags", []),
        "vendor_comments": cve.get("vendorComments", []),
        "cisa": {
            "exploit_add": cve.get("cisaExploitAdd"),
            "action_due": cve.get("cisaActionDue"),
            "required_action": cve.get("cisaRequiredAction"),
            "vulnerability_name": cve.get("cisaVulnerabilityName"),
        },
    }


def get_api_key() -> str | None:
    load_dotenv()
    return os.getenv("NVD_API_KEY")


def fetch_test_cve(cve_id: str = "CVE-2019-1010218") -> dict[str, Any]:
    headers = {
        "User-Agent": "nvd-api-test-script/1.0",
    }

    api_key = get_api_key()
    if api_key:
        headers["apiKey"] = api_key

    params = {
        "cveIds": cve_id,
        "resultsPerPage": 1,
        "startIndex": 0,
    }

    response = requests.get(
        BASE_URL,
        headers=headers,
        params=params,
        timeout=30,
    )

    if not response.ok:
        message = response.headers.get("message")
        raise RuntimeError(
            f"Erro HTTP {response.status_code}. "
            f"Mensagem NVD: {message or response.text[:500]}"
        )

    return response.json()


def main() -> None:
    raw_data = fetch_test_cve()

    structured = {
        "metadata": {
            "results_per_page": raw_data.get("resultsPerPage"),
            "start_index": raw_data.get("startIndex"),
            "total_results": raw_data.get("totalResults"),
            "format": raw_data.get("format"),
            "version": raw_data.get("version"),
            "timestamp": raw_data.get("timestamp"),
        },
        "vulnerabilities": [
            normalize_vulnerability(item)
            for item in raw_data.get("vulnerabilities", [])
        ],
    }

    print(json.dumps(structured, indent=2, ensure_ascii=False))

    with open("../../../datalake/raw/nvd/nvd_structured_output.json", "w", encoding="utf-8") as file:
        json.dump(structured, file, indent=2, ensure_ascii=False)

    print("\nArquivo salvo em: ../../../datalake/raw/nvd/nvd_structured_output.json")


if __name__ == "__main__":
    main()
