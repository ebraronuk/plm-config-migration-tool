# PLM Config Migration Tool

Bu arac su temel hatlari saglar:
- Excel'den JSON benzeri kayitlara donusum
- Cok seviyeli BOM ayristirma (gelistirme asamasinda)
- SQL tasima scripti uretimi

## Mimari Akis
- Pipeline: Excel -> JSON -> BOM -> SQL
- Excel dosyalari okunur, kayitlar normalize edilir, gerekirse BOM yapisi cozulur ve SQL scriptlerine yazilir.

## Mimari Ozeti
- Excel alma: `src/excel/reader.py` workbook yukler; `validator.py` ile sutun dogrular; `normalizer.py` ile normalize ederek kayit listesi olusturur.
- BOM ayristirma: `src/bom/parser.py` cok seviyeli BOM cozumu icin yer tutucudur.
- SQL uretimi: `src/sql/generator.py` bellekteki kayitlardan INSERT scripti yazar.
- Ortak bilesenler: `src/utils/logger.py` paylasilan logger'i tanimlar; `config/settings.yaml` beklenen sutunlar gibi varsayilanlari tasir.

Proje erken gelistirme asamasindadir. Daha fazla dokumantasyon eklenecek.
