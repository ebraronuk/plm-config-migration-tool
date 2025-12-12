import logging
import pathlib

import pytest

from src.excel.reader import load_sheet_records


SAMPLE_PATH = pathlib.Path(__file__).resolve().parents[1] / "examples" / "sample_parts.xlsx"


def test_load_records_with_override_normalizes():
    records = load_sheet_records(
        SAMPLE_PATH,
        required_cols=["PART_NUMBER", "DESCRIPTION", "QUANTITY"],
        normalize=True,
    )

    assert len(records) == 3
    assert records[0]["PART_NUMBER"] == "PART-001"
    assert records[1]["DESCRIPTION"] == "BRACKET"
    assert records[2]["QUANTITY"] == "7"


def test_missing_config_columns_raise(caplog):
    caplog.set_level(logging.INFO, logger="plmtool")

    with pytest.raises(ValueError) as exc:
        load_sheet_records(SAMPLE_PATH)

    assert str(exc.value) == "Zorunlu sutunlar eksik: PART_NO, REV"
    assert "Beklenmeyen sutunlar bulundu: PART_NUMBER" in caplog.text
    assert "Zorunlu sutunlar eksik: PART_NO, REV" in caplog.text
