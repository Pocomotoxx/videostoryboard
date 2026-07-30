# Indulás — amit egyszer kell megcsinálni

Ez a leírás annak szól, aki használni fogja a rendszert. Nem kell hozzá programozói
tudás, és terminált sem kell használnod. Öt lépés, nagyjából negyed óra, és utána soha
többé nem kell elővenni.

Amit a rendszer tud: egy ötletből vagy briefből végigvisz a jelenetbontáson, a képes
storyboardon és a videógeneráláson a kész vágásig. Minden szakasz végén megáll, és
megmutatja, mi készült — te döntöd el, hogy mehet tovább vagy újra kell csinálni.
Kreditet csak olyasmire költ, amit előtte jóváhagytál.

---

## 0. Hova kell mindezt beírni

**Ez a legfontosabb rész, olvasd el, mielőtt bármit csinálnál.**

A rendszer **nem a szokásos Claude-beszélgetésben működik.** Az a felület, ahol kérdezni
szoktál Claude-tól, nem tudja megnyitni a gépeden lévő fájlokat, és nem tud videót
készíteni.

Amire szükséged van, az a **Claude asztali alkalmazás**, azon belül pedig a **Code** fül.

1. Töltsd le a Claude alkalmazást Macre a claude.ai oldalról, és telepítsd.
2. Indítsd el, és lépj be a fiókodba.
3. Fent három fül van: **Chat**, **Cowork** és **Code**. Kattints a **Code** fülre.
4. Válaszd ki a mappát, amiben dolgozni fogsz. Készíts egy újat, például „videok" néven —
   ebben fognak létrejönni a munkáid.

Ezután látsz egy beírómezőt, ugyanolyat, mint egy csevegőablakban. **Minden, ami ebben az
útmutatóban szerepel, ebbe a mezőbe megy.**

Kétféle dolgot fogsz beírni:

- **Perjellel kezdődő parancsok**, például `/mcp`. Ezek a rendszernek szólnak. Ha beírsz
  egy perjelet, feljön a lehetséges parancsok listája, abból is választhatsz.
- **Sima mondatok**, például *„csináljunk egy húszmásodperces reklámot"*. Ezek Claude-nak
  szólnak, ahogy megszoktad.

**Terminált nem kell használnod.** Ha valamihez mégis kellene, egyszerűen kérd meg
Claude-ot, hogy csinálja meg — ő futtatja, te csak jóváhagyod.

---

## 1. A rendszer telepítése

Írd be a beírómezőbe ezt a sort, és nyomj entert:

```
/plugin marketplace add Pocomotoxx/videostoryboard
```

Utána ezt:

```
/plugin install higgsfield-storyboard@videostoryboard
```

Végül ezt:

```
/reload-plugins
```

Ennyi.

**Ha később frissítés jön**, két sor hozza le, ebben a sorrendben:

```
/plugin marketplace update videostoryboard
```

```
/plugin update higgsfield-storyboard@videostoryboard
```

A második parancsnál a `@videostoryboard` rész **kötelező** — nélküle azt írja, hogy nem
találja. Frissítés után indítsd újra az alkalmazást.

## 2. A Higgsfield összekötése

Ehhez nem kell parancsot bemásolnod. Írd be a beírómezőbe, sima mondatként:

> Kösd be a Higgsfield MCP-szervert, a hivatalos címen: https://mcp.higgsfield.ai/mcp

Claude megcsinálja, és megkérdezi, jóváhagyod-e — mondd, hogy igen.

Utána írd be ezt:

```
/mcp
```

Válaszd a listából a `higgsfield` sort, és a böngésződben lépj be a Higgsfield-fiókodba,
ahogy szoktál.

**Jelszót senkinek nem kell megadnod.** A belépés a saját böngésződben történik, a
jelszavad nem megy át a beszélgetésen, és a rendszer soha nem is fogja kérni. Ha valami
mégis jelszót vagy API-kulcsot kérne, az hibás — ne add meg.

## 3. A videóösszefűző telepítése

Ez fűzi össze a kész jeleneteket egy videóvá, a saját gépeden, ingyen. Írd be sima
mondatként:

> Telepítsd az ffmpeg programot a gépemre.

Claude végigvezet rajta. Egyszer kell megcsinálni.

## 4. Az első indítás

**A legegyszerűbb: írj be egy perjelet**, és a felugró listából válaszd ki a `video`
nevű bejegyzést. Így nem kell semmit fejből begépelned, és nem lehet elgépelni sem.

Ha inkább beírnád, a parancs ez:

```
/higgsfield-storyboard:video
```

Ha erre azt írja, hogy nincs ilyen, próbáld a rövidebb alakot:

```
/video
```

**Ha egyik sem működik, akkor sincs baj.** Egyszerűen mondd el sima mondatban, mit
szeretnél, és a rendszer magától elindul:
*„Csináljunk egy 20 másodperces reklámot ehhez a termékhez."*

A perjeles parancs csak kényelmi rövidítés — a rendszer felismeri a feladatot a
leírásából is.

Ugyanezt a parancsot használd később is, ha egy félbehagyott munkát folytatnál — a
rendszer megnézi, hol tartottatok, és onnan viszi tovább. Nem kell emlékezned semmire.

Az első alkalommal kideríti magától, milyen csomagod van, mennyi kredited van, és
mennyibe kerülnek az egyes lépések. Ehhez nem kell semmit csinálnod, legfeljebb a végén
megerősítened, hogy amit talált, az stimmel.

**Az első videót érdemes generálás nélkül végigvinni.** Mondd azt, hogy *„előbb nézzük
meg kredit nélkül, mi lenne belőle"* — ilyenkor elkészül a teljes terv, jelenetekre
bontva, az árral együtt, de egy kredit sem megy el. Ha tetszik, onnan indul a gyártás.

---

## Hogyan dolgozz vele

**Mondd el, mit szeretnél, a többit kérdezni fogja.** Nem kell előre kitalálnod a hosszt,
a képarányt vagy a jelenetszámot. Egyszerre egy kérdést tesz fel, és mindig javasol
valamit — ha rábólintasz, megy tovább. „Harminc másodpercet javaslok, függőlegesben,
mert Instagramra megy. Jó lesz?"

**Nem csak videót tud.** Képes posztot és karusszelt is készít, és ez fontos: **egy kép
nagyságrenddel olcsóbb, mint egy videó.** Ha rendszeresen szeretnél posztolni, a képes
tartalom a járható út, a videó pedig a kiemelt anyagoké. Mondd nyugodtan, hogy „ehhez
inkább egy háromlapos karusszelt szeretnék".

**Visszatérő ügyfélnél nem kell újrakezdeni.** Az első munka után elmentheted az ügyfél
stílusát, és onnantól minden további videója ugyanúgy néz ki. Elég annyit mondanod:
„mentsd el ezt a stílust az X ügyfélhez". A betanított szereplőket sem kell újra
megcsinálni, ami komoly megtakarítás.

**A szöveget is megírja.** A kész képhez vagy videóhoz kísérőszöveget, címet és
hashtageket is ír, a kulcsszavaid alapján. Ehhez viszont tudnia kell, mire optimalizálsz
— ha van kulcsszókutatásod, add oda neki.

**A végén mindent egy mappába rak.** Kész videó a kért képarányokban, képek, felirat,
kísérőszöveg, hashtagek. Onnan már csak fel kell töltened.

## Ha rendszeresen posztolnál

Nem kell minden reggel ötletelned. Felírsz előre egy listát a témákból, és a rendszer
naponta elővesz egyet, és előkészíti. Mondd azt, hogy „szeretnék napi előkészítést", és
végigvezet rajta.

Kétféleképpen működhet, és **rákérdez, melyiket szeretnéd**: vagy teljesen ingyen
elkészíti a tervet, és reggel te indítod a gyártást, vagy a képekig is elmegy egy általad
megadott kis kerettel, és reggel már látod is, hogy fog kinézni.

Egy dolgot tudni kell: **ez csak akkor fut le, ha a géped be van kapcsolva.** Lecsukott
laptopon nem történik semmi. Ezért érdemesebb reggeli időpontot választani, mint hajnalit.

A beállítás lépésről lépésre az `UTEMEZES.md` fájlban van. Ne kezdj bele, amíg nem
készítettél legalább egy videót végig kézzel.

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
