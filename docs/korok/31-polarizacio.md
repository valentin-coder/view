# 31. kör – Többágenses ARLC: két külön polarizációs mechanizmus

## Kérdés

A 17. kör gyenge előzetes eloszlás mellett megerősítési torzítást mutatott: az elsőként érkező
forrás nyer, a második „hazug” lesz. Ha több ARLC-ágens egymás forrásai, okoz-e ez
csoportszintű polarizációt, ahogy a Laputa-modellben (Olsson 2013, ellenőrizendő)?

Megvalósítás: [`experiments/arlc/arlc/multiagent.py`](../../experiments/arlc/arlc/multiagent.py); nyers
eredmények: [`experiments/arlc/results/kor-31/results.json`](../../experiments/arlc/results/kor-31/results.json).

## Elrendezés

- **6 ágens, két tábor.** Az A tábor tankönyve szerint „a dax mérges” (ez az igazság), a B
  táboré szerint „nem mérges” (q = 0,95).
- **12 kör.** Körönként minden ágens kap egy zajos privát megfigyelést (q = 0,8, hibaarány ε) egy
  véletlen daxról, és minden szomszédjától egy állítást.
- **Mit mondanak a szomszédok?** Két változat:
  - *hiedelem:* a szomszéd a saját aktuális (levezetett) hiedelmét mondja egy véletlen daxról,
    forrásként a saját nevével;
  - *nyers:* a szomszéd a legutóbbi nyers érzékelését adja tovább, forrásként az eredeti érzékelővel.
- **Hálózat:** teljes, vagy két klikk (a táborok szerint) egyetlen híddal.
- **Változók:** κ ∈ {3, 30, 100}, ε ∈ {0,1; 0,3; 0,45}, 3 seed. Tanult megbízhatóság, indukció
  bekapcsolva.
- **Mérés:** a szabályszintű hiedelem (igaz / hamis / nem tudja) aránya, polarizáció (van igaz és
  hamis is), entitásszintű pontosság táboronként, és hogy a másik tábortól jövő állítások hány
  %-át utasítja el egy ágens.

## Eredmények

| továbbadás | hálózat | ε | κ | igaz | hamis | polarizált | entitásszintű pontosság A / B |
|---|---|---|---|---|---|---|---|
| hiedelem | teljes | 0,1–0,45 | bármely | 0,94–1,00 | 0 | **0%** | 0,97–1,00 / 0,97–1,00 |
| hiedelem | **klikkek** | 0,1–0,45 | **bármely** | 0,50 | 0,50 | **100%** | 1,00 / **0,00** |
| nyers | teljes | 0,1–0,45 | bármely | 0,94–1,00 | 0 | 0% | 0,95–1,00 |
| nyers | klikkek | 0,1 | bármely | 1,00 | 0 | **0%** | 0,97–1,00 |
| nyers | klikkek | 0,3 | 3 | 0,72 | 0,06 | **33%** | 0,99 / 0,75 |
| nyers | klikkek | 0,3 | 30–100 | 0,72 | 0 | 0% | 0,99 / 0,84 |
| nyers | klikkek | 0,45 | 3 | 0,61 | 0,17 | **67%** | 1,00 / 0,50 |
| nyers | klikkek | 0,45 | 30–100 | 0,61–0,67 | 0 | 0% | 1,00 / 0,69–0,73 |

## Értelmezés: két mechanizmus

1. **Visszhang és kettős számolás (hiedelem továbbadása klikkben): 100% polarizáció, κ-tól és
   zajtól függetlenül**, ε = 0,1-nél is, pedig ott a privát evidencia 90%-ban az igazságot
   mutatja. A B klikk tagjai a *tankönyvükből levezetett* állításokat mondják egymásnak, és a
   címzett ezeket független megfigyelésnek veszi. Körönként két „hamis” társas állítás jut egy
   igaz privát megfigyelésre, és a B ágens a másik tábor állításait 96–100%-ban elutasítja.
   **Ez nem bizalomtanulási hatás, hanem a származás (provenance) elvesztése.** Ugyanaz a
   tankönyv-állítás többszörösen visszhangzik.
2. **Bizalomtanulás okozta (Laputa-típusú) polarizáció:** nyers továbbadás mellett csak kis κ
   (κ = 3) és gyenge evidencia (ε ≥ 0,3) esetén jelenik meg (33–67%). κ ≥ 30-nál eltűnik. Ez a 17.
   kör megerősítési torzításának csoportszintű következménye, de **sokkal gyengébb**, mint az első
   mechanizmus.
3. **Teljes hálózatban egyik sem lép fel.** A két tábor állításai kioltják egymást, és a privát
   evidencia dönt. Még ε = 0,45-nél is (csak 55%-ban helyes privát jel) 94% konvergál.

## Kapcsolódás

- **Információs kaszkádok és kettős számolás:** a korrelált tanúvallomás független evidenciaként
  kezelése klasszikus hiba (pl. „echo chamber” modellek; a DeGroot-típusú átlagolásban a
  „persuasion bias”, DeMarzo, Vayanos és Zwiebel 2003, ellenőrizendő).
- **Laputa** (Olsson 2013): a forrásbizalom tanulása önmagában racionális polarizációt okozhat.
  Itt ez a második mechanizmus, és csak kis κ mellett jelenik meg.
- **Jern, Chang és Kemp 2014:** a polarizáció nem mindig irracionális. Itt a második mechanizmus
  „racionális” (a modell normatív), az első egy *modellezési hiba* (a függetlenség feltételezése).

## Következmények az architektúrára

1. **A származás elsőrendű.** Az ARLC-ben minden megfigyelés forrása egy név. Kell egy
   *származási lánc* is: ha egy állítás egy másik ágens levezetéséből jön, akkor az eredeti
   alátámasztó feltevésekre kell visszavezetni, nem új, független forrásként kezelni. Ez az ATMS
   támaszhalmazainak (15. kör) ágensek közötti kiterjesztése: **a kommunikált állítás hordozza a
   támaszát.**
2. **A 20. kör „függetlenségi jele” itt konkrét alakot ölt:** két állítás akkor független, ha a
   támaszhalmazuk diszjunkt. Szövegből ez nem olvasható ki, kell hozzá a származás vagy egy becslés
   (pl. az LLM-ből a stílus- és tartalomhasonlóság).
3. **Megszorítás:** 6 ágens, egy szabály, egyszerű hálózatok. A klikk szerkezete pontosan a
   táborokat követi, ez a polarizáció legkedvezőbb esete.
