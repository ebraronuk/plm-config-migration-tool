def validate_columns(rows, required_cols):
    """
    Gerekli sütunların mevcut olup olmadığını kontrol eder.
    rows: sözlük listesi
    required_cols: beklenen sütun adları listesi
    """
    if not required_cols:
        return []
    if not rows:
        return list(required_cols)

    reference_row = rows[0] if isinstance(rows[0], dict) else {}
    missing = [c for c in required_cols if c not in reference_row]
    return missing
