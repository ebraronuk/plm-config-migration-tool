# Excel Ingest Pipeline

Excel dosyalari, PLM/ERP staging'e girmeden once nasil okunur, dogrulanir ve normalize edilir bu dokuman aciklar.

## Akis
1. **Workbook Okuma**: `openpyxl.load_workbook` dosyayi acar; aktif sayfa veya verilen sayfa secilir. Sayfa yoksa aninda hata verilir.
2. **Satir Cekme**: Ilk satir `strip().upper()` sonrasi baslik olur. Bos basliklar atlanir. Tamamen bos satirlar veri setine girmeden elenir.
3. **Baslik Dogrulama**:
   - Zorunlu sutunlar `config/settings.yaml` veya verilen override'dan cekilir.
   - Eksik zorunlu basliklar `ValueError` ile durdurulur; beklenmeyenler uyarida loglanir.
4. **Veri Dogrulama**:
   - PART_NUMBER/PART_NO normalize edildikten sonra duplikeler yakalanir, `ValueError` firlatilir.
   - `QUANTITY` pozitif tamsayi olmak zorunda; negatif, sifir veya sayisal olmayan degerlerde `ValueError`.
5. **Normalizasyon**:
   - Parca numaralari: trim + uppercase; numerikler stringe cevrilir; bos stringler `None`.
   - Diger metin alanlari: trim + uppercase; bos stringler `None`.
   - Metin olmayan degerler parca numarasi haric dokunulmaz.
6. **Cikis**: BOM cozumu veya SQL/ETL ciktilarina hazir normalize sozluk listesi.

## Saha Gercegi Excel Sorunlari ve Yonetimi
- **Birlesik hucreler (merged)**: OpenPyXL sadece ilk hucreyi degerli gosterir; bos satirlar elenir, bos stringler `None` olur, hayalet veri olusmaz.
- **Gizli bosluk / kapitalizasyon kaymasi**: Baslik ve metinler trim + uppercase yapilir; `part_number`, ` Part_Number`, `PART_NUMBER` ayni hale gelir.
- **Metin formatli sayilar**: `" 007 "` veya `"10 "` trim + uppercase sonrasi sayi parse edilir; miktar icin pozitif kosul uygulanir.
- **Bos ayirac satirlar**: Cekim asamasinda atilir ki dogrulama/cikis kirlenmesin.
- **Beklenmeyen sutunlar**: WARN seviyesinde loglanir, isleme devam edilir; deneme-yanilma ingest'lerinde veri kaybi olmadan raporlama saglar.

## Operasyon Notlari
- Loglar Turkce, seviye `config/settings.yaml` ile ayarlanir.
- Normalizasyon ve dogrulama, PLM/ERP import veya staging DB yazimi oncesinde calisir; hatalar erken yakalanir.
