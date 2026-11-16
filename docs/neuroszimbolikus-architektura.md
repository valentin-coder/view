# Neuroszimbolikus architektúra fagyasztott LLM fölé: tervezési és formalizálási dokumentum

> Állapot: csak tervezés és formalizálás, kód nincs.
> A feladatleírás „[Ide jöhet a saját korábbi ötleted…]” sora üresen maradt, ezért korábbi megkötést nem vettem figyelembe.

**Cél.** Egy FAGYASZTOTT LLM belső aktivációin mintázatot ismerünk fel, és ezt egy külső, SZIMBOLIKUS, módosítható szerkezet reprezentálja. Kulcsképesség az azonnali, gradiens nélküli átstrukturálás. Ha egy új, meglepő információ sok berögzült szerkezettel ütközik, a szimbolikus réteg egyszerre rendeződik át.

---

## 1. FÁZIS – A paradigma kimondatlan axiómái és tagadásuk

| # | Kimondatlan axióma | Tagadás | Mi következik belőle |
|---|---|---|---|
| A1 | A tudás vektortérben él, a relevancia a közelség (koszinusz). | A tudás egy diszkrét szerkezetben él: függőségekben, ekvivalenciákban, kontextusokban. A vektor csak érzékelési bemenet. | A visszakeresést következtetés (propagáció) váltja fel. A „hasonló” és a „releváns” elválik egymástól: egy távoli tény is lehet döntő, ha a függőségi kúpban van. |
| A2 | A frissítés gradiens vagy hozzáfűzés. | A frissítés diszkrét, kombinatorikus revízió: visszavonás, egyesítés, szétválasztás. | Lehetséges az egylépéses, nem lokális változás. Ennek ára, hogy a frissítés NP-nehéz kereséssé válhat (hitting set, MaxSAT, min-cut). |
| A3 | A memória kulcs-érték tár. | A memória reláció-, ekvivalencia- vagy függőségi szerkezet, a tartalom a helyzetből adódik. | Nincs „egy elem, egy hely”: egy új tény sok tárolt elem jelentését változtatja meg (kongruencia, öröklés). |
| A4 | A tanulás és a lehívás szétválik. | Minden olvasás egyben írás is (rekonszolidáció). | Lehívás közben derül ki a predikciós hiba, és a lehívott séma ilyenkor módosítható. Ennek kockázata a lehívás okozta torzulás. |
| A5 | A memória passzív, csak az LLM számol. | A szimbolikus réteg aktív: következtet, és visszahat az LLM-re. | Kell egy cselekvési útvonal (steering, kontextus-injektálás). Ezzel a rendszer zárt hurkú szabályozóvá válik. |
| A6 | Az interfész a kontextusablak (a memória szövegként megy vissza). | Az interfész a reziduális áram: beavatkozás a köztes aktivációkba. | A tudás a beavatkozásban élhet, nem tárolt szövegben. Kérdés, hogy a lineáris steering elég specifikus-e tényekhez. |
| A7 | A memóriaelemek függetlenek, az ütközést a ranglista vagy a frissesség dönti el. | Az elemek között konzisztencia-kényszerek vannak. | Az ütközés maga információ. Megkérdezhető, melyik a legkisebb elhagyandó feltevéshalmaz. |
| A8 | A fagyasztott LLM rögzített jellemzőkinyerő, ami kijön belőle, az „a jelentés”. | Az LLM dinamikai rendszer. A jellemzők kontextusfüggők, a kinyerés (probe/SAE) maga is torzító modell. | A grounding saját hibamodellt igényel: a kinyerési zaj és a valódi meglepetés különválasztása központi feladat. |
| A9 | A tudás egysége a tény (triplet). | Az egység a szabály, az ekvivalencia, a kontextus vagy a tömörítő program. | A „séma” elsőrendű objektum lesz, és egyetlen szabály visszavonása sok tényt mozdít meg. |
| A10 | A meglepetés elemenkénti (egy hiba, egy elem frissül). | A meglepetés strukturális, globális mennyiség (inkonzisztencia mértéke, energia, kódhossz). | Küszöbös, fázisátmenet-szerű viselkedés várható: anomália-tűrés, aztán hirtelen váltás. |
| A11 | A memória monoton nő. | A memória a legrövidebb leírás, a felejtés és a tömörítés elsődleges. | Az átrendezés kiváltója az, hogy egy új szerkezet rövidebben írja le az eddigieket. |
| A12 | A memória időtlen. | A tudás epizódokhoz és kontextusokhoz kötött. | Két ellentmondó tény lehet egyszerre igaz, különböző kontextusban. Az átrendezés egyik formája a kontextus szétválasztása. |
| A13 | Egyetlen konzisztens világmodell létezik. | Több versengő hipotézis él párhuzamosan. | Az „azonnali” váltás egy előre karbantartott alternatíva kiválasztása, nem újraépítés. |

---

## 2. FÁZIS – 8 architektúra

| # | Név | Tagadott axióma | Diszciplína |
|---|---|---|---|
| 1 | Feltevés-alapú igazságkarbantartás grounding-olt atomokon (ATMS-LLM) | A2, A7, A10 | logika / tudásreprezentáció |
| 2 | Kongruencia-zárt e-gráf memória | A3, A7 | automatikus érvelés |
| 3 | Absztrakció-finomítás (CEGAR) az aktivációs dinamikán | A1, A8 | formális verifikáció |
| 4 | Spinüveg-hiedelemmező klaszterátfordítással | A2, A10 | statisztikus fizika |
| 5 | Látens ok-következtetés és rekonszolidáció | A4, A12, A13 | idegtudomány / kognitív pszichológia |
| 6 | Beavatkozás-memória (a tudás a szabályozóban van) | A5, A6 | irányításelmélet |
| 7 | MDL-tömörítő szabályrendszer regret-triggerrel | A11, A10 | információelmélet |
| 8 | Kéve-konzisztencia kontextus-szétválasztással | A7, A12, A13 | algebrai topológia |

A „gyökeresen különböző” címke nem igaz mindegyikre.

- **Az 1., 4. és 8. ugyanaz a séma más energiafüggvénnyel.** Mindhárom kényszerkielégítés propozicionális hiedelmeken: kemény logika, Ising-energia, illetve kvadratikus energia.
- **A 2. az 1. speciális esete** az egyenlőség elméletére.
- **Valódi diverzitás a 3., 5., 6. és 7.** A 3. az LLM saját dinamikáját modellezi, az 5. epizódokat klaszterez, a 6. visszahat az LLM-re, a 7. tömörít.

---

## Közös keret

### Jelölések

- `f` a fagyasztott LLM. `h_ℓ(x) ∈ ℝ^d` az ℓ-edik réteg reziduális aktivációja az x bemenetre.
- Grounding: `g: ℝ^d → 2^𝒜 × [0,1]`, vagyis literálok konfidenciával. Forrása lineáris probe-ok (`σ(w_a·h+b_a)`) vagy SAE-jellemzők.
- Megfigyelés: `o_t = g(h_ℓ(x_t))`. Szimbolikus állapot: `S_t`. Frissítés: `S_{t+1} = U(S_t, o_t)`. Átrendezés: `R`, ami akkor fut, ha `surprise(S_t, o_t) > θ`.

### Közös játékvilág („Nonce-világ”, CPU)

- 40 kitalált entitás (wug, dax, fep…), 8 kategória, 12 tulajdonság.
- Szabályok:
  - „X egy Y” (öröklés),
  - „minden Y P” (generikus),
  - kivételek.
- Mondatsablonok: 8 parafrázis-sablon (aktív/passzív, tagadás, szinonimák). Ebből 5 tanító és 3 kitartott sablon.
- Fagyasztott modell: GPT-2 small, Pythia-160M, összehasonlításként Qwen2.5-0.5B. Kb. 3–5 ezer rövid mondat forward passza CPU-n percek kérdése.
- Meglepetés-esemény: egy tény, amely egy mély függőségi kúp tetejét mozdítja meg. Példa: „a wug valójában nem dax, hanem fep”. A kúp mélysége 1–4 között állítható.

### Közös mérőszámok

A RippleEdits [Cohen et al. 2024] és a MQuAKE [Zhong et al. 2023] logikáját követik, miniatűr változatban.

- **Ripple-recall:** a változandó következmények hány %-a változott.
- **Kollaterális arány:** a nem változandók hány %-a változott.
- **Átrendezési költség:** műveletszám és falióra-idő. Gradiens-lépésből 0 kell legyen.

### Közös cáfoló kontrollok minden ötletre

- **K1 – orákulum-parser:** az LLM helyett hibátlan szimbolikus bemenet. Ez a felső korlát, és megmutatja, mennyi múlik a groundingon.
- **K2 – bag-of-words / véletlen jellemzős enkóder** az LLM helyett. Ha a kitartott sablonokon ugyanolyan jó, akkor az LLM irreleváns, és az ötlet „neuro” fele megbukott.
- **K3 – generált logikai forma:** az LLM szövegesen kiadja a tripletet, ezt kapja a szimbolikus réteg (Logic-LM [Pan et al. 2023] és LINC [Olausson et al. 2023] mintára). Ha ez ugyanolyan jó, az „aktivációkból olvasunk” premissza fölösleges.

### Közös, ötletfüggetlen kockázat számszerűen

Ha egy literál kinyerési hibája ε = 0,05, és megfigyelésenként 3 literál keletkezik, akkor a megfigyelések `1−0,95³ ≈ 14%`-a tartalmaz hibás literált. Minden ellentmondás-vezérelt architektúra ezt a zajt valódi meglepetésnek fogja nézni. Három parafrázis többségi szavazása független hibák esetén literálonként kb. 0,7%-ra, megfigyelésenként kb. 2,2%-ra csökkenti. A parafrázis-hibák azonban korreláltak, így ez optimista becslés.

**0. fázisú előkísérlet minden más előtt:** literál-kinyerés F1-értéke a kitartott sablonokon, rétegenként. Ha a legjobb réteg F1-e 0,9 alatt van, mind a 8 ötlet alapja hiányzik.

---

## 3. FÁZIS – Az ötletek egyenként

### 1. ATMS-LLM: feltevés-alapú igazságkarbantartás

**Formalizálás**

- Objektumok:
  - Atomok: `𝒜`.
  - Feltevések: `𝔄`. Ide tartozik minden megfigyelt tény ÉS minden szabály, mindegyik `ε(a)` beágyazottsággal (entrenchment).
  - Horn-indoklások: `J: a₁∧…∧a_k → c`.
  - Nogood-ok: `𝒩`, a minimális inkonzisztens feltevéshalmazok.
  - Címkék: `L(c)`, a c-t támogató minimális környezetek.
- Állapot: `S = (𝔄, J, 𝒩, L)`.
- Frissítés:
  1. Az `o` új feltevésként (`a_o`) kerül be.
  2. ATMS-címkepropagáció fut [de Kleer 1986].
  3. Ha nogood keletkezik, kiszámoljuk a minimális költségű hitting setet: `H* = argmin_{H ∩ N ≠ ∅ ∀N∈𝒩} Σ_{a∈H} ε(a)` [Reiter 1987].
  4. Ha `ε(a_o) > cost(H*)`, H* visszavonásra kerül. Ilyenkor minden olyan következmény egyszerre kiesik, amelynek a címkéjében csak H-t tartalmazó környezetek vannak. Ellenkező esetben az új megfigyelést utasítjuk el.

**Meglepetés**

- Szerkezeti meglepetés: `s(o) = cost(H*)`, azaz mennyi beágyazott tudást kellene feladni az új megfigyelésért.
- A kúpméret: `|Cone(H*)|`, a megmozduló következmények száma.
- Az átrendezést a nogood megjelenése váltja ki. A döntés a fenti egyenlőtlenségen múlik.

**Legközelebbi munka**

- Klasszikus: Doyle TMS (1979), de Kleer ATMS (1986), AGM-revízió (1985).
- LLM-es: **BeliefBank** [Kassner et al. 2021]. Ez az LLM kimeneteiből olvas hiedelmeket, és súlyozott MaxSAT-tal tartja konzisztensen őket. Ez nagyon közel van.
- **Őszintén:** ez BeliefBank plusz ATMS. Új elem csak az, hogy aktivációkból olvas, nem kimenetből, és ez akár rosszabb is lehet. Lényegében ismert módszer átcímkézve.

**Játékkísérlet**

- Nonce-világ, egy meglepetés-tény, kúpmélység 1–4.
- Alapvonalak:
  - csak hozzáfűzés, lekérdezéskor frissesség szerinti feloldással;
  - BeliefBank-szerű MaxSAT.
- **Cáfolat:**
  - ripple-recall < 0,8 vagy kollaterális > 0,1 mélység ≤ 3-nál;
  - VAGY ε = 0,05 groundingzaj mellett 50 megfigyelésenként több mint 1 hamis visszavonás;
  - VAGY a K2 kontroll ugyanolyan jó.

**Kudarcmódok**

- A zaj visszavonási kaszkádot indít.
- A címkék mérete exponenciálisan nő.
- A szabályok forrása megoldatlan: csak a szövegben kimondott generikus állításokból tud szabályt.
- `ε` kalibrálása önkényes.

### 2. Kongruencia-zárt e-gráf memória

**Formalizálás**

- Objektumok:
  - Termek: `t ::= c | f(t₁…t_n)`. Az entitásszimbólumok aktivációs klaszterek, a függvényszimbólumok relációtípusok (pl. `kind(x)`, `color(x)`).
  - Union-find `U` az ekvivalencia-osztályokon, hashcons `H`, diszegyenlőségek `D`.
- Állapot: `(U, H, D)`.
- Frissítés:
  - `t₁ = t₂` állítás: union, majd rebuild. A kongruencia-zárás miatt `a≡b ⇒ f(a)≡f(b)` [Nelson–Oppen 1980; Downey–Sethi–Tarjan 1980].
  - `t₁ ≠ t₂` állítás: bekerül D-be.

**Meglepetés**

- Ellentmondás: egy union megsért egy D-beli elemet.
- Szerkezeti nagyság: az indukált merge-ek száma (|Δosztály|).
- Ellentmondáskor bizonyítást előállító kongruencia-zárás [Nieuwenhuis–Oliveras 2005] mutatja meg a felelős bemeneti egyenlőségeket. Ezek visszavonása után a gráf újraépül.

**Legközelebbi munka**

- SMT-megoldók EUF-elmélete (pl. Z3), egg / equality saturation [Willsey et al. 2021], entitásfeloldás.
- **Ez SMT-front-end LLM-parserrel. Átcímkézés.**

**Játékkísérlet**

- Identitás-leleplezés: „A és B ugyanaz”. Minden A-ról szóló lekérdezésre B tényeit kell adnia.
- **Cáfolat:**
  - kongruencia nélküli sima union-find ugyanazt éri el;
  - VAGY 5% entitás-groundingzaj mellett 1%-nál több hamis merge.

**Kudarcmódok**

- Monoton: szétválasztani csak teljes újraépítéssel tud.
- Egy hamis egyenlőség összeomlaszthatja a gráfot („minden egyenlő mindennel”).
- Kvantifikált szabályok nem fejezhetők ki benne.

### 3. CEGAR az aktivációs dinamikán

**Formalizálás**

- Konkrét rendszer: `h_{t+1} = F(h_t, token_t)` a fagyasztott LLM-ben, rögzített réteg és pozíció mellett.
- Absztrakció: `α: ℝ^d → Q` véges partíció, félterek metszeteiből. Absztrakt automata: `M = (Q, Σ, δ, λ: Q→2^𝒜)`.
- Állapot: `(Π, M)`.

**Meglepetés**

- Egy konkrét trajektória absztrakt képét M nem fogadja el, vagy M olyan átmenetet jósol, amit az LLM nem tesz meg (hamis ellenpélda). Sztochasztikus változatban: `−log P_M(α(trajektória))`.

**Átrendezés**

- Az eltérő konkrét állapotokat elválasztó új hipersík bevezetése (zárt alakú LDA, nincs gradiens az LLM-en).
- Utána partíciófinomítás stabilitásig [Paige–Tarjan 1987]. Egyetlen vágás végigfuthat az összes elődállapoton, ez valódi kaszkádos, determinisztikus átrendeződés.

**Legközelebbi munka**

- RNN-ből DFA-kinyerés [Omlin–Giles 1996; Weiss–Goldberg–Yahav 2018].
- CEGAR [Clarke et al. 2000].
- Absztrakció alapú NN-verifikáció [Elboher–Gottschlich–Katz 2020].
- Tudásfenntartásra alkalmazva talán új, de **ellenőrizni kell**.

**Alapvető ellenvetés**

- Ez az LLM saját számítását modellezi, nem a világot. Csak olyan megkülönböztetéseket tud reprezentálni, amelyeket a fagyasztott LLM már kiszámol.
- Ha a régiókhoz külső címkét kötünk, akkor a régió kulcs lesz, és visszatértünk A3-hoz (kulcs-érték tár).

**Játékkísérlet**

- Zárójelezési vagy állapotkövető nyelv. Az absztrakt modellnek az LLM következő-token döntési osztályát kell jósolnia, majd új tokenekkel rezsimváltás jön.
- **Cáfolat:**
  - azonos állapotszámú, nulláról újraklaszterezett k-means ugyanolyan pontos;
  - VAGY |Q| lineárisan nő a megfigyelésekkel (nincs általánosítás).

**Kudarcmódok**

- Állapotrobbanás.
- A választott réteg nem markovi.
- Pozíciófüggés.

### 4. Spinüveg-hiedelemmező klaszterátfordítással

**Formalizálás**

- Változók: `s_i ∈ {±1}` propozíciónként.
- Energia: `H(s) = −Σ J_ij s_i s_j − Σ h_i s_i`.
  - `h_i` akkumulált evidencia a probe-logitokból.
  - `J_ij` lokális Hebb-szabállyal frissül: `ΔJ_ij = η s_i s_j` együtt állított atomokra. Nincs gradiens.
- Állapot: `(J, h, s*)`.

**Meglepetés**

- Energiaugrás a régi konfigurációban: `ΔE = H_new(s*) − H_old(s*)`.
- Vagy frusztráció: `Φ = Σ_i max(0, −s_i(h_i + Σ_j J_ij s_j))`.

**Átrendezés**

- Ha `ΔE > θ`: Fortuin–Kasteleyn-klaszterek építése és egész klaszterek átfordítása (Swendsen–Wang 1987).
- Ferromágneses J-re egzakt MAP min-cut-tal [Greig–Porteous–Seheult 1989].
- Egy egymást erősítő hiedelemcsoport, vagyis egy „séma”, egyszerre fordul át.

**Legközelebbi munka**

- **Thagard ECHO (1989): magyarázó koherencia kényszerhálóval, kifejezetten tudományos forradalmak modellezésére.** Ez gyakorlatilag ugyanaz.
- Markov Logic Networks [Richardson–Domingos 2006].
- **Átcímkézés.** Új elem csak a klaszterlépés, ami ismert mintavételezési trükk.

**Játékkísérlet**

- Nonce-világ. Mérendő a hiszterézis: mennyi ellentmondó evidencia kell egy séma átfordításához a kúpmélység függvényében.
- **Cáfolat:** egyspines mohó ICM ugyanarra a konfigurációra jut ugyanazzal a ripple-recall-lal.

**Kudarcmódok**

- **A J szimmetrikus, az implikáció nem** (a→b nem azonos b→a-val). Ez a formalizmus alapvető hibája.
- Magasabb rendű faktorokkal javítható, de akkor MLN-t kapunk.
- A J korrelációt kódol, nem következtetést.

### 5. Látens ok-következtetés és rekonszolidáció

**Formalizálás**

- Epizód: `e_t = (c_t, o_t)`, ahol `c_t` a kontextuskód az aktivációból, `o_t` a literálok.
- Látens okok `k ∈ ℕ` (sémák). Prior: sticky CRP (α koncentráció). Okonként szimbolikus séma: `θ_k`, pl. Bernoulli-eloszlás atomokon vagy kis szabályhalmaz. Hozzárendelés: `z_t`.
- Állapot: `(z_{1:t}, {θ_k}, epizódpuffer)`.
- Poszterior: `p(z_t=k | ·) ∝ CRP(k) · p(e_t|θ_k)`.

**Meglepetés**

- `s_t = −log p(e_t | θ_{ẑ_t})`.
- Két küszöb:
  - `s < θ₁`: asszimiláció;
  - `θ₁ < s < θ₂`: rekonszolidáció, `θ_k` frissül, mert a lehívott emlék labilis;
  - `s > θ₂`: új ok jön létre.
- **Visszamenőleges átrendezés:** új ok születésekor Gibbs-söprés fut a pufferen, a múltbeli epizódok tömegesen átsorolódnak („most másként látom a korábbi tapasztalataimat”).

**Legközelebbi munka**

- Gershman–Blei–Niv 2010; Gershman–Monfils–Norman–Niv 2017 (a rekonszolidáció számítási modellje).
- Franklin et al. 2020 (SEM).
- **EM-LLM** [Fountas et al. 2024]: Bayes-meglepetés alapú epizódszegmentálás fagyasztott LLM-ben, de nyers KV-gyorsítótárat keres vissza, sémát nem tart, a múltat nem sorolja át.
- Larimar [Das et al. 2024]: tanított modul.
- **A modell maga ismert.** Az alkalmazás (aktivációk, szimbolikus θ) új lehet, **ellenőrizni kell**.

**Játékkísérlet**

- Rejtett rezsimváltás egy állításfolyamban („az északi völgyben a dax mérges”), majd a régi rezsim visszatér.
- Mérőszámok:
  - pontosság a váltás után;
  - megtakarítás a visszatéréskor (nincs katasztrofális felülírás);
  - a múltbeli epizódok átsorolásának pontossága.
- **Cáfolat:**
  - csúszóablakos frissesség-memória mindkettőben egyezik;
  - VAGY az aktivációs meglepetés a valódi rezsimváltást a parafrázis-zajtól AUC < 0,75 mellett választja szét.

**Kudarcmódok**

- Lapos klaszterezés, nincs relációs propagáció.
- A meglepetést a felszíni forma dominálja.
- A küszöbök végzik az érdemi munkát.
- Kevés adatnál hamis okok születnek.

### 6. Beavatkozás-memória (irányításelmélet)

**Formalizálás**

- Az LLM a „szabályozott szakasz”. Beavatkozás: `h_ℓ ← h_ℓ + u`.
- Szabály: `r = (G_r, u_r)`.
  - `G_r` őrfeltétel probe-atomokon.
  - `u_r = Σ β_a v_a`, ahol `v_a` fogalomirányok (átlagkülönbség).
- Állapot: szabályhalmaz és viselkedési kényszerek (`C`).
- Új tény = új kényszer. A β-k minimális normájú megoldással kerülnek elő, linearizált kimeneti feltételekkel. Derivált nélkül, néhány forward passzal, vonalkereséssel.

**Meglepetés**

- Szabályozási hiba: a kényszer sérül a jelenlegi szabályozó mellett.
- Erős formában: a lineáris kényszerrendszer megoldhatatlan. Ekkor a Farkas-tanúsítvány megadja a minimális megoldhatatlan részhalmazt (IIS).

**Átrendezés**

- Az őrfeltételek régióinak felosztása, vagy IIS-beli kényszerek elhagyása prioritás szerint, majd az egész LP egyszeri újramegoldása. Minden u_r egyszerre változik.

**Legközelebbi munka**

- ITI [Li et al. 2023], ActAdd [Turner et al. 2023], RepE [Zou et al. 2023], CAA [Rimsky et al. 2024].
- **GRACE** [Hartvigsen et al. 2023]: diszkrét kódkönyv egy rétegen, aktivációkulcsokkal és hatósugárral, de az értékeket gradiens tanítja.
- SERAC [Mitchell et al. 2022].
- Az LP-alapú konfliktusfeloldás talán új, **ellenőrizni kell**. Az egész nagyon közel van a GRACE-hez és a SERAC-hoz.

**Játékkísérlet**

- Attribútumszintű szabályok GPT-2-n („X-ről negatívan”), utána meglepetés-frissítés („X mégis jó”).
- Mérőszámok: kényszerteljesülés, perplexitás-növekedés, KL eltérés nem érintett promptokon.
- **Cáfolat:**
  - tényszintű kényszereknél a teljesülés 70% alatt marad 10% alatti perplexitás-növekedés mellett;
  - VAGY a szabály szövegként a promptba írva ugyanezt hozza.

**Kudarcmódok**

- **A lineáris steering durva attribútumokra (szentiment, igazmondás) működik, specifikus tényekre megbízhatatlan.**
- Hamis pozitív őrfeltételek.
- A vektorok interferálnak egymással.

### 7. MDL-tömörítő szabályrendszer

**Formalizálás**

- Literálhalmazok folyama.
- Modell: M szabályprogram (asszociációs szabályok vagy döntési lista), `L(M)` kódhosszal.
- Állapot: `M_t` és korlátos elégséges statisztikák (k-ad rendű együttelőfordulások). A nyers adat eldobható.

**Meglepetés**

- `s_t = L(o_t | M_t)` bitben.

**Átrendezés**

- CUSUM bitekben: ha a régi és a jelölt modell közti kódhossz-különbség
  `Σ_{τ≤t} [L(o_τ|M) − L(o_τ|M')] > L(M') − L(M) + κ`,
  akkor a teljes szabályrendszer M'-re cserélődik.
- Példa: „20 kivétel listája” helyett „egy új kategóriaszabály”.

**Legközelebbi munka**

- Rissanen 1978, Grünwald 2007.
- **Krimp** [Vreeken–van Leeuwen–Siebes 2011]: MDL-alapú mintahalmaz-bányászat, nagyon közel.
- DreamCoder [Ellis et al. 2021]; CUSUM [Page 1954].
- **Ez Krimp és CUSUM SAE-jellemzőkön, átcímkézés.**

**Játékkísérlet**

- Hierarchia, amelyben T időpontban egy leleplezés 10 kivételt egyetlen új kategóriával magyaráz meg.
- **Cáfolat:**
  - a váltás nem korábbi, mint a „minden N lépésben újraillesztés” alapvonalé;
  - VAGY a talált szerkezet strukturális Hamming-távolsága nem jobb a gyakori-mintás bányászaténál.

**Kudarcmódok**

- A keresés intraktábilis.
- A kódolás megválasztása önkényes.
- Az átrendezés eleve késleltetett, mert evidenciát gyűjt. Ez ellentmond az „azonnali” célnak.

### 8. Kéve-konzisztencia kontextus-szétválasztással

**Formalizálás**

- Kontextusfedés: `𝒰 = {U_i}`, az aktivációk klaszterezéséből (forrás, téma, időszak).
- Lokális hiedelemterek: `F(U_i)`. Restrikciós leképezések: `ρ_ij`.
- Energia: `E(x) = xᵀL_F x = Σ ‖ρ_ij x_i − ρ_ji x_j‖²`, ahol `L_F` a kéve-Laplace-operátor.
- Állapot: `(𝒰, ρ, x)`.
- Frissítés: harmonikus kiterjesztés megfigyelt peremértékekkel, vagyis egy lineáris egyenletrendszer megoldása.

**Meglepetés**

- Maradék energia: `E* = min E(x)` a megfigyelésekhez rögzítve. Ez a ragasztás akadálya, H¹-szerű mennyiség.
- Lokalizálható: megmutatja, mely éleken ül az ellentmondás.

**Átrendezés**

- Ha `E* > θ`: a restrikciós élek elvágása (az a atom jelentése a két kontextusban eltér), a vágásszám büntetésével.
- Célfüggvény: `min E* + λ·#vágás`, kombinatorikus min-cut. Egyetlen vágás sok konfliktust old fel egyszerre.

**Legközelebbi munka**

- Hansen–Ghrist 2019; **„Opinion dynamics on discourse sheaves”** [Hansen–Ghrist 2021], közel áll.
- Knowledge sheaves [Gebhart–Hansen–Schrater 2023]; Neural Sheaf Diffusion [Bodnar et al. 2022]; kontextualitás kévékkel [Abramsky–Brandenburger 2011].
- **Identitás-restrikciókkal és skalárokkal ez gráf-Laplace-simítás plusz élvágás, vagyis MRF és graph-cut átcímkézve.** Csak nemtriviális ρ-val ad többet, például ha az egyik kontextus „forró” fogalma a másikban „veszélyes”-nek felel meg.

**Játékkísérlet**

- Két forrás ütköző tényekkel, ahol a kontextusjel az aktivációkban jelen van, illetve nincs.
- Mérőszámok: kontextusfüggő lekérdezések pontossága; a létrehozott kontextusok egyezése a valódiakkal (ARI).
- **Cáfolat:**
  - az „atom × klaszterazonosító” konkatenációs alapvonal ugyanolyan pontos;
  - VAGY a konfliktusélek lokalizálásának precizitása 0,5 alatt van.

**Kudarcmódok**

- Triviális megoldás: mindent szétvágni.
- A kontextusok felfedezése az aktivációkból nehéz.
- A skalár szekciók túl szegények.

---

## 4. FÁZIS – Rangsorolás és rombolás

**Szűrés.** Kiesik:

- **2 (e-gráf):** monoton, és egyetlen hamis egyenlőség katasztrofális.
- **3 (CEGAR):** az LLM-et modellezi, nem a világot.
- **4 (spinüveg):** az implikációt nem tudja kifejezni, és ECHO átcímkézve.
- **6 (beavatkozás):** a steering tényszinten gyenge, és GRACE-közeli.
- **7 (MDL):** nem azonnali.
- **8 (kéve):** nemtriviális ρ nélkül átcímkézés, nemtriviális ρ-val pedig tanulást igényel.

**Kiválasztva: az 1. (ATMS-LLM) és az 5. (látens ok).** Két különböző átrendezési formát fednek le: a mag-hiedelem visszavonását és a múlt újraértelmezését. Mindkettő olcsón tesztelhető.

### Az 1. ötlet rombolása

1. **Nem új.** BeliefBank plusz ATMS. *Elfogadva.*
2. **Az AGM minimális változtatása ellentmond a célnak.** Egy séma-átalakulás nagy változás. *Részleges cáfolat:* a változás a feltevésekben minimális, a következményekben nem. Ha a visszavont feltevés kúpja nagy, a hatás is nagy. Ez az emberi esetre jellemző: egy mag-hiedelem megy el, és vele minden, ami rá épült.
3. **Ellenpélda: az ATMS az első meglepő tényt elutasítja.** Ha a régi szabály beágyazott, akkor `ε(a_o) < cost(H*)`, és a rendszer elveti az anomáliát. Ez a kuhni „normál tudomány”. A cél viszont az volt, hogy *egy erős élmény* átrendezzen. A szabály szerint ez csak akkor történik meg, ha `ε(a_o)` kívülről nagy. **Ez a szabad paraméter végzi az egész munkát.** Javítás: egy revízió értéke legyen az, hogy hány *korábbi* nogoodot old fel együtt. Ezzel viszont a rendszer súlyozott MaxSAT-tá szűkül, vagyis BeliefBankká.
4. **Zaj.** A közös keretben számolt 14% hamis nogood-forrás végzetes. *Túlélés:* parafrázis-szavazás (kb. 2%), és a zajjal szembeni ellenállás a beágyazottságból.
5. **Szabályforrás.** Csak a kimondott generikus állításokból van szabály. Az implicit, statisztikus sémákhoz induktív logikai programozás (ILP) kellene, ami tanulás. *Nem cáfolható, korlátként elfogadva:* a gyors átrendezés kész szabályokon működik, a szabályok indukciója lassú folyamat (a komplementer tanulórendszerek [McClelland–McNaughton–O'Reilly 1995] analógiájára).
6. **Az LLM szerepe.** A rendszer olvas, de a válaszokat szimbolikusan adja, így az LLM puszta parser. *Elfogadva*, és ez lesz a fő tesztelendő állítás (lásd lent).

### Az 5. ötlet rombolása

1. **Nem új.** Gershman latens ok modellje. *Elfogadva.*
2. **Ellenpélda: a láncolt propagáció elbukik.** „A wug fep” állításból a fep tulajdonságai nem öröklődnek, mert a θ_k atomeloszlás, nem szabályrendszer. *Halálos az 5. önmagában.*
3. A meglepetést a felszíni forma szennyezi. Ha a literálokon számoljuk, visszajutunk a groundinghoz.
4. A visszamenőleges Gibbs-söpréshez epizódpuffer kell, így az A3 (kulcs-érték tár) csendben visszatér.
5. A θ₁ és θ₂ küszöbök végzik az érdemi munkát.

**Ítélet.** Egyik sem éli túl önmagában. Az 1. hiányzó darabja az, hogy honnan jön az új megfigyelés súlya, és hogyan kezelendő a kontextus. Az 5. hiányzó darabja a relációs propagáció. Egymás hiányát pótolják.

### A túlélő: feltevés-alapú revízió látens kontextusokkal és MDL-döntéssel („ARLC”)

**Objektumok**

- Literálok grounding-gal: `g(x) → {(ℓ, p)}`. Három parafrázis probe-szavazása és kalibrált konfidencia.
- **Minden** feltevés:
  - ténymegfigyelések `F`;
  - szabályok `R` (a szabály is visszavonható, ez a „sémaváltás”);
  - **kontextus-feltevések** `κ_k`, ahol `z_t = k` azt jelenti, hogy az e_t epizód a k kontextushoz tartozik;
  - szabály-hatókörök `S_r ⊆ ℕ`.
- Hipotézis: `ℋ = (F_acc, R_acc, S, z)`.
- Pontszám (bitben):

  `L(ℋ) = L_CRP(z) + L(R_acc, S) + Σ_t L(e_t | Cl(R_acc|_{S∋z_t}, z_t)) + Σ_{t∉F_acc} L_rej(e_t)`

  Kemény feltétel: minden kontextus zárása nogood-mentes.
- Állapot: a legjobb ℋ* és egy B elemű nyalábban tartott alternatíva-készlet (A13 tagadása, ettől lehet a váltás azonnali), ATMS-címkékkel.

**Lépés megfigyelésenként**

1. Grounding és kontextus-hozzárendelés (sticky CRP-poszterior).
2. ATMS-propagáció. Ha nincs nogood: asszimiláció, a költség a kúppal arányos.
3. Ha nogood keletkezik, négy jelölt revízió közül választunk:
   - (a) a megfigyelés elutasítása, ami bekerül egy anomáliapufferbe;
   - (b) minimális hitting set visszavonása (tény vagy szabály);
   - (c) **kontextus-szétválasztás:** új κ, a konfliktusgráfon min-cut-tal kijelölt epizódok átsorolása;
   - (d) egy szabály hatókörének szűkítése.
4. A győztes: `argmin ΔL`. Ha minden ΔL > 0, akkor (a) történik.

**A meglepetés pontos definíciója**

- Pontszerű: `s_t = L(e_t | ℋ*)` bit.
- **Átrendezési trigger:** az első t, amelyre

  `Σ_{τ∈Anom_t} [L(e_τ|ℋ*) − L(e_τ|ℋ')] > L_struct(ℋ') − L_struct(ℋ*)`.

- Ez egyszerre ad anomália-tűrést (a gyenge anomáliák csak gyűlnek) és hirtelen váltást (a küszöb átlépésekor az egész kúp és az átsorolt epizódok egyszerre mozdulnak).
- Az erős élmény az, aminek nagyon nagy a kódhossz-költsége a régi hipotézis alatt (nagy konfidencia, sok érintett literál). Ez egyedül is átlépheti a küszöböt. Az 1. ötlet szabad `ε(a_o)` paraméterét így egy definiált mennyiség váltja fel.

**Legközelebbi munka**

**Poole valószínűségi Horn-abdukciója / ICL (1993/1997)** a legközelebbi formális előd. Továbbá:

- abduktív logikai programozás [Kakas–Kowalski–Toni 1992];
- nyílt univerzumú valószínűségi logika, BLOG [Milch et al. 2005];
- multi-kontextus rendszerek [Brewka–Eiter 2007];
- BeliefBank.

Az ARLC lényegében ICL, plusz CRP-alapú, igény szerint létrejövő kontextus-feltevések, plusz MDL-alapú választás a négy revíziótípus között, plusz grounding fagyasztott aktivációkból. **Nem vagyok biztos benne, hogy ez a kombináció új. Kifejezetten keresni kell rá:** „nonparametric abduction”, „contextual belief revision CRP”, „belief revision LLM probes”.

**Tesztelhető, megkülönböztető előrejelzések**

- **P1:** a váltási pont (hány anomália kell) monoton nő a tettes beágyazottságával. Ehhez képest a frissesség-alapvonal azonnal vált, a többségi szavazás fokozatosan.
- **P2:** kúpmélység ≤ 3 mellett ripple-recall ≥ 0,9 és kollaterális ≤ 0,05.
- **P3:** ha van kontextusjel az aktivációkban, (c) győz; ha nincs, (b).
- **P4:** a régi rezsim visszatérésekor nincs újratanulás.

**Kísérleti terv (CPU, nagyságrendileg órák)**

- **E0:** grounding-F1 a kitartott sablonokon, GPT-2 small, Pythia-160M és Qwen2.5-0.5B modellen, rétegenként.
- **E1:** propagáció, kúpmélység 1–4.
- **E2:** anomália-csepegtetés változó konfidenciával.
- **E3:** két forrás ütköző tényekkel, kontextusjellel és anélkül.
- **E4:** zajinjekció, ε ∈ {0; 0,02; 0,05; 0,1}.

**Előre rögzített cáfolati kritériumok**

| | Feltétel | Következmény |
|---|---|---|
| R0 | E0-ban F1 < 0,9 | Leállás. Az aktivációs grounding nem működik. |
| R1 | A K1 orákulum és az LLM-es változat ripple-recall-különbsége > 20 pont | A „neuro” fél a szűk keresztmetszet. |
| R2 | BeliefBank-szerű MaxSAT (kontextus és MDL nélkül) E1–E3-on 3 ponton belül van | A plusz gépezet nem indokolt. |
| R3 | ε = 0,05 mellett 50 megfigyelésenként több mint 1 hamis átrendezés | Használhatatlan. |
| R4 | P1 Spearman-korrelációja < 0,7 | Az MDL-trigger nem azt csinálja, amit állítunk. |
| R5 | A K2 (BoW) vagy a K3 (generált logikai forma) egyezik az aktivációs groundinggal | Az LLM-aktivációk feleslegesek. |

### Végkövetkeztetés

- Az átrendezés képessége mind a 8 ötletben **a szimbolikus algoritmus tulajdonsága**, és ez a rész klasszikus tudásreprezentáció.
- A fagyasztott LLM mindenhol valószínűségi érzékelő front-end. Ez a nyolc közül egyikben sem változott meg.
- Kérdés, hogy a fagyasztott aktivációk adnak-e kalibráltabb konfidenciát és jobb kontextusjelet a revízió típusának megválasztásához (elutasítás, visszavonás vagy szétválasztás), mint a generált szöveg parse-olása. Ez az R1, R2 és R5 kritériummal tesztelhető. Az újdonság gyanúja egyedül erre az állításra esik.
- Ha az R5 bukik, az egész gyakorlatilag egy LLM-parser és egy ICL-megoldó, és új architektúraként nem védhető.

---

## Hivatkozások, amelyeket ellenőrizni kell

A hivatkozások emlékezetből szerepelnek, nem ellenőriztem őket. Az újdonsági állítások előtt irodalomkeresés szükséges.

- de Kleer 1986 (ATMS); Doyle 1979 (TMS); Alchourrón–Gärdenfors–Makinson 1985 (AGM); Reiter 1987 (diagnózis)
- Kassner et al. 2021 (BeliefBank)
- Nelson–Oppen 1980; Downey–Sethi–Tarjan 1980; Nieuwenhuis–Oliveras 2005; Willsey et al. 2021 (egg)
- Clarke et al. 2000 (CEGAR); Omlin–Giles 1996; Weiss–Goldberg–Yahav 2018; Paige–Tarjan 1987; Elboher–Gottschlich–Katz 2020
- Thagard 1989 (ECHO); Swendsen–Wang 1987; Greig–Porteous–Seheult 1989; Richardson–Domingos 2006 (MLN)
- Gershman–Blei–Niv 2010; Gershman–Monfils–Norman–Niv 2017; Franklin et al. 2020 (SEM); Fountas et al. 2024 (EM-LLM); Das et al. 2024 (Larimar)
- Li et al. 2023 (ITI); Turner et al. 2023 (ActAdd); Zou et al. 2023 (RepE); Rimsky et al. 2024 (CAA); Hartvigsen et al. 2023 (GRACE); Mitchell et al. 2022 (SERAC)
- Rissanen 1978; Grünwald 2007; Vreeken–van Leeuwen–Siebes 2011 (Krimp); Ellis et al. 2021 (DreamCoder); Page 1954 (CUSUM)
- Hansen–Ghrist 2019, 2021; Gebhart–Hansen–Schrater 2023; Bodnar et al. 2022; Abramsky–Brandenburger 2011
- Poole 1993, 1997 (PHA / ICL); Kakas–Kowalski–Toni 1992; Milch et al. 2005 (BLOG); Brewka–Eiter 2007
- Cohen et al. 2024 (RippleEdits); Zhong et al. 2023 (MQuAKE); Pan et al. 2023 (Logic-LM); Olausson et al. 2023 (LINC)
- McClelland–McNaughton–O'Reilly 1995 (komplementer tanulórendszerek)
