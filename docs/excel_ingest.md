Excel ingest pipeline: workbook oku -> satir sozluklerine ayir -> sutunlari dogrula -> normalize et -> kayit listesini don.

`load_sheet_records` adim adim (src/excel/reader.py):
1. `read_excel`: `openpyxl.load_workbook` ile dosya acilir, `sheetnames` cekilir; hata alinirsa `RuntimeError` ile sarilir.
2. Hedef sayfa: `sheet_name` verilmis ise dogrudan, verilmemisse ilk sayfa secilir; sayfa yoksa `ValueError`.
3. `extract_rows`: ilk satir baslik alinip `strip().upper()` uygulanir, bos basliklar atlanir; takip eden tamamen bos satirlar atlanir; kalan satirlar baslik->hucre sozluklerine donusturulur.
4. Zorunlu sutunlar: `settings.excel.expected_columns` (`config/settings.yaml`) baz alinir, `required_cols` verilirse override eder; upper-case normalize edilir; `validate_columns` eksik ve beklenmeyen sutunlari bulur, eksikler loglanip `ValueError` firlar, beklenmeyenler uyarida loglanir.
5. Normalize: `normalize=True` ise her satir `normalize_row` uzerinden gecirilir; logda kayit sayisi ve sayfa adi yazilir, liste doner.

Normalize kurallari (src/excel/normalizer.py):
- PART_NUMBER/PART_NO: trim + upper uygulanir; bos string/None -> None; numerik degerler stringe cevrilip upper edilir.
- Diger metin alanlari: trim + upper; trim sonrasi bos ise None; sayisal/None degerlere dokunulmaz.
- Ornekler: `"  part-001 "` -> `"PART-001"`, `"rev a"` -> `"REV A"`, `""` -> `None`, `5` -> `5`.

Hata senaryolari:
- Eksik sutun: baslik satirinda zorunlu bir sutun yoksa hata loglanir ve `ValueError("Zorunlu sutunlar eksik: ...")` firlar.
- Beklenmeyen sutun: baslikta configte olmayan alan varsa uyarili log yazilir, isleyis devam eder.
- Gecersiz QUANTITY: pozitif tamsayi degilse `validate_columns` ValueError firlatir ve loglar.
- Tekrarlanan PART_NUMBER: normalize edilmis degerler duplikeyse `validate_columns` ValueError firlatir ve loglar.
- Bos satir/sayfa: tamamen bos satirlar `extract_rows` tarafindan atlanir; sayfada veri kalmazsa uyarili log yazilir ve bos liste doner; workbook icinde hic sayfa yoksa `ValueError`.

Loglar: tum loglar `setup_logger` (plmtool) uzerinden Turkce mesajlarla yazilir.
Config fallback: PyYAML yoksa manuel parser devreye girer, varsayilan sutun listesi (`PART_NO`, `DESCRIPTION`, `QUANTITY`, `REV`) kullanilir.

## Neden normalize gerekli?
- PLM/ERP tarafinda parca anahtarlarini uppercase/trim formatina zorlamak, duble kayit veya lokasyon bazli varyant kaynakli cogalmayi erken yakalamaya yardim eder.
- QUANTITY gibi alanlarda tip/isaret belirsizligini azaltir; MRP ve downstream veri modeli pozitif tamsayi bekler.
- Whitespace ve kultur farklarina dayali sapmalari azaltarak staging/production ortamlarinda ayni sorgu sonucunu saglar.

## Sahada sik gorulen Excel sorunlari
- Birlesik hucreler (merged cells): openpyxl sadece ilk hucreye deger koyar; bos kalan satirlari normalize ederken None'a cevirip eksik satir gibi algilanmasini engelleyin.
- Tamamen bos ya da sadece whitespace iceren satirlar: `extract_rows` bunlari atlar; sayisal kontroller oncesi None olasiligini hesaba katin.
- Metin gorunumlu sayilar: `" 007 "` veya `"10 "` gibi stringler; trim/upper sonrasi sayisal parse islemlerine hazirlanir.
- Baslik satirinda gizli whitespace veya farkli kapitalizasyon: basliklar strip+upper oldugu icin zorunlu sutun kontrolu saglikli calisir; ekstra sutunlar loglarda uyarilir.
