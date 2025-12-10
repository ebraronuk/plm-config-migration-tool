import pathlib
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

DEFAULT_EXPECTED_COLUMNS = ["PART_NO", "DESCRIPTION", "QUANTITY", "REV"]
DEFAULT_LOG_LEVEL = "INFO"


@dataclass
class ExcelSettings:
    expected_columns: List[str] = field(default_factory=list)


@dataclass
class LoggingSettings:
    level: str = DEFAULT_LOG_LEVEL


@dataclass
class Settings:
    excel: ExcelSettings
    logging: LoggingSettings


def _read_yaml(path: pathlib.Path) -> Optional[Dict[str, Any]]:
    """
    PyYAML varsa ayarlari okur, yoksa None dondurur.
    """
    try:
        import yaml  # type: ignore
    except ImportError:
        return None

    try:
        with path.open("r", encoding="utf-8") as fh:
            data = yaml.safe_load(fh) or {}
            return data if isinstance(data, dict) else {}
    except Exception:
        return None


def _fallback_parse(path: pathlib.Path) -> Dict[str, Any]:
    """
    Basit YAML yapisini (logging ve excel icin) manuel parse eder.
    """
    parsed: Dict[str, Any] = {"excel": {}, "logging": {}}
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return parsed

    section = None
    in_expected = False
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        if stripped.endswith(":") and not stripped.startswith("-"):
            section = stripped[:-1].strip()
            in_expected = False
            continue

        if section == "excel" and stripped.startswith("expected_columns"):
            in_expected = True
            parsed.setdefault("excel", {})["expected_columns"] = []
            continue

        if in_expected and stripped.startswith("-"):
            item = stripped.lstrip("-").strip()
            if item:
                parsed.setdefault("excel", {}).setdefault("expected_columns", []).append(item)
            continue

        if section == "logging" and stripped.startswith("level:"):
            _, _, value = stripped.partition(":")
            parsed.setdefault("logging", {})["level"] = value.strip()

    return parsed


def _load_settings() -> Settings:
    """
    Ayarlari dosyadan yukler, eksikse varsayilanlari kullanir.
    """
    settings_path = pathlib.Path(__file__).resolve().parents[2] / "config" / "settings.yaml"

    raw: Dict[str, Any] = {}
    if settings_path.exists():
        raw_yaml = _read_yaml(settings_path)
        raw = raw_yaml if raw_yaml is not None else _fallback_parse(settings_path)

    excel_raw = raw.get("excel", {}) if isinstance(raw, dict) else {}
    if not excel_raw and isinstance(raw, dict) and "expected_columns" in raw:
        excel_raw["expected_columns"] = raw.get("expected_columns", [])

    expected_cols = excel_raw.get("expected_columns", DEFAULT_EXPECTED_COLUMNS)
    normalized_expected = [c.strip().upper() for c in expected_cols if c]

    logging_raw = raw.get("logging", {}) if isinstance(raw, dict) else {}
    level = logging_raw.get("level", DEFAULT_LOG_LEVEL)

    return Settings(
        excel=ExcelSettings(expected_columns=normalized_expected or DEFAULT_EXPECTED_COLUMNS),
        logging=LoggingSettings(level=level or DEFAULT_LOG_LEVEL),
    )


settings = _load_settings()
