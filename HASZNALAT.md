# Jóváhagyás telefonról — teljes útmutató

Ezzel a telefonodon nézheted át és hagyhatod jóvá az elkészült képeket, nem kell a gép
előtt ülnöd. Androidra és iPhone-ra is ugyanígy működik, a pár eltérést jelzem.

**Ez választható kiegészítő.** A rendszer nélküle is teljesen működik. Ha most nem
akarsz vele foglalkozni, nyugodtan hagyd ki, és később bármikor visszatérhetsz rá.

---

## Mit fog tudni, és mit nem

A telefonodra megérkeznek az elkészült képek, két gombbal: **Elfogadom** és
**Visszadobom**. Ha visszadobsz valamit, megkérdezi, mi a baj vele, és a válaszod
bekerül a munkába — a következő próbálkozás abból dolgozik.

**Generálni nem tud, és pénzt sem tud költeni.** Nincs benne olyan gomb. Ezért nem is
kell hozzá semmilyen Higgsfield-belépés, és ezért nem tud kárt okozni.

Egy dolgot előre tudj: **a gépednek közben bekapcsolva és ébren kell lennie.** A bot a
te gépeden fut, nem a felhőben. Ez a gyakorlatban nem gond — legenerálsz egy adagot,
elindítod, és amíg ebédelsz vagy sétálsz, telefonról átnézed. Lecsukott laptoppal viszont
nem működik.

---

## 1. rész — Telegram a telefonra

Ha már használsz Telegramot, ugorj a 2. részre.

### Androidon

1. Nyisd meg a **Play Áruház** alkalmazást.
2. Fent a keresőbe írd be: `Telegram`.
3. Válaszd a **Telegram** nevű alkalmazást (kék, papírrepülő ikon, a fejlesztő
   „Telegram FZ-LLC").
4. Koppints a **Telepítés** gombra, majd ha kész, a **Megnyitás** gombra.

### iPhone-on

1. Nyisd meg az **App Store** alkalmazást.
2. Alul koppints a **Keresés** fülre, és írd be: `Telegram`.
3. Válaszd a **Telegram Messenger** alkalmazást (kék, papírrepülő ikon).
4. Koppints a **Letöltés** vagy a felhő ikonra, majd ha kész, a **Megnyitás** gombra.

### Regisztráció (mindkettőn ugyanaz)

1. Koppints a **Start Messaging** gombra.
2. Add meg a telefonszámodat, országhívóval együtt (Magyarország: +36).
3. SMS-ben kapsz egy kódot, azt írd be.
4. Add meg a keresztnevedet. Vezetéknév nem kötelező.

Kész. A Telegram most már működik a telefonodon.

---

## 2. rész — Készíts egy botot

A „bot" itt egy saját beszélgetőpartner, ami a képeket küldi majd neked. Egyszer kell
létrehozni.

1. A Telegramban koppints fent a **nagyítóra** (keresés).
2. Írd be: `BotFather`.
3. A találatok közül válaszd azt, ahol a név mellett **kék pipa** van. Fontos, hogy ezt
   válaszd — több hasonló nevű, hamis fiók is van.
4. Koppints alul a **START** gombra.
5. Írd be az üzenetmezőbe: `/newbot`, és küldd el.
6. Megkérdezi a bot nevét. Írd be például: `Videó jóváhagyás`. Ez csak megjelenő név,
   bármi lehet.
7. Megkérdezi a felhasználónevet. Ennek **egyedinek kell lennie, és `bot`-ra kell
   végződnie**. Próbáld például: `kovacs_video_jovahagyas_bot`. Ha foglalt, szól, és
   kérhetsz másikat.
8. Ha sikerült, egy hosszú üzenetet kapsz. Ebben van egy sor, ami így néz ki:

   ```
   1234567890:AAF-abcdefGHIJKLmnopQRS_tuvWXyz12345
   ```

   **Ez a token.** Erre lesz szükség.

### A token mentése

Koppints hosszan a tokenre, és válaszd a **Másolás** lehetőséget. Utána küldd el
magadnak: a Telegramban keresd meg a saját nevedet (**Mentett üzenetek** / **Saved
Messages**), és illeszd be oda. Így nem vész el.

**A token olyan, mint egy jelszó.** Ne oszd meg senkivel, és ne tedd ki nyilvános
helyre. Ha véletlenül mégis kikerülne, a BotFathernek írd be: `/revoke`, és kapsz újat.

---

## 3. rész — Kérd le a saját azonosítódat

Erre azért van szükség, hogy a bot csak neked válaszoljon, és más ne tudja megnyomni a
gombokat.

1. A Telegramban koppints a **nagyítóra**.
2. Írd be: `userinfobot`.
3. Válaszd a találatot, és koppints a **START** gombra.
4. Azonnal válaszol. A válaszban keresd az **Id** sort — egy 8–10 jegyű szám, például
   `123456789`.
5. Ezt is másold be a **Mentett üzenetek** közé.

---

## 4. rész — Add meg a rendszernek

Most menj a gépedhez.

1. Nyisd meg a **Claude alkalmazást**, és menj a **Code** fülre.
2. Nyisd meg azt a mappát, amiben a videós munkáid vannak.
3. Írd be a beírómezőbe, sima mondatként — a saját adataiddal:

   > Állítsd be a telefonos jóváhagyást. A bot tokenje:
   > 1234567890:AAF-abcdefGHIJKLmnopQRS_tuvWXyz12345
   > Az én Telegram-azonosítóm: 123456789

4. Claude beállítja, és leellenőrzi, hogy minden rendben van-e. Ha valami hiányzik,
   megmondja, mi.

**A tokent máshova ne írd be.** Ne másold fájlokba, ne küldd el senkinek.

---

## 5. rész — Az első jóváhagyás

1. A gépen csináld végig a szokásos munkát addig, amíg elkészülnek a képek.
2. Amikor jóváhagyás következik, mondd Claude-nak:

   > Indítsd el a telefonos jóváhagyást.

3. A telefonodon a botod ír egy üzenetet, hogy elindult.
4. Írd be neki: `/varo`
5. Megérkeznek a képek, mindegyik alatt két gombbal.

### Hogyan nézd meg a képet rendesen

A képek **fájlként** érkeznek, nem sima képként. Ez szándékos: így nem tömöríti őket a
Telegram, és látszanak az apró részletek — az ujjak, az arc, a háttérbe került betűk.
Pont ezeken szokott elcsúszni egy AI-kép.

- **Androidon**: koppints a fájlra, és megnyílik a képnézegetőben. Két ujjal nagyíthatsz.
- **iPhone-on**: koppints a fájlra, majd ha kell, a jobb felső **megosztás** ikonnal
  nyithatod meg teljes méretben.

Mindig nagyíts rá az arcra és a kezekre, mielőtt elfogadod.

### A döntés

- **Elfogadom** — mehet tovább, nincs több teendőd.
- **Visszadobom** — a bot megkérdezi, mi a baj. Írd le egy mondatban, például:
  *„a kabát gombos lett, sima kell"*. Ez lesz a javítás alapja.
- Ha meggondoltad magad a visszadobás közben: írd be, hogy `/megse`.

---

## 6. rész — Napi használat

Amikor van jóváhagyni való, ezeket írhatod a botnak:

| Amit beírsz | Mi történik |
|---|---|
| `/varo` | kiküldi, ami jóváhagyásra vár |
| `/allapot` | megmutatja, hol tart a munka |
| `/koltseg` | mennyi kredit ment el eddig |
| `/megse` | megszakítja a folyamatban lévő visszadobást |

Nem kell megjegyezned őket: ha csak írsz neki bármit, kiírja a listát.

### Értesítések

Hogy ne maradj le róla, amikor megjönnek a képek:

- **Androidon**: nyisd meg a beszélgetést a bottal, koppints fent a nevére, és
  ellenőrizd, hogy az **Értesítések** be van kapcsolva.
- **iPhone-on**: ugyanez, plusz a telefon **Beállítások → Értesítések → Telegram**
  részén engedélyezned kell az értesítéseket.

---

## 7. rész — Ha valami nem működik

**A bot nem ír semmit, amikor elindítom.**
Valószínűleg nincs jóváhagyásra váró anyag. Írd be neki: `/varo`. Ha azt írja, hogy most
nincs mit jóváhagyni, akkor minden rendben, csak még nem készült el semmi.

**Nem érkeznek meg a képek, pedig elindult.**
Nézd meg, hogy a géped nem aludt-e el. A bot a te gépeden fut — ha lecsukod a laptopot
vagy elalszik, a telefonon nem történik semmi.

**Nem jelennek meg a gombok a képek alatt.**
Szólj, és megnézzük. Ez beállítási hiba, nem a te hibád.

**Elfogadtam valamit, amit nem kellett volna.**
Nem baj. Mondd meg Claude-nak a gépen, hogy melyiket kellene visszavonni, és
visszaállítja.

**Nem találom a tokent.**
A Telegramban a **Mentett üzenetek** között keresd. Ha nincs meg, a BotFathernek írd be:
`/mybots`, válaszd ki a botodat, és az **API Token** menüpontban újra megnézheted.

**Valaki más is használni tudná a botomat?**
Nem. A bot minden más feladót válasz nélkül eldob, és a gombokat sem tudja más megnyomni.

---

## Amit érdemes megjegyezni

A bot **nem költ pénzt** — csak megmutat és rögzíti a döntésedet.

A **géped legyen ébren**, amíg a telefonról dolgozol.

A képeket **nagyítsd fel**, mielőtt elfogadod. Az apró hibák — hatujjú kéz, olvashatatlan
felirat a háttérben — telefonon is kiszúrhatók, ha ránézel.

A **visszadobás indokát írd le konkrétan**. A „nem tetszik" nem elég, abból nem lesz jobb
a következő. A „túl sötét az arca" vagy „a termék nem látszik rendesen" viszont igen.
