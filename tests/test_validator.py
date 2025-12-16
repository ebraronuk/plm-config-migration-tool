import logging

import pytest

from src.excel.validator import validate_columns


def test_duplicate_part_number_raises(caplog):
    caplog.set_level(logging.INFO, logger="plmtool")

    rows = [
        {"PART_NUMBER": " part-001 ", "DESCRIPTION": "A", "QUANTITY": 1},
        {"PART_NUMBER": "PART-001", "DESCRIPTION": "B", "QUANTITY": "2"},
    ]

    with pytest.raises(ValueError) as exc:
        validate_columns(rows, ["PART_NUMBER", "DESCRIPTION", "QUANTITY"])

    assert "Tekrarlanan PART_NUMBER degerleri bulundu: PART-001" in str(exc.value)
    assert "PART_NUMBER tekrar kontrolu yapiliyor" in caplog.text


def test_quantity_must_be_positive_integer(caplog):
    caplog.set_level(logging.INFO, logger="plmtool")

    rows = [
        {"PART_NUMBER": "P-01", "DESCRIPTION": "A", "QUANTITY": "0"},
        {"PART_NUMBER": "P-02", "DESCRIPTION": "B", "QUANTITY": "abc"},
    ]

    with pytest.raises(ValueError) as exc:
        validate_columns(rows, ["PART_NUMBER", "DESCRIPTION", "QUANTITY"])

    assert "QUANTITY sutununda pozitif tamsayi bekleniyor" in str(exc.value)
    assert "QUANTITY pozitif tamsayi kontrolu yapiliyor" in caplog.text
