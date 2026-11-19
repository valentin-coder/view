# 70. kör – Típusbizonytalanságot továbbító π (előregisztrált)

## 1. rész: előregisztráció (a futtatás előtt commitolva)

### Miért

A 66. kör szerint egy téves, magabiztos forrástípus esetenként összeomlást okoz. Javaslat: a típusbecslés
bizonytalanságát is továbbítani kell. Ha az osztályozó kalibrált (a becsült típus valószínűsége a, a többi háromé
(1 − a)/3), a keverék-prior pontosan egyetlen π_eff = Σ_t P(t | becslés)·π(t) értékre esik össze, mert a komponensei
(κ₁, q₀, κ₀) típusonként közösek.

| becsült típus | π (kemény) | π_eff, a = 0,8 | π_eff, a = 0,9 |
|---|---|---|---|
| gondozott | 0,999 | 0,943 | 0,971 |
| rivális iskola | 0,5 | 0,577 | 0,538 |
| szakértő | 0,95 | 0,907 | 0,928 |
| pletyka | 0,7 | 0,723 | 0,712 |

### Előzetes elemzés (a futtatás előtt)

A lágyítás **kevés védelmet ad**: egy téves „gondozott” címke a = 0,9 mellett is π_eff = 0,971-et ad (a gestalt-váltás
akadálya marad), egy téves „rivális iskola” címke 0,538-at (a félretevés olcsó marad). **És van ára:** a *helyes*
„gondozott” címke π_eff-je 0,971 (nem 0,999), így a teljes félretevés kb. 10 helyett kb. 5 bitbe kerül. Az A
populációban ez *több* félretevést jósol.

### Elrendezés

Kód: [`run_r70.py`](../../experiments/arlc/arlc/run_r70.py). Seedek **11000–11014** (friss), típusok: átkategorizálás,
szabály-helyesbítés, hazug forrás; A és C populáció: 90 eset. Módszerek: v4.4e; v4.8-π kemény és lágy π-vel, a = 0,8 és 0,9
(a 66. kör szimulált osztályozójával).

### Hipotézisek

- **H70a (C):** a tévesen osztályozott esetekben a lágy π post-acc-ja nagyobb a keményénél (átlag).
- **H70b (A):** a lágy π az A-ban *több* félretevést ad, mint a kemény (a fenti elemzés jóslata).
- **H70c (összesen):** a lágy és a kemény π post-acc-ja közti különbség |Δ| < 0,02 (világok szerinti bootstrap): a
  lágyítás átlagban nem számít.

## 2. rész: eredmények

90 eset (A és C, 45–45); nyers adat és elemzés: [`results/kor-70/`](../../experiments/arlc/results/kor-70/).

| | A post | A tankönyv félretéve | C post | C helyes gestalt-váltás |
|---|---|---|---|---|
| v4.4e | 0,824 | – | 0,380 | – |
| kemény, a = 0,8 | 0,824 | 0 | 0,608 | 26/45 |
| **lágy**, a = 0,8 | 0,804 | **2** | **0,627** | 28/45 |
| kemény, a = 0,9 | 0,824 | 0 | 0,636 | 27/45 |
| **lágy**, a = 0,9 | 0,810 | **1** | 0,640 | 28/45 |

| hipotézis | eredmény | ítélet |
|---|---|---|
| **H70a (C):** a tévesen osztályozott esetekben lágy > kemény | a = 0,8: 0,618 vs. 0,574 (20 eset); a = 0,9: 0,527 vs. 0,507 (8 eset) | **teljesül** |
| **H70b (A):** a lágy π több félretevést ad | 2 és 1 vs. 0 és 0; post 0,804/0,810 vs. 0,824 | **teljesül** (az előzetes elemzés jóslata) |
| **H70c:** \|lágy − kemény\| < 0,02 | +0,000 [−0,028; +0,023]; −0,005 [−0,023; +0,006] | **pontbecslésben teljesül**, a CI a = 0,8-nál szélesebb a ±0,02-nél |

### Értelmezés

1. **A lágyítás egy kicsi, kétirányú cserét hoz:** a C-ben a tévesen osztályozott esetek javulnak, az A-ban a helyesen
   osztályozottak romlanak, mert a „gondozott” címke π_eff-je 0,971 lesz a 0,999 helyett. **Átlagban nem számít.** Ezt
   az előzetes elemzés pontosan megjósolta.
2. **A 60. kör fő eredménye friss seedeken (11000–11014) megismétlődik:** a C-ben a v4.8-π 0,61–0,64 a v4.4e 0,38-ával
   szemben, 58–62%-os helyes gestalt-váltással, és 0,8–0,9-es típuspontosság mellett is.
3. **Tanulság a B fázisra:** a típusbecslés bizonytalanságának továbbítása (π_eff) önmagában nem véd a téves típusok
   ellen. Ehhez az kellene, hogy a *kalibrált* bizonytalanság a valóban nehéz esetekben legyen nagy, a könnyűekben
   kicsi. Egy egyenletes a-val modellezett osztályozó ezt nem tudja, egy valódi LLM-osztályozó talán igen.
