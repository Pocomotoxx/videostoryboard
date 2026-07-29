# higgsfield-storyboard

Automatizált videókészítő projekt Dániel marketing- és SEO-munkájához.

## Állapot

v0 váz. A mappaszerkezet és a skill-belépőpont (`SKILL.md`) megvan, a tényleges
folyamatleírás és a scriptek még hiányoznak.

## Szerkezet

```
higgsfield-storyboard/
├── SKILL.md      # a skill belépőpontja (Claude Code ezt olvassa be)
├── bemenet/      # forrásszövegek, briefek
├── sablonok/     # prompt- és storyboard-sablonok
├── scripts/      # Python segédscriptek
└── kimenet/      # generált storyboardok, prompt-csomagok
```

## Bekötés Claude Code skillként

A mappa egy könyvtár-junctionnel van bekötve a felhasználói skill-mappába:

```bash
cmd /c mklink /J "%USERPROFILE%\.claude\skills\higgsfield-storyboard" "C:\Ai\Dániel\Dániel seo támogatás\video\higgsfield-storyboard"
```

Windowson a `ln -s` helyett junctiont használunk, mert az rendszergazdai jog és
fejlesztői mód nélkül is működik.
