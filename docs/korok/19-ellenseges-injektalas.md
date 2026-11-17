# 19. kör – Ellenséges injektálás (E5): választja-e el valami a becsületes evidenciát a támadótól?

## Kérdés

A 12. kör szerint elválasztó jel nélkül a plaszticitás és a robusztusság ugyanaz a szám: amennyi
evidencia a becsületes átrendezéshez kell, annyi a támadónak is elég. Elválasztó jel lehet a
forrás **múltja**. Ezt teszteltem a 17. kör tanult megbízhatóságával.

## Elrendezés

- **Világ:** egy szabály („a dax mérges”, könyv, q = 0,95), N alátámasztó tény a `field`
  forrásból, és a `field` egy „múlttal”: R darab ütközésmentes, elfogadott állítás más
  entitásokról.
- **Ellenpéldák** (új entitás: „x egy dax” és „x nem mérges”), a forgatókönyv szerint:
  - *becsületes:* a régóta hiteles `field` forrásból;
  - *sybil:* minden ellenpélda egy új, friss forrásból;
  - *egyetlen támadó:* minden ellenpélda ugyanabból az új forrásból.
- **Mérés:** hány ellenpéldánál esik ki a szabály.

## Első eredmény: a legolcsóbb kiút megkerüli a forrásellenőrzést

Az első változatban a tagságot („x egy dax”) egy harmadik, megbízható forrás közölte, az
ellenpéldát a forgatókönyv forrása. **Mindhárom forgatókönyv ugyanannál a pontnál fordult át, a
tanult megbízhatóság mellett is.** Ennek oka az volt, hogy a szabály megtartásakor a rendszer a
*tagságot* bírálta felül („x valójában nem dax”), nem az ellenpéldát. Az ellenpélda forrásának
megbízhatósága így soha nem került mérlegre.

**Ez a kör egyik fő tanulsága:** a legolcsóbb, helyi magyarázat („ez a kivétel nem is
tartozik ide”) teljesen kikerüli a forrás hitelességének vizsgálatát. Ez ugyanaz a mintázat,
mint a 16. kör 4. hibája (példányszintű ütközés helyett szabályszintű). Valószínűleg ez az
ARLC egyik legfontosabb strukturális gyengesége: **egy támadó, aki a tagságot nem állítja, csak
a tulajdonságot, gyakorlatilag észrevétlen marad, és ugyanígy egy becsületes, hiteles forrás
is figyelmen kívül marad.**

## Második eredmény: a tagságot és az ellenpéldát ugyanaz a forrás közli

| N / múlt (R) | megbízhatóság | becsületes | sybil | egyetlen támadó |
|---|---|---|---|---|
| 6 / 20 | rögzített | 4 | 4 | 4 |
| 6 / 20 | tanult, κ = 30 | **3** | 4 | 4 |
| 12 / 40 | rögzített | 5 | 5 | 5 |
| 12 / 40 | tanult, κ = 30 | **4** | 5 | 6 |
| 20 / 80 | rögzített | 8 | 8 | 8 |
| 20 / 80 | tanult, κ = 30 | **5** | 8 | 9 |
| 20 / 80 | tanult, κ = 100 | **6** | 8 | 8 |

(a cellák: hány ellenpélda kell a szabály kieséséhez)

- **Rögzített megbízhatósággal nincs elválasztás.** Ez megerősíti a 12. kör elméleti állítását.
- **Tanult megbízhatósággal van:** a becsületes, régóta hiteles forrás hamarabb fordít át,
  a támadók ugyanott vagy később, mint rögzítettnél. A 12. kör kritériuma szerint ez **valódi
  elválasztás:** a becsületes plaszticitás nő, a támadó költsége nem csökken.
- **Az elválasztás a beágyazottsággal és a múlt hosszával nő** (1 → 3–4 ellenpélda).
- **A sybilek ellen alig véd:** a sok friss forrás csak eggyel olcsóbb a támadónak, mint az
  egyetlen forrás. A tanult megbízhatóság csak az *ismétlődő* hazugot bünteti; a friss
  források mindegyike az előzetes eloszlás szerinti bizalmat kapja.

## Következmények a tervre

1. **A sybil-védelem nem oldható meg forrásonkénti megbízhatósággal.** Kell a 12. kör V3
   (független megerősítés) mechanizmusa, és vele a függetlenség becslése. Ez a valódi
   Sybil-probléma, és nem tudom, hogy szimbolikusan megoldható-e.
2. **A „tagság felülbírálása mint kiút” ellen** kell egy védelem: a tagság elutasítása
   ne legyen olcsóbb, ha a tagságot független, más tulajdonságokat is jósló evidencia
   támasztja alá. Ezt az ARLC tömörítési tagja elvben adja, de csak akkor, ha az entitásról
   más tények is vannak. Az új entitásokon (x_j) nincs más tény, ezért a kiút nyitva marad.
3. **Előre rögzített kockázat:** egy LLM-alapú groundingnál a forrás gyakran nem is ismert
   (egy dokumentum, egy beszélgetés). Ilyenkor ez az egész védelem nem működik.
