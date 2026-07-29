---
name: higgsfield-storyboard
description: Rétegelt, jóváhagyáskapus AI-videógyártás Higgsfield MCP-vel, brieftől a kész vágásig. Használd ezt a skillt, amikor a felhasználó AI-videót, reklámfilmet, storyboardot, jelenetlistát, promptsorozatot, hirdetési kreatívot vagy ügyfélnek szánt mozgóképet készít vagy tervez. Akkor is alkalmazd, ha csak annyit mond, hogy "csináljunk egy videót ebből", "kellene egy spot", "bontsuk jelenetekre", "generáljunk hozzá képeket", vagy ha Higgsfieldet, Klinget, Veo-t, Seedance-t, Sora-t említ. Mindig ezen a folyamaton keresztül dolgozz, soha ne generálj videót ad hoc módon.
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
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/project.py" can-spend <node-id>
```

Ha ez nem nulla kilépési kóddal tér vissza, a hívás tilos. Nincs kivétel, nincs „gyorsan kipróbálom". Ez a szabály a rendszer lényege.

## Rétegek

| # | Réteg | Node | Költség | Mit hagy jóvá az ügyfél |
|---|-------|------|---------|--------------------------|
| 0 | Brief | `brief` | 0 | üzenet, célcsoport, hossz, felhasználási hely |
| 1 | Kezelés | `treatment` | 0 | dramaturgia, hangnem, ív |
| 2 | Jelenetlista | `shotlist` | 0 | jelenetszám, gépállások, időzítés |
| 3 | Látvány és karakter | `look` | alacsony | stíluskód, paletta, Soul-karakterek |
| 4 | Kezdőkockák | `keyframe:sNNN` | alacsony | kompozíció, folytonosság, képes storyboard |
| 5 | Mozgás | `motion:sNNN` | **magas** | jelenetenkénti mozgókép |
| 6 | Összefűzés | `assembly` | 0 | nyersvágás, ritmus |
| 7 | Hang | `sound` | közepes | zene, narráció, effektek |
| 8 | Utómunka | `finish` | közepes | felirat, felskálázás, képarányváltozatok |

Reklámjelenetnél a 4. réteg nem generálás, hanem összeállítás: megvan-e a termékkép, ki az avatár, melyik formátum. Ingyenes, de a jóváhagyása ugyanúgy kapu.

A 0–2. réteg ingyenes. Ha itt esik szét a projekt, semmit nem vesztettél. A 4. réteg állóképei olcsók, és pont ott derül ki, ha egy beállítás nem működik. Az 5. réteg a drága, ezért oda kizárólag jóváhagyott kezdőkockából lépünk be.

## Elévülés

A `project.py` build-rendszerként kezeli a projektet. Minden node tárolja a bemeneteinek ujjlenyomatát. Ha egy réteget módosítasz, az összes ráépülő node automatikusan `stale` állapotba kerül, és újra jóváhagyást igényel. Ha az ügyfél a hetedik jelenet kezdőkockáját visszadobja, a hozzá tartozó mozgókép és az összefűzés is elavul, az első hat jelenet viszont érintetlen marad. Soha ne kerüld meg ezt kézi státuszírással.

## Munkamenet

### Első indulás: a Higgsfield MCP bekötése

A generáló rétegek a Higgsfield hivatalos felhős MCP-szerverén keresztül működnek. Ha a felhasználónál ez még nincs bekötve, ez az első lépés, minden más előtt.

```bash
claude mcp add --transport http --scope user higgsfield https://mcp.higgsfield.ai/mcp
```

Ezután a felhasználó a `/mcp` paranccsal, a saját böngészőjében lép be a Higgsfield-fiókjába, és engedélyezi a hozzáférést. A `--scope user` azért kell, hogy a szerver minden projektjében elérhető legyen.

**Jelszót, API-kulcsot vagy más belépési adatot soha ne kérj tőle, és ne is vegyél át.** A belépés OAuth-tal, a böngészőben történik, a jelszó nem megy át a beszélgetésen. Ha a felhasználó mégis beírná, figyelmeztesd, hogy erre nincs szükség, és irányítsd a `/mcp` parancshoz. Ugyanez vonatkozik a `cloud.higgsfield.ai` API-kulcsaira: a hivatalos MCP-szerverhez nem kellenek.

**A parancssori eszköz hasznos, de nem kötelező.** A folyamat az MCP-vel önmagában is végigvihető. Ellenőrizd, van-e (`higgsfield version`), és rögzítsd az eredményt:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/project.py" config set cli van
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/project.py" config set cli nincs
```

Ha nincs, **ne erőltesd a telepítést**, és semmiképp ne tedd feltételévé a munkakezdésnek. Ajánld fel egyszer, egy mondatban, hogy `npm install -g @higgsfield/cli` paranccsal telepíthető (Node.js kell hozzá), és ha a felhasználó nem kéri, dolgozz nélküle. A parancsokat amúgy is te futtatod, nem ő — neki soha nem kell parancssort használnia.

Amit CLI nélkül másképp kell csinálni, azt a `references/cli.md` végén lévő táblázat sorolja fel. A lényeg: a kilenc réteg és a reklámág teljesen működik MCP-vel, a CLI csak kényelmesebbé teszi.

Belépés után kérd meg, hogy a Higgsfield-fiókjában nézze meg, melyik egyenlegből vont le az első generálás — az előfizetése havi kreditjéből vagy külön fejlesztői API-keretből. A költségbecslés csak akkor lesz valós, ha a megfelelő keretet mérjük.

### Első indulás: telepítési adatok

Minden munkamenet elején futtasd le:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/project.py" config show
```

Ha bármi `HIÁNYZIK`, akkor **először a telepítést vidd végig, és csak utána kezdj munkához**.

A telepítés nagy részét **magadnak kell felderítened, nem a felhasználót kérdezgetni**. Az adatok többsége lekérdezhető a Higgsfield MCP-jén keresztül, és a mért érték mindig jobb, mint amit fejből mondana. Kérdezni csak azt kérdezd, ami nem derül ki. A részletek a `references/mcp-eszkozok.md` fájlban vannak, olvasd el a telepítés előtt.

A telepítés négy lépés, ebben a sorrendben.

**1. Eszközfelderítés.** Nézd meg a ténylegesen elérhető MCP-eszközöket, és feleltesd meg őket az öt szerepkörnek. A `references/mcp-eszkozok.md` megmondja, melyik szerepkörhöz melyik eszközt szokta hívni a platform — de ez csak kiindulópont, a tényleges eszközlista az igazság. Eszköznevet kitalálni tilos. Ha valamelyik szerepkörhöz nincs eszköz, mondd meg a felhasználónak, és tervezz kerülőutat.

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/project.py" config set tool.image_gen "<eszköznév>"
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/project.py" config set tool.image_to_video "<eszköznév>"
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/project.py" config set tool.character_train "<eszköznév>"
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/project.py" config set tool.upscale "<eszköznév>"
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/project.py" config set tool.history "<eszköznév>"
```

**2. Csomag és keret.** A `balance` eszköz kiírja az egyenleget és az előfizetési csomagot. **Ne kérdezd meg a felhasználótól, amit ez megmond.** Csak akkor kérdezz rá, ha az eszköz nem elérhető, vagy a válasza értelmezhetetlen.

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/project.py" config set plan "<csomagnev>"
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/project.py" config set monthly_credits <szam>
```

**3. Kreditárak mérése.** Ne tippelj és ne kérdezz: mérd meg. A `generate_image` és a `generate_video` hívásoknak átadható a `get_cost: true` paraméter, amitől nem indul munka, csak visszajön a becsült ár. Ezzel négy tételt kell megállapítani.

Előbb ellenőrizd a modell paramétersémáját (`models_explore`), mert a képarány és a hossz felsorolt érték, nem szabad szöveg — érvénytelen paraméterrel a mérés is hibás lesz. Utána mérj: egy kezdőkocka ára a képmodellel, egy másodpercnyi mozgókép ára a videómodellel (a teljes klip árát oszd el a hosszal), egy szereplő betanítása, egy felskálázás. Ha egy tétel nem mérhető, azt az egyet kérdezd meg.

**A modellt is rögzítsd**, amivel mértél, mert az ár modellenként eltér, és fél év múlva már senki nem fogja tudni, melyik számhoz melyik modell tartozott. Modellazonosítót ne találj ki: a `model list` adja az aktuális katalógust, a gyakoriakat a `references/cli.md` sorolja fel.

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/project.py" config set model.image <modellazonosito>
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/project.py" config set model.video <modellazonosito>
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/project.py" config set cost.image <szam>
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/project.py" config set cost.video_per_second <szam>
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/project.py" config set cost.character_train <szam>
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/project.py" config set cost.upscale <szam>
```

**4. Az eredmény ellenőriztetése.** A `config show` kimenetét mutasd meg neki, és kérdezd meg, stimmel-e. Ez az egyetlen pont, ahol a telepítés emberi jóváhagyást kér — a többit magad deríted ki.

**Egy kivétel a méréssel.** A Marketing Studio modelljeire nem működik a `get_cost`. Az avatáros reklámok árát csak utólag, a `transactions` eszközzel lehet leolvasni. Ezt előre mondd meg neki, mert ez az egyetlen ág, ahol nem tudsz előre árat mondani.

A beállítások a felhasználó gépén, a `~/.higgsfield-storyboard/config.json` fájlban maradnak, tehát ezt egyszer kell végigcsinálni, nem projektenként. Az `init` innen örökli az árakat és az eszközneveket. Ha később árat vagy csomagot vált, ugyanezekkel a parancsokkal frissíthető, de a **már létező projektek a saját mentett áraikkal dolgoznak tovább**, hogy a korábbi becslések visszakereshetők maradjanak.

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

A `shotlist` réteg a `templates/storyboard.example.json` szerinti szerkezetet tölti fel. Három referenciát olvass el hozzá: a `references/shot-grammar.md` a gépállásokról és kameramozgásokról szól, a `references/prompt-iras.md` arról, hogyan áll össze belőlük a tényleges angol prompt, a `references/nyitohook.md` pedig a nyitójelenetről — ez utóbbi akkor számít, ha a videó közösségi médiába vagy hirdetésnek készül.

Két fontos megkötés. A klipek legfeljebb tizenöt másodpercesek, tehát ennél hosszabb jelenet nem létezik, bontsd szét. A `prompt_en` mező **mindig angol**, a `leiras` mező magyar, mert azt az ügyfél olvassa.

A jelenetlista elkészülte után, még a jóváhagyás előtt futtasd le az ellenőrzést:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/project.py" check-shots
```

Ez kiszűri a túl hosszú klipeket, a hiányzó promptot és a reklámjelenetek formátumhibáit. Olcsóbb itt megtalálni őket, mint egy visszautasított generálás árán.

### Kétféle jelenet: filmes és reklám

A jelenetek `tipus` mezője kétféle lehet.

A **filmes** jelenet az alapértelmezés: generált kezdőkockából készül mozgókép, szabad prompttal. Ez való többjelenetes történethez, visszatérő szereplőkkel.

A **reklám** jelenet a Marketing Studio ága: feltöltött termékkép, egy avatár és egy előre adott hirdetésformátum. Ez való rövid közösségimédia-hirdetéshez, termékbemutatóhoz, kicsomagoláshoz, virtuális próbához — és ez az, amivel egy avatár beszélni tud egy feltöltött termékről.

**Ha a feladat reklám, a `references/reklam-marketing-studio.md` fájlt kötelező elolvasni**, mielőtt jelenetlistát írsz. Más korlátok érvényesek rá: legfeljebb 15 másodperc, pontosan egy avatár, kötelező termékkép, egy helyszín, zárt listás hook. És ami a költségkapunk szempontjából a legfontosabb: **erre az ágra a platform nem ad előzetes árbecslést**, a költség csak utólag olvasható ki. Ezt mondd meg a felhasználónak, mielőtt elindítja az elsőt.

A két típust ne keverd egy jeleneten belül. Egy projektben viszont megférnek egymás mellett.

### Arculat

A `look.brand` blokkban rögzítsd az ügyfél arculatát: elsődleges szín, szövegszín, betűtípus, logó. Ez nem a generálásnak szól — az AI-modellek a márkaszínt sem tartják meg megbízhatóan —, hanem az utómunkának: a záróképnek, a feliratoknak és a szöveges rátéteknek. Így több videón át egységes marad a megjelenés.

A **logót soha ne generáltasd**, hanem utómunkában helyezd rá. Ez a `continuity.md` szabálya, és arculatnál különösen érvényes: a torzított logó az egyetlen hiba, amit az ügyfél biztosan kiszúr.

### Folytonosság

Karakter- és stílusfolytonosságról a `references/continuity.md` szól. Ezt a `look` réteg előtt kötelező elolvasni. Konzisztens szereplő nélkül a többjelenetes videó használhatatlan, és ezen a ponton szokott elhasalni a munka.

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

**Képarányváltásnál figyelj.** Az `assemble.py` egyszerűen levágja a kép szélét, ami 16:9-ből 9:16-ba váltva fontos tartalmat vághat le — feliratot, a szereplő fejét, a terméket. Ha ez fenyeget, a platform tartalomtudatos képarányváltó munkafolyamata a jobb megoldás, lásd `references/cli.md`. Az kreditbe kerül, a helyi vágás nem, ezért előbb nézd meg a helyi eredményt, és csak akkor válts, ha tényleg romlott.

### Hang

A narrációhoz beszédszintézis használható, kiválasztott hanggal — a hangok listája lekérdezhető, kitalálni nem lehet. Kész videó idegen nyelvű változatához külön szinkronizáló munkafolyamat van, a hang cseréjéhez pedig hangcserélő. Mindkettő a `references/cli.md`-ben szerepel.

Ezek költsége **nem becsülhető előre**, ugyanúgy, mint a reklámágé. Szólj róla, mielőtt elindítod.

### Ha egy generálás nem sikerült

Ne futtasd újra automatikusan. Mutasd meg az eredményt, és a `references/hibamintak.md` segítségével derítsd ki, melyik rétegen csúszott el — az alanynál, a cselekvésnél, a kameránál vagy a stílusnál. A javításnál **egyszerre egy dolgot változtass**, különben a következő eredményből nem derül ki, mi segített, és a kredit tanulság nélkül fogy.

## Amit soha ne csinálj

Ne generálj videót jóvá nem hagyott kezdőkockából. Ne írd át kézzel a `project.json` státuszmezőit. Ne ígérj a felhasználónak gombnyomásra kész filmet. Ne fuss neki újra automatikusan egy sikertelen generálásnak, hanem mutasd meg az eredményt és kérdezd meg, mit rontott el. Ne dolgozz több jeleneten párhuzamosan az 5. rétegben, amíg az első kettő minősége nincs elfogadva, mert a hibás stíluskód így tízszeres költséggel sokszorozódik.

## Ügyfélkommunikáció

Amit ígérni lehet, az a jóváhagyható képes storyboard rövid határidőre, onnan a kész anyag néhány nap alatt, előre kalkulált költséggel és meghatározott számú finomító körrel. Amit nem szabad ígérni, az a korlátlan javítás és az azonnali kész film.

Magyar nyelvű szöveg írásakor alkalmazd a `magyar-helyesiras` és a `magyar-termeszetes-stilus` skilleket.
