# higgsfield-storyboard

Rétegelt, jóváhagyáskapus AI-videógyártó folyamat. A működés teljes leírása a `SKILL.md`
fájlban van — Claude Code azt olvassa be, amikor a skill elindul.

Telepítés és előfeltételek: a repó gyökerében lévő `README.md`.

## Szerkezet

```
SKILL.md                            # a folyamat leírása, a skill belépőpontja
.claude-plugin/plugin.json          # plugin-manifest
scripts/project.py                  # rétegek állapotgépe, jóváhagyás-, költség- és plafonkapu
scripts/assemble.py                 # helyi összefűzés ffmpeggel, felirat, hangerő
scripts/frames.py                   # képkockák kimentése a kész klipek ellenőrzéséhez
scripts/beatgrid.py                 # ütemre illesztett jelenethosszak
references/shot-grammar.md          # gépállás, szög, kameramozgás, promptszerkezet
references/continuity.md            # karakter- és stílusfolytonosság
references/mcp-eszkozok.md          # a Higgsfield MCP eszközkészlete, költségmérés
references/cli.md                   # hivatalos parancssori eszköz, modellazonosítók
references/prompt-iras.md           # promptszerkezet, hossz, tipikus félreértések
references/hibamintak.md            # mi szokott elromlani és hogyan javítsd
references/nyitohook.md             # a nyitó két másodperc közösségi médiához
references/reklam-marketing-studio.md  # avatáros és termékreklám, korlátokkal
references/zene-es-ritmus.md        # vágásritmus, ütemre illesztés
references/vegso-ellenorzes.md      # hétpontos ellenőrzés leszállítás előtt
templates/storyboard.example.json   # a storyboard.json szerkezete, kitöltött mintával
```

Ez a mappa csak a tudást tartalmazza. A konkrét munkák a `project.py init <nev>`
paranccsal a saját munkakönyvtáradban keletkeznek (`brief.md`, `treatment.md`,
`storyboard.json`, `project.json`, valamint `characters/`, `shots/`, `output/`,
`delivery/` mappák).

## A scriptek elérése

A `SKILL.md` parancsai `${CLAUDE_PLUGIN_ROOT}`-tal hivatkoznak a scriptekre, mert
telepítéskor a plugin a Claude Code gyorsítótárába másolódik, és ott a relatív
útvonal már nem a plugin mappájára mutatna.
