from src.utils.logger import setup_logger

logger = setup_logger()


def _normalize_text(value):
    if isinstance(value, str):
        return value.strip().upper()
    return value


def _find_part_key(headers):
    if "PART_NUMBER" in headers:
        return "PART_NUMBER"
    if "PART_NO" in headers:
        return "PART_NO"
    return None


def _find_quantity_key(headers):
    return "QUANTITY" if "QUANTITY" in headers else None


def _ensure_no_duplicate_part_number(rows, headers):
    logger.info("PART_NUMBER tekrar kontrolu yapiliyor")
    part_key = _find_part_key(headers)
    if not part_key:
        logger.info("PART_NUMBER sutunu bulunamadi, tekrar kontrolu atlandi")
        return

    seen = set()
    duplicates = set()
    for row in rows:
        if not isinstance(row, dict):
            continue
        value = _normalize_text(row.get(part_key))
        if value is None:
            continue
        if isinstance(value, str) and not value:
            continue
        if value in seen:
            duplicates.add(value)
        else:
            seen.add(value)

    if duplicates:
        formatted = ", ".join(sorted(str(v) for v in duplicates))
        message = f"Tekrarlanan PART_NUMBER degerleri bulundu: {formatted}"
        logger.error(message)
        raise ValueError(message)

    logger.info("PART_NUMBER tekrar kontrolu tamamlandi")


def _parse_positive_int(value):
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value if value > 0 else None
    if isinstance(value, float):
        if value.is_integer() and value > 0:
            return int(value)
        return None
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            return None
        try:
            parsed = int(stripped)
        except ValueError:
            return None
        return parsed if parsed > 0 else None
    return None


def _ensure_positive_quantity(rows, headers):
    logger.info("QUANTITY pozitif tamsayi kontrolu yapiliyor")
    quantity_key = _find_quantity_key(headers)
    if not quantity_key:
        logger.info("QUANTITY sutunu bulunamadi, sayisal kontrol atlandi")
        return

    for idx, row in enumerate(rows, start=1):
        if not isinstance(row, dict):
            continue
        original_value = row.get(quantity_key)
        parsed = _parse_positive_int(original_value)
        if parsed is None:
            message = f"QUANTITY sutununda pozitif tamsayi bekleniyor (satir {idx}: {original_value})"
            logger.error(message)
            raise ValueError(message)

    logger.info("QUANTITY pozitif tamsayi kontrolu tamamlandi")


def validate_columns(rows, expected_cols):
    """
    Beklenen sutunlari dogrular, eksik ve beklenmeyenleri dondurur ve ek veri kontrolleri yapar.
    rows: sozluk listesi
    expected_cols: beklenen sutun adlari listesi
    """
    logger.info("Sutun dogrulamasi basladi (kayit sayisi=%s)", len(rows))

    if not expected_cols:
        logger.info("Beklenen sutun listesi bos, dogrulama atlandi")
        return [], []

    headers = list(rows[0].keys()) if rows and isinstance(rows[0], dict) else []
    expected_set = set(expected_cols)

    missing = [c for c in expected_cols if c not in headers]
    unexpected = [h for h in headers if h not in expected_set]
    logger.info(
        "Beklenen sutun kontrolu tamamlandi (eksik=%s, beklenmeyen=%s)",
        len(missing),
        len(unexpected),
    )

    if rows:
        _ensure_no_duplicate_part_number(rows, headers)
        _ensure_positive_quantity(rows, headers)
    else:
        logger.info("Dogrulanacak satir bulunamadi, veri kontrolleri atlandi")

    return missing, unexpected
