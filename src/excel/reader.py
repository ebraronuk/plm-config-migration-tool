from src.excel.normalizer import normalize_row
from src.excel.validator import validate_columns
from src.utils.logger import setup_logger

logger = setup_logger()


def read_excel(file_path, data_only=True):
    """
    Excel dosyasini okur, workbook ve sayfa adlarini dondurur.
    """
    try:
        import openpyxl
    except ImportError as exc:
        raise RuntimeError("Excel dosyalarini okuyabilmek icin openpyxl gerekli") from exc

    try:
        wb = openpyxl.load_workbook(file_path, data_only=data_only)
        logger.info("Workbook yuklendi: %s", file_path)
        return wb, wb.sheetnames
    except Exception as exc:
        raise RuntimeError(f"Excel okuma hatasi: {exc}") from exc


def extract_rows(wb, sheet_name=None):
    """
    Ilk satiri baslik kabul ederek secili sayfayi sozluk listesine donusturur.
    """
    sheet = wb[sheet_name] if sheet_name else wb.active
    rows = list(sheet.iter_rows(values_only=True))
    if not rows:
        return []

    headers = [str(h).strip().upper() if h is not None else "" for h in rows[0]]
    parsed_rows = []
    for raw in rows[1:]:
        if not any(raw):
            continue

        row_dict = {}
        for idx, header in enumerate(headers):
            if not header:
                continue
            row_dict[header] = raw[idx] if idx < len(raw) else None
        if row_dict:
            parsed_rows.append(row_dict)
    return parsed_rows


def load_sheet_records(file_path, sheet_name=None, required_cols=None, normalize=True):
    """
    Workbook okur, satirlari ceker, zorunlu sutunlari dogrular, degerleri normalize eder ve kayit listesi dondurur.
    """
    wb, sheet_names = read_excel(file_path)
    target_sheet = sheet_name or (sheet_names[0] if sheet_names else None)

    if not target_sheet:
        raise ValueError("Workbook icinde sayfa bulunamadi")
    if target_sheet not in sheet_names:
        raise ValueError(f"Sayfa bulunamadi: {target_sheet}")

    rows = extract_rows(wb, sheet_name=target_sheet)
    if not rows:
        logger.warning("Sayfa icinde veri bulunamadi: '%s'", target_sheet)
        return []

    normalized_required = [c.strip().upper() for c in required_cols] if required_cols else []
    if normalized_required:
        missing = validate_columns(rows, normalized_required)
        if missing:
            raise ValueError(f"Zorunlu sutunlar eksik: {', '.join(missing)}")

    normalized_rows = [normalize_row(r) for r in rows] if normalize else rows
    logger.info("%s kayit hazirlandi (sayfa=%s)", len(normalized_rows), target_sheet)
    return normalized_rows


def excel_to_records(file_path, sheet_name=None, required_cols=None, normalize=True):
    """
    Geriye donuk uyum icin load_sheet_records sarmalayicisi.
    """
    return load_sheet_records(
        file_path=file_path,
        sheet_name=sheet_name,
        required_cols=required_cols,
        normalize=normalize,
    )
