# PLM Config Migration Tool

Excel'den gelen parca verisini PLM/ERP sistemlerine temiz, izlenebilir ve tekrarlanabilir sekilde tasimak icin tasarlandi. Excel'i okur, kritik alanlari dogrular, degerleri normalize eder ve veri akisini BOM cozumu ile SQL/ETL cikislarina hazirlar.

## Kimler icin
- Konfigurasyon yonetimi ve PLM/ERP ekipleri: tedarikci veya miras Excel'lerini standarda cekmek isteyenler.
- Uretim, savunma, havacilik muhendisleri: kurumsal sistemlere izlenebilir ve tekrarlanabilir veri teslimi yapmak isteyenler.
- Veri/otomasyon muhendisleri: parca ve BOM migrasyonu icin staging boru hatlari kuranlar.

## Cozulen sorun
- Karisik buyuk/kucuk harf, bosluk, tekrar eden parca numaralari ve tutarsiz miktarlar.
- Eksik veya beklenmeyen sutunlar nedeniyle gec ortaya cikan duzeltme ihtiyaci.
- PLM/ERP ithalatlari icin tahmin edilebilir, denetlenebilir veri ihtiyaci (BOM toplamlari, MRP, degisiklik kontrolleri).

## Gercek is akislari ile uyum
- Tedarikci/miras Excel ciktilarini PLM/ERP importorlerine gitmeden once normalize eder.
- Zorunlu sutunlari ve alan kurallarini (benzersiz parca numarasi, pozitif miktar) erken uygular.
- Yapilandirilmis loglarla hatalarin ve veri problemlerinin izini surmeyi kolaylastirir.
- Normalizasyon cikti, BOM genisletme ve SQL/ETL adimlarina dogrudan beslenebilir (staging veya sandbox ortamlar).

## Ust seviye veri akisi
1) **Konfigurasyon**: `config/settings.yaml` uzerinden beklenen sutunlar ve log seviye/formatlari okunur.
2) **Excel Ingest**: Workbook acilir, hedef sayfa secilir.
3) **Dogrulama**: Zorunlu basliklar kontrol edilir, beklenmeyenler loglanir, tekrar parca numaralari ve pozitif miktar sartlari uygulanir.
4) **Normalizasyon**: Metinler trim + uppercase, parca numaralari hizalanir, bos stringler `None` olur.
5) **(Opsiyonel) BOM Cozumu**: Cok seviyeli BOM icin yer tutucu.
6) **Cikis**: SQL INSERT olusturma veya ETL kademesine besleme.

## Klasor yapisi
- `src/` - ingest, dogrulama, normalizasyon ve cikis modulleri.
- `docs/` - mimari ve boru hatti dokumantasyonu.
- `examples/` - ornek Excel girdileri.
- `tests/` - regresyon ve davranis testleri.

## Hizli baslangic
```
python -m pip install -r requirements.txt  # varsa
python -m pytest -q                        # testler
```
Beklenen sutun ve veri sekli icin `examples/sample_input.xlsx` dosyasini inceleyin.
