# Napi előkészítés témasorból

Ez a rendszer felügyelet nélküli része. Akkor van értelme, ha a felhasználó rendszeresen
posztol, és nem akar minden reggel üres lappal kezdeni.

## Mit csinál és mit nem

Az előkészítő futás **elővesz egy témát a sorból, és eljut vele addig, ameddig szabad**.
Nem talál ki témát, nem tesz ki semmit, és nem hoz olyan döntést, amit ember nem látott.

Ez a különbség a működő és a hasznavehetetlen automatizálás között. Ha a rendszer maga
találna ki naponta témát, általános tartalmat gyártana, ami kreditbe kerül és senkit nem
érdekel. Sorból dolgozva viszont a felhasználó egyszer leül, felír tíz ötletet, és tíz
napig kész anyag várja reggelente.

## A témasor

A munkakönyvtárban lévő `temasor.md` fájl. Egy sor egy téma, a `## Témák` szakasz alatt:

```
- [ ] Raktárlogisztika: három hiba, amit mindenki elkövet | ugyfel: ugyfelkft | tipus: kep
- [ ] Az új termék bemutatása
```

Az `ugyfel` és a `tipus` elhagyható. Ha van ügyfélprofil megadva, a projekt annak a
látványával indul. Feldolgozás után a sor `[x]`-re vált, és mögé kerül a projekt neve —
így visszakereshető, melyik témából mi lett.

A fájlt a felhasználó tölti fel. Ha üres, a futás nem csinál semmit, csak szól.

## A két mód — ezt meg kell kérdezni

**Nem szabad feltételezni, melyiket akarja.** Az első alkalommal kérdezd meg, és rögzítsd:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/project.py" config set elokeszites.mod ingyenes
```

**Ingyenes.** Elkészül a brief, a kezelés, a teljes jelenetlista az angol promptokkal, és
a gyártási csomag a költségbecsléssel. **Egy kredit sem megy el.** Reggel a felhasználó
elolvassa, és ha jó, ő indítja a generálást.

**Kezdőkockákig.** A fentiek, plusz a kezdőkockák legyártása szűk plafonnal — reggelre
képes storyboard várja. Ehhez plafon is kell:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/project.py" config set elokeszites.mod kezdokockak
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/project.py" config set elokeszites.max_credits <szam>
```

A mozgásréteg **egyik módban sem** indulhat el felügyelet nélkül. Az a drága lépés, és ott
sokszorozódik a hiba.

Ha nem tudja eldönteni, az ingyeneset javasold. Onnan bármikor lehet lépni, visszafelé
viszont a már elköltött kredit nem jön vissza.

## A futás menete

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/project.py" napi
```

Ez kiválasztja a témát, létrehozza a projektet, beírja a témát a briefbe, kipipálja a
sorban, és `kezdokockak` módban elindítja a plafonos futást. Utána a szokásos folyamat
következik, a mód által megszabott határig.

**Hibánál állj meg.** Ne próbálkozz újra, ne keress kerülőutat, ne generálj mást helyette.
Írd le, mi történt, és fejezd be a futást. Éjszaka senki nem látja, mit csinálsz, és egy
végtelen újrapróbálkozás a Claude-tokent is fogyasztja, nem csak a kreditet.

## Amit a felhasználónak tudnia kell

Az időzített futás **csak akkor indul el, ha a gép be van kapcsolva és ébren van.**
Lecsukott laptopon nem történik semmi. Ezért érdemesebb reggeli időpontot választani,
amikor úgyis a gép előtt ül, mint hajnalit — így ha valami elakad, azonnal látja.

Az időzítést a felhasználó a saját gépén állítja be. A rendszer ehhez a `napi` parancsot
adja, az ütemezést nem ő végzi.

## Ami soha nem lehet része

Közzététel. Az előkészítés a `delivery/` mappáig visz, és ott megáll. A posztolás emberi
döntés, felügyelet nélküli futásban különösen.
