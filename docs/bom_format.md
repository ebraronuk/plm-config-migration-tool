# BOM Veri Kontrati

Bu dokuman, arac tarafindan tuketilecek cok seviyeli BOM verisinin beklenen yapisini tarif eder. Alan adlari, zorunlu/opsiyonel nitelikler ve modelleme kisitlari belirtilmistir; parse/uygulama kapsam disidir.

## Varlik Modeli
- **parent** (zorunlu): Cocuk elemani uzerinde tutan montaj veya alt montaj kimligi. Tipik olarak parca master anahtariyla hizalanir.
- **child** (zorunlu): Parent icinde referans verilen parca veya alt montaj kimligi.
- **quantity** (zorunlu): Bu seviyede parent altinda bulunan child miktari; pozitif tamsayi.
- **level** (zorunlu): Derinlik gostergesi (root = 0 veya 1, dataset genelinde tutarli) gezinti ve genisletme sirasi icin kullanilir.
- **uom** (opsiyonel): Miktar icin olcu birimi (EA, SET, M vb.).
- **reference_designators** (opsiyonel): Pozisyonel referanslar gerekirse string listesi.
- **effectivity** (opsiyonel): Ust sistemlerden geliyorsa gecerlilik araliklarini (tarih veya revizyon) tasiyan yapi.
- **attributes** (opsiyonel): Ek metadata icin serbest anahtar/deger sozlugu (ornegin make/buy, tedarikci).

## Zorunlu Alanlar
- `parent`
- `child`
- `quantity`
- `level`

## Opsiyonel Alanlar
- `uom`
- `reference_designators`
- `effectivity`
- `attributes`

## Varsayimlar ve Kisitlar
- Dairesel referans yoktur; veri kumesi DAG olmalidir.
- Her BOM veri kumesi tek bir kok montaj icermelidir; coklu kok varsa ayri datasetlere bolunmelidir.
- Parca kimlikleri upstream tarafinda normalize edilmistir (bosluk/kucuk-buyuuk harf); boylece tekrar tespiti duzgun calisir.
- Miktarlar pozitif tamsayi olmalidir; kesirli miktarlar bu kontratta desteklenmez.
- Seviye numaralari dataset genelinde tutarli olmalidir (root=0 veya root=1) ve bir dal icinde seviye atlanmamasi gerekir.
- Kardes komponentlerin sirasi anlamsal olarak onemli degildir, aksi belirtilmedikce `attributes` icinde ekstra siralama bilgisi verilmelidir.

## Ornek (JSON benzeri pseudocode)
```json
[
  { "parent": "ASSY-1000", "child": "ASSY-1100", "quantity": 1, "level": 1, "uom": "EA" },
  { "parent": "ASSY-1000", "child": "BRKT-2001", "quantity": 2, "level": 1, "uom": "EA" },
  { "parent": "ASSY-1100", "child": "FAST-3005", "quantity": 4, "level": 2, "uom": "EA", "reference_designators": ["R1", "R2", "R3", "R4"] },
  { "parent": "ASSY-1100", "child": "CABL-4100", "quantity": 1, "level": 2, "uom": "M" }
]
```
