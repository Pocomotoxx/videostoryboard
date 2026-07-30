# Gyakori kérdések

## Hol és hogyan használom

**Hova kell beírni a parancsokat?**
A Claude **asztali alkalmazásba**, azon belül a **Code** fülre. Ott van egy beírómező,
ugyanolyan, mint egy csevegőablakban — minden oda megy. Ha perjelet írsz be, feljön a
választható parancsok listája.

**A szokásos Claude-beszélgetésben nem működik?**
Nem. Az a felület nem éri el a gépeden lévő fájlokat, és nem tud videót készíteni.
A rendszernek az asztali alkalmazás **Code** füle kell. Ez a leggyakoribb félreértés.

**Meg kell nyitnom valamilyen mappát?**
Igen, a Code fülön kiválasztod, melyik mappában dolgozol. Készíts egy újat, például
„videok" néven — ebben fognak létrejönni a munkáid, mindegyik külön almappában.

**Kell terminált használnom?**
Nem. Ha valamihez mégis parancs kellene, írd meg Claude-nak sima mondatban, hogy csinálja
meg — ő futtatja, te csak jóváhagyod.

**Azt írja, hogy nincs ilyen skill. Most mi van?**
Először ellenőrizd, hogy a telepítés tényleg befejeződött: írd be, hogy `/plugin`, és
nézd meg, szerepel-e a listában a `higgsfield-storyboard` bekapcsolt állapotban. Ha igen,
írd be, hogy `/reload-plugins`, vagy indítsd újra az alkalmazást. Utána írj be egy sima
perjelet, és válaszd ki a listából a `video` bejegyzést — így nem lehet elgépelni.
Ha továbbra sem megy, egyszerűen mondd el sima mondatban, mit szeretnél: a rendszer a
feladat leírásából is elindul, perjeles parancs nélkül.

**Mi a különbség a perjeles parancs és a sima mondat között?**
A perjellel kezdődő sorok a rendszernek szólnak, például `/mcp`. Minden más sima
beszélgetés Claude-dal: *„csináljunk egy húszmásodperces reklámot ehhez a termékhez"*.

## Pénz és kredit

**Mennyibe kerül egy videó?**
Függ a hosszától és a jelenetek számától, de a rendszer **megmondja előre**, mielőtt
bármit elkezdene. Nagyságrendileg: egy képes poszt pár kredit, egy féloldalas videó több
száz. Ezért is éri meg a rendszeres tartalmat képekből építeni.

**Elfogyhat a keretem véletlenül?**
Nem, ha nem indítasz automata futást. Alapból minden költés előtt megáll és megkérdez.
Automata futásnál pedig te adod meg, mennyit költhet — ha elfogy, megáll, és nem kérdez rá,
hogy folytassa-e.

**Miért mondja, hogy nem tud árat mondani?**
Néhány formátumnál — az avatáros hirdetéseknél, a hangcserénél és a szinkronnál — a
platform nem ad előzetes árat. Ilyenkor csak utólag derül ki, mennyi ment el. A rendszer
ezt előre jelzi, mielőtt elindítanád.

**Csomagot váltottam, kell valamit csinálnom?**
Nem. Minden munkamenet elején megnézi, mennyi kereted van, és ha változott, magától
frissíti.

## A munka menete

**Miért kérdez ennyit? Nem tudná megcsinálni egyben?**
Meg tudná, de az drága lenne. A képgenerálás nem kiszámítható, és a rendszer nem tudja
megítélni, hogy amit csinált, tetszik-e neked. Minden megállás egy hely, ahol olcsón
lehet javítani, mielőtt drágán készülne el rosszul.

**Meg tudom nézni előre, mi lesz belőle, fizetés nélkül?**
Igen, és ezt ajánljuk elsőre. Mondd azt, hogy „nézzük meg kredit nélkül" — elkészül a
teljes terv jelenetekre bontva, az árral együtt, egy kredit nélkül.

**Félbehagytam, hogy folytatom?**
Írd be újra a `/higgsfield-storyboard:video` parancsot ugyanabban a mappában. Megnézi,
hol tartottatok, és onnan viszi tovább. Nem kell emlékezned semmire.

**Elrontottam valamit, baj?**
Nem. Mondd meg, mi nem jó, és javítja. Ha egy jelenetet visszadobsz, csak az arra épülő
dolgok készülnek újra, a többi marad.

## Minőség

**Miért más az arc az egyes jeleneteken?**
Ez az AI-videó legismertebb gyengéje. Három megoldás van rá, és a rendszer ismeri
mindhármat — a legerősebb az, ha a szereplőt betanítjuk fotókból. Ezt egyszer kell
megcsinálni ügyfelenként, utána minden videóban ugyanaz az arc.

**Miért nem ír szöveget a képre?**
Mert a képgenerálók olvashatatlan vagy hibás betűket rajzolnak, magyar ékezetekkel
különösen. Ezért a kép szöveg nélkül készül, üresen hagyott felülettel, és a feliratot
utómunkában tesszük rá — így pontos lesz és a te betűtípusoddal.

**A logót miért nem generálja?**
Ugyanezért. A generált logó torzul, és ez az egyetlen hiba, amit az ügyfél biztosan
kiszúr. Utómunkában kerül rá.

**Miért csak 15 másodperces egy jelenet?**
Ennyit tud egyben a technológia. A hosszabb videó több jelenetből áll össze, amiket a
gépeden fűz egybe — ez ingyenes és akárhányszor ismételhető.

## Automatizálás

**Miért nem tölti fel magától a kész anyagot?**
Mert a közzététel visszafordíthatatlan, és a nevedben történne. A rendszer mindent
előkészít egy mappába — kész fájlok, szöveg, hashtagek —, onnan egyetlen koppintás.
Az időzítést a platform saját ütemezőjével oldd meg.

**Csinálhat naponta videót magától?**
Előkészíteni tud naponta, de nem magától kitalált témából: te írsz fel előre egy listát,
és abból dolgozik. Ez a különbség aközött, hogy hasznos anyagot kapsz reggelre, vagy
általános tartalmat gyártasz, amit senki nem néz meg.

**Napi sok videóval nem lesz nagyobb az elérésem?**
Nem, sőt. A platformok a tömegtermelt és a jelöletlen mesterséges tartalmat visszafogják.
Az elérést az hozza, ha valaki végignézi és megjegyzi, amit csináltál — heti három jó
anyag többet ér napi tíznél.

**Felhőben is futhatna, hogy ne kelljen bekapcsolva hagynom a gépet?**
Sajnos nem. A felhős futásnál nincsenek ott a fájljaid, nincs ott a videóösszefűző, és a
Higgsfield-kapcsolatod sem érhető el onnan. Nekünk a helyi futás kell — az viszont
bekapcsolt, ébren lévő gépet igényel.

**Miért nem futott le az éjszakai előkészítés?**
Valószínűleg mert a gép aludt. Az időzített feladat csak bekapcsolt, ébren lévő gépen
fut le. Ezért javasoljuk a reggeli időpontot a hajnali helyett.

## Technika

**Kell hozzá programozói tudás?**
Nem. A telepítés öt lépés, a használat pedig beszélgetés. Parancsokat nem neked kell
gépelned — azokat a rendszer futtatja.

**Kell telepítenem a Higgsfield parancssori programját?**
Nem. Kényelmi kiegészítő, a rendszer nélküle is teljesen működik. Ha felajánlja, nyugodtan
mondd, hogy nem kell.

**Kérni fogja a jelszavamat?**
Soha. A Higgsfieldbe a saját böngésződben lépsz be, a szokásos módon. Ha bármi mégis
jelszót vagy hozzáférési kulcsot kérne a beszélgetésben, az hibás — ne add meg.

**Hol vannak a fájljaim?**
A saját gépeden, abban a mappában, ahol a munkát elkezdted. Semmi nem kerül fel sehova,
amíg te fel nem töltöd.

## Ügyfélmunka

**Több ügyfélnek is használhatom?**
Igen. Ügyfelenként elmentheted a stílust, és onnantól minden munkájuk ugyanúgy néz ki.
A betanított szereplők is megmaradnak, azokat nem kell újra megcsinálni.

**Mit ígérhetek az ügyfélnek?**
Jóváhagyható képes storyboardot rövid határidőre, onnan néhány nap alatt kész anyagot,
előre kalkulált költséggel és megbeszélt számú javítókörrel. Amit ne ígérj: korlátlan
javítást és azonnali kész filmet.

**Van jogi kockázat?**
Valós személy arcának megjelenítéséhez írásos hozzájárulás kell. Védett karaktert vagy
filmes látványvilágot ügyfélmunkában ne másolj. Az AI-jelölést tedd ki — a rendszer
beleírja a posztszövegbe.
