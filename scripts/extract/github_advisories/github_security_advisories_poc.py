import csv
import json
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv


SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent.parent
ENV_FILE = SCRIPT_DIR / ".env"
SOURCE_NAME = "github_advisory_database"
CSV_COLUMNS = [
    "source_file",
    "ghsa_id",
    "schema_version",
    "modified",
    "published",
    "withdrawn",
    "summary",
    "details",
    "severity",
    "aliases",
    "cve_ids",
    "cwe_ids",
    "affected_ecosystems",
    "affected_packages",
    "affected_versions",
    "patched_versions",
    "references",
    "database_specific",
    "affected_database_specific",
    "affected_ecosystem_specific",
    "raw_json_copied_path",
]


class ConfigError(Exception):
    """Raised when the local configuration is invalid."""


def _resolve_path(path_value, base_dir):
    path = Path(path_value).expanduser()
    if not path.is_absolute():
        path = (base_dir / path).resolve()
    return path


def _parse_bool(raw_value, default=True):
    if raw_value is None or str(raw_value).strip() == "":
        return default

    normalized = str(raw_value).strip().lower()
    truthy = {"1", "true", "yes", "y", "on"}
    falsy = {"0", "false", "no", "n", "off"}

    if normalized in truthy:
        return True
    if normalized in falsy:
        return False

    raise ConfigError(
        "COPY_RAW_JSON deve usar um valor booleano válido: true/false, 1/0, yes/no."
    )


def _compact_json(value):
    if value in ("", None):
        return ""
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return str(value)


def _join_unique(values):
    seen = set()
    result = []
    for value in values:
        text = str(value).strip()
        if not text or text in seen:
            continue
        seen.add(text)
        result.append(text)
    return ";".join(result)


def _package_label(ecosystem, name):
    ecosystem = (ecosystem or "").strip()
    name = (name or "").strip()
    if ecosystem and name:
        return f"{ecosystem}:{name}"
    return ecosystem or name


def _extract_severity(advisory, database_specific):
    severity_items = advisory.get("severity", [])
    parsed = []

    if isinstance(severity_items, list):
        for item in severity_items:
            if isinstance(item, dict):
                severity_type = str(item.get("type", "")).strip()
                score = str(item.get("score", "")).strip()
                if severity_type and score:
                    parsed.append(f"{severity_type}:{score}")
                elif score or severity_type:
                    parsed.append(score or severity_type)
            elif item:
                parsed.append(str(item).strip())
    elif isinstance(severity_items, str) and severity_items.strip():
        parsed.append(severity_items.strip())

    if parsed:
        return _join_unique(parsed)

    fallback = database_specific.get("severity", "")
    if isinstance(fallback, str):
        return fallback.strip()
    return _compact_json(fallback)


def _serialize_affected_range(package, events, range_type):
    parts = []
    if range_type and range_type != "ECOSYSTEM":
        parts.append(f"type={range_type}")

    for event in events:
        if not isinstance(event, dict):
            continue
        for key in ("introduced", "fixed", "last_affected", "limit"):
            value = event.get(key)
            if value not in ("", None):
                parts.append(f"{key}={value}")
        for key in sorted(event.keys()):
            if key in {"introduced", "fixed", "last_affected", "limit"}:
                continue
            value = event.get(key)
            if value not in ("", None):
                parts.append(f"{key}={value}")

    if not parts or not package:
        return ""
    return f"{package}[{','.join(parts)}]"


def load_config():
    if not ENV_FILE.exists():
        raise ConfigError(
            f"Arquivo .env não encontrado em {ENV_FILE}. "
            "Copie .env.example para .env e ajuste GITHUB_ADVISORY_DB_PATH."
        )

    load_dotenv(ENV_FILE)

    source_value = os.getenv("GITHUB_ADVISORY_DB_PATH", "").strip()
    output_value = os.getenv(
        "OUTPUT_BASE_DIR", "datalake/raw/github_advisories"
    ).strip()
    copy_raw_json_enabled = _parse_bool(os.getenv("COPY_RAW_JSON"), default=True)

    if not source_value:
        raise ConfigError(
            "GITHUB_ADVISORY_DB_PATH é obrigatório e deve apontar para o clone local "
            "do github/advisory-database."
        )

    source_path = _resolve_path(source_value, PROJECT_ROOT)
    output_base_dir = _resolve_path(output_value, PROJECT_ROOT)

    if not source_path.exists():
        raise ConfigError(f"GITHUB_ADVISORY_DB_PATH não existe: {source_path}")
    if not source_path.is_dir():
        raise ConfigError(
            f"GITHUB_ADVISORY_DB_PATH não é um diretório válido: {source_path}"
        )

    try:
        next(source_path.rglob("*.json"))
    except StopIteration as exc:
        raise ConfigError(
            f"Nenhum arquivo JSON encontrado em {source_path}. "
            "Os advisories esperados ficam tipicamente em advisories/."
        ) from exc

    return {
        "source_path": source_path,
        "output_base_dir": output_base_dir,
        "copy_raw_json": copy_raw_json_enabled,
    }


def find_json_files(source_path):
    json_files = sorted(
        source_path.rglob("*.json"),
        key=lambda path: (
            0
            if path.relative_to(source_path).as_posix().startswith("advisories/")
            else 1,
            path.relative_to(source_path).as_posix(),
        ),
    )

    if not json_files:
        raise ConfigError(
            f"Nenhum arquivo JSON encontrado em {source_path}. "
            "Os advisories esperados ficam tipicamente em advisories/."
        )

    return json_files


def flatten_advisory(advisory, source_file, raw_json_copied_path):
    database_specific = advisory.get("database_specific", {})
    if not isinstance(database_specific, dict):
        database_specific = {}

    aliases = advisory.get("aliases", [])
    if not isinstance(aliases, list):
        aliases = [aliases] if aliases else []

    cwe_ids = database_specific.get("cwe_ids", [])
    if not isinstance(cwe_ids, list):
        cwe_ids = [cwe_ids] if cwe_ids else []

    ecosystems = []
    packages = []
    affected_versions = []
    patched_versions = []
    affected_database_specific = []
    affected_ecosystem_specific = []

    for affected_item in advisory.get("affected", []):
        if not isinstance(affected_item, dict):
            continue

        package_data = affected_item.get("package", {})
        if not isinstance(package_data, dict):
            package_data = {}

        ecosystem = package_data.get("ecosystem", "")
        package_name = package_data.get("name", "")
        package = _package_label(ecosystem, package_name)

        if ecosystem:
            ecosystems.append(ecosystem)
        if package:
            packages.append(package)

        versions = affected_item.get("versions", [])
        if isinstance(versions, list) and versions:
            version_values = [str(version).strip() for version in versions if version]
            if version_values and package:
                affected_versions.append(f"{package}@{','.join(version_values)}")

        for range_item in affected_item.get("ranges", []):
            if not isinstance(range_item, dict):
                continue

            events = range_item.get("events", [])
            if not isinstance(events, list):
                events = []

            serialized_range = _serialize_affected_range(
                package=package,
                events=events,
                range_type=range_item.get("type"),
            )
            if serialized_range:
                affected_versions.append(serialized_range)

            for event in events:
                if not isinstance(event, dict):
                    continue
                fixed_version = event.get("fixed")
                if fixed_version not in ("", None) and package:
                    patched_versions.append(f"{package}@{fixed_version}")

        nested_database_specific = affected_item.get("database_specific")
        if nested_database_specific not in (None, "", {}, []):
            label = package or source_file
            affected_database_specific.append(
                f"{label}={_compact_json(nested_database_specific)}"
            )

        nested_ecosystem_specific = affected_item.get("ecosystem_specific")
        if nested_ecosystem_specific not in (None, "", {}, []):
            label = package or source_file
            affected_ecosystem_specific.append(
                f"{label}={_compact_json(nested_ecosystem_specific)}"
            )

    references = []
    for reference in advisory.get("references", []):
        if not isinstance(reference, dict):
            continue
        url = str(reference.get("url", "")).strip()
        if url:
            references.append(url)

    return {
        "source_file": source_file,
        "ghsa_id": str(advisory.get("id", "") or ""),
        "schema_version": str(advisory.get("schema_version", "") or ""),
        "modified": str(advisory.get("modified", "") or ""),
        "published": str(advisory.get("published", "") or ""),
        "withdrawn": str(advisory.get("withdrawn", "") or ""),
        "summary": str(advisory.get("summary", "") or ""),
        "details": str(advisory.get("details", "") or ""),
        "severity": _extract_severity(advisory, database_specific),
        "aliases": _join_unique(aliases),
        "cve_ids": _join_unique(
            [alias for alias in aliases if str(alias).strip().startswith("CVE-")]
        ),
        "cwe_ids": _join_unique(cwe_ids),
        "affected_ecosystems": _join_unique(ecosystems),
        "affected_packages": _join_unique(packages),
        "affected_versions": _join_unique(affected_versions),
        "patched_versions": _join_unique(patched_versions),
        "references": _join_unique(references),
        "database_specific": _compact_json(database_specific),
        "affected_database_specific": _join_unique(affected_database_specific),
        "affected_ecosystem_specific": _join_unique(affected_ecosystem_specific),
        "raw_json_copied_path": raw_json_copied_path,
    }


def copy_raw_json(source_file, source_path, json_output_dir, output_dir):
    relative_path = source_file.relative_to(source_path)
    destination = json_output_dir / relative_path
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source_file, destination)
    return destination.relative_to(output_dir).as_posix()


def write_csv(rows, csv_path):
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with csv_path.open("w", encoding="utf-8", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def write_metadata(metadata, metadata_path):
    metadata_path.parent.mkdir(parents=True, exist_ok=True)
    with metadata_path.open("w", encoding="utf-8") as metadata_file:
        json.dump(metadata, metadata_file, ensure_ascii=False, indent=2)


def main():
    started_at = datetime.now().astimezone()

    try:
        config = load_config()
        json_files = find_json_files(config["source_path"])
    except ConfigError as exc:
        print(f"Erro de configuração: {exc}", file=sys.stderr)
        sys.exit(1)

    files_found = len(json_files)

    output_dir = (
        config["output_base_dir"]
        / "output"
        / started_at.date().isoformat()
    )
    json_output_dir = output_dir / "json"
    csv_path = output_dir / "github_security_advisories.csv"
    metadata_path = output_dir / "run_metadata.json"

    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    rows = []
    files_processed = 0
    files_copied = 0
    errors_count = 0
    errors = []

    for source_file in json_files:
        source_file_relative = source_file.relative_to(config["source_path"]).as_posix()
        raw_json_copied_path = ""

        try:
            if config["copy_raw_json"]:
                raw_json_copied_path = copy_raw_json(
                    source_file=source_file,
                    source_path=config["source_path"],
                    json_output_dir=json_output_dir,
                    output_dir=output_dir,
                )
                files_copied += 1

            with source_file.open("r", encoding="utf-8") as advisory_file:
                advisory = json.load(advisory_file)

            rows.append(
                flatten_advisory(
                    advisory=advisory,
                    source_file=source_file_relative,
                    raw_json_copied_path=raw_json_copied_path,
                )
            )
            files_processed += 1
        except Exception as exc:  # noqa: BLE001
            errors_count += 1
            if len(errors) < 20:
                errors.append(
                    {
                        "source_file": source_file_relative,
                        "error": str(exc),
                    }
                )

    write_csv(rows=rows, csv_path=csv_path)

    finished_at = datetime.now().astimezone()
    metadata = {
        "source_name": SOURCE_NAME,
        "source_path": str(config["source_path"]),
        "output_dir": str(output_dir),
        "csv_path": str(csv_path),
        "started_at": started_at.isoformat(),
        "finished_at": finished_at.isoformat(),
        "files_found": files_found,
        "files_processed": files_processed,
        "files_copied": files_copied,
        "errors_count": errors_count,
        "errors_sample": errors,
        "copy_raw_json": config["copy_raw_json"],
    }
    write_metadata(metadata=metadata, metadata_path=metadata_path)

    print(f"JSON files found: {files_found}")
    print(f"Files processed: {files_processed}")
    print(f"Files copied: {files_copied}")
    print(f"Errors: {metadata['errors_count']}")
    print(f"CSV generated at: {csv_path}")
    print(f"Metadata generated at: {metadata_path}")


if __name__ == "__main__":
    main()
