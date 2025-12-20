from src.utils.logger import setup_logger

logger = setup_logger()


class BomParser:
    """Cok seviyeli BOM kayitlarini okuyup yapilandirmak icin iskelet parser sinifi."""

    def parse(self, records):
        """Girdi kayitlarini alir, dogrular ve agac yapisi icin hazirlar (detaylari TODO)."""
        # TODO: Kayit formati kontrolu, temel alan dogrulama ve sonraki adimlarin zincirlenmesi eklenecek.
        raise NotImplementedError("TODO: parse implement edilecek")

    def validate_structure(self, nodes):
        """BOM dugumlerinin yapisal tutarliligini kontrol eder (zorunlu alanlar, seviyeler, tekrarlar)."""
        # TODO: Zorunlu alan denetimi, level tutarliligi ve parent-child tekrar kontrolu eklenecek.
        raise NotImplementedError("TODO: validate_structure implement edilecek")

    def detect_cycles(self, nodes):
        """Parent-child baglantilarinda dongu olup olmadigini tespit eder."""
        # TODO: Grafik gezintisiyle cycle tespiti eklenip hata/uyari uretilecek.
        raise NotImplementedError("TODO: detect_cycles implement edilecek")

    def build_hierarchy(self, nodes):
        """Dogrulanmis dugumleri agac/katman yapisina donusturur."""
        # TODO: Seviyelere gore hiyerarsi olusturma ve baglanti kurallari uygulanacak.
        raise NotImplementedError("TODO: build_hierarchy implement edilecek")

    def validate_levels(self, records, root_level=0):
        """BOM kayitlarindaki level alaninin tutarliligini kontrol eder (tamsayi, kok seviyesi, seviye atlamama)."""
        logger.info("BOM seviye dogrulamasi basladi (kayit sayisi=%s)", len(records))

        if not records:
            logger.info("Kayit bulunamadi, seviye dogrulama atlandi")
            return

        def _level_value(record, index):
            if not isinstance(record, dict):
                raise ValueError(f"Kayit sozluk olmali (satir {index})")
            if "level" not in record:
                raise ValueError(f"level alani eksik (satir {index})")
            value = record.get("level")
            if isinstance(value, bool) or not isinstance(value, int):
                raise ValueError(f"level alani tamsayi olmali (satir {index})")
            return value

        first_level = _level_value(records[0], 1)
        if first_level != root_level:
            raise ValueError(f"Ilk kaydin level degeri {root_level} olmali (bulunan: {first_level})")

        previous = first_level
        for idx, record in enumerate(records[1:], start=2):
            current = _level_value(record, idx)
            if current - previous > 1:
                raise ValueError(f"Seviye atlanamaz: onceki={previous}, yeni={current}, satir={idx}")
            previous = current

        logger.info("BOM seviye dogrulamasi tamamlandi")
