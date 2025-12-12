def validate_columns(rows, expected_cols):
    """
    Beklenen sutunlari dogrular, eksik ve beklenmeyenleri dondurur.
    rows: sozluk listesi
    expected_cols: beklenen sutun adlari listesi
    """
    if not expected_cols:
        return [], []

    headers = list(rows[0].keys()) if rows and isinstance(rows[0], dict) else []
    expected_set = set(expected_cols)

    missing = [c for c in expected_cols if c not in headers]
    unexpected = [h for h in headers if h not in expected_set]
    return missing, unexpected
