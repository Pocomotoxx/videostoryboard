# Források és köszönetnyilvánítás

A projekt folyamatlogikája, állapotgépe és költségkapuja saját fejlesztés. A Higgsfield
platformra vonatkozó ismeretek egy része nyilvános, nyílt forrású projektekből származik.

## OSideMedia / higgsfield-ai-prompt-skill (MIT)

https://github.com/OSideMedia/higgsfield-ai-prompt-skill

Ebből származik a Higgsfield MCP eszközkészletére, a költségbecslés és egyenleg-lekérdezés
módjára, a Marketing Studio működésére és a prompt-szerkezetre vonatkozó ismeretek egy
része. A tartalmat nem másoltuk: a tényeket saját megfogalmazásban, a saját folyamatunkhoz
igazítva írtuk meg. Az eredeti projekt MIT-licenc alatt érhető el, szerzője az O-Side Media.

```
MIT License

Copyright (c) O-Side Media

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## higgsfield-ai/cli (MIT)

https://github.com/higgsfield-ai/cli

A Higgsfield hivatalos parancssori eszközének dokumentációja. Innen származnak a
parancsnevek, a modellazonosítók, a Marketing Studio paraméterei és a munkafolyamatok
(képarányváltás, szinkronizálás, hangcsere) leírásai. Ez az elsődleges, hiteles forrás:
ahol ellentmond bármely más forrásnak, ez az irányadó. MIT-licenc alatt érhető el.

## digitalsamba/claude-code-video-toolkit (MIT)

https://github.com/digitalsamba/claude-code-video-toolkit

Egy másik felépítésű, saját GPU-ra és nyílt forrású modellekre épülő videógyártó
készlet. A teljes eszközláncát nem vettük át, mert az külön infrastruktúrát igényelne
(saját felhős GPU, tárhely, Node.js-alapú képi összeállítás). Három megoldás viszont
átkerült, saját megvalósításban: a ráégetett felirat, a műsorhangerő egységesítése, és
a jelenetenkénti, rögzített válaszlehetőségekkel dolgozó átnézési kör. Az arculati
profil ötlete szintén innen származik. MIT-licenc alatt érhető el.

## bradautomates/claude-video (MIT)

https://github.com/bradautomates/claude-video

Önálló plugin, ami videót tölt le, képkockákat ment ki és feliratot nyer ki, hogy a
modell meg tudja nézni a videót. **Ebből semmit nem másoltunk**, mert karbantartott,
külön telepíthető projekt — a rendszerünk csak hivatkozik rá, referenciavideók
elemzéséhez. A gondolat viszont, hogy a modellnek látnia kell a videót, innen jött:
a saját kimenetünk ellenőrzésére a `scripts/frames.py` készült, önálló megvalósításban,
csak ffmpegre támaszkodva.

## Licenc nélküli források

Két további nyilvános projektet is átnéztünk a tervezés során:

- https://github.com/beshuaxian/higgsfield-seedance2-jineng
- https://github.com/AKCodez/higgsfield-claude-skills

Egyik sem tartalmaz licencfájlt, ezért alapértelmezés szerint minden jog fenntartva.
**Ezekből semmilyen szöveget nem vettünk át.** Ahol a bennük is tárgyalt szakmai
ismeret megjelenik nálunk (például a nyitóképek dramaturgiája), ott az általános,
szabadon felhasználható szakmai tudásról van szó, saját megfogalmazásban.
