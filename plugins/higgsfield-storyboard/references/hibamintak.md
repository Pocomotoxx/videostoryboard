# Tipikus hibák és javításuk

Ezt akkor nézd meg, ha egy generálás nem jó, de nem nyilvánvaló, min múlt. A cél az, hogy
ne találomra futtass újra, mert minden újrafutás kreditbe kerül.

## Először azt derítsd ki, melyik rétegen hibázott

Nézd végig ebben a sorrendben, és állj meg az első helyen, ahol valami nem stimmel:

1. **Alany** — az van a képen, akinek lennie kell? Jó a kinézete, a kora, a ruhája?
2. **Cselekvés** — azt csinálja, amit kértél?
3. **Kamera** — a kért gépállásból és mozgással?
4. **Stílus** — a fény, a paletta, az anyagszerűség stimmel?
5. **Hang** — ha van, illeszkedik?
6. **Kimenet** — jó a képarány, a hossz, a felbontás?

A hibák többsége az első két ponton dől el. Ha ott rendben van, a stílust ne bántsd,
mert az elrontja a többi jelenettel való összhangot.

## Test és mozgás

**Fölös vagy lebegő végtag.** Akkor jön elő, ha a testtartás kétértelmű vagy takart.
Írd le egyértelműen a testhelyzetet, és kérd, hogy minden végtag látható és természetes
állásban legyen.

**Két szereplő karja összeolvad.** Túl közel vannak egymáshoz. Vagy tartsd őket
karnyújtásnyira, vagy vedd külön jelenetbe őket.

**Ugráló, akadozó mozgás.** Túl sok cselekvést kértél egy klipben. Bontsd szét.

**Gyors mozgásnál szétesik a kép.** Generáld lassítva, és utómunkában gyorsítsd fel.

**Megnevezett mozdulat nem sikerül.** A pontos szakkifejezések (egy konkrét rúgásfajta,
egy megnevezett fogás) többkockás koreográfiát kívánnának, amit a modell nem tud
végigvinni. Az eredményt írd le, ne a technikát.

## Arc és azonosság

**A szereplő arca jelenetenként más.** Ez a leggyakoribb és leglátványosabb hiba.
Megoldásai a `continuity.md`-ben vannak: karaktertanítás, referenciakép, kockaláncolás.
Kevés jelenetnél a referenciakép is elég, soknál a tanítás éri meg.

**A ruha vagy a haj csúszik el.** Ugyanaz a gyökere: az azonosságot leíró blokknak szó
szerint azonosnak kell lennie minden jelenetben. Ha átfogalmazod, más lesz.

**Kéz és ujjak.** Jóváhagyás előtt nézd meg. Ez az a részlet, amit a modell szeret
elrontani, és amit az ügyfél biztosan észrevesz.

## Szöveg és logó a képen

A modellek olvashatatlan írásjeleket rajzolnak a háttérbe, ha van rá alkalom.
Kérj tiszta, felirat nélküli felületeket — **állításként, ne tiltásként**, mert a tagadást
több modell nem értelmezi.

Márkalogót ne a generátorral rajzoltass. Utómunkában kell ráhelyezni, mert a pontos
formát a modell nem adja vissza megbízhatóan.

## Amikor nem a promptban van a hiba

Ha a paraméter érvénytelen — nem engedett képarány, nem támogatott hossz —, a generálás
elszáll vagy mást ad vissza, és a promptot hiába csiszolod. Ilyenkor a modell
paramétersémáját kell megnézni, nem a szöveget.

## A drága hiba, amit érdemes elkerülni

Ne indíts párhuzamosan sok jelenetet, amíg az első kettő minősége nincs elfogadva. Ha a
stíluskód rossz, azt tízszeres költséggel sokszorozod. Ez a rendszer egyik alapszabálya,
és pontosan ez az a hiba, ami miatt a rétegek között kapuk vannak.

---

*A hibakatalógus egy része az
[OSideMedia/higgsfield-ai-prompt-skill](https://github.com/OSideMedia/higgsfield-ai-prompt-skill)
MIT-licences projektből származik, saját megfogalmazásban. Lásd a `NOTICE.md` fájlt.*
