# PLM Config Migration Tool

Bu araç şu temel hattı sağlar:
- Excel → JSON dönüşümü
- Çok seviyeli BOM ayrıştırma
- SQL taşıma scripti üretimi

## Mimari Özeti
- Excel alma: `src/excel/reader.py` workbook yükler, `validator.py` ile doğrulayıp `normalizer.py` ile normalize ederek kayıt listesi oluşturur.
- BOM ayrıştırma: `src/bom/parser.py` çok seviyeli BOM çözümü için yer tutucudur.
- SQL üretimi: `src/sql/generator.py` bellekteki kayıtlardan INSERT scripti yazar.
- Ortak bileşenler: `src/utils/logger.py` paylaşılan logger'ı tanımlar; `config/settings.yaml` beklenen sütunlar gibi varsayılanları taşır.

Proje erken geliştirme aşamasındadır. Daha fazla dokümantasyon eklenecek.
