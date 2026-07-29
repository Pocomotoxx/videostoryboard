# Jelenetnyelvtan

Ezt a `shotlist` réteg előtt olvasd el. A `prompt_en` mezőbe kerülő angol kifejezéseket használd, a magyar megnevezés az ügyfélnek szóló `leiras` mezőhöz való.

## Gépállás

| Kód | Angol | Magyar | Mire jó |
|-----|-------|--------|---------|
| ELS | extreme long shot | totál | helyszín bemutatása, léptékérzet |
| WS | wide shot | nagytotál | szereplő a környezetében |
| FS | full shot | egészalakos | testbeszéd, járás |
| MS | medium shot | szekond | párbeszéd, cselekvés |
| MCU | medium close up | mellkép | arckifejezés és gesztus együtt |
| CU | close up | közeli | érzelem |
| ECU | extreme close up | szuperközeli | részlet, feszültség |

## Szög

`eye-level` semleges. `low angle` erőt és fenyegetést ad. `high angle` kiszolgáltatottságot. `over the shoulder` kapcsolatot két szereplő között. `dutch angle` nyugtalanságot, óvatosan bánj vele, mert AI-modelleknél gyakran túlzásba viszi.

## Kameramozgás

`static`, `slow push in`, `pull out`, `pan left/right`, `tilt up/down`, `tracking shot`, `handheld`, `crane up`, `orbit`.

A modellek nem egyformán kezelik a mozgást. A lassú, egytengelyű mozgás megbízható. Az összetett utasítás, például egyszerre svenk és zoom, jellemzően torzuláshoz vezet. Egy jelenet egy mozgást kapjon.

## Promptszerkezet

Az angol prompt bevált sorrendje: gépállás és szög, alany és cselekvés, környezet és fény, kameramozgás, végül a technikai stílusblokk. A stílusblokk minden jelenetnél szó szerint ugyanaz legyen, mert ez tartja össze a látványt.

Példa a sorrendre:

```
Close up, low angle. [alany és cselekvés]. [környezet, fény].
[kameramozgás]. 35mm, shallow depth of field, cinematic film grain,
muted cold blue palette.
```

## Modellválasztás

Kezdőkockához képmodell való, mozgáshoz a kép-videó irány. Szöveg-videó generálást csak akkor használj, ha nincs jóváhagyott kezdőkocka, ami ebben a folyamatban nem fordulhat elő. Kezdő- és végkocka vezérlést támogató modellt válassz, ha két jelenet között sima átmenet kell.

## Dramaturgiai ökölszabályok

Vágókép hossza két és hat másodperc között tartható jól. Nyitóképnek legyen levegője, zárókép maradjon a képen egy ütemmel tovább. Ne kövessen közelit közeli ugyanarról az alanyról, mert ugrásnak látszik. Ha a jelenet nem visz előre semmit, ki kell venni, mert minden jelenet kreditbe kerül.
