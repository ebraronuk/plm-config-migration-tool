def normalize_row(row):
    """
    Metin alanlarını normalize eder.
    """
    normalized = {}
    for k, v in row.items():
        if isinstance(v, str):
            normalized[k] = v.strip().upper()
        else:
            normalized[k] = v
    return normalized
