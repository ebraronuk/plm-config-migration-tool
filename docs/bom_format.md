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

## Dogrulama Kurallari ve Kenar Durumlar (parse oncesi)
- **Tekrar eden parent-child iliskisi**
  - Neden: Aynı parent altinda ayni child'in coklu kaydi MRP/BOM toplamlari icin yanlis miktar cikar.
  - Tespit: parent+child kombinasyonunu uniq kabul edip tekrar eden satirlari bulmak.
  - Beklenen davranis: Hata ile reddet; manuel konsolidasyon gerektirir.
  - Ornek: `parent=ASSY-1000, child=BRKT-2001` iki ayri satirda.
- **Dairesel referans (cycle)**
  - Neden: Traversal sonsuz donguye girer, patlama listeleri bozulur.
  - Tespit: Graph cycle tespiti (DFS/visited) ile parent-child baglanti halkasi aramak.
  - Beklenen davranis: Hata ile reddet; BOM DAG olmalidir.
  - Ornek: A -> B, B -> C, C -> A.
- **Tutarsiz level numarasi**
  - Neden: Seviye siralamasina bagli genisleme ve raporlama sapar.
  - Tespit: Root degerini sabitleyip (0 veya 1) her parent-child icin level(child) = level(parent)+1 kosulunu kontrol etmek.
  - Beklenen davranis: Hata veya en azindan bloklayici uyarı; derinlik yeniden hesaplanmadan ilerlenmemeli.
  - Ornek: Root=1 iken child level 3 verilmis.
- **Gecersiz veya sifir miktar**
  - Neden: MRP ve malzeme ihtiyac hesaplari icin fiziksel anlam tasimaz.
  - Tespit: quantity pozitif tamsayi mi kontrol etmek.
  - Beklenen davranis: Hata ile reddet; sifir veya negatif miktar kabul edilmez.
  - Ornek: `quantity=0` veya `quantity=-2`.
- **Tek BOM icinde coklu kok**
  - Neden: Karmasik agaclari ayni dataset icinde karmasik tutar, kok bazli raporlari ve patlamalari zorlastirir.
  - Tespit: parent olup child olmayan kok sayisini saymak; >1 ise coklu kok.
  - Beklenen davranis: Hata veya dataset bolme onerisi; her kok ayri dataset olarak islenmeli.
  - Ornek: ASSY-1000 ve ASSY-2000 ayni tabloda hicbirinin parent'i yok.

## Ornek (JSON benzeri pseudocode)
```json
[
  { "parent": "ASSY-1000", "child": "ASSY-1100", "quantity": 1, "level": 1, "uom": "EA" },
  { "parent": "ASSY-1000", "child": "BRKT-2001", "quantity": 2, "level": 1, "uom": "EA" },
  { "parent": "ASSY-1100", "child": "FAST-3005", "quantity": 4, "level": 2, "uom": "EA", "reference_designators": ["R1", "R2", "R3", "R4"] },
  { "parent": "ASSY-1100", "child": "CABL-4100", "quantity": 1, "level": 2, "uom": "M" }
]
```
