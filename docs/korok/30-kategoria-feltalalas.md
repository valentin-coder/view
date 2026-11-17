# 30. kör – Kategória-feltalálás anomáliákból (Thagard 6. fokozata)

## Kérdés

A 27. körben bevezetett osztályszintű kivétel csak *megnevezett* alosztályra működik. Ha az
anomáliák egy közös, de meg nem nevezett tulajdonságban osztoznak (például mind csíkosak), a
rendszer nem talál osztályszintű megoldást. Képes-e az ARLC **új fogalmat alkotni**
(c′ = dax ∧ csíkos, és c′ → ¬mérges)? Ha igen, **általánosít-e** ez a fogalom új, nem látott
példányokra? Utóbbi különbözteti meg a fogalomalkotást a kivételek puszta tömörítésétől.

Megvalósítás: [`core.py`](../../experiments/arlc/arlc/core.py) (`_invent`, kétfeltételes szabály) és
[`invention.py`](../../experiments/arlc/arlc/invention.py); nyers eredmény:
[`results/kor-30/results.json`](../../experiments/arlc/results/kor-30/results.json).

## Formalizálás

- **Új szabálytípus:** `isa(X, c) ∧ has(X, F) → isa(X, c′)`. A feltétel explicit tény kell
  legyen; levezetett tényre nem működik.
- **Feltalálási lépés:** ha a `c → p` szabálynak legalább 2 olyan tagja van, amelyről ¬p-t
  figyeltünk meg, és ezek mind osztoznak egy F tényben, amelyet a „normális” tagok (p-vel)
  közül egyik sem mutat, akkor a jelölt a következő:
  - új kategória `c′ = c ∧ F`;
  - új szabály `c′ → ¬p`;
  - osztályszintű kivétel: a `c → p` szabály nem vonatkozik c′-re;
  - az érintett példányszintű kivételek és elutasítások visszavonása.
- **Költség:** két indukált szabály (egyenként `log₂(2·|C|·|P|)` bit) és egy osztályszintű
  kivétel (`log₂|C| + 1`), itt összesen kb. 15 bit. **Megtérül**, ha az így megmagyarázott
  anomáliák együttes megtakarítása (anomáliánként kb. 3,9 bit az elutasításhoz képest, kb. 0,93
  bit a szabály elvetéséhez képest) ennél nagyobb.
- **Fontos:** az MDL csak a *látott* adat tömörítését jutalmazza. Az általánosítás haszna nem
  része a pontszámnak; az csak mellékterméke lehet.

## Elrendezés

N normál dax (mérges, nem csíkos), m anomális dax (csíkos, nem mérges, mindegyik más friss
forrásból), és véletlen zavaró attribútumok (40% eséllyel öt másik tulajdonság). Utána négy új
csíkos és négy új sima dax, csak tagsággal és csíkossággal. **Általánosítás:** a csíkosakról
„nem mérges”, a simákról „mérges” a helyes válasz. Három változat: feltalálás nélkül;
feltalálással; és feltalálással, amely egy már elvetett szabályt is visszavehet. 3 seed;
„vegyes” változatban egy normál dax is csíkos.

## Eredmények (tiszta jel)

Cellák: feltalált kategória aránya / általánosítás (csíkos helyes; sima helyes).

| N | változat | m = 3 | m = 4 | m = 5 | m = 6 | m = 8 |
|---|---|---|---|---|---|---|
| 4 | nincs | 0% / 0,00; 0,00 | 0% / 0,00; 0,00 | 0% | 0% | 0% |
| 4 | feltalálás | 0% | 0% | 0% | 0% | 33% / 0,33; 0,33 |
| 4 | + visszavétel | 0% | 0% | 0% | 33% | **100% / 1,00; 1,00** |
| 8 | nincs | 0% / 0,00; 1,00 | 0% / 0,00; 0,00 | 0% | 0% | 0% |
| 8 | feltalálás | 0% | 67% | 33% | **0%** | **0%** |
| 8 | + visszavétel | 0% | **100% / 1,00; 1,00** | 100% | 100% | 100% |
| 12 | feltalálás | 0% | 100% | 100% | 33% | **0%** |
| 12 | + visszavétel | 0% | **100%** | 100% | 100% | 100% |

## Értelmezés

1. **A fogalomalkotás működik, és általánosít.** Visszavétellel, N ≥ 8 mellett 4 anomáliától
   kezdve a rendszer 100%-ban feltalálja a „dax & csíkos” kategóriát. Az új csíkos daxokról
   helyesen „nem mérges”, a simákról „mérges” a válasz (1,00/1,00). **Ez nem kivétel-tömörítés:
   a nem látott példányokra is helyes jóslatot ad.**
2. **Visszavétel nélkül útfüggés lép fel, és ez a kör legfontosabb mechanikai megállapítása.**
   A „feltalálás” sorban az arány a 4–5. anomália után *csökken* (N = 8-nál 67% → 0%). Ekkor a
   szabály elvetése még olcsóbb, mint az új kategória modellköltsége, és ha a szabály egyszer
   kiesett, a feltalálás már nem jöhet szóba. **A rendszer túl korán feladja az elméletet, és
   ezzel elzárja magát a finomítás elől.** Ez a „korai elméletfeladás” mint a
   fogalomalkotás akadálya. A tudománytörténeti párhuzam kézenfekvő, de csak analógia.
3. **Kis beágyazottságnál (N = 4) a feltaláláshoz sok anomália kell** (8), mert a szabály elvetése
   nagyon olcsó. Ez arányos: egy alig alátámasztott szabályt nem éri meg finomítani.
4. **Vegyes jel (egy normál dax is csíkos):** a rendszer feltalálja a kategóriát és az
   osztályszintű kivételt, de a „csíkos dax nem mérges” szabályt az ellenpélda miatt eldobja.
   A végső állapot: „a csíkos daxok mérgességéről nem tudunk semmit”. **Ez a Chinn–Brewer-féle
   kizárás**, és vegyes evidencia mellett ez a helyes ismeretelméleti álláspont. Az
   általánosítási mérőszám ezt tévesen kudarcnak számolja (a válasz „nem tudom”, nem „nem
   mérges”).

## Korlátok

- **A jelöltgenerálás szigorú:** csak olyan F jöhet szóba, amelyet *egyik* normál tag sem mutat.
  Valódi adatban a jel ritkán ilyen tiszta. Egy valószínűségi változat (F jól elválaszt, de nem
  tökéletesen) a következő lépés.
- **Csak egy feltétel**, explicit tényként. Kétfeltételes vagy levezetett feltétel nincs.
- **A zavaró attribútumok** (40%) itt nem okoztak hamis feltalálást, mert a szigorú elválasztás
  kizárta őket. Laza változatnál ez lesz a fő kockázat: túltanulás véletlen közös jegyekre.
- **Átcímkézés-gyanú:** ez a predikátum-invenció (induktív logikai programozás; Muggleton és
  Buntine 1988, Cropper és Muggleton munkái, ellenőrizendő) egyszerű, MDL-vezérelt formája. Az
  új elem az, hogy *revízió közben*, anomáliák hatására indul, egy nem monoton revíziós
  keretben, és a visszavétel szerepe (2. pont).

## Következmény az architektúrára

- ARLC v4: a feltalálás része a revíziós lépéseknek, visszavétellel együtt.
- Thagard 6. fokozata (új fogalom) szimbolikus szinten megvalósítható. A 9. kör szerint ez az
  ARLC-ből „részben” hiányzott, most a szimbolikus fele megvan. A grounding fele (az új fogalomnak
  nincs iránya az LLM-ben) továbbra is nyitott.
