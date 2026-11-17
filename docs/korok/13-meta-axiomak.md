# 13. kör – Az ARLC v2 saját kimondatlan axiómái

Az 1. fázist megismétlem, de most a saját túlélő tervemen. Mit feltételez az ARLC v2,
amit sehol nem mondtunk ki?

## Axiómák, tagadások, következmények

| # | Kimondatlan axióma | Tagadás | Mi következik |
|---|---|---|---|
| M1 | A tudás igen/nem literálokból áll. | A tudás fokozatos, mennyiségi vagy szerkezeti (számok, rangsorok, eloszlások). | Az MDL-pontszám kódhosszai folytonos értékekre is értelmezhetők, de a nogood fogalma elmosódik: „mennyire” ütközik. |
| M2 | Az átrendezés írásidőben történik (mohó). | Lusta átrendezés: nincs tárolt revízió, minden lekérdezésnél argumentáció dönt. | Az „azonnali” definíció szerint teljesül, a költség a lekérdezésre megy át. Lásd az alábbi L-ötletet. |
| M3 | Egyetlen LLM, egyetlen szempont. | Több fagyasztott LLM, különböző családokból. | A grounding-hibák kevésbé korreláltak (5. kör, D-ötlet függetlenségi problémája), és a támadónak több modellt kell becsapnia (12. kör). |
| M4 | A kontextusok diszkrétek és laposak. | A kontextusok hierarchiát vagy folytonos teret alkotnak. | A szétválasztás helyett finomhangolt hatókör: egy szabály „mennyire” érvényes egy kontextusban. |
| M5 | A rétegválasztás és az igazítás a sweep után rögzített. | Az igazítás fogalomfüggő: más fogalom más rétegben él. | Új fogalomnál újra kell illeszteni; az IIA (8. kör) jelzi, mikor. |
| M6 | A sémák deklaratívak (tények és szabályok). | A sémák procedurálisak: forgatókönyvek, események sorrendje. | Lásd az alábbi P-ötletet. |
| M7 | A rendszer passzívan fogadja a megfigyeléseket. | Aktívan kérdez, hogy a versengő hipotézisek közül döntsön. | Lásd az alábbi A-ötletet. |
| M8 | **A világ statikus, csak a hiedelmek változnak.** | **A világ változik.** Egy új tény azt is jelentheti, hogy a világ megváltozott, nem csak azt, hogy tévedtünk. | **Lásd az alábbi U-ötletet. Ez a legfontosabb hiány.** |

## Új ötletek a tagadásokból

### U – Frissítés vs. revízió (M8 tagadása) ★

- **A probléma:** Katsuno és Mendelzon (1991) óta ismert, hogy két különböző műveletről
  van szó:
  - *revízió:* tévedtünk, a világ mindig is ilyen volt;
  - *frissítés (update):* a világ megváltozott, a régi tény korábban igaz volt.
- Az ARLC mindkettőt revízióként kezeli. **Ez hiba.** Ha „Anna Budapesten lakik”, majd
  „Anna Bécsben lakik”, a revízió azt mondja, hogy soha nem lakott Budapesten. A
  helyes válasz: korábban ott lakott.
- **Formalizálás:** minden tény kap egy érvényességi intervallum-feltevést, `valid(f, [t₁, t₂))`.
  Az új operátor (e): *frissítés*. A régi tény intervallumát a t időpontban lezárjuk, nem
  vonjuk vissza.
- **Döntés:** az MDL-pontszám tartalmaz egy frissítési priort, ennek mértéke
  tulajdonságtípusonként eltér. A lakhely gyakran változik, az, hogy valami madár-e, szinte
  soha. **Ezt a priort az LLM-től lehet kérdezni:** „Változhat-e idővel X tulajdonság?”
  Ez az LLM tudásának egy újabb, értelmes felhasználása.
- **Legközelebbi munka:** Katsuno–Mendelzon 1991; temporális tudásgráfok és időérzékeny
  tudásszerkesztés (pl. „temporal knowledge editing”, 2024, ellenőrizendő).
- **Cáfolat:** egy olyan feladatkészleten, amely vegyesen tartalmaz revíziót és frissítést,
  az U-ötlet nem javítja a „korábban mi volt igaz?” típusú kérdések pontosságát
  legalább 20 ponttal.

### A – Aktív megkülönböztető kérdezés (M7 tagadása) ★

- **Ötlet:** a váltás előtt, ha a nyaláb két hipotézise közel áll, a rendszer kérdést tesz
  fel, amely a legjobban szétválasztja őket. A kérdést feltesz a felhasználónak, egy
  megbízható forrásnak, vagy az LLM-nek.
- **Formalizálás:** a q kérdés várható információnyeresége a nyaláb poszteriorján,
  `EIG(q) = H(ℋ) − E_{válasz}[H(ℋ | q, válasz)]`, és a legnagyobb EIG-ű kérdést tesszük fel.
- **Miért jó:** Posner termékenysége (7. kör) aktívan ellenőrizhető, és a 12. kör V4
  ideiglenes állapotát rövidíti. A támadó dolga nehezebb, mert a hamis séma jóslatai az
  aktív ellenőrzésen elbuknak.
- **Legközelebbi munka:** Bayes-i kísérlettervezés, aktív tanulás; „20 kérdés”-típusú
  LLM-ágensek. **Átcímkézésnek számít**, a hozzáadott érték csak a nyalábbal és az
  MDL-pontszámmal való összekötés.

### L – Lusta argumentáció (M2 tagadása)

- **Ötlet:** nincs tárolt revízió. Minden lekérdezésnél a rendszer argumentumokat épít
  (Dung 1995 absztrakt argumentációs keretrendszer, ASPIC+). Az ütközéseket az
  argumentumok közti támadási reláció dönti el, az elfogadott szemantika szerint.
- **Előny:** az átrendezés definíció szerint azonnali, mert semmit nem kell átírni.
- **Hátrány:** minden lekérdezés drága. Ugyanaz a konfliktus újra és újra feloldódik.
- **Hibrid (JIT):** lusta, amíg egy séma ritkán szerepel; ha gyakran, a feloldás
  „lefordul” mohó revízióvá. Ez a 10. kör anytime revíziójának egy variánsa.
- **Átcímkézés?** Igen, az argumentációelmélet és a TMS kapcsolata ismert. Új csak a
  JIT-hibrid költségmodellje.

### P – Procedurális sémák (M6 tagadása)

- **Ötlet:** a séma egy forgatókönyv (Schank–Abelson 1977): események részben rendezett
  halmaza előfeltételekkel. Klasszikus példa: étterem → „rendelés, evés, fizetés”.
- **Meglepetés:** egy esemény, amely sérti a sorrendet („először fizettünk”).
- **Átrendezés:** a részben rendezés minimális szerkesztése, VAGY kontextus-szétválasztás
  („gyorsétterem” mint új forgatókönyv-változat). **Ez ugyanaz, mint az ARLC (c) operátora,**
  csak eseménysorrendre alkalmazva. Az ARLC tehát kiterjeszthető forgatókönyvekre a nyelv
  bővítésével, új mechanizmus nélkül.
- **Miért érdekes az LLM szempontjából:** az LLM-ek nagyon jól ismerik a hétköznapi
  forgatókönyveket. A procedurális tudás grounding-ja ezért valószínűleg könnyebb, mint a
  kategóriáké.

### T – Több LLM mint több szem (M3 tagadása)

- **Ötlet:** két különböző családba tartozó kis modell (pl. Qwen2.5-0.5B és Pythia-410M)
  egymástól függetlenül groundingol. A literál csak akkor kerül be, ha mindkettő egyetért.
- **Várt hatás:** a parafrázis-szavazásnál (1. fázis közös keret) jobban csökkenti a
  zajt, mert a hibák kevésbé korrelálnak.
- **Cáfolat:** ha a két modell hibakorrelációja nem kisebb, mint a parafrázisoké
  ugyanazon a modellen, nincs nyereség.

## Rangsor és rombolás

**A két legfontosabb: U és A.**

**Az U rombolása:**
- *Ellenvetés:* a frissítés és a revízió szétválasztása a szövegből gyakran eldönthetetlen.
  „A Plútó nem bolygó.” Ez frissítés (2006-ban változott a definíció) vagy revízió (soha
  nem volt az)? *Válasz:* ez a kétértelműség valódi. A rendszernek mindkét értelmezést
  meg kell tartania a nyalábban, és ez pont az A-ötlet (aktív kérdezés) tipikus esete.
- *Ellenvetés:* az intervallum-feltevések felrobbantják a címkeméretet. *Válasz:* igen.
  Csak azoknál a tulajdonságtípusoknál kell, ahol a frissítési prior nem elhanyagolható.
- **Túléli.** Ez a kör legfontosabb kimenete. Az ARLC v3-ba bekerül az (e) operátor.

**Az A rombolása:**
- *Ellenvetés:* az LLM-től kérdezni körbeforgás, mert ugyanaz a forrás, amely a priort is adja.
  *Válasz:* a kérdés lehet a felhasználó felé is, de offline kísérletben csak az orákulum
  vagy az LLM áll rendelkezésre. Az orákulum-változat a felső korlát.
- *Ellenvetés:* a nyaláb nem mindig tartalmazza a helyes hipotézist (10. kör M2). Ilyenkor
  a kérdezés két rossz közül választ.
- **Túléli, gyengébb formában.** Hasznos, de nem alapvető.

**ARLC v3 bővítései ebből a körből:** (e) frissítés-operátor intervallum-feltevésekkel;
aktív kérdezés EIG szerint, ha a nyaláb két legjobb hipotézisének pontszámkülönbsége
egy küszöb alatt van; a hipotézisnyelv bővítése forgatókönyvekre.
