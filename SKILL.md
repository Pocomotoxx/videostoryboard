---
name: higgsfield-storyboard
description: Automatizált videókészítés storyboard-alapon (Higgsfield). Használd, amikor egy témából, szövegből vagy briefből jelenetekre bontott storyboardot, képi prompt-sorozatot és videógenerálási csomagot kell készíteni. Triggerek: "storyboard", "videó forgatókönyv", "jelenetbontás", "Higgsfield", "videó prompt", "automatizált videó".
---

# Higgsfield storyboard — automatizált videókészítés

## Mire való

Ez a skill egy bemeneti szövegből (blogcikk, termékleírás, kampánybrief, kulcsszókutatás)
végigviszi a videókészítés lépéseit a jelenetbontástól a generálásra kész prompt-csomagig.

## Állapot

**v0 váz.** A folyamat lépései és a scriptek még nincsenek kitöltve — a valós Higgsfield
munkamenet leírása alapján kell feltölteni. Amíg ez nem történik meg, a skill nem futtatható.

## Folyamat (vázlat)

1. **Bemenet beolvasása** — a `bemenet/` mappából a brief vagy forrásszöveg.
2. **Jelenetbontás** — a szöveg tagolása 5–15 másodperces jelenetekre, jelenetenként
   cél, képi tartalom, kameramozgás és hossz megadásával.
3. **Prompt-írás** — jelenetenként képi és mozgás-prompt a `sablonok/` sablonjai alapján.
4. **Storyboard fájl** — a jelenetek strukturált (JSON + olvasható) mentése a `kimenet/` mappába.
5. **Generálás** — a promptok átadása a videógeneráló felületnek.
6. **Ellenőrzés** — vizuális konzisztencia, hossz, felirat, hangalámondás.

## Mappák

- `bemenet/` — forrásszövegek, briefek.
- `sablonok/` — prompt- és storyboard-sablonok.
- `scripts/` — segédscriptek (Python).
- `kimenet/` — generált storyboardok és prompt-csomagok.

## Kapcsolat a fő projekttel

A tartalmi és nyelvi szabályokat a gyökér `CLAUDE.md`, a projektspecifikus adatokat a
`projekt-adatok.md` adja. Minden magyar szöveg az MHSz12 szerint, természetes megfogalmazással.
