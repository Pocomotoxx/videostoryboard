# videostoryboard

Claude Code plugin marketplace az AI-videógyártáshoz. Jelenleg egy plugint tartalmaz:
a **higgsfield-storyboard** rétegelt, jóváhagyáskapus videógyártó folyamatot.

## Telepítés

Claude Code-ban, egyszer:

```
/plugin marketplace add Pocomotoxx/videostoryboard
```

```
/plugin install higgsfield-storyboard@videostoryboard
```

Utána `/reload-plugins`. A folyamat a `/higgsfield-storyboard:video` paranccsal indul —
egy meglévő projekt könyvtárában ugyanez folytatja a félbehagyott munkát. Frissítés
később `/plugin marketplace update`, majd `/plugin update higgsfield-storyboard@videostoryboard`.

## Átadás a felhasználónak

Három szakzsargon nélküli dokumentum annak, aki használni fogja a rendszert:

- **[ATADAS.md](ATADAS.md)** — telepítés négy lépésben, és hogyan dolgozz vele.
- **[MIT-TUD.md](MIT-TUD.md)** — mit készít, mit tud a szakmáról, és mit nem csinál szándékosan.
- **[GYIK.md](GYIK.md)** — gyakori kérdések: pénz, minőség, automatizálás, ügyfélmunka.
- **[UTEMEZES.md](UTEMEZES.md)** — a napi automatikus előkészítés beállítása, lépésről lépésre.

## Előfeltételek

- **Python 3** — macOS és Linux: `python3`; Windowson `python`, mert ott a `python3`
  csak egy nem működő Microsoft Store-alias.
- **ffmpeg** — az összefűzéshez. macOS: `brew install ffmpeg`.
- **Higgsfield MCP** — a generáló rétegekhez (látvány, kezdőkockák, mozgás). A hivatalos
  felhős szervert kösd be, ehhez nem kell se API-kulcs, se telepítés:

  ```bash
  claude mcp add --transport http --scope user higgsfield https://mcp.higgsfield.ai/mcp
  ```

  Utána a `/mcp` parancs a böngésződben nyitja meg a Higgsfield belépőoldalát. A jelszavad
  a böngészőben marad, a Claude Code csak hozzáférési tokent kap.

## Szerkezet

```
.claude-plugin/marketplace.json          # a katalógus
plugins/higgsfield-storyboard/           # maga a plugin
├── .claude-plugin/plugin.json
├── skills/video/SKILL.md                # a belépőpont
├── scripts/project.py                   # rétegek állapotgépe, jóváhagyás- és költségkapu
├── scripts/assemble.py                  # helyi összefűzés ffmpeggel
├── references/                          # jelenetnyelvtan, folytonosság
└── templates/                           # storyboard-minta
```

Az ügyfélmunkák nem ebbe a repóba kerülnek: a `project.py init <nev>` a saját
munkakönyvtáradban hoz létre külön projektmappát.

## Fejlesztés

Telepítés nélkül, helyben kipróbálva:

```bash
claude --plugin-dir ./plugins/higgsfield-storyboard
```

Változtatás után `/reload-plugins`. Kiadás előtt:

```bash
claude plugin validate ./plugins/higgsfield-storyboard
```

A `plugin.json` `version` mezőjét minden kiadásnál emelni kell, különben a felhasználók
nem kapják meg a frissítést.
