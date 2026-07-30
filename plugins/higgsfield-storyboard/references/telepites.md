# Telepítés: MCP-bekötés és a gépszintű adatok

Ezt akkor kell végigvinni, ha a `config show` bármit `HIÁNYZIK`-ként jelez. Egyszer kell
megcsinálni gépenként, nem projektenként.

## Csomagváltás és áremelkedés

A rendszer **soha ne feltételezzen semmilyen előfizetési csomagot**. A csomag neve és a
havi keret a `balance` eszköz válaszából jön, a kreditárak pedig mérésből — mindkettő
adat, nem tudás.

Ha a felhasználó csomagot vált, a keret és sokszor az árak is változnak. Ezért **minden
munkamenet elején kérdezd le az egyenleget**, és ha eltér attól, ami a beállításokban
van, frissítsd:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/project.py" config set plan "<uj-csomagnev>"
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/project.py" config set monthly_credits <szam>
```

Csomagváltás után a kreditárakat is mérd újra, mert modellenként és csomagonként
eltérhetnek. A már futó projektek a saját mentett áraikkal dolgoznak tovább — ez
szándékos, hogy a korábbi ügyfélbecslések visszakereshetők maradjanak.

## A Higgsfield MCP bekötése

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

## A telepítési adatok

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
