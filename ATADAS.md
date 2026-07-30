# Indulás — amit egyszer kell megcsinálni

Ez a leírás annak szól, aki használni fogja a rendszert. Nem kell hozzá programozói
tudás. Négy lépés, nagyjából negyed óra, és utána soha többé nem kell elővenni.

Amit a rendszer tud: egy ötletből vagy briefből végigvisz a jelenetbontáson, a képes
storyboardon és a videógeneráláson a kész vágásig. Minden szakasz végén megáll, és
megmutatja, mi készült — te döntöd el, hogy mehet tovább vagy újra kell csinálni.
Kreditet csak olyasmire költ, amit előtte jóváhagytál.

---

## 1. A rendszer telepítése

Claude Code-ban írd be ezt a két sort, egyesével:

```
/plugin marketplace add Pocomotoxx/videostoryboard
```

```
/plugin install higgsfield-storyboard@videostoryboard
```

Végül `/reload-plugins`, és kész. Ha frissítés jön, ugyanitt a
`/plugin marketplace update` és a `/plugin update higgsfield-storyboard` hozza le.

## 2. A Higgsfield összekötése

Ez az egyetlen lépés, ami kicsit technikásnak néz ki, de csak egy sor:

```
claude mcp add --transport http --scope user higgsfield https://mcp.higgsfield.ai/mcp
```

Utána írd be, hogy `/mcp`, válaszd a `higgsfield` sort, és a böngésződben lépj be a
Higgsfield-fiókodba, ahogy szoktál.

**Jelszót senkinek nem kell megadnod.** A belépés a saját böngésződben történik, a
jelszavad nem megy át a beszélgetésen, és a rendszer soha nem is fogja kérni. Ha valami
mégis jelszót vagy API-kulcsot kérne, az hibás — ne add meg.

## 3. Az ffmpeg telepítése

Ez fűzi össze a kész jeleneteket egy videóvá, a saját gépeden, ingyen. Macen a
Terminálban:

```
brew install ffmpeg
```

Ha a `brew` parancsot nem ismeri a gép, kérdezd meg Claude-ot, ő végigvezet.

## 4. Az első indítás

Írd be ezt:

```
/higgsfield-storyboard:video
```

Ezután már csak annyi a dolgod, hogy elmondod, mit szeretnél. Például:
*„Csináljunk egy 20 másodperces reklámot ehhez a termékhez."*

Ugyanezt a parancsot használd később is, ha egy félbehagyott munkát folytatnál — a
rendszer megnézi, hol tartottatok, és onnan viszi tovább. Nem kell emlékezned semmire.

Az első alkalommal kideríti magától, milyen csomagod van, mennyi kredited van, és
mennyibe kerülnek az egyes lépések. Ehhez nem kell semmit csinálnod, legfeljebb a végén
megerősítened, hogy amit talált, az stimmel.

**Az első videót érdemes generálás nélkül végigvinni.** Mondd azt, hogy *„előbb nézzük
meg kredit nélkül, mi lenne belőle"* — ilyenkor elkészül a teljes terv, jelenetekre
bontva, az árral együtt, de egy kredit sem megy el. Ha tetszik, onnan indul a gyártás.

---

## Amit nem kell megcsinálnod

Van a Higgsfieldnek egy parancssori programja is. **Neked nem kell telepítened**, és
parancsokat sem kell gépelned — a rendszer nélküle is teljesen működik. Ha Claude
felajánlja, nyugodtan mondd, hogy nem kell.

## Amit érdemes tudni az első héten

**Nézd meg, honnan fogy a kredit.** Az első generálás után ellenőrizd a fiókodban, hogy
az előfizetésed havi kreditjéből ment-e le. Ha valami mást látsz, szólj — akkor a
rendszer rossz keretet számol.

**A videó több darabból áll össze.** Egy klip legfeljebb 15 másodperc lehet, ezért egy
hosszabb videó több jelenetből épül fel, amiket a gépeden fűzünk össze. Ez ingyenes és
akárhányszor ismételhető.

**A képes storyboardnál állj meg alaposan.** Az állóképek olcsók, a mozgóképek drágák.
Ha egy arc vagy egy beállítás nem stimmel, ott mondd meg, ne később — a mozgásnál
ugyanaz a hiba sokszoros áron jön vissza.

**Ne indíts sok jelenetet egyszerre.** Előbb két jelenet minőségét fogadd el, és csak
utána a többit. Ha a stílus rossz, egyszerre tíz jeleneten fizeted meg.

## Ha valami nem megy

Mondd el Claude-nak, mit láttál. A rendszerbe be van építve, mit kell ilyenkor
végignézni, és a javításnál egyszerre egy dolgot változtat — így kiderül, mi segített,
és nem fogy feleslegesen a kredit.
