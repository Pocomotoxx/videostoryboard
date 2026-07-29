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

A 0–2. réteg ingyenes. Ha itt esik szét a projekt, semmit nem vesztettél. A 4. réteg állóképei olcsók, és pont ott derül ki, ha egy beállítás nem működik. Az 5. réteg a drága, ezért oda kizárólag jóváhagyott kezdőkockából lépünk be.

## Elévülés

A `project.py` build-rendszerként kezeli a projektet. Minden node tárolja a bemeneteinek ujjlenyomatát. Ha egy réteget módosítasz, az összes ráépülő node automatikusan `stale` állapotba kerül, és újra jóváhagyást igényel. Ha az ügyfél a hetedik jelenet kezdőkockáját visszadobja, a hozzá tartozó mozgókép és az összefűzés is elavul, az első hat jelenet viszont érintetlen marad. Soha ne kerüld meg ezt kézi státuszírással.

## Munkamenet

### Első indulás: telepítés

Minden munkamenet elején futtasd le:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/project.py" config show
```

Ha bármi `HIÁNYZIK`, akkor **először a telepítést vidd végig, és csak utána kezdj munkához**. Az adatokat kérdezd meg a felhasználótól, egyesével, magyarázattal. Soha ne tippelj helyette, és ne töltsd ki alapértékkel: a kreditárak modellenként és csomagonként eltérnek, egy rossz szám hibás ügyfélárajánlatot eredményez.

A telepítés három kérdéskörből áll, ebben a sorrendben.

**Előfizetés.** Kérdezd meg, melyik Higgsfield-csomagja van, és mennyi kredit jár rá havonta. Ez a fiókja számlázási oldalán látszik. Ebből tudja majd a rendszer megmondani, hogy egy projekt mekkora részét eszi meg a havi keretnek.

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/project.py" config set plan "<csomagnev>"
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/project.py" config set monthly_credits <szam>
```

**MCP-eszközök.** A Higgsfield MCP eszközkészlete változik, ezért ne dolgozz beégetett eszköznevekkel. Nézd meg a ténylegesen elérhető eszközöket, javasolj hozzárendelést az öt szerepkörre, és a felhasználóval hagyasd jóvá, mielőtt rögzíted. Ha valamelyik szerepkörhöz nincs eszköz, mondd meg neki, és tervezz kerülőutat — eszköznevet kitalálni tilos.

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/project.py" config set tool.image_gen "<eszköznév>"
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/project.py" config set tool.image_to_video "<eszköznév>"
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/project.py" config set tool.character_train "<eszköznév>"
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/project.py" config set tool.upscale "<eszköznév>"
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/project.py" config set tool.history "<eszköznév>"
```

**Kreditárak.** Négy tételt kell megadnia, a saját csomagjában érvényes árakkal. Ezeket a Higgsfield felületén látja generálás előtt. Magyarázd el, mit jelentenek: `image` egy kezdőkocka ára, `video_per_second` a mozgókép másodpercenkénti ára, `character_train` egy szereplő betanítása, `upscale` egy klip felskálázása. Ha több modell közül választhat, a ténylegesen használni tervezett modell árát vegyétek.

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/project.py" config set cost.image <szam>
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/project.py" config set cost.video_per_second <szam>
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/project.py" config set cost.character_train <szam>
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/project.py" config set cost.upscale <szam>
```

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

Jóváhagyás rögzítése:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/project.py" approve keyframe:s003
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/project.py" reject keyframe:s003 --note "a kabát gombos lett, sima kell"
```

### Jelenetlista

A `shotlist` réteg a `templates/storyboard.example.json` szerinti szerkezetet tölti fel. Olvasd el a `references/shot-grammar.md` fájlt a gépállások, szögek és kameramozgások helyes használatához.

Két fontos megkötés. A klipek legfeljebb tizenöt másodpercesek, tehát ennél hosszabb jelenet nem létezik, bontsd szét. A `prompt_en` mező **mindig angol**, a `leiras` mező magyar, mert azt az ügyfél olvassa.

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

## Amit soha ne csinálj

Ne generálj videót jóvá nem hagyott kezdőkockából. Ne írd át kézzel a `project.json` státuszmezőit. Ne ígérj a felhasználónak gombnyomásra kész filmet. Ne fuss neki újra automatikusan egy sikertelen generálásnak, hanem mutasd meg az eredményt és kérdezd meg, mit rontott el. Ne dolgozz több jeleneten párhuzamosan az 5. rétegben, amíg az első kettő minősége nincs elfogadva, mert a hibás stíluskód így tízszeres költséggel sokszorozódik.

## Ügyfélkommunikáció

Amit ígérni lehet, az a jóváhagyható képes storyboard rövid határidőre, onnan a kész anyag néhány nap alatt, előre kalkulált költséggel és meghatározott számú finomító körrel. Amit nem szabad ígérni, az a korlátlan javítás és az azonnali kész film.

Magyar nyelvű szöveg írásakor alkalmazd a `magyar-helyesiras` és a `magyar-termeszetes-stilus` skilleket.
