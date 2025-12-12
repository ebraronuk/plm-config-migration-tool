Excel ingest pipeline: read workbook -> sheet rows -> validate sutunlar -> normalize -> kayit listesi.
Config: `config/settings.yaml` icindeki `excel.expected_columns` zorunlu sutunlarin kaynagi.
Ithalat modulu: `src/excel/reader.py` uzerinden `load_sheet_records` kullanilir.
Basliklar: ilk satir baslik kabul edilir, tum basliklar upper-case yapilir.
Normalize: `src/excel/normalizer.py` string degerleri strip + upper ile temizler, digerleri aynen kalir.
Dogrulama: `src/excel/validator.py` zorunlu sutun eksigini kontrol eder.
Hata: zorunlu sutun eksigi varsa `ValueError` firlatilir.
Hata: sayfa yoksa veya hic satir yoksa bos liste veya `ValueError` doner; detaylar loglanir.
Loglar: tum loglar `setup_logger` (plmtool) uzerinden Turkce mesajlarla yazilir.
Not: PyYAML yoksa config icin fallback parser devreye girer, varsayilan sutun listesi kullanilir.
