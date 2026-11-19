# 73. kör – Jelhez kötött kontextuson belüli elsőbbség (előregisztrált)

## 1. rész: előregisztráció (a futtatás előtt commitolva)

A 71. kör szerint a kontextuson belüli elsőbbség jó jellel együtt +0,20-at hoz a „más régió” célkérdésein, de jel nélkül
az ellenőrző csomag E3-ját (kontextus vagy elutasítás) 0,75-ről 0,5-re rontja. Javaslat: **az elsőbbség csak a jel által
„más kontextusnak” jelzett forrásra érvényes** (`ctx_override_sources`). Jel nélkül (mint az E3-ban) így nincs
elsőbbség.

Kód: [`run_r73.py`](../../experiments/arlc/arlc/run_r73.py). A populáció, seedek **13000–13019** (friss), „hazug forrás” és
„más régió” (40 eset). Mind v4.8-π + kontextusjel (a = 0,99); változatok: elsőbbség nélkül, elsőbbség minden izolált
forrásra (71. kör), elsőbbség csak a jelzett forrásra.

**Hipotézisek:**
- **H73a:** a „más régió” célkérdésein a jelzett elsőbbség target-acc-ja legalább 0,1-gyel nagyobb az elsőbbség nélkülinél
  (a 71. kör +0,197-ének ismétlése, óvatosabb küszöbbel).
- **H73b:** a jelzett és a teljes elsőbbség target-acc-ja között |Δ| < 0,05 (a jó jelnél a kettő szinte ugyanaz).
- **H73c:** az ellenőrző csomagban a jelzett elsőbbség E3-ja 0,75 (jel nélkül nincs elsőbbség, ezért azonos a v4.8-π-vel).

## 2. rész: eredmények

40 eset; nyers adat: [`results/kor-73/`](../../experiments/arlc/results/kor-73/).

| típus | jel (post / target) | jel + elsőbbség | jel + jelzett elsőbbség | régióforrás izolálva |
|---|---|---|---|---|
| hazug forrás | 0,847 / 0,825 | 0,847 / 0,825 | 0,847 / 0,825 | – |
| más régió | 0,837 / 0,282 | 0,832 / 0,344 | 0,832 / 0,344 | 1 → 4 → 4 (20-ból) |

| hipotézis | eredmény | ítélet |
|---|---|---|
| **H73a:** más régió target: jelzett elsőbbség − jel ≥ 0,1 | **+0,062** [0,000; +0,175] | **nem teljesül** |
| **H73b:** \|jelzett − teljes elsőbbség\| < 0,05 | 0,000 | **teljesül** (azonos) |
| **H73c:** ellenőrző csomag E3 = 0,75 a jelzett elsőbbséggel (jel nélkül) | **0,75** | **teljesül** (a 71. körbeli kár megszűnt) |

### Értelmezés

1. **A jelhez kötés a kárt költségmentesen megszünteti:** jel nélkül nincs elsőbbség (E3 = 0,75), jó jellel ugyanazt adja,
   mint a teljes elsőbbség.
2. **A hatás nagysága friss seedeken kisebb:** a 71. kör +0,197-e itt +0,062, és nem szignifikáns. A régióforrást 4-szer
   izolálja (jel+elsőbbség nélkül 1-szer). A 62. kör szerint a „más régió” eset sok seeden holtverseny-közeli, ezért egy
   20 seedes halmazon a hatás erősen ingadozik. **A 71. kör eredményét ezért óvatosan kell kezelni: az irány két független
   halmazon is ugyanaz, a nagyság bizonytalan.**
