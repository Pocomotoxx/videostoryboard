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

### Indulás

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/project.py" init "ugyfel-projektnev"
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/project.py" status
```

Ha félbeszakadt munkamenetet folytatsz, mindig `status` és `next` hívással kezdj. Az igazság a `project.json`-ban van, nem a beszélgetésben.

### Eszközfelderítés

A Higgsfield MCP eszközkészlete változik, ezért ne dolgozz beégetett eszköznevekkel. Az első futásnál nézd meg a ténylegesen elérhető eszközöket, és rögzítsd a szerepkör-hozzárendelést:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/project.py" set-tool image_gen "<eszköznév>"
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/project.py" set-tool image_to_video "<eszköznév>"
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/project.py" set-tool character_train "<eszköznév>"
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/project.py" set-tool upscale "<eszköznév>"
```

Szükséges szerepkörök: `image_gen`, `image_to_video`, `character_train`, `upscale`, `history`. Ha valamelyikhez nincs eszköz, jelezd a felhasználónak, és tervezd meg a kerülőutat, ne találj ki eszköznevet.

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

A becslést mutasd meg a felhasználónak, mielőtt az 5. rétegbe lépnél. Az elköltött kreditet a `project.py spend` rögzíti, az `report` pedig kiírja a projekt tényleges költségét, ami ügyfélszámlázáshoz kell.

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
