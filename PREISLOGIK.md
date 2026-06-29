# Preislogik — Business-Übersicht

**Stand:** 2026-06-25 (Marge-Modell E104 + GLD-Aufschlag E103). Gilt für alle Pipeline-Artikel.

## Die Idee in einem Satz
Wir rechnen den Verkaufspreis **aus den echten Kosten auf eine feste Ziel-Marge** — nicht mehr über Faustformeln und Puffer. Es gibt nur **einen Hebel: die GLD** (unsere Stück-Kosten). Ändert sich die GLD, folgt der VK automatisch.

## Der Rechenweg (4 Schritte)
1. **Netto-EK** des Lieferanten, in EUR umgerechnet (falls Rechnung in USD/AUD).
2. **+ Beschaffungs-Aufschlag** = unsere **GLD** (Ø-Netto-EK, die „echten" Stück-Kosten):
   - **EU-Lieferant:** + **1,00 €** (innereurop. Versand/Bank, kein Zoll)
   - **Nicht-EU-Lieferant:** + **5,00 €** (Zoll ~12 % + Fracht + Bank, bewusst konservativ)
   - Fremdwährungs-EK vorher mit **festem konservativem Kurs** in EUR (USD 0,95 / AUD 0,65) — bewusst „schlechter Kurs" als Puffer, **nicht** tageskursabhängig.
3. **Brutto-VK** so gewählt, dass die **Marge = 40 %** (JTL-Spalte „Gewinn %", also Netto-VK gegen die GLD). Rechnerisch: `Netto-VK = GLD / 0,60`, dann **+ 19 % MwSt**.
4. **Kaufmännisch auf X,90** runden (Charm: keine runden Zehner, z. B. 40,90 → 39,90).

## Warum das eine Vereinfachung ist
- **Früher:** „EK × 2" auf den Bruttopreis (MwSt fraß die Marge → nur ~37 %), plus zwei separate Puffer (+1 € EU auf EK, +5 € Nicht-EU auf VK), plus ein GLD-Aufschlag — drei Hebel, die sich gegenseitig verzerrten, Ergebnis-Marge unklar (~37–50 %).
- **Jetzt:** **ein** Hebel (GLD = echte Kosten), **eine** Zielgröße (40 % Marge). Der VK ist immer das Ergebnis daraus. Die alten Puffer sind weg — die Kosten stecken sauber in der GLD.
- **40 %** ist der **Haus-Standard**, an dem auch das Bestandssortiment liegt (Bandurska ~42 %, FANNA/Shark/Juicee ~40 %). Wir sind damit weder zu teuer (Konkurrenz) noch zu knapp.

## Konkret (Beispiele)
| Lieferant | Netto-EK | + Aufschlag | GLD | Brutto-VK | Marge |
|---|---|---|---|---|---|
| HotCakes (EU) | 21,00 € | +1,00 | 22,00 € | **43,90 €** | ~40 % |
| Paradise Chick (EU) | 26,61 € | +1,00 | 27,61 € | **54,90 €** | ~40 % |
| Shark (Nicht-EU, USD) | 22,57 € | +5,00 | 27,57 € | **54,90 €** | ~40 % |

## Übergangslösung → Zukunft
Die Aufschläge **1,00 € (EU) / 5,00 € (Nicht-EU)** und die festen Kurse (USD 0,95 / AUD 0,65) sind **konservative Pauschalen** — bewusst eher zu hoch angesetzt, damit die Marge auch bei Zoll, Fracht und ungünstigem Wechselkurs sicher steht (lieber etwas höherer VK als die Arbeit umsonst). **Nächster Schritt (Backlog B68/B70):** statt Pauschalen die **echten historischen Beschaffungskosten pro Lieferant** ansetzen — über eine Anbindung an ein Buchhaltungssystem, in dem die historischen Rechnungen je Lieferant sichtbar sind. Dann ist die GLD exakt, und der VK stimmt automatisch mit, ohne je wieder am Preis zu schrauben.
