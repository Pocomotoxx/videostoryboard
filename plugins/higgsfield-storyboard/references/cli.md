# A Higgsfield parancssori eszköze

A Higgsfieldnek az MCP mellett hivatalos parancssori eszköze is van, és a mi
munkafolyamatunk szempontjából **több ponton ez a pontosabb felület**: itt lehet
modellsémát lekérdezni, előzetes árat számolni, Soul-karaktert tanítani és fájlt
feltölteni, mindezt kiszámítható parancsokkal.

Mindkét felület ugyanabból a kreditkeretből és ugyanabból a munkasorból dolgozik. A
választás ergonómia kérdése, a sorban elfoglalt helyet a fizetős csomag szintje dönti el.

## Telepítés és belépés

Windowson és mindenhol máshol:

```bash
npm install -g @higgsfield/cli
```

macOS-en Homebrew-val is megy: `brew install higgsfield-ai/tap/higgsfield`.

```bash
higgsfield auth login
```

**Jelszót itt sem kérünk és nem veszünk át** — a belépés a felhasználó saját
folyamata. Ugyanaz a szabály, mint az MCP-nél.

## Amit a mi folyamatunkhoz használunk

| Feladat | Parancs |
|---|---|
| Elérhető modellek | `higgsfield model list` |
| Egy modell paramétersémája | `higgsfield model get <modell>` |
| Előzetes költségbecslés | `higgsfield generate cost <modell> [--param ertek]...` |
| Kredit és egyenleg | `higgsfield account status` |
| Kreditmozgások | `higgsfield account transactions --size N` |
| Generálás | `higgsfield generate create <modell> --prompt "..." --wait` |
| Fájlfeltöltés | `higgsfield upload` |
| Szereplő betanítása | `higgsfield soul-id create --name <nev> --soul-2 --image ... --image ...` |
| Hangok listája | `higgsfield voices list` |

Bármelyik parancshoz adható `--json`, gépi feldolgozáshoz.

Az egyenleg alparancsa **`account status`** — az `account balance` és az
`account credits` nem létezik, ez visszatérő tévedés.

## Modellazonosítók

A generáló parancsok modellazonosítót várnak, nem emberi nevet. Néhány, ami a mi
folyamatunkban előjön:

| Szerep | Azonosító |
|---|---|
| Kezdőkocka, általános kép | `nano_banana_2`, `seedream_v4_5`, `gpt_image_2`, `flux_2` |
| Kép betanított szereplővel | `text2image_soul_v2` (`--soul-id` paraméterrel) |
| Mozgókép | `kling3_0`, `seedance_2_0`, `veo3_1`, `wan2_7` |
| Avatáros és termékreklám | `marketing_studio_video`, `marketing_studio_image` |
| Beszédszintézis | `text2speech_v2` |

**A teljes és aktuális listát mindig a `model list` adja**, ez itt csak tájékozódás.
Új modellek jönnek, régiek eltűnnek, és a kitalált modellnév azonnali hibát okoz.

## Szereplő betanítása

A visszatérő szereplő betanítása nem generáló modell, hanem külön parancs:

```bash
higgsfield soul-id create --name <nev> --soul-2 --image ./1.jpg --image ./2.jpg --image ./3.jpg
higgsfield soul-id wait <soul_id>
```

A kapott azonosítót utána a képgeneráláshoz adod át `--soul-id`-ként. Ezt írd be a
storyboard `look.characters[].soul_id` mezőjébe, hogy minden jelenet ugyanazt használja.

## Munkafolyamatok: amit érdemes ismerni

A `generate workflow` külön, összetettebb folyamatokat futtat. Kettő közvetlenül a mi
rétegeinkbe illik.

**`reframe`** — képarányváltás. Ez tartalomtudatos átkeretezés, tehát **jobb, mint a mi
ffmpeges vágásunk**, ami egyszerűen levágja a kép szélét. Ha a 9:16-os változatnál fontos
tartalom csúszna ki a képből, ezt használd az `assemble.py` helyett.

```bash
higgsfield generate workflow reframe --video ./forras.mp4 --aspect-ratio 9:16 --resolution 720p --wait
```

**`dubbing`** — a kész videó szinkronizálása másik nyelvre, ISO-639-3 nyelvkóddal
(`eng`, `spa`, `deu`). Idegen nyelvű változathoz ez a legrövidebb út.

**`voice-change`** — a hang cseréje egy kiválasztott hangra a kész videón.

A `reframe` és a `draw_to_video` költsége előre becsülhető
(`generate cost workflow <nev> ...`), a **`voice-change` és a `dubbing` költsége nem** —
ezek is abba a körbe tartoznak, ahol csak utólag derül ki az ár.

## Hol nincs előzetes árbecslés

Három helyen: a Marketing Studio modelljeinél, a `voice-change` és a `dubbing`
munkafolyamatnál. Ezeknél a `transactions` mondja meg utólag, mi ment el. Minden más
esetben a `generate cost` az előírt lépés generálás előtt.

## Ha nincs parancssori eszköz

**A folyamat enélkül is végigvihető.** A parancssori eszköz kényelmi réteg, nem
előfeltétel. Ne tedd a munkakezdés feltételévé, és ne kérd a felhasználót, hogy
parancsokat gépeljen be — a parancsokat te futtatod.

| Feladat | CLI-vel | CLI nélkül, MCP-n |
|---|---|---|
| Modellséma | `model get` | `models_explore(action="get", ...)` |
| Árbecslés | `generate cost` | `get_cost: true` a generáló hívásban |
| Egyenleg | `account status` | `balance` |
| Kreditmozgások | `account transactions` | `transactions` |
| Generálás | `generate create` | `generate_image` / `generate_video` |
| Fájlfeltöltés | `upload` | `media_import_url` vagy a feltöltő eszköz |
| Szereplőtanítás | `soul-id create` | felderítéssel kell megkeresni a betanító eszközt |
| Képarányváltás | `generate workflow reframe` | helyi vágás az `assemble.py`-jal |
| Narráció, szinkron | `generate workflow` | ha nincs MCP-eszköz, külső hang és helyi keverés |

Két helyen érdemes szólni a felhasználónak, ha nincs CLI. A **szereplőtanítás** nélkül a
folytonosságot referenciaképpel és kockaláncolással kell megoldani, ahogy a
`continuity.md` írja — kevés jelenetnél ez amúgy is elég. A **képarányváltásnál** pedig a
helyi vágás levághat fontos tartalmat; ilyenkor inkább tervezz eleve két képarányra, vagy
komponálj biztonságos középre.

---

*A parancsok és azonosítók forrása a [higgsfield-ai/cli](https://github.com/higgsfield-ai/cli)
hivatalos, MIT-licences dokumentációja. Lásd a `NOTICE.md` fájlt.*
