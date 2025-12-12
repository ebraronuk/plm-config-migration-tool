Excel ingest pipeline: workbook oku -> satir sozluklerine ayir -> sutunlari dogrula -> normalize et -> kayit listesini don.

`load_sheet_records` adim adim (src/excel/reader.py):
1. `read_excel`: `openpyxl.load_workbook` ile dosya acilir, `sheetnames` cekilir; hata alinirsa `RuntimeError` ile sarilir.
2. Hedef sayfa: `sheet_name` verilmis ise dogrudan, verilmemisse ilk sayfa secilir; sayfa yoksa `ValueError`.
3. `extract_rows`: ilk satir baslik alinip `strip().upper()` uygulanir, bos basliklar atlanir; takip eden tamamen bos satirlar atlanir; kalan satirlar baslik->hucre sozluklerine donusturulur.
4. Zorunlu sutunlar: `settings.excel.expected_columns` (`config/settings.yaml`) baz alinir, `required_cols` verilirse override eder; upper-case normalize edilir; `validate_columns` ilk satirdan eksik ve beklenmeyen sutunlari bulur, eksikler loglanip `ValueError` firlar, beklenmeyenler uyarida loglanir.
5. Normalize: `normalize=True` ise her satir `normalize_row` uzerinden gecirilir; logda kayit sayisi ve sayfa adi yazilir, liste doner.

Normalize kurallari (src/excel/normalizer.py):
- Sadece `str` alanlar `strip()` + `upper()` ile temizlenir; sayisal/None degerleri aynen korunur.
- Ornekler:
  - `"  part-001 "` -> `"PART-001"`
  - `"rev a"` -> `"REV A"`
  - `5` veya `None` aynen kalir.

Hata senaryolari:
- Eksik sutun: baslik satirinda zorunlu bir sutun yoksa hata loglanir ve `ValueError("Zorunlu sutunlar eksik: ...")` firlar.
- Beklenmeyen sutun: baslikta configte olmayan alan varsa uyarili log yazilir, isleyis devam eder.
- Gecersiz QUANTITY: sayisal olmayan deger aynen doner, anlik kontrol yok; sonraki isleyici sayisal bekliyorsa tip donusumunde `ValueError` olusabilir.
- Bos satir/sayfa: tamamen bos satirlar `extract_rows` tarafindan atlanir; sayfada veri kalmazsa uyarili log yazilir ve bos liste doner; workbook icinde hic sayfa yoksa `ValueError`.

Loglar: tum loglar `setup_logger` (plmtool) uzerinden Turkce mesajlarla yazilir.
Config fallback: PyYAML yoksa manuel parser devreye girer, varsayilan sutun listesi (`PART_NO`, `DESCRIPTION`, `QUANTITY`, `REV`) kullanilir.
