# Telefonos jóváhagyás

A `scripts/bot.py` kiküldi a jóváhagyásra váró anyagot Telegramra, és a döntést
visszaírja a projektbe. Opcionális kényelmi réteg — a rendszer enélkül is teljes.

## A vágás, ami miatt biztonságos

**A bot nem generál.** Nincs benne egyetlen olyan parancs sem, ami kreditet költene.
Amit tud: listázni, kiküldeni, jóváhagyni, visszadobni, állapotot és költséget mutatni.

Ebből három dolog következik. Nem kell hozzá Higgsfield-kulcs. Nem tudja megkerülni a
költségkaput vagy a futásplafont, mert nem is ér hozzá a generáláshoz. És egy elveszett
telefon vagy egy félrenyomás legrosszabb következménye az, hogy valamit elfogadsz vagy
visszadobsz — nem az, hogy elmegy a havi kereted.

A generálás marad a gépen, a szokásos úton.

## Hogyan illeszkedik a folyamatba

A bot a `pending` állapotú node-okkal dolgozik. Vagyis a menet ez:

1. A gépen legenerálod az anyagot, és letöltöd (`set-asset --file`).
2. A node-ot jóváhagyásra küldöd (`pending`).
3. A felhasználó a telefonján megkapja, és dönt.
4. A döntés a `project.json`-ba kerül, ugyanoda, mintha a gépen hagytad volna jóvá.

Amikor legközelebb `status`-t futtatsz, a döntés már ott van. Nem kell semmit
összefésülni.

## Amit a bot kiküld

Minden váró tételt **fájlként küld, nem képként**. Ez szándékos: a képként küldött anyagot
a Telegram tömöríti, és pont az apró részletek vesznek el, amiket ellenőrizni kell — ujjak,
arcvonások, háttérbe rajzolt betűk.

A felirat tartalmazza a node nevét, az esetleges korábbi indokot, és külön figyelmeztetést,
ha a jelenet a beküldés óta megváltozott.

## Parancsok

| Parancs | Mit csinál |
|---|---|
| `/varo` | a jóváhagyásra váró anyagok kiküldése |
| `/allapot` | a `status` kimenete |
| `/koltseg` | az eddig elköltött kredit |
| `/megse` | a folyamatban lévő visszadobás megszakítása |

Visszadobásnál a bot rákérdez az indokra, és a következő üzenetet írja be indokként —
kivéve, ha az egy parancs, mert a felhasználó meggondolhatta magát.

## Beállítás

A token és az azonosító a gépszintű beállításban tárolódik, tehát egyszer kell megadni:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/project.py" config set telegram.token "<token>"
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/project.py" config set telegram.owner "<szam>"
```

**A token értékét soha ne írd vissza a beszélgetésbe.** A `config show` sem írja ki, csak
azt, hogy megvan-e. A beállításfájl jogosultsága mentéskor a tulajdonosra szűkül.

Környezeti változóval is megadható (`TG_TOKEN`, `TG_OWNER`), és az erősebb a mentettnél —
így egy eseti indítás felülírhatja anélkül, hogy a beállításhoz hozzányúlnánk.

## Indítás

Előbb ellenőrzés, a Telegram megszólítása nélkül:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/bot.py" --project . --onteszt
```

Ez megnézi, hogy megvan-e a projekt, a token és az azonosító, és hogy a gombok
szerializálása helyes-e. Csak utána:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/bot.py" --project .
```

A bot egy projektre figyel. Ha több munkád fut párhuzamosan, mindegyikhez külön
példány kell — vagy egyszerűbben: csak arra indítsd el, amelyiknél épp jóváhagyás kell.

## Amit a felhasználónak tudnia kell

**A botnak futnia kell.** Ha a folyamat leáll vagy a gép elalszik, a telefonon nem
történik semmi. Ez ugyanaz a korlát, mint az időzített előkészítésnél.

**Csak a tulajdonos írhat neki.** A bot minden más feladótól érkező üzenetet válasz nélkül
eldob, és gombnyomásnál is a megnyomó azonosítóját nézi, nem a chatét.

## Ha nincs beállítva

Ne tedd a munka feltételévé. Ha nincs Telegram, a jóváhagyás a szokásos módon, a
beszélgetésben történik — az `${CLAUDE_PLUGIN_ROOT}/scripts/frames.py` képkockáival
és a `Read` hívással.
