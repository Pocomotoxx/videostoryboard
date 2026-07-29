# Avatáros és termékreklám: a Marketing Studio ág

Ezt akkor olvasd el, ha a feladat rövid hirdetés: valaki beszél egy termékről, kicsomagolja,
kipróbálja, vagy a termék önmagában mozog látványosan. Ez **nem** a kilencrétegű filmes
futószalag, hanem egy rövidebb ág, más korlátokkal.

## Mikor ez kell, és mikor nem

A Marketing Studio egy hirdetésgyártó felület, ami saját konvenciók szerint dolgozik: te
megadod a terméket, az avatárt és a formátumot, ő intézi a kameranyelvet és a ritmust.
Cserébe kötöttebb, mint a szabad prompt.

Akkor válaszd ezt, ha a végeredmény rövid közösségimédia-hirdetés vagy termékbemutató. Ha
viszont többjelenetes, folytonos történet kell, visszatérő szereplőkkel, akkor a filmes ág
való rá — a kettőt ne keverd egy jeleneten belül.

## Amit tudni kell, mielőtt bármit ígérsz

**Legfeljebb 15 másodperc egy klip.** Ez kemény korlát. Hosszabb hirdetést több klipből
kell összerakni, és helyben összefűzni.

**Pontosan egy avatár szerepelhet.** Nem nulla, nem kettő. Ha üresen hagyod, a rendszer
minden generálásnál más arcot tesz bele, ami több klipnél használhatatlan. Kétszereplős
jelenethez a másodikat referenciaképként kell megadni, de az arcazonosság ilyenkor
bizonytalan.

**Termékkép kötelező.** Ez a bemenet, nem generált kép. Ezért is olcsóbb ez az ág: a
terméket nem kell kitalálni, hanem adott.

**Egy helyszín egy klipben.** Nincs osztott képernyő, nincs „első nap – hetedik nap"
szerkezet egyetlen generálásban. Több helyszínhez több klip kell.

**Nincs előzetes árbecslés.** A `get_cost` erre a modellre nem működik. A tényleges
költséget utólag, a `transactions` eszközzel lehet leolvasni. Ezt mondd meg a felhasználónak,
mielőtt elindítja az elsőt.

**Amit egyáltalán ne próbálj**: beszélő termék vagy más nem emberi arc szájmozgása, több
szereplő összehangolt párbeszéde vágásokon át. Ezek megbízhatatlanok. Ha az ötlethez
tényleg ez kell, a filmes ág és egy erre való videómodell a helyes út.

## A kilenc formátum

| Formátum | Azonosító | Hook-lista | Mire való |
|---|---|---|---|
| UGC | `ugc` | van | Telefonnal felvett hatású, egyszálas videó emberrel és termékkel |
| Oktató | `tutorial` | van | Lépésről lépésre bemutató, recept, használati útmutató |
| Kicsomagolás | `ugc_unboxing` | van | Csomagolásból előkerülő termék, kézzel, tapintható közelikkel |
| Hyper Motion | `hyper_motion` | nincs | Látványos termékmozgás: kiöntés, pörgés, csobbanás. **Avatár nélkül is megy** |
| Termékértékelés | `product_review` | van | Beszélő fej kézben tartott termékkel, tárgyilagos hangnemben |
| TV-spot | `tv_spot` | nincs | Mozis, letisztult reklámfilm, felépített ívvel |
| Wild Card | `wild_card` | nincs | Szürreális, szabályt szegő kreatív ötletek |
| Virtuális próba, hétköznapi | `ugc_virtual_try_on` | van | Ruhapróba tükrös vagy szelfis beállításban |
| Virtuális próba, stúdiós | `virtual_try_on` | nincs | Divatkatalógus-hatású próba, tiszta háttérrel |

Két buktató. A stúdiós próba azonosítója `virtual_try_on`, nem `pro_virtual_try_on` — ez
nem következik a nevéből. A TV-spot alapból tesz a végére egy különálló termékképet;
ha ez nem kell, kifejezetten meg kell tiltani a promptban.

## A tényleges paraméterek

A hivatalos dokumentáció szerint a modell azonosítója `marketing_studio_video`, és a
formátum nem külön mezőben, hanem a **`mode`** paraméterben megy át (alapértéke `ugc`).
A klip hossza `duration`, alapértéke 15 másodperc. A felbontás `480p`, `720p` vagy
`1080p` lehet, alapból `720p` — függőleges hirdetéshez ezt érdemes feljebb venni.
A képarány felsorolt érték, a `9:16` is köztük van.

Egy ütközés, amit érdemes tudni: ha korábbi hirdetésre hivatkozol
(`ad_reference_id`), akkor hookot és helyszínt **nem** adhatsz meg mellé. A termék
megadásának két módja sem kombinálható egymással.

Ezek a paraméterek is változhatnak, ezért generálás előtt a modell sémáját akkor is
kérdezd le, ha ez a fájl mást mond. A séma az igazság.

## Hook és helyszín

Öt formátumnál választható a nyitóhook és a helyszín, de **csak zárt listából**: a
lehetséges értékeket le kell kérdezni, és a kapott azonosítót átadni. Kitalált azonosítót a
rendszer visszautasít. Ha nem kell hook, egyszerűen nem adsz meg egyet sem.

## Az avatár háromféle lehet

**Beépített** — a platform saját avatárkönyvtárából, negyven körüli arc. Akkor jó, ha
mindegy, ki mondja, csak gyorsan legyen meg.

**Feltöltött** — a felhasználó saját fotójából, például az ügyfél arca vagy egy márkanagykövet.
Valós személy szerepeltetéséhez írásos hozzájárulás kell, ezt kérdezd meg.

**Szöveggel generált** — leírásból készül az arc, például „ötvenes éveiben járó nő, rövid
ősz haj". Akkor hasznos, ha adott célcsoportra kell arcot választani, és nincs valós modell.

## Hogyan illeszkedik a rétegrendszerbe

A reklámjelenetnek is van kezdőkocka és mozgás rétege, csak mást jelentenek.

A **kezdőkocka réteg** itt nem generálás, hanem összeállítás: megvan-e a termékkép, ki az
avatár, melyik formátum, melyik hook. Ez ingyenes, és a jóváhagyása pont ugyanolyan kapu,
mint a filmes ágon — ezért kell.

A **mozgás réteg** a tényleges hirdetésrenderelés. Ez kerül kreditbe, és ez az, aminek az
árát csak utólag látod.

A jelenetlistában a `tipus` mező különbözteti meg a kétféle jelenetet. A szerkezetet a
`templates/storyboard.example.json` mutatja, az ellenőrzést pedig a
`project.py check-shots` végzi el — ezt futtasd le, mielőtt bármit generálnál.

---

*A platform működésére vonatkozó ismeret egy része az
[OSideMedia/higgsfield-ai-prompt-skill](https://github.com/OSideMedia/higgsfield-ai-prompt-skill)
MIT-licences projektből származik, saját megfogalmazásban. Lásd a `NOTICE.md` fájlt.*
