# Folytonosság

Ezt a `look` réteg előtt kötelező elolvasni. A többjelenetes AI-videó itt szokott elbukni, nem a promptírásnál.

## Mi romlik el

A bunda árnyalata jelenetenként elcsúszik. A kabát hirtelen gombos lesz. A helyszín ugyanaz akar lenni, mégis más az utcabútor. A fény iránya jelenetről jelenetre ugrik. A modell mindezt boldogan jelenti késznek, mert nincs eszköze arra, hogy megítélje a saját eredményét. Az ellenőrzés emberi feladat, és ezért van a 4. rétegben kapu.

## Három kapaszkodó

**Karaktertanítás.** Egy szereplőt referenciafotókból megtanítasz, és onnantól azonosítóval hivatkozol rá. Ez a legerősebb eszköz visszatérő szereplőhöz, viszont fizetős és időigényes, tehát csak akkor éri meg, ha a karakter több jelenetben szerepel. Tanításhoz egységes stílusú, éles képek kellenek, vegyes stílusú vagy homályos anyag rontja az eredményt.

**Referenciakép.** Kevesebb jelenetnél elég, ha minden kezdőkocka generálásához odaadod ugyanazt a referenciaképet. Olcsóbb, gyorsabb, cserébe lazább a hasonlóság.

**Kockaláncolás.** Az előző jelenet utolsó kockáját adod az következő kezdőkockájának kiindulásul. Ezt a `continuity_from` mező jelöli a jelenetlistában, és a `project.py` ebből épít függőséget, tehát a lánc közepén végzett módosítás automatikusan elévülteti a rá következő jeleneteket. Vágás nélküli folytatáshoz ez a legjobb megoldás.

## Stíluskód

A `look.stilus` és a `look.paletta` szövege minden angol promptba szó szerint bekerül, változatlanul. Ne fogalmazd át jelenetenként, mert a legkisebb eltérés is más képi világot ad. Ha a stíluskódon változtatsz, minden kezdőkocka elévül, és ez így helyes.

## Ellenőrzőlista jóváhagyás előtt

Nézd végig a kezdőkockákat egymás mellett, ne egyenként. Ugyanaz az arc, ugyanaz a ruha, ugyanaz a fényirány. Nézd meg a kezeket és az ujjak számát. Nézd meg a feliratokat és a logókat a képen, mert a modellek szeretnek olvashatatlan szöveget rajzolni a háttérbe. Ha bármi eltér, `reject` a node-ra, és az indokot írd bele, mert a következő futásnál az lesz a javítás alapja.

## Amit nem lehet megoldani

Az ügyfél arcának pontos visszaadása kockázatos, valós személy megjelenítéséhez írásos hozzájárulás kell. Márkalogó pontos rajzolására ne a generátort használd, hanem utómunkában helyezd rá. Létező védett karakter vagy filmes látványvilág másolása jogi kockázat, ügyfélmunkában kerüld.
