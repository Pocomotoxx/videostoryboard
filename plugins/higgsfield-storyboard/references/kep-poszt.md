# Képes poszt

Ezt akkor olvasd el, ha a végtermék nem videó, hanem álló kép vagy képsorozat:
közösségimédia-poszt, karusszel, termékfotó, hirdetési kreatív.

## Mikor kép, és mikor videó

A döntő szempont többnyire nem esztétikai, hanem költség és kapacitás.

Egy kép nagyságrenddel olcsóbb, mint egy videójelenet: a kép egyszeri díj, a mozgókép
másodpercenként fogy. Egy háromlapos karusszel jellemzően annyiba kerül, mint egy
másodpercnyi mozgókép. **Ezért a rendszeres, napi jelenléthez a kép a járható út**, a
videó pedig a kiemelt tartalomé.

Videó kell, ha mozgás, folyamat vagy időbeli változás a mondanivaló: hogyan használják,
mi történik, mi lesz belőle. Kép elég, ha állapotot mutatsz: hogy néz ki, mi az ajánlat,
mi a három érv.

## Hogyan illeszkedik a folyamatba

A képes poszt ugyanaz a futószalag, csak a drága fele hiányzik. A tétel `tipus` mezője
`kep`, és ilyenkor **a kezdőkocka maga a végtermék**, nem közbülső lépés — nem készül
belőle mozgókép, nincs összefűzés és nincs hang.

A rendszer ezt magától kezeli: képes tételhez nem épít mozgás-node-ot, és tisztán képes
projektnél az összefűzés és a hang réteg meg sem jelenik.

A brief, a kezelés, a látvány és a folytonosság viszont **ugyanúgy érvényes**. Egy
karusszel pontosan attól működik, hogy a lapjai egy világból valók.

## Karusszel

A karusszel több tétel, nem egy. Minden lap külön sor a listában, sorrendben.

A dramaturgia más, mint videónál: itt nincs kényszerített idő, a néző maga lapoz. Ezért
**az első lap dolga, hogy lapozásra bírja** — ugyanaz a logika, mint a videó nyitó két
másodpercénél, lásd `nyitohook.md`. Az utolsó lapon legyen kimondva, mit tegyen.

Négy-hat lap a jól kezelhető tartomány. Ennél több ritkán jut el a végéig.

## Szöveg a képen: ne generáltasd

Ez a leggyakoribb hiba. A képgeneráló modellek **olvashatatlan vagy hibás betűket
rajzolnak**, magyar ékezetekkel különösen. Ha a promptban szöveget kérsz, hibás szöveget
kapsz — és a poszt épp attól lesz használhatatlan.

A helyes út: a képet szöveg nélkül generáltasd, üresen hagyott, nyugodt felülettel, ahová
a felirat kerül. A szöveget utómunkában helyezed rá, a `look.brand` szerinti betűtípussal
és színnel. Ugyanez vonatkozik a logóra.

A promptban ezt **állításként** fogalmazd meg, ne tiltásként — „tiszta, üres felület a kép
felső harmadában" —, mert a tagadást több modell nem értelmezi. Lásd `prompt-iras.md`.

## Képarányok

A közösségi felületeken a négyzetes és az álló formátum viszi a legtöbb helyet a
képernyőn. A `4:5` álló és az `1:1` négyzetes a legbiztosabb választás hírfolyamhoz,
a `9:16` a teljes képernyős felületekhez való.

Ha ugyanaz a poszt több helyre megy, **ne vágd át utólag** — a fontos tartalom
elcsúszhat. Inkább generáld le a kellő képarányokban, vagy komponálj úgy, hogy a lényeg
biztonságos középen legyen.

## Termékfotó és hirdetési kreatív

Ha kész termékképből kell hirdetési látvány, arra a platformnak külön képmodellje van —
ugyanaz a logika, mint a `reklam-marketing-studio.md`-ben leírt videós ágnál, csak
állóképre. Ilyenkor a termékkép bemenet, nem generált tartalom, tehát a termék pontosan
úgy néz ki, ahogy a valóságban.

## A poszt szövege is a munka része

A kép önmagában nem poszt. A leszállítandó anyaghoz tartozik a **kísérőszöveg**, a
javasolt hashtagek, és ha AI-generált a kép, az arra vonatkozó jelölés. Ezeket a
`brief.md` célja és hangneme alapján írd meg, magyarul, a `magyar-helyesiras` és a
`magyar-termeszetes-stilus` skillek szerint.

Ne ígérj elérést és ne javasolj napi tömeges posztolást: a platformok a jelöletlen vagy
tömegtermelt szintetikus tartalmat visszafogják.
