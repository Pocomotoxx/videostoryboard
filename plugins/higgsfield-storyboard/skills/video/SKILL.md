---
name: video
user-invocable: true
description: Rétegelt, jóváhagyáskapus AI-videó- és képgyártás Higgsfield MCP-vel, brieftől a kész anyagig. Használd ezt a skillt, amikor a felhasználó AI-videót, reklámfilmet, storyboardot, jelenetlistát, promptsorozatot, hirdetési kreatívot, ügyfélnek szánt mozgóképet, közösségimédia-posztot vagy képes karusszelt készít vagy tervez. Akkor is alkalmazd, ha csak annyit mond, hogy "csináljunk egy videót ebből", "kellene egy spot", "bontsuk jelenetekre", "generáljunk hozzá képeket", vagy ha Higgsfieldet, Klinget, Veo-t, Seedance-t, Sora-t említ. Mindig ezen a folyamaton keresztül dolgozz, soha ne generálj videót ad hoc módon.
---

# Higgsfield storyboard futószalag

Rétegelt gyártási folyamat AI-videóhoz. Minden réteg egy jóváhagyási kapu. Kreditet csak jóváhagyott előzményre költünk.

## Környezet

A parancsokat mindig a projekt könyvtárából futtasd, mert a scriptek alapértelmezésben az aktuális könyvtárat tekintik projektnek. A `${CLAUDE_PLUGIN_ROOT}` a plugin telepítési helyére mutat, ezt ne írd át kézzel.

Windowson a `python3` egy nem működő Microsoft Store-alias, ezért ott a `python` parancsot használd a `python3` helyett. Az `assemble.py` futtatásához ffmpeg kell (macOS: `brew install ffmpeg`).

## Alapelv

A generálás nem determinisztikus, a modell nem tudja megítélni a saját eredményét, és minden újrafuttatás pénzbe kerül. Ezért a folyamat nem egy hosszú automatikus lánc, hanem rövid szakaszok sora, mindegyik végén emberi döntéssel. A drága lépés mindig egy már elfogadott olcsó lépésből nő ki.

**Kötelező szabály.** Bármilyen generáló MCP-hívás előtt le kell futtatni:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/project.py" can-spend <node-id> --cost <becsult-ar>
```

Ha ez nem nulla kilépési kóddal tér vissza, a hívás tilos. Nincs kivétel, nincs „gyorsan kipróbálom". Ez a szabály a rendszer lényege.

## Két üzemmód

**Kézi (alapértelmezés).** Minden réteg végén megállsz, és a felhasználó dönt. Ez a biztonságos mód, és ebben nem kell külön engedély a költéshez, csak jóváhagyott előzmény.

**Automata, kreditplafonnal.** A felhasználó megad egy plafont, és a folyamat addig fut magától, ameddig az tart:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/project.py" run start --max-credits 25
```

Ebben a módban három dolog változik. A `can-spend` **kötelezően kéri a becsült árat**, mert e nélkül a plafon nem véd — az árat előbb mérd meg (`get_cost`). A **mozgásréteg alapból tiltott**, mert az a drága lépés; csak `--allow-motion` kapcsolóval indítható. Ha a plafon elfogy, a rendszer **megáll, nem kérdez** — ez szándékos.

Ahol nincs előzetes árbecslés — Marketing Studio, hangcsere, szinkron —, ott az automata mód nem tud dolgozni. Ez így helyes: felügyelet nélkül nem költünk ismeretlen összeget.

Az állapot `run status`-szal nézhető, a futás `run stop`-pal zárható. **Automata futást soha ne indíts magadtól**, csak ha a felhasználó kifejezetten kéri, és a plafont ő adja meg.

### Napi előkészítés témasorból

Ha a felhasználó rendszeres posztolást szeretne, nem naponta kell témát kitalálni: felír egy sort előre, és a rendszer minden nap elővesz egyet.

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/project.py" napi
```

Két mód van — **ingyenes** (brief, jelenetlista, gyártási csomag) és **kezdőkockákig** (szűk plafonnal). **Kérdezd meg, melyiket szeretné**, ne feltételezz. Ha nem tud dönteni, az ingyeneset javasold: onnan bármikor lehet lépni, a már elköltött kredit viszont nem jön vissza.

A részletek a `${CLAUDE_PLUGIN_ROOT}/references/napi-elokeszites.md` fájlban. A lényeg: a rendszer **nem talál ki témát**, és felügyelet nélkül **soha nem indít mozgásréteget**. Hibánál megáll és leírja, mi történt — nem próbálkozik újra.

### Generálás nélküli végigfutás

Ha a felhasználó azt szeretné látni, „mi lenne belőle", anélkül hogy egy kredit is elmenne: vidd végig a 0–2. réteget, majd

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/project.py" package
```

Ez legyárt egy teljes gyártási csomagot — jelenetek, angol promptok, stíluskód, költségbecslés, és hogy mi hiányzik még az indításhoz. Nulla kredit. Sok esetben ez elég is: onnantól már csak jóvá kell hagyni és elindítani.

Bizonytalan felhasználónál **ezzel kezdj**, ne a generálással.

## Rétegek

| # | Réteg | Node | Költség | Mit hagy jóvá az ügyfél |
|---|-------|------|---------|--------------------------|
| 0 | Brief | `brief` | 0 | üzenet, célcsoport, hossz, felhasználási hely, kulcsszavak, referenciák |
| 1 | Kezelés | `treatment` | 0 | dramaturgia, hangnem, ív |
| 2 | Jelenetlista | `shotlist` | 0 | jelenetszám, gépállások, időzítés |
| 3 | Látvány és karakter | `look` | alacsony | stíluskód, paletta, Soul-karakterek |
| 4 | Kezdőkockák | `keyframe:sNNN` | alacsony | kompozíció, folytonosság, képes storyboard |
| 5 | Mozgás | `motion:sNNN` | **magas** | jelenetenkénti mozgókép |
| 6 | Összefűzés | `assembly` | 0 | nyersvágás, ritmus |
| 7 | Hang | `sound` | közepes | zene, narráció, effektek |
| 8 | Utómunka | `finish` | közepes | felirat, felskálázás, képarányváltozatok, posztszöveg |

Reklámjelenetnél a 4. réteg nem generálás, hanem összeállítás: megvan-e a termékkép, ki az avatár, melyik formátum. Ingyenes, de a jóváhagyása ugyanúgy kapu.

A 0–2. réteg ingyenes. Ha itt esik szét a projekt, semmit nem vesztettél. A 4. réteg állóképei olcsók, és pont ott derül ki, ha egy beállítás nem működik. Az 5. réteg a drága, ezért oda kizárólag jóváhagyott kezdőkockából lépünk be.

## Elévülés

A `project.py` build-rendszerként kezeli a projektet. Minden node tárolja a bemeneteinek ujjlenyomatát. Ha egy réteget módosítasz, az összes ráépülő node automatikusan `stale` állapotba kerül, és újra jóváhagyást igényel. Ha az ügyfél a hetedik jelenet kezdőkockáját visszadobja, a hozzá tartozó mozgókép és az összefűzés is elavul, az első hat jelenet viszont érintetlen marad. Soha ne kerüld meg ezt kézi státuszírással.

## Munkamenet

### Referenciavideók a briefhez

Ha a felhasználó egy meglévő videóra hivatkozik — versenytárs hirdetése, „ilyet szeretnék" —, azt érdemes ténylegesen megnézni, nem a leírásából dolgozni. Helyi fájlból a `frames.py` kockákat ment ki, amiket `Read` hívással végignézel.

Webes videóhoz külön eszköz kell, ami letölti és a feliratot is kinyeri. Erre a `claude-video` nevű plugin való (`/watch` paranccsal), ami külön telepíthető. **Nem előfeltétel** — ha nincs meg, kérd meg a felhasználót, hogy mondja el vagy mutassa meg, mi tetszik neki a referenciában.

Amit a referenciából kinyersz, az a brief része: milyen a nyitóhorog, milyen hosszúak a vágások, milyen a hangnem. A képi világ szó szerinti másolása viszont jogi kockázat, ügyfélmunkában kerüld — erről a `continuity.md` szól.

### Így indulj, minden alkalommal

**Az igazság a fájlokban van, nem a beszélgetésben.** Soha ne a korábbi üzenetekből próbáld kitalálni, hol tartotok — kérdezd meg az állapotot.

Első lépésként, kivétel nélkül:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/project.py" config show
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/project.py" status
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/project.py" next
```

Ha a `config show` bármit hiányol, előbb a telepítés jön (`${CLAUDE_PLUGIN_ROOT}/references/telepites.md`). Ha minden megvan, akkor is **ellenőrizd az egyenleget** a `balance` eszközzel: ha a csomag vagy a havi keret eltér a mentettől, a felhasználó csomagot váltott, és frissíteni kell. Csomagot soha ne feltételezz. Ha nincs projekt az aktuális könyvtárban, akkor új munka indul. Minden más esetben folytatás — a `next` megmondja, mi a következő lépés.

Ezután **egy mondatban** foglald össze a felhasználónak, hol tartotok, és tedd fel a következő kérdést. Ne listázd ki az összes lehetőséget.

### Egyszerre egy kérdés, javaslattal

Ez a rendszer legfontosabb kommunikációs szabálya. A felhasználó marketinges, nem rendszergazda: ne kérdéssorokat kapjon, hanem egy kérdést, amire elég annyit mondania, hogy jó.

Rosszul: „Milyen hosszú legyen, milyen képarányban, hány jelenettel, milyen hangnemben, és melyik modellel dolgozzunk?"

Jól: „Harminc másodpercet javaslok, függőlegesben, mert Instagramra megy. Jó lesz?"

Mindig **legyen javaslatod**, és mondd meg, miért azt javaslod. Ha a felhasználó nem válaszol érdemben, hanem rábólint, akkor haladj tovább — a javaslat a te felelősséged.

Ha menet közben olyasmi derül ki, ami a korábbi döntést érinti, **kérdezz vissza**, ne írd felül csendben.

### Az ingyenes rétegeken haladj folyamatosan

A brief, a kezelés és a jelenetlista nem kerül kreditbe. Ott ne kérj teljes értékű jóváhagyást minden lépésnél, mert az lassú és feleslegesen hivatalos.

Ehelyett: minden réteg végén **mutasd meg az eredményt, és kérdezz vissza egy könnyű kérdéssel** — „ez a felépítés jó, vagy vigyünk máshova?". Ha rábólint, `approve`, és mész tovább. Nem vársz külön engedélyt a következő réteg megkezdéséhez.

A jelenetlistánál azért állj meg alaposabban, mert onnantól a döntések pénzbe kerülnek: a jelenetszám és a hosszak határozzák meg a költséget.

### A kredites rétegeknél kemény megállás

A látvány, a kezdőkockák és a mozgás előtt **teljes megállás**: mutasd a becslést, mondd meg, mi következik, és várj kifejezett igenre. Itt a rábólintás nem elég, kérdezz rá a költségre is.

### Indulás

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/project.py" init "ugyfel-projektnev"
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/project.py" status
```

Ha félbeszakadt munkamenetet folytatsz, mindig `status` és `next` hívással kezdj. Az igazság a `project.json`-ban van, nem a beszélgetésben.

Az új projekt a telepítéskor megadott eszközneveket és árakat örökli. Ha egy adott munkánál el kell térni ettől — mondjuk más videómodellel dolgoztok —, a projekten belül felülírható, a gépszintű beállítás érintetlenül hagyásával:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/project.py" set-tool image_to_video "<eszköznév>"
```

### Rétegenkénti haladás

Mindig a `next` mondja meg, mi jön. Egy réteg befejezése után **állj meg, és kérj jóváhagyást**. Ne haladj tovább magadtól, akkor sem, ha nyilvánvalónak tűnik a folytatás.

### Nézd meg te is, mielőtt megmutatod

Az állóképeket `Read` hívással közvetlenül meg tudod nézni. A **mozgóképeket nem** — abból előbb képkockákat kell kimenteni:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/frames.py" shots/s003.mp4 --db 6
```

A kimentett kockákat nézd végig `Read` hívással, és vesd össze a `${CLAUDE_PLUGIN_ROOT}/references/hibamintak.md` listájával: stimmel-e a szereplő, a kéz, a ruha, nincs-e olvashatatlan szöveg a háttérben, azt csinálja-e, amit a prompt kért.

**Ha nyilvánvaló hibát látsz, ne tedd a felhasználó elé jóváhagyásra.** Mondd meg, mit látsz, és javasolj javítást. A jóváhagyás az ő döntése, de az ő idejét ne olyasmire fordítsd, amit magad is kiszűrsz.

Ez nem helyettesíti az emberi ellenőrzést. A folytonosságot, a márkahangot és azt, hogy az anyag jó-e az ügyfélnek, továbbra is ember dönti el.

### Hogyan kérj jóváhagyást

Ne ömlesztve tedd le az egészet azzal, hogy „megfelel?". Vedd végig **jelenetenként, egyesével**, és minden jelenetnél ugyanazt az öt lehetőséget kínáld fel:

1. **Elfogadom** — mehet a következő
2. **Igazítás** — apró módosítás a jelenet paraméterein, újragenerálás nélkül
3. **Újragenerálás** — a felhasználó megmondja, mi a baj, és abból lesz a javítás alapja
4. **Megjelölöm** — később térünk vissza rá, most menjünk tovább
5. **Kihagyom** — ez a jelenet kimarad a videóból

A negyedik és az ötödik azért fontos, hogy a felhasználó ne akadjon el egyetlen problémás jelenetnél. A megjelölteket a végén vedd elő újra, mielőtt a következő rétegbe lépnétek.

Amikor újragenerálást kér, az indokot **szó szerint írd bele** az elutasításba, mert abból dolgozol a következő körben. A „nem tetszik" nem indok — kérdezz vissza, mi konkrétan.

Jóváhagyás rögzítése:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/project.py" approve keyframe:s003
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/project.py" reject keyframe:s003 --note "a kabát gombos lett, sima kell"
```

### Jelenetlista

A `shotlist` réteg a `${CLAUDE_PLUGIN_ROOT}/templates/storyboard.example.json` szerinti szerkezetet tölti fel. Három referenciát olvass el hozzá: a `${CLAUDE_PLUGIN_ROOT}/references/shot-grammar.md` a gépállásokról és kameramozgásokról szól, a `${CLAUDE_PLUGIN_ROOT}/references/prompt-iras.md` arról, hogyan áll össze belőlük a tényleges angol prompt, a `${CLAUDE_PLUGIN_ROOT}/references/nyitohook.md` pedig a nyitójelenetről — ez utóbbi akkor számít, ha a videó közösségi médiába vagy hirdetésnek készül.

**Ha erős ritmusú zene lesz alatta, a zenét itt már ismerni kell.** A jelenethosszak generálási paraméterek, utólag nem nyújthatók — vagyis ha a vágásoknak ütemre kell esniük, azt a jelenetlistában kell eldönteni, nem az összefűzésnél. A `${CLAUDE_PLUGIN_ROOT}/references/zene-es-ritmus.md` mondja meg, hogyan, a `${CLAUDE_PLUGIN_ROOT}/scripts/beatgrid.py` pedig kiszámolja az ütemre eső hosszakat. Ha még nincs zene, a tartalom ritmusa szerint ossz, és ne próbálj kockapontos illesztést.

Két fontos megkötés. A klipek legfeljebb tizenöt másodpercesek, tehát ennél hosszabb jelenet nem létezik, bontsd szét. A `prompt_en` mező **mindig angol**, a `leiras` mező magyar, mert azt az ügyfél olvassa.

A jelenetlista elkészülte után, még a jóváhagyás előtt futtasd le az ellenőrzést:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/project.py" check-shots
```

Ez kiszűri a túl hosszú klipeket, a hiányzó promptot és a reklámjelenetek formátumhibáit. Olcsóbb itt megtalálni őket, mint egy visszautasított generálás árán.

### Háromféle tétel: filmes, reklám, kép

A tételek `tipus` mezője háromféle lehet.

A **filmes** jelenet az alapértelmezés: generált kezdőkockából készül mozgókép, szabad prompttal. Ez való többjelenetes történethez, visszatérő szereplőkkel.

A **reklám** jelenet a Marketing Studio ága: feltöltött termékkép, egy avatár és egy előre adott hirdetésformátum. Ez való rövid közösségimédia-hirdetéshez, termékbemutatóhoz, kicsomagoláshoz, virtuális próbához — és ez az, amivel egy avatár beszélni tud egy feltöltött termékről.

**Ha a feladat reklám, a `${CLAUDE_PLUGIN_ROOT}/references/reklam-marketing-studio.md` fájlt kötelező elolvasni**, mielőtt jelenetlistát írsz. Más korlátok érvényesek rá: legfeljebb 15 másodperc, pontosan egy avatár, kötelező termékkép, egy helyszín, zárt listás hook. És ami a költségkapunk szempontjából a legfontosabb: **erre az ágra a platform nem ad előzetes árbecslést**, a költség csak utólag olvasható ki. Ezt mondd meg a felhasználónak, mielőtt elindítja az elsőt.

A **kép** tétel nem videó: álló kép közösségimédia-poszthoz, karusszelhez vagy hirdetéshez. Itt a kezdőkocka maga a végtermék, nem készül belőle mozgókép, és tisztán képes munkánál az összefűzés meg a hang réteg meg sem jelenik. Részletek: `${CLAUDE_PLUGIN_ROOT}/references/kep-poszt.md`.

**A kép nagyságrenddel olcsóbb a videónál.** Ha a felhasználó rendszeres, napi jelenlétet szeretne, a kép a járható út, a videó a kiemelt tartalomé. Ha valaki napi videót emleget korlátos kerettel, ezt mondd el neki, mielőtt belevágtok.

A típusokat ne keverd egy tételen belül. Egy projektben viszont megférnek egymás mellett — például egy videó és a hozzá tartozó karusszel.

### Visszatérő ügyfél: profil

Ha ugyanannak az ügyfélnek többedik videója készül, a látványt **ne találd ki újra**. Az első munka jóváhagyott látványából profil készíthető, amit minden további munka örököl:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/project.py" ugyfel add <ugyfelnev> --forras <projektkonyvtar>
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/project.py" ugyfel list
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/project.py" init "uj-munka" --ugyfel <ugyfelnev>
```

A profilba **csak jóváhagyott látvány kerülhet** — a script ezt ellenőrzi. Ez a lényeg: a stílust egyszer egy ember hagyta jóvá, onnantól a rendszer nem dönt, hanem ismétel.

Az új projekt a stíluskóddal, a palettával, az arculattal és a **betanított szereplők azonosítóival** indul. Ez utóbbi kredites megtakarítás: a szereplőt nem kell újratanítani.

A profil **bemásolódik** a projektbe, nem hivatkozásként marad. Ha az ügyfél később arculatot vált, a régi munkák érintetlenek maradnak — ugyanaz az elv, mint a kreditáraknál.

Amikor profillal indul egy munka, a `look` réteg gyakorlatilag készen van. Ettől még **kérdezz rá**: „ugyanaz a stílus, mint az eddigieknél, jó?" — mert lehet, hogy ez a videó másik terméknek vagy másik célcsoportnak szól.

Ha az ügyfél stílusa változik, a profilt írd felül (`--felulir`) egy újabb jóváhagyott projektből.

### Arculat

A `look.brand` blokkban rögzítsd az ügyfél arculatát: elsődleges szín, szövegszín, betűtípus, logó. Ez nem a generálásnak szól — az AI-modellek a márkaszínt sem tartják meg megbízhatóan —, hanem az utómunkának: a záróképnek, a feliratoknak és a szöveges rátéteknek. Így több videón át egységes marad a megjelenés.

A **logót soha ne generáltasd**, hanem utómunkában helyezd rá. Ez a `continuity.md` szabálya, és arculatnál különösen érvényes: a torzított logó az egyetlen hiba, amit az ügyfél biztosan kiszúr.

### Folytonosság

Karakter- és stílusfolytonosságról a `${CLAUDE_PLUGIN_ROOT}/references/continuity.md` szól. Ezt a `look` réteg előtt kötelező elolvasni. Konzisztens szereplő nélkül a többjelenetes videó használhatatlan, és ezen a ponton szokott elhasalni a munka.

### Költség

Generálás előtt mindig:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/project.py" estimate
```

A becslés megmutatja azt is, hogy a projekt a havi keret hány százalékát viszi el, és figyelmeztet, ha a kreditárak nincsenek kalibrálva. Kalibrálatlan becslést ügyfélnek ne mutass. A becslést mutasd meg a felhasználónak, mielőtt az 5. rétegbe lépnél. Az elköltött kreditet a `project.py spend` rögzíti, az `report` pedig kiírja a projekt tényleges költségét, ami ügyfélszámlázáshoz kell.

### Összefűzés

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/project.py" check-assembly
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/assemble.py" --project . --aspect 16:9
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/assemble.py" --project . --aspect 9:16
```

Az összefűzés helyben fut ffmpeggel, nem az MCP-n keresztül. A `check-assembly` ellenőrzi, hogy minden jelenet jóváhagyott és letöltött állapotban van-e.

**Felirat és hangerő.** A felirat ráégethető a képre egy SRT-fájlból, a `--subtitles` kapcsolóval — a méretét a script a képarányhoz igazítja, tehát 16:9-ben és 9:16-ban is arányos marad. A hangerőt alapból egységesíti is: enélkül a jelenetek hangereje ugrál, mert minden klip külön generálásból származik. Ezt a `--no-loudnorm` kapcsolja ki, ha valamiért nem kell.

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/assemble.py" --project . --aspect 9:16 --subtitles felirat.srt --music zene.m4a
```

**Képarányváltásnál figyelj.** Az `assemble.py` egyszerűen levágja a kép szélét, ami 16:9-ből 9:16-ba váltva fontos tartalmat vághat le — feliratot, a szereplő fejét, a terméket. Ha ez fenyeget, a platform tartalomtudatos képarányváltó munkafolyamata a jobb megoldás, lásd `${CLAUDE_PLUGIN_ROOT}/references/cli.md`. Az kreditbe kerül, a helyi vágás nem, ezért előbb nézd meg a helyi eredményt, és csak akkor válts, ha tényleg romlott.

### Hang

A narrációhoz beszédszintézis használható, kiválasztott hanggal — a hangok listája lekérdezhető, kitalálni nem lehet. Kész videó idegen nyelvű változatához külön szinkronizáló munkafolyamat van, a hang cseréjéhez pedig hangcserélő. Mindkettő a `${CLAUDE_PLUGIN_ROOT}/references/cli.md`-ben szerepel.

Ezek költsége **nem becsülhető előre**, ugyanúgy, mint a reklámágé. Szólj róla, mielőtt elindítod.

### Ha egy generálás nem sikerült

Ne futtasd újra automatikusan. Mutasd meg az eredményt, és a `${CLAUDE_PLUGIN_ROOT}/references/hibamintak.md` segítségével derítsd ki, melyik rétegen csúszott el — az alanynál, a cselekvésnél, a kameránál vagy a stílusnál. A javításnál **egyszerre egy dolgot változtass**, különben a következő eredményből nem derül ki, mi segített, és a kredit tanulság nélkül fogy.

### Kísérőszöveg a kész anyaghoz

A kép vagy a videó önmagában még nem poszt. A `finish` réteg része a **posztszöveg** is: kísérőszöveg, cím ahol van, hashtagek és az AI-jelölés. A szabályok a `${CLAUDE_PLUGIN_ROOT}/references/poszt-szoveg.md` fájlban vannak, olvasd el írás előtt.

Két dolgot emelj ki magadnak. Az **első sor önmagában is működjön**, mert a felületek levágják a szöveget — ez felülír minden szövegírási keretrendszert. És a **kulcsszavakat ne találd ki**: a briefben kell szerepelniük, és ha nincsenek benne, kérdezd meg, mire optimalizáltok.

A szöveg ugyanabból a briefből nő ki, mint maga a videó. Ne utólag aggasd rá, és ne ígérj benne olyat, amit az anyag nem mutat meg.

### A leszállítási csomag összeállítása

Amikor minden elkészült, állítsd össze a csomagot:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/project.py" delivery
```

Ez egy helyre gyűjti a kért képarányú vágásokat és a képeket, vázat készít a posztszöveghez, és **felsorolja, mi hiányzik még** — hiányzó képarány, meg nem generált kép, kitöltetlen szövegrész, hiányzó AI-jelölés. Amíg hiányzik valami, nem nulla kóddal tér vissza.

A posztszöveget te írod meg a vázba, a `${CLAUDE_PLUGIN_ROOT}/references/poszt-szoveg.md` szerint — a script csak összeszedi és ellenőrzi, nem ír helyetted.

Futtasd le újra, amíg tisztán le nem fut. Utána jön a végső ellenőrzés.

### Végső ellenőrzés leszállítás előtt

A `finish` réteg után, még az átadás előtt menj végig a `${CLAUDE_PLUGIN_ROOT}/references/vegso-ellenorzes.md` hét pontján. Ez nem ugyanaz, mint a rétegek jóváhagyása: ott jelenetenként néztétek, itt a **kész egészet** kell megnézni, és összevetni az eredeti briefel.

Ne javíts magadtól ebben a szakaszban. Sorold fel, amit találtál, három súlyossági csoportban, és a felhasználó döntsön. A leszállítás előtti kapkodó javítás új hibát visz be.

## Amit soha ne csinálj

Ne generálj videót jóvá nem hagyott kezdőkockából. Ne írd át kézzel a `project.json` státuszmezőit. Ne ígérj a felhasználónak gombnyomásra kész filmet. Ne fuss neki újra automatikusan egy sikertelen generálásnak, hanem mutasd meg az eredményt és kérdezd meg, mit rontott el. Ne dolgozz több jeleneten párhuzamosan az 5. rétegben, amíg az első kettő minősége nincs elfogadva, mert a hibás stíluskód így tízszeres költséggel sokszorozódik.

## Ügyfélkommunikáció

Amit ígérni lehet, az a jóváhagyható képes storyboard rövid határidőre, onnan a kész anyag néhány nap alatt, előre kalkulált költséggel és meghatározott számú finomító körrel. Amit nem szabad ígérni, az a korlátlan javítás és az azonnali kész film.

Magyar nyelvű szöveg írásakor alkalmazd a `magyar-helyesiras` és a `magyar-termeszetes-stilus` skilleket.
