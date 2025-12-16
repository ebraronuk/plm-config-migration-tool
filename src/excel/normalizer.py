def _normalize_string(value):
    """Metinleri trim+upper yapar; trim sonrasi bos ise None dondurur."""
    stripped = value.strip()
    return stripped.upper() if stripped else None


def _normalize_part_number(value):
    """PART_NUMBER alanlarini trim+upper ile hizalar; bos veya None varsa None dondurur."""
    if value is None:
        return None
    if isinstance(value, (int, float)):
        value = str(int(value)) if isinstance(value, float) and value.is_integer() else str(value)
    if isinstance(value, str):
        return _normalize_string(value)
    text = str(value).strip()
    return text.upper() if text else None


def normalize_row(row):
    """Satirdaki alanlari normalize eder: PART_NUMBER/PART_NO ozel, diger metinler trim+upper, boslar None olur."""
    normalized = {}
    for k, v in row.items():
        key_upper = k.upper() if isinstance(k, str) else k
        if key_upper in {"PART_NUMBER", "PART_NO"}:
            normalized[k] = _normalize_part_number(v)
        elif isinstance(v, str):
            normalized[k] = _normalize_string(v)
        else:
            normalized[k] = v
    return normalized
