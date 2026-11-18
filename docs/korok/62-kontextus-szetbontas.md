# 62. kör – A 60. kör H60d-kudarcának szétbontása

## 1. rész: jóslatok (a futtatás előtt)

A 60. körben a v4.8 a „más régió” célkérdésein 0,276-tal rosszabb volt, mint a v4.4e. Két jelölt ok: (a) a jel
téves riasztásai (a = 0,9), (b) a keverék-prior / kétszintű csoportosítás a régióforrás állításaira. Két változat
ugyanazon a 60 „más régió” eseten (A, B, C × seed 6000–6019); kód: [`run_r62.py`](../../experiments/arlc/arlc/run_r62.py):
- **v4.8-π:** metaadat-π, jel nélkül, minden forrás kontextusa 6 bit (mint a v4.4e-ben);
- **v4.8-a0,99:** a jel pontossága 0,99.

**Jóslatok:**
- **J1:** ha a fő ok (a), a v4.8-a0,99 target-acc-ja a v4.4e-é közelében lesz (legfeljebb 0,05-tel alatta).
- **J2:** ha a fő ok (b), a v4.8-π is a v4.4e alatt marad (legalább 0,1-gyel).
- Mindkettő teljesülhet, ha mindkét ok hat.

## 2. rész: eredmények

*(a futtatás után)*
