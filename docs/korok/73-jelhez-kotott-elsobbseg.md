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

*(a futtatás után)*
