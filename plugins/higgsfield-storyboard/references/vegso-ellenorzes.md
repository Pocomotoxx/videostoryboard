# Végső ellenőrzés leszállítás előtt

Ezt a `finish` réteg után, az ügyfélnek való átadás előtt kell végigmenni. Friss szemmel,
nem a munka folytatásaként — ezért is van külön fájlban: aki a videót készítette, az már
nem látja a hibáit.

A menete: nézd meg a kész videót képkockákra bontva (`scripts/frames.py`), és menj végig
az alábbi pontokon. Amit találsz, azt sorold fel a felhasználónak, súlyosság szerint —
ne javíts magadtól, mert a leszállítás előtti változtatás új hibát vihet be.

## 1. Az eredeti cél

Vedd elő a `brief.md`-t, és tedd fel a kérdést: **ez a videó azt csinálja, amit a brief
kért?** Nem azt, hogy szép-e, hanem hogy az üzenet átmegy-e, a célcsoportnak szól-e, a
kért hosszúságú-e, és oda való-e, ahová szánták.

Ez a leggyakoribb csendes hiba: a munka közben a videó elmegy egy szép, de más irányba,
és a végén senki nem veti össze a kiindulással.

## 2. Teljesség

Minden jelenet benne van, amit a jóváhagyott jelenetlista tartalmaz? Nincs benne olyan,
ami kimaradt volna? A sorrend a jóváhagyott sorrend?

Megvan minden kért kimeneti változat — képarányok, feliratos és felirat nélküli verzió?

## 3. Folytonosság

Ez az, amit egymás után játszva látni, kockánként nem. Ugyanaz az arc, ugyanaz a ruha,
ugyanaz a fényirány, ugyanaz a színvilág? A `continuity.md` ellenőrzőlistája ide is
érvényes, de most a **jelenetek közötti átmenetekre** figyelj, ne a jeleneteken belülre.

## 4. Szöveg és arculat

Van-e a képen olvashatatlan, generált szövegtöredék? A feliratok helyesek — elírás,
elválasztás, időzítés? A magyar szöveg a helyesírási szabályok szerint van?

A logó a helyén van, nem torzult, nem generált? A márkaszínek stimmelnek a
`look.brand` blokkhoz?

## 5. Hang és ritmus

Egyenletes-e a hangerő a videó folyamán? Nem ugrál jelenetenként? A zene nem nyomja el
a narrációt, és nem szakad el hirtelen a végén?

Ha erős ritmusú zene van alatta, a vágások ütemre esnek? A `zene-es-ritmus.md` szerint
ellenőrizhető.

## 6. Technikai minőség

A felbontás és a képarány a kért? Nincs fekete sáv, nincs levágott fontos tartalom a
képarányváltás miatt? Nincs akadás a vágásoknál? A fájl mérete kezelhető ott, ahová
feltöltik?

## 7. Jogi és adatbiztonsági szempontok

Van-e a videóban valós személy arca, akire hozzájárulás kell? Szerepel-e védett karakter,
márka vagy filmes látványvilág, amit nem lenne szabad? Került-e a képbe olyan adat —
képernyőkép, dokumentum, név —, ami nem szánt nyilvánosságra?

Ez a pont ügyfélmunkánál nem formalitás. A `continuity.md` végén szereplő korlátok itt
kapnak utolsó ellenőrzést.

## A jelentés

Három csoportba sorold, amit találtál:

- **Leszállítást gátló** — hibás üzenet, jogi kockázat, hiányzó jelenet, elírás a feliratban.
- **Javasolt javítás** — hangerőugrás, csúszó vágás, kisebb folytonossági hiba.
- **Megjegyzés** — amit érdemes tudni, de nem kell javítani.

Ha semmit nem találtál, azt is mondd ki egyenesen. De előbb menj végig mind a hét ponton —
a „szerintem rendben van" nem ellenőrzés.
