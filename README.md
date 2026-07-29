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

Utána `/reload-plugins`, és a skill elérhető `higgsfield-storyboard` néven. Frissítés
később `/plugin marketplace update`, majd `/plugin update higgsfield-storyboard`.

## Előfeltételek

- **Python 3** — macOS és Linux: `python3`; Windowson `python`, mert ott a `python3`
  csak egy nem működő Microsoft Store-alias.
- **ffmpeg** — az összefűzéshez. macOS: `brew install ffmpeg`.
- **Higgsfield MCP** — a generáló rétegekhez (látvány, kezdőkockák, mozgás).

## Szerkezet

```
.claude-plugin/marketplace.json          # a katalógus
plugins/higgsfield-storyboard/           # maga a plugin
├── .claude-plugin/plugin.json
├── SKILL.md                             # a folyamat leírása
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
