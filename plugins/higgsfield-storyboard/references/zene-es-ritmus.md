# Zene és vágásritmus

Ezt akkor olvasd el, ha a videó alá erős ritmusú zene kerül. Halk aláfestésnél kevésbé
számít, de hirdetésnél és közösségimédia-videónál majdnem mindig ez van.

## Miért fontos

Erős dobos zenénél a néző **azonnal észreveszi, ha a vágás nem ütemre esik** — akkor is,
ha nem tudja megnevezni, mi a baj. Csak azt érzi, hogy a videó amatőr. Körülbelül három
képkocka az érzékelési határ, ennél nagyobb csúszás már látszik.

Ez a mi folyamatunkban azért kritikus, mert a jelenethosszakat a `shotlist` rétegben
döntjük el, a generálás előtt — és a klip hossza generálási paraméter, tehát utólag nem
lehet szabadon nyújtani. **Ha a ritmus fontos, a zenét a jelenetlista előtt kell
kiválasztani.**

## A sorrend

Ha a felhasználónak már van zenéje, akkor a jelenethosszak a zenéhez igazodnak. Ha még
nincs, akkor a jelenethosszak a tartalom ritmusát követik, és a zenét később, az
összefűzéskor keresitek — ilyenkor ne próbálj kockapontos illesztést, mert nincs mihez.

Ezt a döntést a brief rétegben tedd fel, ne később.

## A tempó megállapítása

A BPM-et a zene forrása többnyire megadja — a legtöbb zenei könyvtár kiírja. Ha nem, a
felhasználó megmérheti egy ütemkopogtatóval: elég ha húsz-harminc ütést kikopogtat a
zenére, az átlagból jó becslés lesz.

Ne találd ki, és ne becsüld hallás után. Egy-két százalék tévedés is elég ahhoz, hogy egy
egyperces videó végén másodperces csúszás legyen.

## A számolás

A `scripts/beatgrid.py` végzi. Javaslatot ad az ütemre eső jelenethosszakra:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/beatgrid.py" --bpm 128 --hossz 30
```

Ellenőrzi is a kész jelenetlistát, jelenetenként megmutatva, mennyit csúszik a vágás:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/beatgrid.py" --bpm 128 --project .
```

Ha a zene nem ütéssel indul, a `--kezdet` paraméterrel adható meg az első ütés helye.
A képkockasebesség alapból 30, ez a `--fps`-sel változtatható.

## Mit jelent a gyakorlatban

128 BPM-nél egy ütem 1,875 másodperc. Vagyis a jelenetek 1,875 / 3,75 / 5,625 / 7,5
másodpercesek lehetnek, nem pedig „úgy öt". Ez elsőre kényelmetlennek tűnik, de a
generálás amúgy is egész vagy fél másodperces értékeket vesz — ilyenkor a legközelebbi
engedett hosszat kell választani, és a maradékot az összefűzésnél levágni.

Ha a modell csak egész másodperceket enged, akkor a kockapontos illesztés nem megy
minden vágásnál. Ilyenkor a **fontos vágások** essenek ütemre: a nyitás, a fordulat és
a zárás. A közbülsőknél kisebb a baj.

## Dramaturgia: a ritmus nem csak matematika

Ütemre esni szükséges, de nem elég. A vágások sűrűsége mondja meg, milyen energiájú a
videó, és ez a videó folyamán változzon: a nyitás legyen sűrű, a közép engedjen, a zárás
szoruljon össze. Végig egyenletes vágásritmus monoton, akkor is, ha minden ütemre esik.

Egy hatásos kameramozgást ne használj kétszer ugyanabban a videóban. Ami egyszer feltűnő,
másodszorra már modoros — és a néző rájön, hogy trükk.
