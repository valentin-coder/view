# 67. kör – Azonosíthatóság: döntési margó meglepetéstípusonként (feltáró)

## 1. rész: terv és jóslat (a futtatás előtt)

A 62. kör szerint a „más régió” eset holtverseny. A 64. kör javaslata: minden meglepetéstípusra mérni kell, mennyire
dönti el az adat a célkérdést. Olcsó közelítés a **döntési margó**: L(H\*) − L(MAP), ahol H\* a nyaláb legjobb olyan
hipotézise, amely legalább egy célkérdésre mást válaszol. Ha nincs ilyen, a nyaláb teljes szórása alsó becslés.
**Korlát:** a 63. kör szerint a nyaláb nem poszterior-minta, ezért a margó felülbecsülheti az azonosíthatóságot,
ha a nyaláb nem tartalmazza a versengő magyarázatot.

Kód: [`run_r67.py`](../../experiments/arlc/arlc/run_r67.py). A populáció, seed 9000–9014 (friss), 5 típus, v4.8-π.

**Jóslatok (a futtatás előtt):**
- **J1:** a „más régió” típus medián margója a legkisebb (< 1 bit).
- **J2:** a target-acc a margóval nő: a < 1 bites esetekben legfeljebb 0,6, a > 3 bitesekben legalább 0,8.

## 2. rész: eredmények

*(a futtatás után)*
