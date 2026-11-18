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

59 „más régió” eset (egy C-eset nem fejeződött be a kiértékelésig); eredmény:
[`results/kor-62/`](../../experiments/arlc/results/kor-62/).

| | v3 | v4.4e | v4.8 (a = 0,9; 60. kör) | **v4.8-π** (jel nélkül) | **v4.8-a0,99** |
|---|---|---|---|---|---|
| target-acc (más régió) | 0,033 | **0,341** | 0,072 | 0,157 | 0,106 |
| post-acc | – | 0,601 | 0,672 | 0,674 | 0,669 |

v4.8-π − v4.4e = **−0,184** [−0,286; −0,084]; v4.8-a0,99 − v4.4e = −0,235 [−0,335; −0,138].

- **J2 teljesül:** jel nélkül is a v4.4e alatt marad. A fő ok nem a jel.
- **J1 nem teljesül:** 0,99-es jellel sem javul.

### A valódi ok: egy kényes holtverseny

A 6005-ös eset pontszám-felbontása szerint a két versengő hipotézis:
- „a régióforrás téved” (5 állítása elvetve, 1 tankönyvi szabály és 9 terepi tény elvetve);
- „a régióforrásnak igaza van” (2 tankönyvi szabály és 12 terepi tény elvetve).

| pontozás | H(régió elvetve) | H(régió elfogadva) | különbség |
|---|---|---|---|
| v4.4e | 196,91 | 196,95 | **0,04 bit** |
| v4.8-π | 197,46 | 197,03 | **0,43 bit** |

**A „más régió” meglepetés ebben a generátorban gyakorlatilag holtverseny.** A régióforrás 4 ténye és 1 szabálya
egymást erősíti, és egy olyan tankönyvi szabállyal ütközik, amelyet a terepi adatok sem támogatnak egyértelműen.
Egy fél bites eltolás, például a keverék-prior kétszintű csoportosítása, átbillenti a döntést. **A H60d kudarca
tehát nem egy rendszerszintű hibamód, hanem egy alulhatározott eset kényes holtverseny-feloldása.** A
célkérdés-pontosság erre a típusra kevés, véletlenszerű bitkülönbséget mér.

### Következmények

1. **A „más régió” target-acc nem alkalmas módszerek rangsorolására** ebben a generátorban, legalábbis amíg a
   meglepetés ilyen kevés és belsőleg konzisztens evidenciát hoz. Az 50., 55. és 57. kör „nagy” target-előnyei erre
   a típusra (+0,40 a v3-hoz képest) ugyanígy holtverseny-oldali különbségek lehetnek. Ez visszamenőleg gyengíti
   azokat az állításokat.
2. **A helyes válasz a bizonytalanság jelzése:** egy 0,04 bites különbségre a MAP-válasz önkényes. A nyaláb
   poszterior-súlyú átlaga (49–50. kör) itt kb. ½ valószínűséget adna, és ezt a Brier-pontszám jutalmazná.
3. **Nyitott:** miért nem segít a jó (0,99-es) kontextusjel. A régióforrás izolálása ekkor 0,7 bitbe kerülne, mégsem ezt
   választja a rendszer. Valószínű ok, hogy az izolált kontextusban a régióforrás szabálya ütközik az örökölt
   tankönyvi szabállyal (az 50. kör „kontextuson belüli elsőbbség” kérdése), és ennek feloldása drága.
