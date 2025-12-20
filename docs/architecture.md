# Mimari Ozet

Bu arac, parca ana verisini Excel'den PLM/ERP staging ortamlarina tasiyan moduler bir boru hattidir. Her asama bagimsiz tasarlanmistir; dogrulama, normalizasyon ve cikis katmanlari ayri gelistirilebilir.

## Pipeline Asamalari
- **Konfigurasyon Yukleme**: `config/settings.yaml` icinden beklenen sutunlar ve log seviyesi okunur; YAML pars edilemezse varsayilanlar devreye girer, kisitli ortamlarda bile calismaya devam eder.
- **Excel Ingest**: Workbook (OpenPyXL) acilir, hedef sayfa secilir, ilk satir basliklari trim + uppercase ile normalize edilir; tamamen bos satirlar erken safhada elenir.
- **Dogrulama**: Zorunlu basliklar uygulanir, beklenmeyen basliklar uyarilir; PART_NUMBER/PART_NO duplikeleri ve pozitif tamsayi QUANTITY kontrol edilir; hatalar hizla `ValueError` ile durdurulur.
- **Donusum / Normalizasyon**: Metinler trim + uppercase; parca numaralari tutarli hale getirilir; bos stringler `None` olur ki downstream export bosluk depolamasin.
- **Cikis**: Mevcut haliyle staging veritabanlari icin SQL INSERT uretir; cok seviyeli BOM cozumu icin genisletme noktasi mevcuttur.

## Tasarim Hedefleri
- **Izlenebilirlik**: Her asamada yapilandirilmis loglar, tasima calismalarinda iz surme ve hata kok neden analizi icin kayit birakir.
- **Yapilandirilabilirlik**: Beklenen sutunlar ve log seviyesi konfig dosyasindan yonetilir; parca numarasi normalizasyonu PLM/ERP anahtar semantigine uygun sekilde ozel ele alinir.
- **Test Edilebilirlik**: Ingest/dogrulama/normalizasyon davranislari pytest ile kapsanir; yan etkisi az fonksiyonlar regresyonu kolaylastirir.
- **Birlikte Calisabilirlik**: Giris/cikis tipleri sade Python veri yapilari olarak tutulur; ETL isleri, staging DB yazicilari veya PLM API musterileri ile kolayca entegre edilir.
