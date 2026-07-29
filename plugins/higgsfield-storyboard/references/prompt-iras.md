# Promptírás

Ezt a `shotlist` réteg promptjainak megírása előtt olvasd el. A `shot-grammar.md` a
gépállásokról és a kameramozgásról szól, ez a fájl arról, hogyan áll össze belőlük a
tényleges angol prompt.

## Öt réteg, mindig ebben a sorrendben

Egy videóprompt öt dolgot mond meg: **melyik modell, milyen kamera, ki vagy mi, hogyan néz
ki, mi történik**. A sorrend nem esztétikai kérdés — a modellek az elején lévő szavakra
súlyoznak erősebben, ezért az alany és a cselekvés az első húsz-harminc szóba kerüljön.

A technikai stílusblokk a végére megy, és jelenetről jelenetre **szó szerint ugyanaz**.
Ez tartja össze a látványt, ahogy a `continuity.md` írja.

## Hossz

Rövidebb prompt jobb eredményt ad, mint a hosszú. Kétszáz szó fölött már nem pontosítasz,
hanem hígítasz. Műfajonként érdemes célt tartani: termékbemutatónál harminc-ötven szó,
életképnél negyven-hatvan, drámai jelenetnél hatvan-száz. Ha nem fér bele, az többnyire
azt jelenti, hogy a jelenetet ketté kell vágni.

## Egy jelenet, egy cselekvés

Egy klipben egy fő cselekvés legyen, mellette legfeljebb egy-két másodlagos. Ha többet
kérsz, a modell ingadozni kezd köztük, és az eredmény ugrál. Ugyanez igaz a kameramozgásra:
egy jelenet egy mozgást kap.

Gyors mozgásnál külön trükk, hogy lassítva generálsz, és utómunkában gyorsítod fel — a
modellek időbeli koherenciája gyors mozgásnál esik szét leghamarabb.

## Tiltás helyett állítás

Több modell **nem értelmezi a tagadást**. Ha azt írod, „ne legyen szöveg a képen", az
gyakran pont szöveget eredményez. A megoldás az, hogy a kívánt állapotot írod le:
„tiszta, felirat nélküli háttérfal".

Ez a rendszer egyik legtöbb kárt okozó félreértése, mert a tagadás kézenfekvőnek tűnik.

## Konkrét helyett ne általánost

Az érzelemszavak önmagukban semmit nem mondanak a modellnek. A „szomorú" helyett azt kell
leírni, ami látszik: lesütött tekintet, elernyedt vállak, lassú pislogás, összeszorított
száj. Ugyanez a helyzet a dicsérő jelzőkkel: a „lenyűgöző", „gyönyörű", „epikus" típusú
szavak nem tesznek hozzá semmit, csak helyet foglalnak. Helyettük fizikai leírás kell —
milyen fény, milyen anyag, milyen mozgás.

## Azonosság és mozgás szétválasztása

Visszatérő szereplőnél a prompt két blokkból álljon: az egyik azt írja le, **ki ő**
(arc, haj, ruha, testalkat), a másik azt, **mit csinál**. A kettőt ne keverd egy
mondatba, mert a modell a mozgás leírásából elkezdi átértelmezni a külsőt. Az azonosságot
leíró blokk jelenetről jelenetre változatlan.

## Párbeszéd hossza

Tizenöt másodpercbe nagyjából huszonöt-harminc kimondott szó fér. Ha több van, nem
gyorsítani kell a beszédet, hanem a mondanivaló egy részét viselkedéssé alakítani: amit
egy mozdulat elmond, azt ne mondja el a szereplő is.

## Iteráció: egyszerre egy dolgot változtass

Ha egy generálás nem jó, **egyetlen változót írj át**, és futtasd újra. Ha egyszerre
cserélsz kameramozgást, fényt és promptszöveget, akkor a következő eredményből nem tudod
megállapítani, melyik változtatás segített. Ez kreditben mérhető veszteség, mert a
tanulság vész el, nem csak egy próbálkozás.

## Képarány és hossz nem promptkérdés

A képarány és a klip hossza **felsorolt paraméter**, nem a prompt szövegébe írandó. Az
egyes modellek eltérő értékeket engednek, ezért generálás előtt le kell kérdezni a modell
paramétersémáját. A „széles vásznú", „anamorf" típusú kifejezések a stílusleírásba
tartoznak, nem a kimeneti képarány helyére.

---

*A szerkezeti megközelítés egy része az
[OSideMedia/higgsfield-ai-prompt-skill](https://github.com/OSideMedia/higgsfield-ai-prompt-skill)
MIT-licences projektből származik, saját megfogalmazásban. Lásd a `NOTICE.md` fájlt.*
