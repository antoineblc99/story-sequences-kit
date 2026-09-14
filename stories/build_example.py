#!/usr/bin/env python3
"""Gabarit d'une séquence de 4 slides. Copie-le en build.py et remplace les textes.

Il rend tel quel avec le fond de démo et une carte de démo, pour que tu voies la
composition avant d'avoir tes propres photos. Ensuite : une photo de
pictures/moi/ en fond, ta capture de pictures/screens/ en carte.
"""
import datetime as dt
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from deck import MARKER, Slide  # noqa: E402
from PIL import Image, ImageDraw  # noqa: E402

PHOTOS = os.path.join(ROOT, "pictures", "moi")
SCREENS = os.path.join(ROOT, "pictures", "screens")
OUT = os.path.join(ROOT, "out", dt.date.today().isoformat() + "-exemple")
os.makedirs(OUT, exist_ok=True)

FOND = os.path.join(PHOTOS, "_demo-fond.jpg")            # remplace par ta photo
CAPTURE = os.path.join(SCREENS, "_demo-capture.png")    # remplace par ta capture
if not os.path.exists(CAPTURE):
    # une carte de démo, pour voir où va la preuve ; ta vraie capture la remplace
    from deck import body, display
    im = Image.new("RGB", (1600, 400), (246, 245, 242)); d = ImageDraw.Draw(im)
    d.text((70, 130), "ta capture ici", font=body(56, weight=600), fill=(40, 40, 40))
    d.text((70, 215), "un dashboard, un compteur, un message reçu", font=body(34), fill=(120, 116, 110))
    d.text((1300, 130), "194", font=display(96), fill=(20, 20, 20))
    im.save(CAPTURE)

# --- 01 · qui parle : le point de départ ------------------------------------
s = Slide()
s.shot(FOND, dim=0.35)
s.block(["je faisais mes séquences", "stories à la main.",
         "le texte, les captures,", "le montage, la mise en ligne.",
         "j'ai arrêté."], x=72, y=330, size=50)
s.save(os.path.join(OUT, "slide-1.jpg"))

# --- 02 · ce qui s'est passé --------------------------------------------------
s = Slide()
s.shot(FOND, dim=0.4)
s.block(["aujourd'hui l'ia les fait", "aussi bien.", "souvent mieux.",
         "à une condition…"], x=72, y=330, size=52)
s.save(os.path.join(OUT, "slide-2.jpg"))

# --- 03 · la preuve : la capture en carte, le chiffre cerclé ------------------
s = Slide()
s.shot(FOND, dim=0.3)
cx, cy, cw, ch = s.inset(CAPTURE, x=20, y=900, w=1040, radius=16)
s.block(["le bon modèle,", "avec les bonnes références,",
         "et la possibilité de publier", "en automatique."], x=72, y=440, size=50)
s.block(["des centaines de leads", "sont arrivés comme ça."], x=72, y=1200, size=48)
# le cercle vise le chiffre dans la carte : ajuste cx/cy en regardant le rendu
s.circle(cx + cw * 0.84, cy + ch * 0.45, 48, 40)
s.arrow((640, 1200), (cx + cw * 0.80, cy + ch + 4), bend=160)
s.save(os.path.join(OUT, "slide-3.jpg"))

# --- 04 · le mot-clé ----------------------------------------------------------
s = Slide()
s.shot(FOND, dim=0.35)
y = s.block(["réponds MOT."], x=72, y=1380, size=54, fill=MARKER)
s.block(["je t'envoie le système complet."], x=72, y=y, size=54)
s.save(os.path.join(OUT, "slide-4.jpg"))

print("→", OUT)
