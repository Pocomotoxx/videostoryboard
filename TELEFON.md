# Jóváhagyás telefonról

Ez egy **választható** kiegészítő. A rendszer nélküle is teljesen működik — ez csak arra
való, hogy a képeket ne a gép előtt ülve kelljen átnézned, hanem a telefonodon, útközben.

Ha nem érzed szükségét, nyugodtan hagyd ki.

## Mit tud és mit nem

A telefonodra megérkeznek az elkészült képek és videók, két gombbal: **Elfogadom** és
**Visszadobom**. Ha visszadobsz valamit, megkérdezi, mi a baj vele, és a válaszod bekerül
a projektbe — a következő próbálkozás abból dolgozik.

**Generálni nem tud.** Nincs benne olyan gomb, ami kreditet költene. Ezért nem is kell
hozzá semmilyen Higgsfield-belépés, és ezért nem tud kárt okozni: a legrosszabb, ami
történhet, hogy elfogadsz valamit, amit nem kellett volna. Azt vissza tudod vonni.

A gyártás marad a gépen.

## Beállítás — egyszer kell

### 1. Készíts egy botot

A Telegramban keresd meg a **@BotFather** nevű fiókot, és írd be neki: `/newbot`.
Kérdezni fog egy nevet és egy felhasználónevet. A végén ad egy hosszú kódot — ez a
**token**. Tedd el.

### 2. Kérd le a saját azonosítódat

Keresd meg a **@userinfobot** nevű fiókot, és írj neki bármit. Válaszul megmondja a
számokból álló azonosítódat. Ez kell ahhoz, hogy a bot csak neked válaszoljon.

### 3. Add meg a rendszernek

Írd meg Claude-nak sima mondatban, a **Code** fülön:

> Állítsd be a telefonos jóváhagyást. A token: <ide a tokent>, az azonosítóm: <ide a számot>

Ő beállítja és leellenőrzi. A tokent ne írd be sehova máshova.

## Használat

Amikor van jóváhagyni való, szólj Claude-nak, hogy indítsa el a telefonos jóváhagyást.
Onnantól a botodnak ezeket írhatod:

- `/varo` — küldje ki, ami jóváhagyásra vár
- `/allapot` — hol tart a munka
- `/koltseg` — mennyi kredit ment el eddig
- `/megse` — ha meggondoltad magad egy visszadobásnál

A képek **fájlként** érkeznek, nem képként. Ez szándékos: így nem tömöríti őket a
Telegram, és látszanak az apró részletek — az ujjak, az arc, a háttérbe került betűk.
Pont azok, amiken el szokott csúszni egy AI-kép.

## Amit tudni kell

**A gépnek futnia kell.** A bot a te gépeden fut. Ha lecsukod a laptopot, a telefonon
nem történik semmi. Ugyanaz a korlát, mint a napi előkészítésnél.

**Csak neked válaszol.** Más nem tud vele beszélni, és a gombokat sem tudja megnyomni
senki más.

**Egy munkára figyel egyszerre.** Ha több projekted fut, arra indítsd el, amelyiknél épp
jóváhagyás kell.

## Ha nem működik

Kérd meg Claude-ot, hogy futtassa le az ellenőrzést — megmondja, mi hiányzik: a token,
az azonosító, vagy a projekt. Ha a bot elindult, de nem ír semmit, valószínűleg nincs
jóváhagyásra váró anyag; próbáld a `/varo` parancsot.
