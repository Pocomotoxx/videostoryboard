# higgsfield-storyboard

Rétegelt, jóváhagyáskapus AI-videógyártó folyamat. A működés leírása a `SKILL.md`
fájlban van — Claude Code azt olvassa be, amikor a skill elindul.

## Szerkezet

```
higgsfield-storyboard/
├── SKILL.md                          # a folyamat leírása, a skill belépőpontja
├── scripts/
│   ├── project.py                    # a rétegek állapotgépe, jóváhagyás és költségkapu
│   └── assemble.py                   # helyi összefűzés ffmpeggel
├── references/
│   ├── shot-grammar.md               # gépállás, szög, kameramozgás, promptszerkezet
│   └── continuity.md                 # karakter- és stílusfolytonosság
└── templates/
    └── storyboard.example.json       # a storyboard.json szerkezete, kitöltött mintával
```

A konkrét munkák nem itt keletkeznek: a `project.py init <nev>` egy külön projektkönyvtárat
hoz létre (`brief.md`, `treatment.md`, `storyboard.json`, `project.json`, valamint
`characters/`, `shots/`, `output/`, `delivery/` mappák).

## Bekötés Claude Code skillként

A mappa könyvtár-junctionnel van bekötve a felhasználói skill-mappába:

```bash
cmd /c mklink /J "%USERPROFILE%\.claude\skills\higgsfield-storyboard" "C:\Ai\Dániel\Dániel seo támogatás\video\higgsfield-storyboard"
```

Windowson a `ln -s` helyett junctiont használunk, mert az rendszergazdai jog és
fejlesztői mód nélkül is működik.

## Környezet

- **Python** — a `SKILL.md` parancsai `python`-nal hívják a scripteket, mert ezen a gépen
  a `python3` csak egy nem működő Microsoft Store-alias.
- **ffmpeg** — az `assemble.py` futtatásához kell, telepítve van.
- **Higgsfield MCP** — a generáló rétegekhez (3–5.) szükséges, még nincs beállítva.
