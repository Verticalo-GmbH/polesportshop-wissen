"""
Content-Builder (Hybrid, P5): erzeugt pipeline/content/hotcakes_content.json.

- artikeldetails: hand-autoriert (E74/E82-Stil), als strukturierte Teile (h2/p/li),
  HTML wird programmatisch zusammengesetzt -> keine Quote-Konflikte.
- material_and_care + size_and_fit: programmatisch aus Datentabellen (template-fähig),
  in 5 Sprachen, E78-konform.
- merkmal_farbe + style_werte: pro Modell gesetzt (aus body_html-Cues).

Aufruf: python -m pipeline.content_build  (schreibt JSON, validiert Style/Schema).
"""
from __future__ import annotations

import json
from . import config, constants as C, spec

LANGS = C.LANGUAGES

# --- Material-/Pflege-Lokalisierung --------------------------------------
MAT = {
    "polyester": {"de": "Polyester", "en": "Polyester", "fr": "Polyester", "it": "Poliestere", "es": "Poliéster"},
    "polyamide": {"de": "Polyamid", "en": "Polyamide", "fr": "Polyamide", "it": "Poliammide", "es": "Poliamida"},
    "elastane":  {"de": "Elasthan", "en": "Spandex", "fr": "Élasthanne", "it": "Elastan", "es": "Elastano"},
}
LABEL = {
    "printed": {"de": "Bedruckter Stoff", "en": "Printed fabric", "fr": "Tissu imprimé", "it": "Tessuto stampato", "es": "Tejido estampado"},
    "tulle":   {"de": "Tüll", "en": "Tulle", "fr": "Tulle", "it": "Tulle", "es": "Tul"},
}
CARE = {
    30: {"de": "Handwäsche bei 30°C, nicht bleichen, nicht in den Trockner, nicht bügeln, nicht chemisch reinigen.",
         "en": "Hand wash at 30°C, do not bleach, do not tumble dry, do not iron, do not dry clean.",
         "fr": "Lavage à la main à 30°C, ne pas blanchir, ne pas sécher en machine, ne pas repasser, ne pas nettoyer à sec.",
         "it": "Lavare a mano a 30°C, non candeggiare, non asciugare in asciugatrice, non stirare, non lavare a secco.",
         "es": "Lavar a mano a 30°C, no usar lejía, no secar en secadora, no planchar, no limpiar en seco."},
    40: {"de": "Handwäsche oder Maschinenwäsche bei 40°C, nicht bleichen, nicht in den Trockner, nicht bügeln, nicht chemisch reinigen.",
         "en": "Hand or machine wash at 40°C, do not bleach, do not tumble dry, do not iron, do not dry clean.",
         "fr": "Lavage à la main ou en machine à 40°C, ne pas blanchir, ne pas sécher en machine, ne pas repasser, ne pas nettoyer à sec.",
         "it": "Lavare a mano o in lavatrice a 40°C, non candeggiare, non asciugare in asciugatrice, non stirare, non lavare a secco.",
         "es": "Lavar a mano o a máquina a 40°C, no usar lejía, no secar en secadora, no planchar, no limpiar en seco."},
}
FITNOTE = {
    "true":     {"de": "fällt größengetreu aus", "en": "runs true to size", "fr": "taille normalement", "it": "veste fedele alla taglia", "es": "talla de forma fiel"},
    "bit_small":{"de": "fällt etwas klein aus", "en": "runs a bit small", "fr": "taille un peu petit", "it": "veste un po' piccolo", "es": "talla un poco pequeño"},
    "small_up": {"de": "fällt klein aus, wir empfehlen eine Nummer größer", "en": "runs small, we recommend sizing up", "fr": "taille petit, prends une taille au-dessus", "it": "veste piccolo, consigliamo una taglia in più", "es": "talla pequeño, recomendamos una talla más"},
}
MASS = {"de": ("Brust", "Taille", "Hüfte", "Körpergröße"),
        "en": ("bust", "waist", "hips", "tall"),
        "fr": ("de poitrine", "de taille", "de hanches", "mesure"),
        "it": ("di seno", "di vita", "di fianchi", "è alta"),
        "es": ("de pecho", "de cintura", "de cadera", "mide")}


def _mat_p1(groups, lang):
    parts = []
    for label, comps in groups:
        s = ", ".join(f"{pct}% {MAT[m][lang]}" for pct, m in comps)
        parts.append((LABEL[label][lang] + " " if label else "") + s + ".")
    return " ".join(parts)


def material_and_care(groups, temp):
    return {lang: f"<p>{_mat_p1(groups, lang)}</p><p>{CARE[temp][lang]}</p>" for lang in LANGS}


def _height(h, lang):
    return (f"{h:.2f}".replace(".", "," if lang != "en" else ".")) + " m"


def size_and_fit(modell, model, h, size, b, w, hp, fit):
    out = {}
    for lang in LANGS:
        bust, waist, hips, tall = MASS[lang]
        fn = FITNOTE[fit][lang]
        if lang == "de":
            base = f"{model} trägt Größe {size} bei {_height(h,lang)} Körpergröße"
            meas = f", mit {b} cm Brust, {w} cm Taille und {hp} cm Hüfte" if b else ""
            out[lang] = f"<p>{base}{meas}. {modell} {fn}.</p>"
        elif lang == "en":
            base = f"{model} is {_height(h,lang)} tall and wears size {size}"
            meas = f", with a {b} cm bust, {w} cm waist and {hp} cm hips" if b else ""
            out[lang] = f"<p>{base}{meas}. {modell} {fn}.</p>"
        elif lang == "fr":
            base = f"{model} mesure {_height(h,lang)} et porte la taille {size}"
            meas = f", avec {b} cm de poitrine, {w} cm de taille et {hp} cm de hanches" if b else ""
            out[lang] = f"<p>{base}{meas}. {modell} {fn}.</p>"
        elif lang == "it":
            base = f"{model} è alta {_height(h,lang)} e indossa la taglia {size}"
            meas = f", con {b} cm di seno, {w} cm di vita e {hp} cm di fianchi" if b else ""
            out[lang] = f"<p>{base}{meas}. {modell} {fn}.</p>"
        else:  # es
            base = f"{model} mide {_height(h,lang)} y lleva la talla {size}"
            meas = f", con {b} cm de pecho, {w} cm de cintura y {hp} cm de cadera" if b else ""
            out[lang] = f"<p>{base}{meas}. {modell} {fn}.</p>"
    return out


def _assemble_ad(parts):
    """parts[lang] = {'h2':str,'p':[..],'li':[..]} -> HTML pro Sprache."""
    out = {}
    for lang in LANGS:
        pr = parts[lang]
        html = f"<h2>{pr['h2']}</h2>"
        html += "".join(f"<p>{p}</p>" for p in pr["p"])
        html += '<ul class="check">' + "".join(f"<li>{li}</li>" for li in pr["li"]) + "</ul>"
        out[lang] = html
    return out


# === MODELL-DATEN (Batch 1: Hekate, Peonies, Dark Roast, Toffee Latte, Arachne) ===
# Jeder Eintrag: farbe(Merkmal), style[], ad{lang:{h2,p[],li[]}}, mat, care, size
MODELS: dict[str, dict] = {}

def M(artnr, farbe, style, ad, mat, care, size):
    MODELS[artnr] = {"merkmal_farbe": farbe, "style_werte": style,
                     "attribute": {"artikeldetails": _assemble_ad(ad),
                                   "material_and_care": material_and_care(mat, care),
                                   "size_and_fit": size_and_fit(*size)}}

# --- Hekate Bodysuit (konsistent neu) ---
M("HC-Hekate-Bodysuit", "Schwarz", ["Bodysuit", "Rundausschnitt", "Open Back"],
  {"de": {"h2": "Hekate, dein Statement-Piece mit Marble-Print",
          "p": ["Inspiriert von der griechischen Göttin der Magie zieht dich Hekate sofort in ihren Bann. Mesh-Tüll mit Marble-Print legt sich wie eine zweite Haut an und gibt dir genau den Halt, den du im Climb und am Boden brauchst.",
                "Die schwarzen Details an den Kanten und an den Booty-Straps setzen klare Akzente, der athletische Rückenschnitt lässt deine Schultern frei für jede Bewegung."],
          "li": ["Mesh-Tüll innen, Marble-Print außen", "Schwarze Details an Kanten und Booty-Straps", "Tiefer, runder Ausschnitt", "Hoher Beinausschnitt für eine lange Beinlinie", "Athletischer Open-Back-Schnitt, sitzt ohne zu verrutschen"]},
   "en": {"h2": "Hekate, your marble-print mesh statement",
          "p": ["Named after the Greek goddess of magic, Hekate pulls you in from the first glance. Mesh tulle with a marble print sits like a second skin and gives you the hold you want for every climb and floor sequence.",
                "Black trims along the edges and booty straps sharpen the look, while the athletic back keeps your shoulders free to move."],
          "li": ["Mesh tulle inside, marble print outside", "Black details on edges and booty straps", "Deep round neckline", "High leg rise for a longer leg line", "Athletic open-back cut that stays put"]},
   "fr": {"h2": "Hekate, ton statement en mesh marble-print",
          "p": ["Inspirée de la déesse grecque de la magie, Hekate te captive dès le premier regard. Le mesh tulle au marble-print épouse ta peau comme une seconde peau et te donne le maintien qu'il te faut pour chaque climb et chaque passage au sol.",
                "Les détails noirs sur les bords et les booty straps affirment la silhouette, et le dos athlétique laisse tes épaules libres de bouger."],
          "li": ["Mesh tulle à l'intérieur, marble-print à l'extérieur", "Détails noirs sur les bords et les booty straps", "Décolleté rond et profond", "Échancrure haute pour allonger la jambe", "Coupe dos ouvert athlétique qui ne bouge pas"]},
   "it": {"h2": "Hekate, il tuo statement in mesh marble-print",
          "p": ["Ispirato alla dea greca della magia, Hekate ti conquista al primo sguardo. Il mesh tulle con marble-print aderisce come una seconda pelle e ti dà il sostegno giusto per ogni climb e ogni sequenza a terra.",
                "I dettagli neri sui bordi e sui booty straps danno carattere, mentre la schiena atletica lascia le spalle libere di muoversi."],
          "li": ["Mesh tulle all'interno, marble-print all'esterno", "Dettagli neri su bordi e booty straps", "Scollo rotondo e profondo", "Gamba alta per allungare la linea", "Taglio schiena aperta atletico che resta al suo posto"]},
   "es": {"h2": "Hekate, tu statement en mesh marble-print",
          "p": ["Inspirado en la diosa griega de la magia, Hekate te atrapa desde la primera mirada. El mesh tulle con marble-print se ajusta como una segunda piel y te da el soporte que buscas en cada climb y cada secuencia de suelo.",
                "Los detalles negros en los bordes y en las booty straps marcan el look, y la espalda atlética deja tus hombros libres para moverte."],
          "li": ["Mesh tulle por dentro, marble-print por fuera", "Detalles negros en bordes y booty straps", "Escote redondo y profundo", "Pierna alta para estilizar la silueta", "Corte de espalda abierta atlético que no se mueve"]}},
  [("", [(92, "polyester"), (8, "elastane")])], 30,
  ("Hekate", "Elena", 1.72, "S", 82, 61, 92, "true"))

# --- Peonies Top nude ---
M("HC-Peonies-Top-Nude", "Beige", ["Rundausschnitt"],
  {"de": {"h2": "Peonies Top in zarten Nude-Tönen",
          "p": ["Der Peonies-Print in Hauttönen wirkt zart und bleibt dabei robust. Das leichte Neopren mit Vierwege-Stretch sitzt wie angegossen und macht jede Drehung und jeden Climb mit.",
                "Das Mesh-Detail an der Front setzt einen feinen Akzent, der runde Ausschnitt schmeichelt deiner Silhouette. Dein neues Lieblingsstück für jede Dance-Class."],
          "li": ["Leichtes Neopren mit Vierwege-Stretch", "Peonies-Print in Nude-Tönen", "Voll gefüttert", "Mesh-Detail an der Front", "Runder Ausschnitt"]},
   "en": {"h2": "Peonies top in soft nude tones",
          "p": ["The peonies print in skin tones feels delicate and stays durable. The light neoprene with four-way stretch fits like a glove and follows every spin and climb.",
                "A mesh detail at the front adds a fine accent, and the round neckline flatters your silhouette. Your new go-to for every dance class."],
          "li": ["Light neoprene with four-way stretch", "Peonies print in nude tones", "Fully lined", "Mesh detail at the front", "Round neckline"]},
   "fr": {"h2": "Peonies top dans des tons nude délicats",
          "p": ["L'imprimé peonies dans des tons chair reste délicat et résistant à la fois. Le néoprène léger à stretch quatre directions épouse ta silhouette et suit chaque rotation et chaque climb.",
                "Le détail en mesh sur le devant pose un accent subtil, et le décolleté rond met ta silhouette en valeur. Ta nouvelle pièce favorite pour chaque cours de danse."],
          "li": ["Néoprène léger à stretch quatre directions", "Imprimé peonies dans des tons nude", "Entièrement doublé", "Détail mesh sur le devant", "Décolleté rond"]},
   "it": {"h2": "Peonies top in delicate tonalità nude",
          "p": ["La stampa peonies in tonalità pelle resta delicata e allo stesso tempo resistente. Il neoprene leggero con stretch quattro direzioni calza alla perfezione e segue ogni giro e ogni climb.",
                "Il dettaglio in mesh sul davanti aggiunge un tocco fine, e lo scollo rotondo valorizza la tua silhouette. Il tuo nuovo pezzo preferito per ogni lezione di danza."],
          "li": ["Neoprene leggero con stretch quattro direzioni", "Stampa peonies in tonalità nude", "Completamente foderato", "Dettaglio mesh sul davanti", "Scollo rotondo"]},
   "es": {"h2": "Peonies top en suaves tonos nude",
          "p": ["El estampado peonies en tonos piel se siente delicado y a la vez resistente. El neopreno ligero con stretch en cuatro direcciones se ajusta como un guante y acompaña cada giro y cada climb.",
                "El detalle de mesh en el frente aporta un acento fino, y el escote redondo favorece tu silueta. Tu nueva pieza favorita para cada clase de baile."],
          "li": ["Neopreno ligero con stretch en cuatro direcciones", "Estampado peonies en tonos nude", "Totalmente forrado", "Detalle de mesh en el frente", "Escote redondo"]}},
  [("", [(70, "polyester"), (30, "elastane")])], 30,
  ("Peonies", "Yifan Li", 1.67, "S", 81, 67, 94, "true"))

# --- Peonies Bottom nude ---
M("HC-Peonies-Bottom-Nude", "Beige", ["High Waist", "High Leg"],
  {"de": {"h2": "Peonies Shorts in zarten Nude-Tönen",
          "p": ["Der Peonies-Print in Hauttönen wirkt zart und bleibt dabei robust. Das leichte Neopren mit Vierwege-Stretch sitzt wie angegossen und macht jede Bewegung mit.",
                "Der hohe Bund und der hohe Beinausschnitt verlängern optisch die Beine und geben dir Halt bei jedem Climb. Dein neues Lieblingsstück für jede Dance-Class."],
          "li": ["Leichtes Neopren mit Vierwege-Stretch", "Peonies-Print in Nude-Tönen", "Voll gefüttert", "Hoher Bund", "Hoher Beinausschnitt"]},
   "en": {"h2": "Peonies shorts in soft nude tones",
          "p": ["The peonies print in skin tones feels delicate and stays durable. The light neoprene with four-way stretch fits like a glove and follows every move.",
                "The high waist and high leg rise visually lengthen your legs and give you hold for every climb. Your new go-to for every dance class."],
          "li": ["Light neoprene with four-way stretch", "Peonies print in nude tones", "Fully lined", "High waist", "High leg rise"]},
   "fr": {"h2": "Peonies short dans des tons nude délicats",
          "p": ["L'imprimé peonies dans des tons chair reste délicat et résistant à la fois. Le néoprène léger à stretch quatre directions épouse ta silhouette et suit chaque mouvement.",
                "La taille haute et l'échancrure haute allongent visuellement les jambes et te donnent du maintien pour chaque climb. Ta nouvelle pièce favorite pour chaque cours de danse."],
          "li": ["Néoprène léger à stretch quatre directions", "Imprimé peonies dans des tons nude", "Entièrement doublé", "Taille haute", "Échancrure haute"]},
   "it": {"h2": "Peonies shorts in delicate tonalità nude",
          "p": ["La stampa peonies in tonalità pelle resta delicata e allo stesso tempo resistente. Il neoprene leggero con stretch quattro direzioni calza alla perfezione e segue ogni movimento.",
                "La vita alta e la gamba alta allungano otticamente le gambe e ti danno sostegno in ogni climb. Il tuo nuovo pezzo preferito per ogni lezione di danza."],
          "li": ["Neoprene leggero con stretch quattro direzioni", "Stampa peonies in tonalità nude", "Completamente foderato", "Vita alta", "Gamba alta"]},
   "es": {"h2": "Peonies shorts en suaves tonos nude",
          "p": ["El estampado peonies en tonos piel se siente delicado y a la vez resistente. El neopreno ligero con stretch en cuatro direcciones se ajusta como un guante y acompaña cada movimiento.",
                "El talle alto y la pierna alta alargan ópticamente las piernas y te dan soporte en cada climb. Tu nueva pieza favorita para cada clase de baile."],
          "li": ["Neopreno ligero con stretch en cuatro direcciones", "Estampado peonies en tonos nude", "Totalmente forrado", "Talle alto", "Pierna alta"]}},
  [("", [(70, "polyester"), (30, "elastane")])], 30,
  ("Peonies", "Yifan Li", 1.67, "S", 81, 67, 94, "true"))

# --- Dark Roast Top ---
M("HC-DarkRoast-Top", "Schwarz", ["Rundausschnitt", "Open Back"],
  {"de": {"h2": "Dark Roast Top, dein schwarzes Trainings-Piece",
          "p": ["Dein Liebling Black Coffee ist zurück, neu aufgelegt und auf den Punkt geröstet. Der gerippte Stoff folgt jeder Bewegung und gibt dir einen cleanen, satten Look fürs Training.",
                "Der runde Ausschnitt vorn und der tiefe Rückenausschnitt setzen klare Linien, die Fütterung in Weinrot bringt einen warmen Twist. Nichts sitzt richtiger als ein schwarzes Outfit, wenn du Vollgas gibst."],
          "li": ["Gerippter Stoff mit viel Stretch", "Tiefschwarze Optik", "Gefüttert in Weinrot", "Runder Ausschnitt", "Tiefer Rückenausschnitt"]},
   "en": {"h2": "Dark Roast top, your black training piece",
          "p": ["Your favourite Black Coffee is back, re-roasted to perfection. The ribbed fabric follows every move and gives you a clean, rich look for training.",
                "The round neckline at the front and the low back cut draw clean lines, and the wine-red lining adds a warm twist. Nothing feels more right than a black outfit when you go full power."],
          "li": ["Ribbed fabric with plenty of stretch", "Deep black look", "Lined in wine red", "Round neckline", "Low back cut"]},
   "fr": {"h2": "Dark Roast top, ta pièce noire d'entraînement",
          "p": ["Ton favori Black Coffee est de retour, torréfié à la perfection. Le tissu côtelé suit chaque mouvement et te donne un look net et profond pour l'entraînement.",
                "Le décolleté rond devant et le dos échancré dessinent des lignes nettes, et la doublure rouge bordeaux apporte une touche chaleureuse. Rien ne te va mieux qu'une tenue noire quand tu donnes tout."],
          "li": ["Tissu côtelé bien extensible", "Noir profond", "Doublure rouge bordeaux", "Décolleté rond", "Dos échancré"]},
   "it": {"h2": "Dark Roast top, il tuo pezzo nero da allenamento",
          "p": ["Il tuo preferito Black Coffee è tornato, tostato alla perfezione. Il tessuto a coste segue ogni movimento e ti dà un look pulito e intenso per l'allenamento.",
                "Lo scollo rotondo davanti e la schiena profonda disegnano linee pulite, e la fodera rosso vino aggiunge un tocco caldo. Niente ti sta meglio di un completo nero quando dai il massimo."],
          "li": ["Tessuto a coste molto elastico", "Nero profondo", "Foderato in rosso vino", "Scollo rotondo", "Schiena profonda"]},
   "es": {"h2": "Dark Roast top, tu pieza negra de entrenamiento",
          "p": ["Tu favorito Black Coffee está de vuelta, tostado a la perfección. El tejido de canalé sigue cada movimiento y te da un look limpio e intenso para entrenar.",
                "El escote redondo delante y la espalda baja trazan líneas limpias, y el forro rojo vino aporta un toque cálido. Nada te queda mejor que un conjunto negro cuando lo das todo."],
          "li": ["Tejido de canalé con mucha elasticidad", "Negro profundo", "Forrado en rojo vino", "Escote redondo", "Espalda baja"]}},
  [("", [(87, "polyamide"), (13, "elastane")])], 30,
  ("Dark Roast", "Konstantina", 1.78, "M", 90, 82, 97, "true"))

# --- Dark Roast Bottom ---
M("HC-DarkRoast-Bottom", "Schwarz", ["High Waist", "High Leg"],
  {"de": {"h2": "Dark Roast Shorts, dein schwarzes Trainings-Piece",
          "p": ["Dein Liebling Black Coffee ist zurück, neu aufgelegt und auf den Punkt geröstet. Der gerippte Stoff folgt jeder Bewegung und gibt dir einen cleanen, satten Look fürs Training.",
                "Der hohe Bund und der hohe Beinausschnitt verlängern optisch die Beine, die Fütterung in Weinrot bringt einen warmen Twist. Nichts sitzt richtiger als ein schwarzes Outfit, wenn du Vollgas gibst."],
          "li": ["Gerippter Stoff mit viel Stretch", "Tiefschwarze Optik", "Gefüttert in Weinrot", "Hoher Bund", "Hoher Beinausschnitt"]},
   "en": {"h2": "Dark Roast shorts, your black training piece",
          "p": ["Your favourite Black Coffee is back, re-roasted to perfection. The ribbed fabric follows every move and gives you a clean, rich look for training.",
                "The high waist and high leg rise visually lengthen your legs, and the wine-red lining adds a warm twist. Nothing feels more right than a black outfit when you go full power."],
          "li": ["Ribbed fabric with plenty of stretch", "Deep black look", "Lined in wine red", "High waist", "High leg rise"]},
   "fr": {"h2": "Dark Roast short, ta pièce noire d'entraînement",
          "p": ["Ton favori Black Coffee est de retour, torréfié à la perfection. Le tissu côtelé suit chaque mouvement et te donne un look net et profond pour l'entraînement.",
                "La taille haute et l'échancrure haute allongent visuellement les jambes, et la doublure rouge bordeaux apporte une touche chaleureuse. Rien ne te va mieux qu'une tenue noire quand tu donnes tout."],
          "li": ["Tissu côtelé bien extensible", "Noir profond", "Doublure rouge bordeaux", "Taille haute", "Échancrure haute"]},
   "it": {"h2": "Dark Roast shorts, il tuo pezzo nero da allenamento",
          "p": ["Il tuo preferito Black Coffee è tornato, tostato alla perfezione. Il tessuto a coste segue ogni movimento e ti dà un look pulito e intenso per l'allenamento.",
                "La vita alta e la gamba alta allungano otticamente le gambe, e la fodera rosso vino aggiunge un tocco caldo. Niente ti sta meglio di un completo nero quando dai il massimo."],
          "li": ["Tessuto a coste molto elastico", "Nero profondo", "Foderato in rosso vino", "Vita alta", "Gamba alta"]},
   "es": {"h2": "Dark Roast shorts, tu pieza negra de entrenamiento",
          "p": ["Tu favorito Black Coffee está de vuelta, tostado a la perfección. El tejido de canalé sigue cada movimiento y te da un look limpio e intenso para entrenar.",
                "El talle alto y la pierna alta alargan ópticamente las piernas, y el forro rojo vino aporta un toque cálido. Nada te queda mejor que un conjunto negro cuando lo das todo."],
          "li": ["Tejido de canalé con mucha elasticidad", "Negro profundo", "Forrado en rojo vino", "Talle alto", "Pierna alta"]}},
  [("", [(87, "polyamide"), (13, "elastane")])], 30,
  ("Dark Roast", "Konstantina", 1.78, "L", 90, 82, 97, "true"))

# --- Toffee Latte Top ---
M("HC-ToffeeLatte-Top", "Beige", ["Rundausschnitt", "Open Back"],
  {"de": {"h2": "Toffee Latte Top in cremigem Beige",
          "p": ["Cremig, süß und auf den Punkt verfeinert. Dein Toffee-Liebling kommt neu aufgelegt in besserer Qualität und Passform und legt sich wie eine zweite Haut um deine Kurven.",
                "Der gerippte Stoff in milchigem Beige bringt deine Linien zur Geltung, der runde Ausschnitt und der tiefe Rücken halten die Optik clean."],
          "li": ["Gerippter Stoff mit viel Stretch", "Milchiges Beige", "Gefüttert im selben Ton", "Runder Ausschnitt", "Tiefer Rückenausschnitt"]},
   "en": {"h2": "Toffee Latte top in creamy beige",
          "p": ["Creamy, sweet and refined to the point. Your Toffee favourite returns in better quality and fit, hugging your curves like a second skin.",
                "The ribbed fabric in milky beige shows off your lines, while the round neckline and low back keep the look clean."],
          "li": ["Ribbed fabric with plenty of stretch", "Milky beige", "Lined in the same tone", "Round neckline", "Low back cut"]},
   "fr": {"h2": "Toffee Latte top en beige crémeux",
          "p": ["Crémeux, doux et peaufiné juste comme il faut. Ton favori Toffee revient en meilleure qualité et coupe, et épouse tes courbes comme une seconde peau.",
                "Le tissu côtelé en beige laiteux met tes lignes en valeur, et le décolleté rond et le dos bas gardent le look net."],
          "li": ["Tissu côtelé bien extensible", "Beige laiteux", "Doublé dans le même ton", "Décolleté rond", "Dos échancré"]},
   "it": {"h2": "Toffee Latte top in beige cremoso",
          "p": ["Cremoso, dolce e rifinito al punto giusto. Il tuo preferito Toffee torna in qualità e vestibilità migliori, e avvolge le tue curve come una seconda pelle.",
                "Il tessuto a coste in beige latteo valorizza le tue linee, mentre lo scollo rotondo e la schiena bassa mantengono il look pulito."],
          "li": ["Tessuto a coste molto elastico", "Beige latteo", "Foderato nello stesso tono", "Scollo rotondo", "Schiena profonda"]},
   "es": {"h2": "Toffee Latte top en beige cremoso",
          "p": ["Cremoso, dulce y perfilado en su punto. Tu favorito Toffee vuelve en mejor calidad y ajuste, y abraza tus curvas como una segunda piel.",
                "El tejido de canalé en beige lechoso resalta tus líneas, mientras el escote redondo y la espalda baja mantienen el look limpio."],
          "li": ["Tejido de canalé con mucha elasticidad", "Beige lechoso", "Forrado en el mismo tono", "Escote redondo", "Espalda baja"]}},
  [("", [(87, "polyamide"), (13, "elastane")])], 30,
  ("Toffee Latte", "Yifan Li", 1.67, "S", 81, 67, 94, "true"))

# --- Toffee Latte Bottom ---
M("HC-ToffeeLatte-Bottom", "Beige", ["High Waist", "High Leg"],
  {"de": {"h2": "Toffee Latte Shorts in cremigem Beige",
          "p": ["Cremig, süß und auf den Punkt verfeinert. Dein Toffee-Liebling kommt neu aufgelegt in besserer Qualität und Passform und legt sich wie eine zweite Haut um deine Kurven.",
                "Der hohe Bund und der hohe Beinausschnitt verlängern optisch die Beine, der gerippte Stoff in milchigem Beige bringt deine Linien zur Geltung."],
          "li": ["Gerippter Stoff mit viel Stretch", "Milchiges Beige", "Gefüttert im selben Ton", "Hoher Bund", "Hoher Beinausschnitt"]},
   "en": {"h2": "Toffee Latte shorts in creamy beige",
          "p": ["Creamy, sweet and refined to the point. Your Toffee favourite returns in better quality and fit, hugging your curves like a second skin.",
                "The high waist and high leg rise visually lengthen your legs, and the ribbed fabric in milky beige shows off your lines."],
          "li": ["Ribbed fabric with plenty of stretch", "Milky beige", "Lined in the same tone", "High waist", "High leg rise"]},
   "fr": {"h2": "Toffee Latte short en beige crémeux",
          "p": ["Crémeux, doux et peaufiné juste comme il faut. Ton favori Toffee revient en meilleure qualité et coupe, et épouse tes courbes comme une seconde peau.",
                "La taille haute et l'échancrure haute allongent visuellement les jambes, et le tissu côtelé en beige laiteux met tes lignes en valeur."],
          "li": ["Tissu côtelé bien extensible", "Beige laiteux", "Doublé dans le même ton", "Taille haute", "Échancrure haute"]},
   "it": {"h2": "Toffee Latte shorts in beige cremoso",
          "p": ["Cremoso, dolce e rifinito al punto giusto. Il tuo preferito Toffee torna in qualità e vestibilità migliori, e avvolge le tue curve come una seconda pelle.",
                "La vita alta e la gamba alta allungano otticamente le gambe, e il tessuto a coste in beige latteo valorizza le tue linee."],
          "li": ["Tessuto a coste molto elastico", "Beige latteo", "Foderato nello stesso tono", "Vita alta", "Gamba alta"]},
   "es": {"h2": "Toffee Latte shorts en beige cremoso",
          "p": ["Cremoso, dulce y perfilado en su punto. Tu favorito Toffee vuelve en mejor calidad y ajuste, y abraza tus curvas como una segunda piel.",
                "El talle alto y la pierna alta alargan ópticamente las piernas, y el tejido de canalé en beige lechoso resalta tus líneas."],
          "li": ["Tejido de canalé con mucha elasticidad", "Beige lechoso", "Forrado en el mismo tono", "Talle alto", "Pierna alta"]}},
  [("", [(87, "polyamide"), (13, "elastane")])], 30,
  ("Toffee Latte", "Yifan Li", 1.67, "S", 81, 67, 94, "true"))

# --- Arachne Top black ---
M("HC-Arachne-Top-Black", "Schwarz", ["Langärmlig", "High Neck"],
  {"de": {"h2": "Arachne Top in tiefem Schwarz",
          "p": ["Arachne war die begabte Weberin, die die Götter herausforderte und zur ewigen Weberin wurde. Ihr Set trägt diese ungezähmte Energie, mit Mesh und Schnürungen in dunklen, geheimnisvollen Tönen.",
                "Der hohe Halsausschnitt und die langen Ärmel hüllen dich elegant ein, das satinierte Cut-out und die elastische Schnürung unter der Brust geben dem Look Struktur. Mystisch und selbstbewusst zugleich."],
          "li": ["Elastischer Mesh-Tüll, vollständig transparent", "Tiefschwarze Optik", "Satiniertes Cut-out-Detail", "Lange Ärmel", "Hoher Halsausschnitt"]},
   "en": {"h2": "Arachne top in deep black",
          "p": ["Arachne was the gifted weaver who challenged the gods and was turned into a weaver for eternity. Her set carries that untamed energy, with mesh and lacing in dark, mysterious tones.",
                "The high neckline and long sleeves wrap you elegantly, while the satin cut-out and the elastic lacing under the bust give the look structure. Mysterious and self-assured at once."],
          "li": ["Elastic mesh tulle, fully sheer", "Deep black look", "Satin cut-out detail", "Long sleeves", "High neckline"]},
   "fr": {"h2": "Arachne top en noir profond",
          "p": ["Arachne était la tisseuse douée qui défia les dieux et fut condamnée à tisser pour l'éternité. Son ensemble porte cette énergie indomptée, avec du mesh et des laçages dans des tons sombres et mystérieux.",
                "Le col haut et les manches longues t'enveloppent avec élégance, et le cut-out satiné et le laçage élastique sous la poitrine structurent le look. Mystérieuse et sûre de toi à la fois."],
          "li": ["Mesh tulle élastique, totalement transparent", "Noir profond", "Détail cut-out satiné", "Manches longues", "Col haut"]},
   "it": {"h2": "Arachne top in nero profondo",
          "p": ["Arachne era la tessitrice di talento che sfidò gli dèi e fu trasformata in tessitrice per l'eternità. Il suo set porta quell'energia indomita, con mesh e lacci in toni scuri e misteriosi.",
                "Il collo alto e le maniche lunghe ti avvolgono con eleganza, mentre il cut-out satinato e i lacci elastici sotto il seno danno struttura al look. Misteriosa e sicura di sé allo stesso tempo."],
          "li": ["Mesh tulle elastico, totalmente trasparente", "Nero profondo", "Dettaglio cut-out satinato", "Maniche lunghe", "Collo alto"]},
   "es": {"h2": "Arachne top en negro profundo",
          "p": ["Arachne fue la tejedora talentosa que desafió a los dioses y fue convertida en tejedora para la eternidad. Su conjunto lleva esa energía indomable, con mesh y cordones en tonos oscuros y misteriosos.",
                "El cuello alto y las mangas largas te envuelven con elegancia, y el cut-out satinado y el cordón elástico bajo el pecho dan estructura al look. Misteriosa y segura de ti a la vez."],
          "li": ["Mesh tulle elástico, totalmente transparente", "Negro profundo", "Detalle cut-out satinado", "Mangas largas", "Cuello alto"]}},
  [("", [(92, "polyamide"), (8, "elastane")])], 30,
  ("Arachne", "Elena", 1.72, "S", 82, 61, 92, "true"))

# --- Arachne Bottom black ---
M("HC-Arachne-Bottom-Black", "Schwarz", ["Riemchenshorts"],
  {"de": {"h2": "Arachne Shorts in tiefem Schwarz",
          "p": ["Arachne war die begabte Weberin, die die Götter herausforderte und zur ewigen Weberin wurde. Ihr Set trägt diese ungezähmte Energie, mit Mesh und Schnürungen in dunklen, geheimnisvollen Tönen.",
                "Die criss-cross geschnürten Elastikbänder und das satinierte V-Detail vorn und hinten zeichnen klare Linien, der vollständig transparente Tüll macht daraus ein mutiges Statement."],
          "li": ["Elastischer Mesh-Tüll, vollständig transparent", "Tiefschwarze Optik", "Criss-cross-Schnürung", "Satiniertes V-Detail vorn und hinten", "Schmale Passform"]},
   "en": {"h2": "Arachne shorts in deep black",
          "p": ["Arachne was the gifted weaver who challenged the gods and was turned into a weaver for eternity. Her set carries that untamed energy, with mesh and lacing in dark, mysterious tones.",
                "The criss-cross elastic laces and the satin V detail front and back draw clean lines, and the fully sheer tulle turns it into a bold statement."],
          "li": ["Elastic mesh tulle, fully sheer", "Deep black look", "Criss-cross lacing", "Satin V detail front and back", "Slim fit"]},
   "fr": {"h2": "Arachne short en noir profond",
          "p": ["Arachne était la tisseuse douée qui défia les dieux et fut condamnée à tisser pour l'éternité. Son ensemble porte cette énergie indomptée, avec du mesh et des laçages dans des tons sombres et mystérieux.",
                "Les lacets élastiques croisés et le détail en V satiné devant et derrière dessinent des lignes nettes, et le tulle totalement transparent en fait un statement audacieux."],
          "li": ["Mesh tulle élastique, totalement transparent", "Noir profond", "Laçage croisé", "Détail en V satiné devant et derrière", "Coupe ajustée"]},
   "it": {"h2": "Arachne shorts in nero profondo",
          "p": ["Arachne era la tessitrice di talento che sfidò gli dèi e fu trasformata in tessitrice per l'eternità. Il suo set porta quell'energia indomita, con mesh e lacci in toni scuri e misteriosi.",
                "I lacci elastici incrociati e il dettaglio a V satinato davanti e dietro disegnano linee pulite, e il tulle totalmente trasparente lo rende uno statement audace."],
          "li": ["Mesh tulle elastico, totalmente trasparente", "Nero profondo", "Allacciatura incrociata", "Dettaglio a V satinato davanti e dietro", "Vestibilità aderente"]},
   "es": {"h2": "Arachne shorts en negro profundo",
          "p": ["Arachne fue la tejedora talentosa que desafió a los dioses y fue convertida en tejedora para la eternidad. Su conjunto lleva esa energía indomable, con mesh y cordones en tonos oscuros y misteriosos.",
                "Los cordones elásticos cruzados y el detalle en V satinado delante y detrás trazan líneas limpias, y el tul totalmente transparente lo convierte en un statement atrevido."],
          "li": ["Mesh tulle elástico, totalmente transparente", "Negro profundo", "Cordones cruzados", "Detalle en V satinado delante y detrás", "Corte ajustado"]}},
  [("", [(92, "polyamide"), (8, "elastane")])], 30,
  ("Arachne", "Elena", 1.72, "S", 82, 61, 92, "true"))

# --- Arachne Top teal ---
M("HC-Arachne-Top-Teal", "Blau", ["Langärmlig", "High Neck"],
  {"de": {"h2": "Arachne Top in dunklem Türkis",
          "p": ["Arachne war die begabte Weberin, die die Götter herausforderte und zur ewigen Weberin wurde. Ihr Set trägt diese ungezähmte Energie, mit Mesh und Schnürungen in dunklen, geheimnisvollen Tönen.",
                "Der hohe Halsausschnitt und die langen Ärmel hüllen dich elegant ein, das satinierte Türkis-Cut-out und die elastische Schnürung unter der Brust geben dem Look Struktur. Mystisch und selbstbewusst zugleich."],
          "li": ["Elastischer Mesh-Tüll, vollständig transparent", "Dunkles Türkis", "Satiniertes Türkis-Cut-out", "Lange Ärmel", "Hoher Halsausschnitt"]},
   "en": {"h2": "Arachne top in dark teal",
          "p": ["Arachne was the gifted weaver who challenged the gods and was turned into a weaver for eternity. Her set carries that untamed energy, with mesh and lacing in dark, mysterious tones.",
                "The high neckline and long sleeves wrap you elegantly, while the satin teal cut-out and the elastic lacing under the bust give the look structure. Mysterious and self-assured at once."],
          "li": ["Elastic mesh tulle, fully sheer", "Dark teal", "Satin teal cut-out", "Long sleeves", "High neckline"]},
   "fr": {"h2": "Arachne top en turquoise foncé",
          "p": ["Arachne était la tisseuse douée qui défia les dieux et fut condamnée à tisser pour l'éternité. Son ensemble porte cette énergie indomptée, avec du mesh et des laçages dans des tons sombres et mystérieux.",
                "Le col haut et les manches longues t'enveloppent avec élégance, et le cut-out turquoise satiné et le laçage élastique sous la poitrine structurent le look. Mystérieuse et sûre de toi à la fois."],
          "li": ["Mesh tulle élastique, totalement transparent", "Turquoise foncé", "Cut-out turquoise satiné", "Manches longues", "Col haut"]},
   "it": {"h2": "Arachne top in turchese scuro",
          "p": ["Arachne era la tessitrice di talento che sfidò gli dèi e fu trasformata in tessitrice per l'eternità. Il suo set porta quell'energia indomita, con mesh e lacci in toni scuri e misteriosi.",
                "Il collo alto e le maniche lunghe ti avvolgono con eleganza, mentre il cut-out turchese satinato e i lacci elastici sotto il seno danno struttura al look. Misteriosa e sicura di sé allo stesso tempo."],
          "li": ["Mesh tulle elastico, totalmente trasparente", "Turchese scuro", "Cut-out turchese satinato", "Maniche lunghe", "Collo alto"]},
   "es": {"h2": "Arachne top en turquesa oscuro",
          "p": ["Arachne fue la tejedora talentosa que desafió a los dioses y fue convertida en tejedora para la eternidad. Su conjunto lleva esa energía indomable, con mesh y cordones en tonos oscuros y misteriosos.",
                "El cuello alto y las mangas largas te envuelven con elegancia, y el cut-out turquesa satinado y el cordón elástico bajo el pecho dan estructura al look. Misteriosa y segura de ti a la vez."],
          "li": ["Mesh tulle elástico, totalmente transparente", "Turquesa oscuro", "Cut-out turquesa satinado", "Mangas largas", "Cuello alto"]}},
  [("", [(92, "polyamide"), (8, "elastane")])], 30,
  ("Arachne", "Maro", 1.79, "M", 82, 66, 97, "true"))

# --- Arachne Bottom teal ---
M("HC-Arachne-Bottom-Teal", "Blau", ["Riemchenshorts"],
  {"de": {"h2": "Arachne Shorts in dunklem Türkis",
          "p": ["Arachne war die begabte Weberin, die die Götter herausforderte und zur ewigen Weberin wurde. Ihr Set trägt diese ungezähmte Energie, mit Mesh und Schnürungen in dunklen, geheimnisvollen Tönen.",
                "Die criss-cross geschnürten Elastikbänder und das satinierte Türkis-V-Detail vorn und hinten zeichnen klare Linien, der vollständig transparente Tüll macht daraus ein mutiges Statement."],
          "li": ["Elastischer Mesh-Tüll, vollständig transparent", "Dunkles Türkis", "Criss-cross-Schnürung", "Satiniertes Türkis-V-Detail", "Schmale Passform"]},
   "en": {"h2": "Arachne shorts in dark teal",
          "p": ["Arachne was the gifted weaver who challenged the gods and was turned into a weaver for eternity. Her set carries that untamed energy, with mesh and lacing in dark, mysterious tones.",
                "The criss-cross elastic laces and the satin teal V detail front and back draw clean lines, and the fully sheer tulle turns it into a bold statement."],
          "li": ["Elastic mesh tulle, fully sheer", "Dark teal", "Criss-cross lacing", "Satin teal V detail", "Slim fit"]},
   "fr": {"h2": "Arachne short en turquoise foncé",
          "p": ["Arachne était la tisseuse douée qui défia les dieux et fut condamnée à tisser pour l'éternité. Son ensemble porte cette énergie indomptée, avec du mesh et des laçages dans des tons sombres et mystérieux.",
                "Les lacets élastiques croisés et le détail en V turquoise satiné devant et derrière dessinent des lignes nettes, et le tulle totalement transparent en fait un statement audacieux."],
          "li": ["Mesh tulle élastique, totalement transparent", "Turquoise foncé", "Laçage croisé", "Détail en V turquoise satiné", "Coupe ajustée"]},
   "it": {"h2": "Arachne shorts in turchese scuro",
          "p": ["Arachne era la tessitrice di talento che sfidò gli dèi e fu trasformata in tessitrice per l'eternità. Il suo set porta quell'energia indomita, con mesh e lacci in toni scuri e misteriosi.",
                "I lacci elastici incrociati e il dettaglio a V turchese satinato davanti e dietro disegnano linee pulite, e il tulle totalmente trasparente lo rende uno statement audace."],
          "li": ["Mesh tulle elastico, totalmente trasparente", "Turchese scuro", "Allacciatura incrociata", "Dettaglio a V turchese satinato", "Vestibilità aderente"]},
   "es": {"h2": "Arachne shorts en turquesa oscuro",
          "p": ["Arachne fue la tejedora talentosa que desafió a los dioses y fue convertida en tejedora para la eternidad. Su conjunto lleva esa energía indomable, con mesh y cordones en tonos oscuros y misteriosos.",
                "Los cordones elásticos cruzados y el detalle en V turquesa satinado delante y detrás trazan líneas limpias, y el tul totalmente transparente lo convierte en un statement atrevido."],
          "li": ["Mesh tulle elástico, totalmente transparente", "Turquesa oscuro", "Cordones cruzados", "Detalle en V turquesa satinado", "Corte ajustado"]}},
  [("", [(92, "polyamide"), (8, "elastane")])], 30,
  ("Arachne", "Maro", 1.79, "M", 82, 66, 97, "true"))

# --- Echidna Top ---
M("HC-Echidna-Top", ["Rot", "Braun"], ["Triangle Ausschnitt"],
  {"de": {"h2": "Echidna Top in Terrakotta und Plum",
          "p": ["Weck dein wildes, kantiges Selbst. Das Echidna-Set kombiniert mutige Cutouts und Mesh-Details zu einem Look, der deine Stärke in jeder Performance in Szene setzt.",
                "Hochwertige, super elastische Texturen geben dir Halt, der tiefe V-Ausschnitt und die Plum-Fütterung setzen Akzente. Athletisch und sleek zugleich."],
          "li": ["Hochwertiger, elastischer Stoff", "Dunkle Terrakotta- und Plum-Töne", "Voll gefüttert in Plum", "Tiefer V-Ausschnitt", "Atmungsaktiv"]},
   "en": {"h2": "Echidna top in terracotta and plum",
          "p": ["Wake up your wild, edgy self. The Echidna set combines bold cutouts and mesh details for a look that puts your strength on show in every performance.",
                "High-quality, super stretchy textures give you hold, while the deep V neckline and the plum lining set the accents. Athletic and sleek at once."],
          "li": ["High-quality, stretchy fabric", "Dark terracotta and plum tones", "Fully lined in plum", "Deep V neckline", "Breathable"]},
   "fr": {"h2": "Echidna top en terracotta et prune",
          "p": ["Réveille ton moi sauvage et tranchant. L'ensemble Echidna combine des découpes audacieuses et des détails en mesh pour un look qui met ta force en avant à chaque performance.",
                "Des textures de haute qualité et très extensibles te donnent du maintien, et le décolleté en V profond et la doublure prune posent les accents. Athlétique et sleek à la fois."],
          "li": ["Tissu de haute qualité et extensible", "Tons terracotta et prune foncés", "Entièrement doublé en prune", "Décolleté en V profond", "Respirant"]},
   "it": {"h2": "Echidna top in terracotta e prugna",
          "p": ["Risveglia il tuo io selvaggio e spigoloso. Il set Echidna combina tagli audaci e dettagli in mesh per un look che mette in mostra la tua forza in ogni performance.",
                "Texture di alta qualità e super elastiche ti danno sostegno, mentre lo scollo a V profondo e la fodera prugna creano gli accenti. Atletico e sleek allo stesso tempo."],
          "li": ["Tessuto di alta qualità ed elastico", "Tonalità terracotta e prugna scure", "Completamente foderato in prugna", "Scollo a V profondo", "Traspirante"]},
   "es": {"h2": "Echidna top en terracota y ciruela",
          "p": ["Despierta tu lado salvaje y afilado. El conjunto Echidna combina cortes atrevidos y detalles de mesh para un look que muestra tu fuerza en cada performance.",
                "Texturas de alta calidad y muy elásticas te dan soporte, y el escote en V profundo y el forro ciruela ponen los acentos. Atlético y sleek a la vez."],
          "li": ["Tejido de alta calidad y elástico", "Tonos terracota y ciruela oscuros", "Totalmente forrado en ciruela", "Escote en V profundo", "Transpirable"]}},
  [("", [(80, "polyamide"), (20, "elastane")])], 40,
  ("Echidna", "Maro", 1.79, "M", 82, 66, 97, "true"))

# --- Echidna Bottom ---
M("HC-Echidna-Bottom", ["Rot", "Braun"], ["High Waist"],
  {"de": {"h2": "Echidna Shorts in Terrakotta und Plum",
          "p": ["Weck dein wildes, kantiges Selbst. Das Echidna-Set kombiniert mutige Cutouts und Mesh-Details zu einem Look, der deine Stärke in jeder Performance in Szene setzt.",
                "Der hohe Bund und die seitlichen Mesh-Cutouts formen die Silhouette, die super elastische Textur gibt dir Halt bei jeder Bewegung."],
          "li": ["Hochwertiger, elastischer Stoff", "Dunkle Terrakotta- und Plum-Töne", "Voll gefüttert in Plum-Mesh", "Hoher Bund", "Seitliche Mesh-Cutouts"]},
   "en": {"h2": "Echidna shorts in terracotta and plum",
          "p": ["Wake up your wild, edgy self. The Echidna set combines bold cutouts and mesh details for a look that puts your strength on show in every performance.",
                "The high waist and the side mesh cutouts shape your silhouette, while the super stretchy texture gives you hold in every move."],
          "li": ["High-quality, stretchy fabric", "Dark terracotta and plum tones", "Fully lined in plum mesh", "High waist", "Side mesh cutouts"]},
   "fr": {"h2": "Echidna short en terracotta et prune",
          "p": ["Réveille ton moi sauvage et tranchant. L'ensemble Echidna combine des découpes audacieuses et des détails en mesh pour un look qui met ta force en avant à chaque performance.",
                "La taille haute et les découpes en mesh sur les côtés dessinent la silhouette, et la texture très extensible te donne du maintien dans chaque mouvement."],
          "li": ["Tissu de haute qualité et extensible", "Tons terracotta et prune foncés", "Entièrement doublé en mesh prune", "Taille haute", "Découpes mesh sur les côtés"]},
   "it": {"h2": "Echidna shorts in terracotta e prugna",
          "p": ["Risveglia il tuo io selvaggio e spigoloso. Il set Echidna combina tagli audaci e dettagli in mesh per un look che mette in mostra la tua forza in ogni performance.",
                "La vita alta e i tagli in mesh sui lati modellano la silhouette, mentre la texture super elastica ti dà sostegno in ogni movimento."],
          "li": ["Tessuto di alta qualità ed elastico", "Tonalità terracotta e prugna scure", "Completamente foderato in mesh prugna", "Vita alta", "Tagli in mesh sui lati"]},
   "es": {"h2": "Echidna shorts en terracota y ciruela",
          "p": ["Despierta tu lado salvaje y afilado. El conjunto Echidna combina cortes atrevidos y detalles de mesh para un look que muestra tu fuerza en cada performance.",
                "El talle alto y los cortes de mesh en los laterales moldean la silueta, y la textura muy elástica te da soporte en cada movimiento."],
          "li": ["Tejido de alta calidad y elástico", "Tonos terracota y ciruela oscuros", "Totalmente forrado en mesh ciruela", "Talle alto", "Cortes de mesh laterales"]}},
  [("", [(80, "polyamide"), (20, "elastane")])], 40,
  ("Echidna", "Maro", 1.79, "M", 82, 66, 97, "true"))

# --- Lynx Top ---
M("HC-Lynx-Top", "Schwarz", ["Langärmlig"],
  {"de": {"h2": "Lynx Top mit Leopardenprint",
          "p": ["Zeig deine Raubkatzen-Energie. Das Lynx-Set kombiniert schwarzen Mesh-Tüll mit Leopardenprint-Details und markanten Cuts für einen Look mit Biss.",
                "Das bedruckte Scuba-Brustband mit schwarzer Fütterung gibt Struktur, die langen Ärmel machen daraus ein echtes Statement. Ein dekorativer Ring setzt das Highlight."],
          "li": ["Schwarzer Mesh-Tüll", "Leopardenprint-Details", "Bedrucktes Scuba-Brustband", "Lange Ärmel", "Dekorativer Ring vorn"]},
   "en": {"h2": "Lynx top with leopard print",
          "p": ["Show your feline energy. The Lynx set combines black mesh tulle with leopard print details and bold cuts for a look with bite.",
                "The printed scuba chest band with black lining adds structure, while the long sleeves turn it into a real statement. A decorative ring sets the highlight."],
          "li": ["Black mesh tulle", "Leopard print details", "Printed scuba chest band", "Long sleeves", "Decorative ring at the front"]},
   "fr": {"h2": "Lynx top à imprimé léopard",
          "p": ["Montre ton énergie féline. L'ensemble Lynx associe le tulle mesh noir à des détails imprimé léopard et des coupes marquées pour un look qui a du mordant.",
                "La bande poitrine en scuba imprimé avec doublure noire apporte de la structure, et les manches longues en font un vrai statement. Un anneau décoratif pose le point fort."],
          "li": ["Tulle mesh noir", "Détails imprimé léopard", "Bande poitrine scuba imprimée", "Manches longues", "Anneau décoratif sur le devant"]},
   "it": {"h2": "Lynx top con stampa leopardo",
          "p": ["Mostra la tua energia felina. Il set Lynx unisce il tulle mesh nero a dettagli stampa leopardo e tagli decisi per un look che ha mordente.",
                "La fascia pettorale in scuba stampato con fodera nera aggiunge struttura, e le maniche lunghe lo rendono un vero statement. Un anello decorativo crea il punto luce."],
          "li": ["Tulle mesh nero", "Dettagli stampa leopardo", "Fascia pettorale in scuba stampato", "Maniche lunghe", "Anello decorativo sul davanti"]},
   "es": {"h2": "Lynx top con estampado de leopardo",
          "p": ["Muestra tu energía felina. El conjunto Lynx combina tul mesh negro con detalles de estampado de leopardo y cortes marcados para un look con carácter.",
                "La banda de pecho de scuba estampado con forro negro aporta estructura, y las mangas largas lo convierten en un verdadero statement. Un anillo decorativo pone el acento."],
          "li": ["Tul mesh negro", "Detalles de estampado de leopardo", "Banda de pecho de scuba estampado", "Mangas largas", "Anillo decorativo en el frente"]}},
  [("printed", [(87, "polyester"), (13, "elastane")]), ("tulle", [(92, "polyamide"), (8, "elastane")])], 30,
  ("Lynx", "Aphroditi", 1.77, "M", 85, 65, 96, "true"))

# --- Lynx Bottom ---
M("HC-Lynx-Bottom", "Schwarz", ["Mid Waist"],
  {"de": {"h2": "Lynx Shorts mit Leopardenprint",
          "p": ["Zeig deine Raubkatzen-Energie. Das Lynx-Set kombiniert schwarzen Mesh-Tüll mit Leopardenprint-Details und markanten Cuts für einen Look mit Biss.",
                "Der Leoparden-bedruckte Scuba-Mittelteil und das Taillenband treffen auf schwarzen Mesh-Tüll an den Seiten, schwarze Fütterung in allen Printteilen sorgt für Halt."],
          "li": ["Schwarzer Mesh-Tüll an den Seiten", "Leopardenprint im Mittelteil", "Schwarze Fütterung", "Dekorativer Ring vorn", "Moderate Bedeckung"]},
   "en": {"h2": "Lynx shorts with leopard print",
          "p": ["Show your feline energy. The Lynx set combines black mesh tulle with leopard print details and bold cuts for a look with bite.",
                "The leopard-printed scuba middle part and the waist band meet black mesh tulle at the sides, and black lining in all printed parts keeps the hold."],
          "li": ["Black mesh tulle at the sides", "Leopard print in the middle part", "Black lining", "Decorative ring at the front", "Moderate coverage"]},
   "fr": {"h2": "Lynx short à imprimé léopard",
          "p": ["Montre ton énergie féline. L'ensemble Lynx associe le tulle mesh noir à des détails imprimé léopard et des coupes marquées pour un look qui a du mordant.",
                "La partie centrale en scuba imprimé léopard et la ceinture rencontrent le tulle mesh noir sur les côtés, et la doublure noire sur toutes les parties imprimées assure le maintien."],
          "li": ["Tulle mesh noir sur les côtés", "Imprimé léopard sur la partie centrale", "Doublure noire", "Anneau décoratif sur le devant", "Couverture modérée"]},
   "it": {"h2": "Lynx shorts con stampa leopardo",
          "p": ["Mostra la tua energia felina. Il set Lynx unisce il tulle mesh nero a dettagli stampa leopardo e tagli decisi per un look che ha mordente.",
                "La parte centrale in scuba stampato leopardo e la fascia in vita incontrano il tulle mesh nero sui lati, e la fodera nera in tutte le parti stampate mantiene il sostegno."],
          "li": ["Tulle mesh nero sui lati", "Stampa leopardo nella parte centrale", "Fodera nera", "Anello decorativo sul davanti", "Copertura moderata"]},
   "es": {"h2": "Lynx shorts con estampado de leopardo",
          "p": ["Muestra tu energía felina. El conjunto Lynx combina tul mesh negro con detalles de estampado de leopardo y cortes marcados para un look con carácter.",
                "La parte central de scuba estampado de leopardo y la banda de cintura se unen al tul mesh negro en los laterales, y el forro negro en todas las partes estampadas mantiene el soporte."],
          "li": ["Tul mesh negro en los laterales", "Estampado de leopardo en la parte central", "Forro negro", "Anillo decorativo en el frente", "Cobertura moderada"]}},
  [("printed", [(87, "polyester"), (13, "elastane")]), ("tulle", [(92, "polyamide"), (8, "elastane")])], 30,
  ("Lynx", "Aphroditi", 1.77, "M", 85, 65, 96, "true"))

# --- Savanna Top mauve ---
M("HC-Savanna-Top-Mauve", "Lila", ["Riemchentop"],
  {"de": {"h2": "Savanna Top im Mauve-Ton",
          "p": ["Earthy Vibes, die dein Herz erobern. Der neue Mauve-Ton bringt deinen Bestseller-Liebling Savanna in frischer, verbesserter Qualität. Ob im Studio oder am Strand, alle schauen hin.",
                "Die verstellbaren Front-Schnürungen und die Tie-around-Bänder passen sich deiner Form an, die Fütterung in Dunkelrot bringt Tiefe."],
          "li": ["Voll gefüttert in Dunkelrot", "Mauve-Ton", "Verstellbare Front-Schnürung", "Tie-around-Bänder", "Limitierte Farbe"]},
   "en": {"h2": "Savanna top in mauve",
          "p": ["Earthy vibes that win your heart. The new mauve shade brings your best-seller favourite Savanna in fresh, improved quality. Whether in the studio or at the beach, everyone is looking.",
                "The adjustable front laces and the tie-around straps adapt to your shape, and the dark red lining adds depth."],
          "li": ["Fully lined in dark red", "Mauve shade", "Adjustable front lacing", "Tie-around straps", "Limited colour"]},
   "fr": {"h2": "Savanna top en mauve",
          "p": ["Des vibes earthy qui conquièrent ton cœur. La nouvelle teinte mauve apporte ton best-seller favori Savanna dans une qualité fraîche et améliorée. Au studio ou à la plage, tous les regards se tournent.",
                "Les laçages réglables sur le devant et les liens à nouer s'adaptent à ta forme, et la doublure rouge foncé apporte de la profondeur."],
          "li": ["Entièrement doublé en rouge foncé", "Teinte mauve", "Laçage réglable sur le devant", "Liens à nouer", "Couleur limitée"]},
   "it": {"h2": "Savanna top in mauve",
          "p": ["Vibe earthy che conquistano il cuore. La nuova tonalità mauve porta il tuo best-seller preferito Savanna in qualità fresca e migliorata. In studio o in spiaggia, tutti ti guardano.",
                "I lacci frontali regolabili e i nastri da annodare si adattano alla tua forma, e la fodera rosso scuro aggiunge profondità."],
          "li": ["Completamente foderato in rosso scuro", "Tonalità mauve", "Allacciatura frontale regolabile", "Nastri da annodare", "Colore limitato"]},
   "es": {"h2": "Savanna top en mauve",
          "p": ["Vibes earthy que conquistan tu corazón. El nuevo tono mauve trae tu favorito best-seller Savanna en calidad fresca y mejorada. En el estudio o en la playa, todos miran.",
                "Los cordones frontales ajustables y las cintas para atar se adaptan a tu forma, y el forro rojo oscuro aporta profundidad."],
          "li": ["Totalmente forrado en rojo oscuro", "Tono mauve", "Cordón frontal ajustable", "Cintas para atar", "Color limitado"]}},
  [("", [(80, "polyamide"), (20, "elastane")])], 40,
  ("Savanna", "Vika", 1.75, "S", 84, 60, 90, "true"))

# --- Savanna Bottom mauve ---
M("HC-Savanna-Bottom-Mauve", "Lila", ["High Leg"],
  {"de": {"h2": "Savanna Shorts im Mauve-Ton",
          "p": ["Earthy Vibes, die dein Herz erobern. Der neue Mauve-Ton bringt deinen Bestseller-Liebling Savanna in frischer, verbesserter Qualität. Ob im Studio oder am Strand, alle schauen hin.",
                "Der hohe Beinausschnitt verlängert optisch die Beine, die Cut-out-Details an der Seite setzen Akzente. Perfekt abgestimmt auf das Savanna Mauve Top."],
          "li": ["Voll gefüttert in Dunkelrot", "Mauve-Ton", "Hoher Beinausschnitt", "Seitliche Cut-out-Details", "Limitierte Farbe"]},
   "en": {"h2": "Savanna shorts in mauve",
          "p": ["Earthy vibes that win your heart. The new mauve shade brings your best-seller favourite Savanna in fresh, improved quality. Whether in the studio or at the beach, everyone is looking.",
                "The high leg rise visually lengthens your legs, and the side cut-out details set the accents. A perfect match for the Savanna mauve top."],
          "li": ["Fully lined in dark red", "Mauve shade", "High leg rise", "Side cut-out details", "Limited colour"]},
   "fr": {"h2": "Savanna short en mauve",
          "p": ["Des vibes earthy qui conquièrent ton cœur. La nouvelle teinte mauve apporte ton best-seller favori Savanna dans une qualité fraîche et améliorée. Au studio ou à la plage, tous les regards se tournent.",
                "L'échancrure haute allonge visuellement les jambes, et les détails découpés sur les côtés posent les accents. Le match parfait avec le top Savanna mauve."],
          "li": ["Entièrement doublé en rouge foncé", "Teinte mauve", "Échancrure haute", "Détails découpés sur les côtés", "Couleur limitée"]},
   "it": {"h2": "Savanna shorts in mauve",
          "p": ["Vibe earthy che conquistano il cuore. La nuova tonalità mauve porta il tuo best-seller preferito Savanna in qualità fresca e migliorata. In studio o in spiaggia, tutti ti guardano.",
                "La gamba alta allunga otticamente le gambe, e i dettagli con taglio sui lati creano gli accenti. L'abbinamento perfetto con il top Savanna mauve."],
          "li": ["Completamente foderato in rosso scuro", "Tonalità mauve", "Gamba alta", "Dettagli con taglio sui lati", "Colore limitato"]},
   "es": {"h2": "Savanna shorts en mauve",
          "p": ["Vibes earthy que conquistan tu corazón. El nuevo tono mauve trae tu favorito best-seller Savanna en calidad fresca y mejorada. En el estudio o en la playa, todos miran.",
                "La pierna alta alarga ópticamente las piernas, y los detalles de corte en los laterales ponen los acentos. El match perfecto con el top Savanna mauve."],
          "li": ["Totalmente forrado en rojo oscuro", "Tono mauve", "Pierna alta", "Detalles de corte laterales", "Color limitado"]}},
  [("", [(80, "polyamide"), (20, "elastane")])], 40,
  ("Savanna", "Vika", 1.75, "S", 84, 60, 90, "true"))

# --- Savanna Top original ---
M("HC-Savanna-Top-Original", "Weiß", ["Open Back", "Samt"],
  {"de": {"h2": "Savanna Original Top mit Zebra-Print",
          "p": ["Ihr habt gerufen, wir haben geliefert. Die Original Savanna ist zurück und neu interpretiert. Zebra-Print trifft auf brandneue Samt-Optik. Die O.G. der Savanna-Designs bleibt.",
                "Der gescoopte Rücken und die langen Elastikbänder zum Binden geben dir Freiheit beim Styling, die strukturierte Samt-Optik macht den Look besonders."],
          "li": ["Strukturierter Zebra-Print", "Samt-Optik", "Gescoopter Rücken", "Lange Bänder zum Binden", "Minimaler Halt"]},
   "en": {"h2": "Savanna Original top with zebra print",
          "p": ["You called, we delivered. The original Savanna is back and re-imagined. Zebra print meets a brand-new velvet look. The O.G. of the Savanna designs is here to stay.",
                "The scooped back and the long elastic ties give you freedom to style, and the textured velvet look makes it special."],
          "li": ["Textured zebra print", "Velvet look", "Scooped back", "Long ties to wrap", "Minimum support"]},
   "fr": {"h2": "Savanna Original top à imprimé zèbre",
          "p": ["Vous avez demandé, on a livré. La Savanna originale est de retour et réinventée. L'imprimé zèbre rencontre un tout nouveau look velours. La O.G. des designs Savanna est là pour rester.",
                "Le dos échancré et les longs liens élastiques à nouer te donnent la liberté de styliser, et le look velours texturé le rend spécial."],
          "li": ["Imprimé zèbre texturé", "Look velours", "Dos échancré", "Longs liens à nouer", "Maintien minimal"]},
   "it": {"h2": "Savanna Original top con stampa zebra",
          "p": ["Avete chiamato, abbiamo risposto. La Savanna originale è tornata e reinterpretata. La stampa zebra incontra un nuovissimo look velluto. La O.G. dei design Savanna è qui per restare.",
                "La schiena scollata e i lunghi nastri elastici da annodare ti danno libertà di stile, e il look velluto testurizzato lo rende speciale."],
          "li": ["Stampa zebra testurizzata", "Look velluto", "Schiena scollata", "Lunghi nastri da annodare", "Sostegno minimo"]},
   "es": {"h2": "Savanna Original top con estampado de cebra",
          "p": ["Lo pedisteis, lo entregamos. La Savanna original está de vuelta y reinventada. El estampado de cebra se encuentra con un nuevo look de terciopelo. La O.G. de los diseños Savanna llegó para quedarse.",
                "La espalda escotada y las largas cintas elásticas para atar te dan libertad de estilo, y el look de terciopelo texturizado lo hace especial."],
          "li": ["Estampado de cebra texturizado", "Look de terciopelo", "Espalda escotada", "Cintas largas para atar", "Soporte mínimo"]}},
  [("", [(92, "polyester"), (8, "elastane")])], 30,
  ("Savanna", "Yifan Lee", 1.67, "S", 85, 63, 90, "bit_small"))

# --- Savanna Bottom original ---
M("HC-Savanna-Bottom-Original", "Weiß", ["High Waist", "High Leg", "Samt"],
  {"de": {"h2": "Savanna Original Shorts mit Zebra-Print",
          "p": ["Ihr habt gerufen, wir haben geliefert. Die Original Savanna ist zurück und neu interpretiert. Zebra-Print trifft auf brandneue Samt-Optik. Die O.G. der Savanna-Designs bleibt.",
                "Der hohe Bund und der hohe Beinausschnitt strecken die Silhouette, die asymmetrischen Cut-out-Details setzen Akzente. Die strukturierte Samt-Optik macht den Look besonders."],
          "li": ["Strukturierter Zebra-Print", "Samt-Optik", "Hoher Bund", "Hoher Beinausschnitt", "Asymmetrische Cut-out-Details"]},
   "en": {"h2": "Savanna Original shorts with zebra print",
          "p": ["You called, we delivered. The original Savanna is back and re-imagined. Zebra print meets a brand-new velvet look. The O.G. of the Savanna designs is here to stay.",
                "The high waist and high leg rise stretch your silhouette, and the asymmetric cut-out details set the accents. The textured velvet look makes it special."],
          "li": ["Textured zebra print", "Velvet look", "High waist", "High leg rise", "Asymmetric cut-out details"]},
   "fr": {"h2": "Savanna Original short à imprimé zèbre",
          "p": ["Vous avez demandé, on a livré. La Savanna originale est de retour et réinventée. L'imprimé zèbre rencontre un tout nouveau look velours. La O.G. des designs Savanna est là pour rester.",
                "La taille haute et l'échancrure haute étirent la silhouette, et les détails découpés asymétriques posent les accents. Le look velours texturé le rend spécial."],
          "li": ["Imprimé zèbre texturé", "Look velours", "Taille haute", "Échancrure haute", "Détails découpés asymétriques"]},
   "it": {"h2": "Savanna Original shorts con stampa zebra",
          "p": ["Avete chiamato, abbiamo risposto. La Savanna originale è tornata e reinterpretata. La stampa zebra incontra un nuovissimo look velluto. La O.G. dei design Savanna è qui per restare.",
                "La vita alta e la gamba alta allungano la silhouette, e i dettagli con taglio asimmetrico creano gli accenti. Il look velluto testurizzato lo rende speciale."],
          "li": ["Stampa zebra testurizzata", "Look velluto", "Vita alta", "Gamba alta", "Dettagli con taglio asimmetrico"]},
   "es": {"h2": "Savanna Original shorts con estampado de cebra",
          "p": ["Lo pedisteis, lo entregamos. La Savanna original está de vuelta y reinventada. El estampado de cebra se encuentra con un nuevo look de terciopelo. La O.G. de los diseños Savanna llegó para quedarse.",
                "El talle alto y la pierna alta estilizan la silueta, y los detalles de corte asimétrico ponen los acentos. El look de terciopelo texturizado lo hace especial."],
          "li": ["Estampado de cebra texturizado", "Look de terciopelo", "Talle alto", "Pierna alta", "Detalles de corte asimétrico"]}},
  [("", [(92, "polyester"), (8, "elastane")])], 30,
  ("Savanna", "Yifan Lee", 1.67, "S", 85, 63, 90, "small_up"))

# --- Savanna Top sky ---
M("HC-Savanna-Top-Sky", "Blau", ["Samt"],
  {"de": {"h2": "Savanna Top in Himmelblau aus Samt",
          "p": ["Die größte Liebe von allen. Dein Lieblings-Savanna-Design, jetzt in Samt, um deinen Tag zum Leuchten zu bringen.",
                "Die hochwertige Samt-Optik und die asymmetrischen Cut-out-Details machen den Look besonders, der weiche Griff schmeichelt der Haut."],
          "li": ["Hochwertige Samt-Optik", "Himmelblauer Ton", "Asymmetrische Cut-out-Details", "Weicher Griff", "Mittlerer Halt"]},
   "en": {"h2": "Savanna top in sky velvet",
          "p": ["The biggest love of them all. Your favourite Savanna design, now in velvet, to light up your day.",
                "The high-quality velvet look and the asymmetric cut-out details make it special, and the soft hand flatters your skin."],
          "li": ["High-quality velvet look", "Sky shade", "Asymmetric cut-out details", "Soft hand", "Medium support"]},
   "fr": {"h2": "Savanna top en velours bleu ciel",
          "p": ["Le plus grand amour de tous. Ton design Savanna favori, désormais en velours, pour illuminer ta journée.",
                "Le look velours de haute qualité et les détails découpés asymétriques le rendent spécial, et le toucher doux flatte ta peau."],
          "li": ["Look velours de haute qualité", "Teinte bleu ciel", "Détails découpés asymétriques", "Toucher doux", "Maintien moyen"]},
   "it": {"h2": "Savanna top in velluto azzurro cielo",
          "p": ["Il più grande amore di tutti. Il tuo design Savanna preferito, ora in velluto, per illuminare la tua giornata.",
                "Il look velluto di alta qualità e i dettagli con taglio asimmetrico lo rendono speciale, e il tatto morbido valorizza la pelle."],
          "li": ["Look velluto di alta qualità", "Tonalità azzurro cielo", "Dettagli con taglio asimmetrico", "Tatto morbido", "Sostegno medio"]},
   "es": {"h2": "Savanna top en terciopelo azul cielo",
          "p": ["El amor más grande de todos. Tu diseño Savanna favorito, ahora en terciopelo, para iluminar tu día.",
                "El look de terciopelo de alta calidad y los detalles de corte asimétrico lo hacen especial, y el tacto suave favorece tu piel."],
          "li": ["Look de terciopelo de alta calidad", "Tono azul cielo", "Detalles de corte asimétrico", "Tacto suave", "Soporte medio"]}},
  [("", [(90, "polyester"), (10, "elastane")])], 30,
  ("Savanna", "Elena", 1.72, "M", None, None, None, "true"))

# --- Savanna Bottom sky ---
M("HC-Savanna-Bottom-Sky", "Blau", ["High Waist", "High Leg", "Samt"],
  {"de": {"h2": "Savanna Shorts in Himmelblau aus Samt",
          "p": ["Die größte Liebe von allen. Dein Lieblings-Savanna-Design, jetzt in Samt, um deinen Tag zum Leuchten zu bringen.",
                "Der hohe Bund und der hohe Beinausschnitt strecken die Silhouette, die hochwertige Samt-Optik macht den Look besonders."],
          "li": ["Hochwertige Samt-Optik", "Himmelblauer Ton", "Hoher Bund", "Hoher Beinausschnitt", "Weicher Griff"]},
   "en": {"h2": "Savanna shorts in sky velvet",
          "p": ["The biggest love of them all. Your favourite Savanna design, now in velvet, to light up your day.",
                "The high waist and high leg rise stretch your silhouette, and the high-quality velvet look makes it special."],
          "li": ["High-quality velvet look", "Sky shade", "High waist", "High leg rise", "Soft hand"]},
   "fr": {"h2": "Savanna short en velours bleu ciel",
          "p": ["Le plus grand amour de tous. Ton design Savanna favori, désormais en velours, pour illuminer ta journée.",
                "La taille haute et l'échancrure haute étirent la silhouette, et le look velours de haute qualité le rend spécial."],
          "li": ["Look velours de haute qualité", "Teinte bleu ciel", "Taille haute", "Échancrure haute", "Toucher doux"]},
   "it": {"h2": "Savanna shorts in velluto azzurro cielo",
          "p": ["Il più grande amore di tutti. Il tuo design Savanna preferito, ora in velluto, per illuminare la tua giornata.",
                "La vita alta e la gamba alta allungano la silhouette, e il look velluto di alta qualità lo rende speciale."],
          "li": ["Look velluto di alta qualità", "Tonalità azzurro cielo", "Vita alta", "Gamba alta", "Tatto morbido"]},
   "es": {"h2": "Savanna shorts en terciopelo azul cielo",
          "p": ["El amor más grande de todos. Tu diseño Savanna favorito, ahora en terciopelo, para iluminar tu día.",
                "El talle alto y la pierna alta estilizan la silueta, y el look de terciopelo de alta calidad lo hace especial."],
          "li": ["Look de terciopelo de alta calidad", "Tono azul cielo", "Talle alto", "Pierna alta", "Tacto suave"]}},
  [("", [(90, "polyester"), (10, "elastane")])], 30,
  ("Savanna", "Elena", 1.72, "M", None, None, None, "small_up"))

if __name__ == "__main__":
    from . import content as content_mod
    content = dict(MODELS)
    path = config.PIPELINE_DIR / "content" / "hotcakes_content.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(content, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"geschrieben: {len(content)} Modelle -> {path}")
