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

*(a futtatás után)*
