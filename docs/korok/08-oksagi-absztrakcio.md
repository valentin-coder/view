# 8. kör – Újrakeretezés: online oksági absztrakció, és honnan jönnek a szabályok

## A felismerés

A KTP-ben a szimbolikus réteg kimondja, hogy „a rigó hal”, mi a kategória-változót
beavatkozással átírjuk az LLM reprezentációjában, és megnézzük, követik-e a tulajdonságok.
Ez **pontosan egy interchange-intervenció** az oksági absztrakció irodalmának értelmében
[Geiger, Lu, Icard, Potts 2021; Geiger et al. 2023/2024, DAS]. Ott a kérdés az, hogy egy
magas szintű oksági modell (szimbolikus változók és élek) *implementálja-e* a hálózatot:
ha a magas szintű változót beavatkozással átállítjuk, a hálózat kimenete úgy változik-e,
ahogy a magas szintű modell jósolja.

**Ebből egy újrakeretezés adódik:** az ARLC szimbolikus rétege nem egy külön tudásbázis,
hanem **a fagyasztott LLM egy magas szintű oksági absztrakciója, kiegészítve a világról
szóló új tényekkel**. A szimbolikus átrendezés ennek az absztrakciónak a karbantartása.

## Formalizálás

- **Magas szintű modell:** `𝓗 = (V, E, f)`. V a szimbolikus változók halmaza (entitás
  kategóriája, tulajdonságok), E az élek (`kategória → tulajdonság`), f a mechanizmusok
  (szabálytáblák).
- **Igazítás (alignment):** `π: V → altér-régiók a reziduális áramban`, az ℓ rétegben.
  A KTP-ben ez zárt alakú: a kategória-altér (`P_K`) és a kategóriaátlagok (μ).
- **Interchange-intervenciós pontosság (IIA):** mekkora arányban egyezik a hálózat
  kimenete a magas szintű modell jóslatával, ha a v változót π szerint beavatkozással
  egy másik bemenet értékére állítjuk.
- **Az ARLC kiterjesztése:** minden szabály (él) mellé egy *eredetcímke* kerül:
  - `ext`: szövegből kimondott, külső tény;
  - `llm`: az LLM-ből interventív úton kiolvasott;
  - `rev`: revízió eredménye.

## Válasz a nyitott kérdésre: interventív szabálybányászat

Az 5. körben a B-ötlet (geometriai tartalmazás) volt a javaslat a szabályok forrására, és
az R8 kritérium szerint lehet, hogy elbukik. Az oksági keretezés jobb forrást ad:

**Interventív szabálybányászat (ISZB):** az `a → b` szabály akkor és csak akkor kerül
a szimbolikus rétegbe `llm` eredettel, ha:
1. *megfigyelés szerint:* a szerkesztetlen modell az a-tagokra b-t, a nem-a-tagokra
   nem-b-t mond (ez a KTP tudásszűrője, prototípusokon);
2. *interventív szerint:* ha egy nem-a entitást transzplantációval a-ba visszük, a b
   megjelenik; ha egy a-entitást kiviszünk, eltűnik. Az ehhez tartozó IIA legalább `γ`.

Az 1. feltétel a korreláció, a 2. azt mutatja, hogy az LLM ezt az összefüggést valóban
*használja*. Ez erősebb, mint a geometriai tartalmazás, és **a KTP mérése melléktermékként
megadja**: a KTP D-kérdésein mért ripple-recall kategória-tulajdonság páronként éppen
ennek az élnek az IIA-ja.

**A KTP és a szabálybányászat tehát ugyanaz a kísérlet, más nézőpontból.** A KTP azt
kérdezi, vezeti-e az LLM a következményeket, az ISZB pedig azt, mely élek léteznek az LLM-ben.

## Legközelebbi munkák

| Munka | Mit csinál | Eltérés |
|---|---|---|
| Geiger et al. 2021 (causal abstraction) | magas szintű modellt illeszt NN-re interchange-intervencióval | offline elemzés, a magas szintű modellt kézzel adják, nem frissül |
| DAS [Geiger et al. 2024] | forgatást tanul az igazításhoz (gradiens az igazításon, nem a súlyokon) | nálunk zárt alakú; olcsóbb, de gyengébb |
| **RAVEL** [Huang et al. 2024] | entitás-attribútumok szétválaszthatóságát méri intervencióval | **nagyon közel a KTP S2-kérdéséhez** (megtartódik-e az egyéni attribútum). Ezt kell először elolvasni, mielőtt a KTP-t újnak állítjuk. |
| Interpretálható tudásbázis-kinyerés (LAMA [Petroni et al. 2019]; Cohen et al. 2023 „Crawling the internal KB”) | a tudást *promptolással* olvassa ki | megfigyelés, nem intervenció |

**Őszintén:** az „online oksági absztrakció” kifejezésre a 2024-es irodalom után nem
tudok konkrét előzményt, de az alkotóelemek mind ismertek. Új csak a kombináció lehet:
*folyamatosan frissített* magas szintű modell, amelyet az LLM-től független, világról
szóló új tények is módosítanak, és amely intervencióval vissza is hat. **Kifejezetten
keresni kell rá:** „online causal abstraction”, „causal abstraction knowledge editing”.

## Új kísérlet: ISZB-pilot (a KTP kódjára épül)

- **Feladat:** a 6 kategória × 17 tulajdonság mátrix minden élére IIA-t mérni
  transzplantációval, mindkét irányban (be- és kivitel).
- **Igazság:** a `data.py` tulajdonságtáblája (a kézzel írt ontológia).
- **Mérőszám:** az élek kinyerésének pontossága és fedése γ küszöb mellett, összevetve a
  promptolásos kinyeréssel („Does a fish have fins?”, ez a B2 logikája kategóriaszinten).
- **Cáfolat:**
  - Az interventív élek F1-e nem jobb a promptolásosénál 0,05-tel. Ekkor az intervenció
    nem ad többet a kérdezésnél, és a szabályokat egyszerűbb promptolással kinyerni.
  - VAGY az IIA-k kategóriapárok között erősen ingadoznak (szórás > 0,3 azonos élre).
    Ekkor az igazítás nem stabil, a keretezés nem működik.
- **Költség:** a KTP sweep után a választott konfigurációval kb. 6 × 5 × 17 × 2
  intervenció entitásonként. CPU-n percek.

## Mit ad ez a keret, amit eddig nem adtunk meg?

1. **Válasz arra, honnan jönnek a szabályok:** intervencióval, és nem csak abból, amit kimondanak.
2. **Mérhető fogalom a „jó igazításra”:** az IIA. Eddig a groundinghoz csak F1 volt.
3. **Kudarckritérium a teljes neuroszimbolikus állításra:** ha a frissített magas szintű
   modell IIA-ja a revízió után jelentősen esik, akkor a szimbolikus átrendezés
   és az LLM elvált egymástól. A szimbolikus réteg ilyenkor már csak külön tudásbázis,
   nem az LLM absztrakciója. Ez az L1 lyuk (a 4. kör szerint az LLM pótolható) mérhető
   formában.
