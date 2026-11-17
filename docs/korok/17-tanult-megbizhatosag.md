# 17. kör – Tanult forrás-megbízhatóság: kontextus vagy hazug?

## Kiindulás

A 16. kör E3 kísérletében rögzített forrás-hitelesség mellett a „kontextus-szétválasztás vagy
elutasítás” döntés csak egy szűk, a feladat méretétől függő `c_ctx` sávban volt helyes. A 12.
kör V2 védekezését vezettem be: minden forrás hibaaránya tanult.

## Formalizálás

- **Előzetes eloszlás:** a forrás hibaaránya `r_s ~ Beta(κ·(1−q_s), κ·q_s)`, ahol `q_s` a
  forrás deklarált hitelessége (az előzetes átlag), κ pedig az, hogy hány megfigyelésnyi
  súlya van a deklarációnak.
- **Kódhossz:** egy forrás elfogadás/elutasítás sorozatát a béta-binomiális marginális
  valószínűség kódolja:
  `L_s = log₂ B(κq, κ(1−q)) − log₂ B(κq + n_s − k_s, κ(1−q) + k_s)`,
  ahol n_s a forrás megfigyeléseinek száma, k_s az elutasítottaké. Ez helyettesíti a
  megfigyelésenkénti `−log₂ q` és `−log₂(1−q)` tagokat.
- **Hatás:** egy forrás, amelyet a hipotézis sokszor elutasít, egyre olcsóbban tévedhet.
  A hibaarányát a rendszer megtanulja.

## Eredmények (n entitás, két forrás ütközik, c_ctx = 6 rögzítve)

| κ | n = 4 | n = 8 | n = 16 | n = 32 |
|---|---|---|---|---|
| 10 | elutasít; **a sorrend dönt** | elutasít; a sorrend dönt | elutasít; a sorrend dönt | elutasít; a sorrend dönt |
| 30 | elutasít (kevés az evidencia) | **helyes** mindkét esetben | **helyes** | **helyes** |
| 100 | elutasít | **helyes** | **helyes** | **helyes** |
| 300 | elutasít | helyes | helyes | **zajnál is szétválaszt ✘** |

(helyes = rendszerszerű ütközésnél szétválaszt, zajnál a zajos forrás állításait utasítja el)

**Összevetés:** rögzített megbízhatósággal ugyanebben a rácsban egy `c_ctx` sem volt
helyes minden n-re. Tanulttal κ ∈ [30, 100] mellett n ≥ 8 esetén minden méretben helyes.
A szabad paraméter megmaradt, de **a helyes sáv a feladat méretétől függetlenné vált.**

## A κ = 10 eset: megerősítési torzítás

Gyenge előzetes eloszlás mellett a rendszer a következőt teszi:
1. Az elsőként érkező forrás (A) egybehangzó tényeiből **szabályt indukál** („a daxok
   mérgesek”). Ettől A tényei tömörebbek, olcsóbbak lesznek.
2. A később érkező, ellentmondó forrás (B) összes állítását elutasítja. A hibaaránya gyorsan
   1-re tanulódik, így minden további elutasítás szinte ingyenes.
3. **Ha a sorrendet megfordítjuk, B nyer, és A lesz a „hazug”.**

Ez a megerősítési torzítás formális mechanizmusa: indukció plusz tanult megbízhatóság. Nem
mi építettük be szándékosan, a pontszámból következik.

## Az alapvető korlát: az identifikálhatóság

Egy forrás, amely *mindig az ellenkezőjét* mondja, két, tömörítés szempontjából közel
egyenértékű módon magyarázható:
- **„más kontextusról beszél”** (szétválasztás);
- **„hazudik”** (elutasítás tanult hibaaránnyal).

**Csak az adatokból ez nem dönthető el.** A döntést mindig valamilyen előzetes eloszlás hozza:
itt κ és `c_ctx`, emberben valószínűleg a forrásról szóló háttértudás. Három kiút van:
1. **Háttértudás a forrásról:** például B egy másik völgyről ír. Ez egy kontextus-jel, és
   pontosan ezt kérdezi a 13. kör M4 tagadása és az 5. kör F-ötlete (a kontextus-jel az LLM
   aktivációiból).
2. **Aktív kérdezés** (13. kör, A-ötlet): olyan kérdés, amelyre a két magyarázat mást jósol.
   Például: „B szerint is igaz-e, hogy a daxok ugyanazok az állatok?”
3. **Az indukció kontextusfüggővé tétele:** most csak a globális kontextusban indukál.
   Emiatt a szétválasztott hipotézis hátrányban van. **Ezt javítani kell, mielőtt a κ-sávot
   véglegesnek tekintjük.**

## Mit vesz el és mit ad ez a kör?

- **Ad:** egy méretfüggetlen, értelmezhető paramétert (κ = mennyire bízunk a deklarált
  hitelességben), és egy cáfolható jóslatot. Gyenge előzetes eloszlásnál sorrendhatás
  várható, erősnél nem.
- **Elvesz:** azt a reményt, hogy a kontextus-szétválasztás „magától” helyesen működik.
  Elvben kell hozzá egy külső jel. Az ARLC-nek ezt a jelet az LLM-ből kellene kapnia, és ezzel
  az L1 lyuk (az LLM pótolhatósága) egy új, konkrét helyen jelenik meg: **a kontextus-jel
  forrásaként.**
