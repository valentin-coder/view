# 51. kör – A generatív v5 terve: minden lépés egy látens változó

(Tervezési kör, kód nélkül. Előzmény: a 49. kör kritikája. Az ARLC kiskapuinak szerkezeti oka, hogy
minden lépéstípus külön, kézzel árazott tag. A számozás a terv szerinti; az 50. kör eredményei a 44.
kör befejezése után készülnek el.)

## 1. Az elv

A v5 pontszáma **egyetlen generatív modell negatív log-valószínűsége**: −log₂ P(D, Z), ahol D a
megfigyelések, Z a látens változók teljes hozzárendelése. Az ARLC „lépései” ekkor nem önálló
objektumok, hanem Z egyes koordinátáinak átállításai. Két következménye van:
- **egy hiedelemállapot ára nem függhet attól, melyik lépés vezetett oda.** Ha két Z ugyanazt a
  hiedelemállapotot adja, mindkettő egy-egy legitim történet a saját priorjával. Ha ezek összege
  helyett a maximumot vesszük (MAP), az közelítés, nem kiskapu;
- **egy „lépés”, amelyhez nem tartozik generatív történet, nem létezhet.** Ilyen volt a felső osztályra
  adott kivétel (48. kör): nincs olyan folyamat, amely azt generálná, hogy „az R2bb-k R1a-k, kivéve az
  R2b-ket”, ha minden R2bb R2b.

## 2. A látens változók

| ARLC-lépés | látens változó | prior | megjegyzés |
|---|---|---|---|
| tény/szabály elutasítása | rel_i ∈ {0, 1} jelentésenként | rel_i ~ Bern(r_s), r_s ~ Beta(κ·q, κ·(1 − q)) forrásonként és **állítástípusonként** | a q-csoportok (48. kör) itt természetesek; a csoportok közös hiperpriorral kapcsolhatók |
| elmélet egészének elvetése | g_T ∈ {0, 1} („szemét elmélet”) elméletenként | Bern(1 − π_típus) | **π forrástípusonként** (tankönyv, szakértő, pletyka); g_T = 1 esetén rel_i ~ Bern(½) |
| kontextus (izolálás) | ctx_s ∈ {fő, más} forrásonként | Bern(ρ_típus) | **ρ forrástípusonként**; a 49. kör szerint π és ρ megfigyelésileg ekvivalens, ezért **közös hiperpriorral** kell kezelni, különben a kisebbik árú nyer |
| példánykivétel | ab(r, e) minden *aktív, megfigyelt következményű* alkalmazásra | Bern(ε_terület) | a nem megfigyelt alkalmazások kiösszegezve (45. kör, 2.2) |
| specifikusság | **nem látens**: determinisztikus prioritás a szigorú alosztály-reláció szerint | – | a 49. kör `auto_specificity`; a Nixon-gyémánt (összemérhetetlen ősök) marad ütközés |
| osztályszintű kivétel | ab(r, c) szabályonként és **szigorú alosztályonként** | Bern(ε_osztály) | a felső osztályos változat nem létezik |
| indukált szabály | a szabály létezése egy szabálynyelvtanból | 2^(−hossz) | a mostani log₂(2·|C|·|P|) ennek egyenletes esete |
| feltalált kategória | c′ = b ∧ F a nyelvtanból | 2^(−hossz) | a kétfeltételes szabály ára ugyanígy |
| frissítés (vágás) | változáspont (e, csoport) párokra | hazard h_csoport | a 13. és 16. kör update_prior-ja ennek egy pontja |
| tény-érték | érték | ha szabály jósolja és rel = 1, ab = 0: 1 − δ; különben ½ | a mostani „1 bit, ha nem jósolt” |

**Ami a v4-ben nem generatív, és a v5-ben megszűnik:**
1. a felső osztályos osztálykivétel (48. kör);
2. a forrásmérettől független, fix 6 bites kontextusár, amely független a „szemét elmélet” priortól (49.
   kör). A v5-ben a kettő közös hiperprior alatt van;
3. a minden (szabály, entitás) párra kiszabott −log₂(1 − ε) konstans, amely a paraméterbecslést torzítja
   (45. kör);
4. a lépésenkénti helyi költségbecslés csak keresési heurisztika marad (42. kör), a pontszám nem függ
   tőle.

## 3. Következtetés

- **MAP:** a mostani nyalábkeresés megmarad, de a pontszám a fenti modellből jön. A lépéskészlet
  pontosan a Z koordinátáinak egyenkénti átállítása, így teljes: a 47. kör tanulsága (az eredmény a
  célfüggvény *és* a lépéskészlet együttes terméke) ezzel szerkezetileg kezelhető.
- **Ellenőrzés:** a kimerítő keresés és a ProbLog-összevetés a v5-ben **minden** látens típusra kiterjed,
  mert a modell egyetlen programként felírható. Ez a 43., 45. és 48. kör lefedettségi hibáinak
  ellenszere.
- **Átlagolás:** mivel a pontszám valódi valószínűség, a nyaláb súlyozott átlaga értelmes poszterior-
  közelítés (49. kör, 6.4). Az egyik ekvivalens állapothoz vezető több Z összeadható.

## 4. Kockázatok (a saját tervem ellen)

1. **Ez a ProbLog/BLOG/Markov-logika újrafeltalálása.** Igaz, és ez a cél: a 36. kör óta tudjuk, hogy a
   következtető nem újdonság. A v5 értéke a modellezési döntésekben van (mely látens változók, milyen
   hiperpriorral), és abban, hogy a revíziós viselkedés (gestalt, specifikusság, frissítés vs. revízió)
   ezekből *levezethető*.
2. **A hiperpriorok** (π, ρ, ε, κ forrástípusonként) a 45. kör szerint egy világból nem becsülhetők. A v5
   ezért vagy rögzített, deklarált forrásmetaadatra támaszkodik (a q mintájára: „ez egy tankönyv”),
   vagy sok világon át tanul (52. kör). Az első egy új, külső bemenetet tesz szükségessé. A második a
   B fázisban az LLM-től származhatna: a forrás típusa a szövegből felismerhető. **Ez az LLM egy új,
   konkrét szerepe:** nem a tények kinyerése, hanem a források *típusának* becslése.
3. **A gestalt ↔ téves elvetés feszültség** (49. kör, 5. pont) a v5-ben sem tűnik el, csak láthatóvá és
   paraméterezetté válik: π_típus. Ez őszintébb, de nem megoldás.
4. **Futási idő:** a pontszám nem lesz drágább (ugyanazok a tagok, másképp csoportosítva), de a
   közös hiperpriorok (π és ρ együtt) a forrásokat összekötik, és ez a pontszám lokalitását rontja
   (46. kör).

## 5. Döntés

A v5-öt **nem** kezdem el, amíg a 44. kör eredménye nincs meg. Ha a befagyasztott v4 a független
benchmarkon nem jobb a v3-nál (H44b), az a sorozat eddigi irányának komoly cáfolata. Akkor a v5 nem a
v4 javítása, hanem az újrakezdés tiszta alapja.
