# A Higgsfield MCP eszközkészlete

Ez a fájl azt írja le, milyen eszközöket szokott kiajánlani a Higgsfield MCP-szervere, és
melyiket mire használjuk. **Kiindulópont, nem szentírás**: a platform eszközkészlete
kiadásonként változik, ezért az itt szereplő neveket az első futásnál mindig ellenőrizni
kell a ténylegesen elérhető eszközlistán. Ha egy név nem stimmel, az eszközlista az igazság,
nem ez a fájl.

## Szerepkörök és a hozzájuk tartozó eszközök

| Szerepkör a rendszerünkben | Várható eszköz | Mit csinál |
|---|---|---|
| `image_gen` | `generate_image` | Kezdőkocka és állókép generálása |
| `image_to_video` | `generate_video` | Mozgókép egy kezdőkockából |
| `character_train` | lásd lent | Visszatérő szereplő betanítása referenciafotókból |
| `upscale` | `generate_image` felskálázó modellel | Felbontásnövelés |
| `history` | `job_display` | Egy korábbi job eredményének megjelenítése |

**A szereplő betanítása nem generáló modell.** A parancssori eszközön külön parancs
(`soul-id create`), az MCP-n pedig felderítéssel kell megkeresni a megfelelő eszközt.
Figyelj rá, hogy a `soul_cast` **képgeneráló modell neve**, nem a betanításé — ez könnyen
összetéveszthető. Ha az MCP-n nincs betanító eszköz, a `references/cli.md` mutatja a
parancssori utat.

## Amit a költségkapunkhoz használunk

**`balance`** — kiírja a kredit-egyenleget és az előfizetési csomagot. Ebből tölthető ki a
telepítéskor a csomag neve és a havi keret, tehát ezt nem kell a felhasználótól megkérdezni.
A CLI-n ugyanez `higgsfield account status` (a `balance` és a `credits` nem érvényes
alparancs, ez visszatérő tévedés).

**`get_cost: true`** — a `generate_image` és a `generate_video` hívásoknak átadható
paraméter, amitől a hívás nem indít munkát, csak visszaadja a becsült kreditköltséget.
Ezzel a kreditárak mérhetők, nem kell tippelni. A válaszban egy `adjustments` blokk is
jön, ami megmutatja, milyen alapértékeket tett be a szerver a meg nem adott paraméterek
helyére — ezt érdemes a felhasználónak is megmutatni.

**`transactions`** — a legutóbbi kreditmozgások, időrendben visszafelé. Ott kell használni,
ahol nincs előzetes becslés (lásd lent), tehát a tényleges költséget utólag olvassuk ki.
CLI-n `higgsfield account transactions --size N`.

**`models_explore`** — a modellek listája és paramétersémája. Az `action="get"` és a
`model_id` megadásával egy adott modell paramétereit adja vissza: milyen képarányok
engedettek, milyen hosszak, milyen módok. A képarány és a hossz **felsorolt érték, nem
szabad szöveg** — mindig ebből ellenőrizd, ne abból, ami kézenfekvőnek tűnik.

## Fájlok bejuttatása

Feltöltött termékkép vagy referenciafotó nem adható át nyers URL-ként. A helyes út:
`media_import_url` egy webes címhez, vagy a feltöltő eszköz (`media_upload` /
`media_confirm`, illetve a felugró feltöltőablak) helyi fájlhoz. Mindkettő egy azonosítót
ad vissza, és a generáló hívás azt kapja meg.

## Ahol nincs előzetes árbecslés

A Marketing Studio modelljeire, valamint a hangcsere és a szinkronizálás
munkafolyamatára **nem működik a `get_cost`**. Ezeknél a költséget csak utólag, a
`transactions` eszközzel lehet leolvasni. Ezt a felhasználónak előre meg kell mondani.

## Két felület: MCP és CLI

A Higgsfieldnek van hivatalos parancssori eszköze is. Mindkettő ugyanabból a
kreditkeretből és ugyanabból a munkasorból dolgozik, tehát a választás ergonómia kérdése.

Beszélgetős munkához az MCP a kényelmesebb, a bekötése is egyszerűbb, ezért az a
rendszerünk alapértelmezése. **A parancssori eszköz viszont több ponton pontosabb**:
ott van modellséma-lekérdezés, előzetes árszámítás, szereplőtanítás és a képarányváltó
munkafolyamat. Ha egy lépéshez az MCP-n nem találsz eszközt, nézd meg a
`references/cli.md` fájlt, mielőtt kerülőutat terveznél — jó eséllyel ott megvan.

---

*A platformismeret egy része az [OSideMedia/higgsfield-ai-prompt-skill](https://github.com/OSideMedia/higgsfield-ai-prompt-skill)
MIT-licences projektből származik, saját megfogalmazásban. Lásd a `NOTICE.md` fájlt.*
