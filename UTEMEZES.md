# Napi automatikus előkészítés beállítása

Ez a leírás akkor kell, ha azt szeretnéd, hogy a rendszer **magától elkészítse reggelre a
következő anyag tervét**, és neked már csak át kelljen nézned.

Nem kötelező. A rendszer enélkül is teljesen működik — ez csak kényelmi lehetőség annak,
aki rendszeresen posztol.

Mielőtt belefogsz, legyen kész a telepítés az `ATADAS.md` szerint, és készíts legalább
egy videót végig kézzel. Ha még nem tudod, hogyan viselkedik a rendszer, ne automatizáld.

---

## 1. Mit fog csinálni

Minden reggel, egy általad megadott időpontban a rendszer:

1. Elővesz egy témát abból a listából, amit előre felírtál.
2. Készít belőle briefet, forgatókönyvet és jelenetlistát.
3. Kiszámolja, mennyibe kerülne legyártani.
4. Megáll, és megvárja, hogy reggel átnézd.

**Témát nem talál ki magától.** Ha a listád üres, nem csinál semmit, csak szól. Ez
szándékos: a magától kitalált tartalom általános lesz, és senki nem nézi meg.

**Nem tesz ki semmit sehova.** A közzététel mindig a te döntésed marad.

---

## 2. Két fajta ütemezés van — nekünk a helyi kell

A Claude alkalmazásban kétféle automatikus futás létezik, és ezt fontos nem összekeverni.

**Felhős** — az Anthropic szerverein fut, akkor is, ha a géped ki van kapcsolva. Ez
jól hangzik, de **nekünk nem jó**: a felhőben nincsenek ott a fájljaid, nincs ott a
videóösszefűző program, és a Higgsfield-kapcsolatod sem érhető el onnan.

**Helyi** — a saját gépeden fut, a saját fájljaiddal és a saját Higgsfield-fiókoddal.
**Ez kell nekünk.** Cserébe csak akkor indul el, ha a gép be van kapcsolva, ébren van, és
a Claude alkalmazás nyitva van.

Amikor létrehozod, ügyelj rá, hogy a **Local** lehetőséget válaszd, ne a felhőset.

---

## 3. A témalista elkészítése

Előbb legyen mit feldolgozni.

Indítsd el a rendszert a szokásos módon (`/higgsfield-storyboard:video`), és mondd meg neki:

> Szeretnék napi előkészítést. Készítsd el a témalistát.

Létrehoz egy `temasor.md` nevű fájlt a munkamappádban. Nyisd meg, és írd bele a témákat,
soronként egyet, ebben a formában:

```
- [ ] Raktárlogisztika: három hiba, amit mindenki elkövet
- [ ] Az új termékünk bemutatása
- [ ] Vevői kérdés: meddig tart a szállítás?
```

Ha egy témához tartozik ügyfél vagy formátum, azt is megadhatod:

```
- [ ] Téli akció | ugyfel: kovacskft | tipus: kep
```

Írj fel legalább öt-tíz témát, hogy legyen miből dolgoznia egy-két hétig.

Amit feldolgozott, azt kipipálja, és mögé írja, melyik munka lett belőle — így később
visszakereshető.

---

## 4. Döntsd el, meddig menjen el

Ezt a rendszer meg fogja kérdezni tőled, de jó előre végiggondolni.

**Ingyenes.** Elkészíti a teljes tervet, a jelenetekre bontást, az angol utasításokat és
a költségbecslést. **Egy kredit sem megy el.** Reggel elolvasod, és ha jó, te indítod a
gyártást.

**Képekig is elmegy.** A fentiek, plusz legyártja a képeket egy általad megadott kis
kerettel — így reggel már látod is, hogy fog kinézni. Ehhez meg kell adnod, mennyit
költhet egy futás.

**Kezdd az ingyenessel.** Onnan bármikor tudsz lépni, a már elköltött kredit viszont nem
jön vissza.

A mozgóképes rész egyik módban sem indul el magától. Az a drága lépés, és ott ember kell.

---

## 5. Az ütemezés létrehozása, lépésről lépésre

1. Nyisd meg a Claude alkalmazást, és maradj a **Code** fülön.
2. A bal oldali sávban kattints a **Routines** feliratra.
3. Kattints a **New routine** gombra.
4. Válaszd a **Local** lehetőséget. **Ne a felhőset** — lásd a 2. pontot.
5. **Name**: írd be, hogy `napi-elokeszites`.
6. **Description**: `Elővesz egy témát a listából és előkészíti.`
7. **Instructions**: ide másold be a következő szakasz szövegét.
8. Válaszd ki a **mappát**, amiben a munkáid vannak (ugyanaz, amit a rendszer használ).
9. **Schedule**: válaszd a **Daily** lehetőséget, és állítsd be az időpontot.
10. Mentsd el.

### Milyen időpontot válassz

**Ne hajnalt.** Válassz olyan időpontot, amikor a géped úgyis be van kapcsolva és te is
a közelben vagy — például reggel nyolcat vagy kilencet. Így ha valami elakad, azonnal
látod, és nem másnap derül ki.

---

## 6. A beírandó utasítás

Ezt másold be szó szerint az **Instructions** mezőbe:

```
Napi előkészítés a higgsfield-storyboard rendszerrel.

1. Ellenőrizd, hány óra van. Ha a helyi idő szerint már elmúlt dél, ne csinálj
   semmit: csak írd le, hogy a futás megcsúszott, és állj le. Ez azért kell,
   mert az elmaradt futásokat a gép bekapcsolásakor pótolja, és nem akarunk
   este munkát kezdeni.

2. Futtasd a napi előkészítést a rendszer "napi" parancsával. Ez elővesz egy
   témát a temasor.md listából és létrehozza hozzá a projektet.

3. Vidd végig a folyamatot addig, ameddig a beállított előkészítési mód
   engedi. A mozgóképes réteghez semmilyen körülmények között ne nyúlj.

4. Ha bármi hibába ütközöl, ÁLLJ MEG. Ne próbálkozz újra, ne keress
   kerülőutat, és ne csinálj helyette mást. Írd le egy mondatban, mi történt,
   és fejezd be a futást.

5. Ne tegyél közzé semmit sehol, és ne küldj el semmit senkinek.

6. A végén írj egy rövid összefoglalót: melyik témát dolgoztad fel, mi
   készült el, mennyi kredit ment el, és mi az, amit reggel át kell néznem.
```

Az első pont nem felesleges óvatoskodás: ha a géped egész nap aludt, az alkalmazás
bekapcsoláskor pótolja az elmaradt futást — így egy reggel kilencre időzített feladat
elindulhatna este tizenegykor is.

---

## 7. Az első futtatás — ezt ne hagyd ki

Miután elmentetted, nyisd meg a feladatot, és kattints a **Run now** gombra.

Ez azért fontos, mert az első futásnál engedélyt fog kérni bizonyos műveletekhez.
Minden ilyen kérdésnél válaszd az **„always allow"** (mindig engedélyezd) lehetőséget.
Ha ezt kihagyod, a későbbi automatikus futások **megállnak és várnak rád**, te pedig
csak akkor veszed észre, amikor reggel nem talál kész anyagot.

Nézd végig, mit csinál. Ha valami nem tetszik, most javítsd, ne éles helyzetben.

---

## 8. Ha nem futott le

**Aludt a gép.** Ez a leggyakoribb ok. A helyi feladat csak akkor indul el, ha a
számítógép be van kapcsolva, ébren van, és a Claude alkalmazás fut. A lecsukott laptop
alvó állapotba kerül, akkor is, ha be van dugva.

Ha szeretnéd, hogy ne aludjon el magától, a Claude beállításaiban a **Desktop app →
General** részen van erre kapcsoló. A lecsukott fedél viszont mindenképp elaltatja.

**Be volt zárva az alkalmazás.** A Claude alkalmazásnak nyitva kell lennie. Nem kell
csinálnod benne semmit, csak fusson.

**Engedélyre várt.** Ha az első futásnál nem adtál mindenre engedélyt, a futás megáll és
vár. A bal oldali sávban látod a félbemaradt munkamenetet — nyisd meg és válaszolj.

Minden futás előzménye megmarad: a feladat oldalán látod, mikor futott le, és mikor maradt
el, és azt is, hogy miért.

---

## 9. Kezelés

A feladat oldalán:

- **Run now** — azonnali futtatás, nem kell megvárni a következő időpontot.
- **Status** — átkapcsolható szüneteltetettre, ha egy időre nem kell. Nem törlődik.
- **Edit** — az utasítás, az időpont vagy a mappa módosítása.
- **Delete** — végleges törlés.

Ezt szóban is kérheted bármelyik beszélgetésben: *„szüneteltesd a napi előkészítést"*
vagy *„mutasd meg az ütemezett feladataimat"*.

---

## 10. Amire figyelj

**Nézd át, amit készített.** Az automatikus előkészítés terv, nem kész munka. Ugyanúgy
jóvá kell hagynod, mint amikor te ülsz mellette.

**Ne emeld a keretet, amíg nem szoktad meg.** Ha a képekig menő módot használod, kezdd
nagyon kicsi kerettel. Bővíteni bármikor tudsz.

**Tartsd karban a témalistát.** Ha kifogy, a rendszer nem csinál semmit — csak szól. Ez
nem hiba, hanem így van jól.

**Ne futtasd naponta többször.** A gyakoribb futás nem hoz több elérést, viszont fogyasztja
a keretet. Napi egy anyag előkészítése bőven elég ahhoz, hogy legyen miből válogatnod.
