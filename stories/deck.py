#!/usr/bin/env python3
"""Renderer de séquences stories, 1080x1920, structure Nik Setting.

    from deck import Slide, MARKER
    s = Slide()
    s.shot("pictures/moi/ma-photo.jpg", dim=0.4)          # photo plein cadre, assombrie
    s.inset("pictures/screens/ma-capture.png", 60, 900, 960)  # la preuve, posée en carte
    s.block(["une ligne", "une autre"], x=72, y=330, size=50)  # blocs texte natifs IG
    s.circle(cx, cy, rx, ry) ; s.arrow((x1, y1), (x2, y2))     # annotation rouge
    s.block(["réponds MOT."], x=72, y=1380, size=54, fill=MARKER)
    s.save("out/slide-1.jpg")

Le mode crème (dark=False : grille, titres display, cards blanches) sert aux
carrousels, pas aux stories.
"""
import math
import os

from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1080, 1920
# Bandes recouvertes par l'UI Instagram (avatar/nom en haut, champ réponse en bas).
SAFE_TOP, SAFE_BOTTOM = 250, 290

CREAM = (251, 249, 244)
INK = (21, 18, 14)
INK_SOFT = (92, 85, 74)
CORAL = (204, 120, 92)
CORAL_INK = (168, 91, 63)
# Annotations tracées main : le coral de marque passe mal sur une capture claire.
# On garde la famille, saturée, pour que le trait reste lisible sur du blanc.
MARKER = (222, 74, 40)
LINE = (233, 228, 217)
WHITE = (255, 255, 255)

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "fonts")
DISPLAY = os.path.join(FONTS, "BricolageGrotesque.ttf")
BODY = os.path.join(FONTS, "HankenGrotesk.ttf")
SERIF = os.path.join(FONTS, "InstrumentSerif-Italic.ttf")
# Polices système optionnelles : si elles manquent (Windows, Linux), Hanken prend le relais.
MONO = os.path.expanduser("~/Library/Fonts/JetBrainsMonoNL-Medium.ttf")
IG_FONT = "/System/Library/Fonts/HelveticaNeue.ttc"  # index 1 = Bold
LOGOS = os.path.join(HERE, "logos")


def display(size, weight=800, width=100, opsz=96):
    """Bricolage Grotesque. Axes dans l'ordre du fichier : opsz, wght, wdth."""
    f = ImageFont.truetype(DISPLAY, size)
    f.set_variation_by_axes([opsz, weight, width])
    return f


def body(size, weight=430):
    f = ImageFont.truetype(BODY, size)
    f.set_variation_by_axes([weight])
    return f


def mono(size):
    if os.path.exists(MONO):
        return ImageFont.truetype(MONO, size)
    return body(size, weight=500)


def serif(size):
    return ImageFont.truetype(SERIF, size)


def insta(size):
    """La police des blocs de texte natifs Instagram : grotesque bold, neutre.

    Helvetica Neue Bold est le plus proche d'Instagram Sans parmi les polices
    système. Bricolage est trop typée pour ce rôle, elle se voit.
    """
    if os.path.exists(IG_FONT):
        return ImageFont.truetype(IG_FONT, size, index=1)
    return body(size, weight=700)


def _wrap(draw, text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for wd in words:
        t = (cur + " " + wd).strip()
        if draw.textlength(t, font=font) <= maxw:
            cur = t
        else:
            lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


def _tracked(draw, xy, text, font, fill, track):
    """Texte lettre par lettre avec letterspacing : les labels mono du carrousel."""
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill)
        x += draw.textlength(ch, font=font) + track
    return x


def tracked_width(draw, text, font, track):
    return sum(draw.textlength(c, font=font) + track for c in text) - track


class Slide:
    MARGIN = 78

    def __init__(self, index=None, total=None, eyebrow="", grid=True, dark=True,
                 chrome=False):
        """dark=True : fond noir, mode screenshot annoté (structure Nik Setting).

        chrome=False retire le bandeau signature (wordmark + pagination) : une story
        native n'a pas d'en-tête de marque, elle a juste du texte posé sur l'écran.
        """
        self.dark = dark
        self.img = Image.new("RGB", (W, H), (10, 10, 10) if dark else CREAM)
        self.chrome_d = ImageDraw.Draw(self.img)
        if grid and not dark:
            self._grid()
        if chrome:
            self._chrome(index, total, eyebrow)
        # Le contenu vit sur son propre calque : save() le recentre.
        self.layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        self.d = ImageDraw.Draw(self.layer)
        self.y = 0

    # --- fond et chrome ---------------------------------------------------
    def _grid(self, step=44):
        for x in range(0, W, step):
            self.chrome_d.line([(x, 0), (x, H)], fill=LINE, width=1)
        for y in range(0, H, step):
            self.chrome_d.line([(0, y), (W, y)], fill=LINE, width=1)

    def _asterisk(self, d, cx, cy, r, width=7, color=CORAL, branches=8):
        for i in range(branches):
            a = math.pi * i / branches
            d.line([(cx - r * math.cos(a), cy - r * math.sin(a)),
                    (cx + r * math.cos(a), cy + r * math.sin(a))], fill=color, width=width)

    def _chrome(self, index, total, eyebrow):
        """Header : ✳ + wordmark à gauche, pill de pagination à droite."""
        d, y = self.chrome_d, 128
        ink = CREAM if self.dark else INK
        soft = (150, 143, 132) if self.dark else INK_SOFT
        self._asterisk(d, self.MARGIN + 20, y, 22, width=6)
        f = display(46, weight=800)
        d.text((self.MARGIN + 58, y - 31), "Antoine", font=f, fill=ink)
        fm = mono(26)
        x = self.MARGIN + 58 + d.textlength("Antoine", font=f) + 22
        d.text((x, y - 15), "×", font=fm, fill=soft)
        _tracked(d, (x + 30, y - 15), eyebrow.lower(), fm, soft, 1.2)

        if index and total:
            label = f"{index:02d} / {total:02d}"
            fp = mono(28)
            pw, ph = tracked_width(d, label, fp, 2) + 56, 56
            px = W - self.MARGIN - pw
            d.rounded_rectangle([px, y - ph // 2, px + pw, y + ph // 2],
                                radius=ph // 2, fill=CORAL)
            _tracked(d, (px + 28, y - 18), label, fp, CREAM, 2)

    def footer(self, text):
        """Filet coral + légende mono uppercase, ancrés en bas de zone sûre."""
        d, y = self.chrome_d, H - SAFE_BOTTOM + 30
        d.line([(self.MARGIN, y), (W - self.MARGIN, y)], fill=CORAL, width=3)
        f = mono(25)
        tw = tracked_width(d, text, f, 3)
        _tracked(d, ((W - tw) / 2, y + 30), text, f, INK_SOFT, 3)

    # --- blocs ------------------------------------------------------------
    def eyebrow(self, text, gap=30):
        """Label mono uppercase précédé du filet coral vertical."""
        self.d.line([(self.MARGIN, self.y + 2), (self.MARGIN, self.y + 34)],
                    fill=CORAL, width=5)
        _tracked(self.d, (self.MARGIN + 22, self.y), text.upper(), mono(26), INK_SOFT, 2.5)
        self.y += 38 + gap
        return self.y

    def title(self, segments, size=100, align="center", gap=46, leading=0.92):
        """segments = [(texte, couleur), ...] — une ligne par segment."""
        f = display(size, weight=800)
        for text, color in segments:
            tw = self.d.textlength(text, font=f)
            x = (W - tw) / 2 if align == "center" else self.MARGIN
            self.d.text((x, self.y), text, font=f, fill=color)
            self.y += round(size * leading)
        self.y += gap
        return self.y

    def paragraph(self, text, size=40, color=INK_SOFT, gap=44, align="left", maxw=None):
        f = body(size)
        maxw = maxw or (W - 2 * self.MARGIN)
        for ln in _wrap(self.d, text, f, maxw):
            tw = self.d.textlength(ln, font=f)
            x = (W - tw) / 2 if align == "center" else self.MARGIN
            self.d.text((x, self.y), ln, font=f, fill=color)
            self.y += round(size * 1.42)
        self.y += gap
        return self.y

    def signature(self, text, size=54, gap=0):
        f = serif(size)
        tw = self.d.textlength(text, font=f)
        self.d.text(((W - tw) / 2, self.y), text, font=f, fill=INK)
        self.y += round(size * 1.3) + gap
        return self.y

    def space(self, px):
        self.y += px
        return self.y

    # --- objets -----------------------------------------------------------
    def card(self, x, y, w, h, radius=26, fill=WHITE, shadow=True):
        if shadow:
            sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            ImageDraw.Draw(sh).rounded_rectangle([x + 4, y + 12, x + w + 4, y + h + 12],
                                                 radius=radius, fill=(21, 18, 14, 38))
            self.layer.alpha_composite(sh.filter(ImageFilter.GaussianBlur(12)))
            self.d = ImageDraw.Draw(self.layer)
        self.d.rounded_rectangle([x, y, x + w, y + h], radius=radius,
                                 fill=fill, outline=LINE, width=2)
        return x, y, w, h

    def photo(self, path, w=None, ratio=None, gap=44, caption=None):
        """Photo ou screenshot dans une card blanche, centrée, façon polaroid."""
        w = w or (W - 2 * self.MARGIN)
        x = round((W - w) / 2)
        img = Image.open(path).convert("RGB")
        inner = w - 32
        if ratio:
            k = max(inner / img.width, (inner * ratio) / img.height)
            img = img.resize((round(img.width * k), round(img.height * k)))
            th = round(inner * ratio)
            left, top = (img.width - inner) // 2, (img.height - th) // 2
            img = img.crop((left, top, left + inner, top + th))
        else:
            img = img.resize((inner, round(img.height * inner / img.width)))
        h = img.height + 32
        self.card(x, self.y, w, h)
        mask = Image.new("L", img.size, 0)
        ImageDraw.Draw(mask).rounded_rectangle([0, 0, *img.size], radius=14, fill=255)
        self.layer.paste(img.convert("RGBA"), (x + 16, self.y + 16), mask)
        self.d = ImageDraw.Draw(self.layer)
        self.y += h + (14 if caption else gap)
        if caption:
            f = mono(24)
            tw = tracked_width(self.d, caption, f, 2)
            _tracked(self.d, ((W - tw) / 2, self.y), caption.upper(), f, INK_SOFT, 2)
            self.y += 30 + gap
        return self.y

    def terminal(self, lines, gap=44, size=30, pad=52):
        """Card blanche avec des commandes réelles ; la ligne `>` passe en coral."""
        f = mono(size)
        w = W - 2 * self.MARGIN
        h = len(lines) * round(size * 1.72) + 2 * pad
        self.card(self.MARGIN, self.y, w, h)
        for i, ln in enumerate(lines):
            self.d.text((self.MARGIN + 44, self.y + pad + i * round(size * 1.72)),
                        ln, font=f, fill=CORAL_INK if ln.startswith(">") else INK)
        self.y += h + gap
        return self.y

    def chip(self, cx, cy, label, w=200, h=88):
        """Card blanche avec un nom de plateforme en mono, comme les tuiles d'icônes."""
        x, y = round(cx - w / 2), round(cy - h / 2)
        self.card(x, y, w, h, radius=22)
        f = mono(24)
        tw = tracked_width(self.d, label, f, 2)
        _tracked(self.d, (cx - tw / 2, cy - 16), label, f, INK, 2)
        return x, y, w, h

    def logo_chip(self, cx, cy, slug, label=None, size=112, glyph=72):
        """Logo de plateforme dans une card carrée + label mono dessous."""
        path = os.path.join(LOGOS, f"{slug}.png")
        x, y = round(cx - size / 2), round(cy - size / 2)
        self.card(x, y, size, size, radius=26)
        img = Image.open(path).convert("RGBA")
        img = img.crop(img.getbbox())
        k = glyph / max(img.width, img.height)
        img = img.resize((max(1, round(img.width * k)), max(1, round(img.height * k))))
        self.layer.alpha_composite(img, (round(cx - img.width / 2), round(cy - img.height / 2)))
        self.d = ImageDraw.Draw(self.layer)
        if label:
            f = mono(22)
            tw = tracked_width(self.d, label, f, 2)
            _tracked(self.d, (cx - tw / 2, y + size + 16), label.upper(), f, INK_SOFT, 2)
        return x, y, size, size

    def dotted(self, p1, p2, bend=0, color=CORAL, dot=5, step=17, arrow=True):
        """Connecteur pointillé courbé + tête de flèche, signature du carrousel."""
        (x1, y1), (x2, y2) = p1, p2
        mx, my = (x1 + x2) / 2 + bend, (y1 + y2) / 2 - abs(bend) * 0.12
        n = max(14, int(math.hypot(x2 - x1, y2 - y1) / step))
        pts = []
        for i in range(n + 1):
            s = i / n
            pts.append(((1 - s) ** 2 * x1 + 2 * (1 - s) * s * mx + s ** 2 * x2,
                        (1 - s) ** 2 * y1 + 2 * (1 - s) * s * my + s ** 2 * y2))
        for px, py in (pts[:-2] if arrow else pts):
            self.d.ellipse([px - dot / 2, py - dot / 2, px + dot / 2, py + dot / 2], fill=color)
        if arrow:
            (ax, ay), (bx, by) = pts[-1], pts[-4]
            ang = math.atan2(ay - by, ax - bx)
            for da in (0.42, -0.42):
                self.d.line([ax, ay, ax - 22 * math.cos(ang + da),
                             ay - 22 * math.sin(ang + da)], fill=color, width=5)

    def statboxes(self, items, h=210, gap_x=30, gap=48):
        """Rangée de compteurs : gros chiffre display + label mono."""
        w = (W - 2 * self.MARGIN - (len(items) - 1) * gap_x) / len(items)
        for i, (value, label) in enumerate(items):
            x = self.MARGIN + i * (w + gap_x)
            self.card(x, self.y, w, h, radius=22, shadow=False)
            fv = display(74, weight=800)
            tw = self.d.textlength(value, font=fv)
            self.d.text((x + (w - tw) / 2, self.y + h * 0.16), value, font=fv, fill=INK)
            fl = mono(23)
            lw = tracked_width(self.d, label, fl, 2.5)
            _tracked(self.d, (x + (w - lw) / 2, self.y + h * 0.64), label, fl, INK_SOFT, 2.5)
        self.y += h + gap
        return self.y

    def bigword(self, text, size=200, pad=28, gap=46):
        """Le mot-clé en pavé coral plein, comme le AUTO de la dernière slide."""
        f = display(size, weight=800)
        # bbox de l'encre, pas l'avance : sinon la dernière lettre touche le bord du pavé.
        box = self.d.textbbox((0, 0), text, font=f)
        iw, ih = box[2] - box[0], box[3] - box[1]
        x = (W - iw) / 2
        self.d.rounded_rectangle([x - pad, self.y, x + iw + pad, self.y + ih + 2 * pad],
                                 radius=18, fill=CORAL)
        self.d.text((x - box[0], self.y + pad - box[1]), text, font=f, fill=CREAM)
        self.y += ih + 2 * pad + gap
        return self.y

    def hub(self, platforms, spread=352, row=176, gap=52, size=112):
        """Astérisque central relié en pointillés aux logos des plateformes.

        platforms = [(slug, label), ...] — slug = fichier dans assets-stories/logos.
        """
        half = (len(platforms) + 1) // 2
        left, right = platforms[:half], platforms[half:]
        height = (max(len(left), len(right)) - 1) * row + size + 44
        cy = self.y + height / 2
        cx = W / 2
        for col, side in ((left, -1), (right, 1)):
            top = cy - (len(col) - 1) * row / 2
            for i, (slug, lab) in enumerate(col):
                y = top + i * row
                self.dotted((cx + side * 60, cy), (cx + side * (spread - size / 2 - 26), y),
                            bend=side * 46)
                self.logo_chip(cx + side * spread, y, slug, lab, size=size)
        self._asterisk(self.d, cx, cy, 52, width=9)
        self.y += height + gap
        return self.y

    # --- mode "screenshot annoté" (structure Nik Setting) ------------------
    def shot(self, path, focus=None, zoom=1.0, dim=0.0, top=None, height=None, radius=0):
        """Capture d'écran posée sur le fond.

        Sans `height` : plein cadre 9:16. Avec `height` : bande de cette hauteur
        posée à `top`, le reste du fond reste visible (le noir de Nik Setting
        autour de la capture). focus = (fx, fy) en fractions 0..1, le point de
        l'image à garder au centre. zoom > 1 rentre dedans pour qu'un chiffre
        reste lisible sur un écran de téléphone.
        """
        bw, bh = W, height or H
        img = Image.open(path).convert("RGB")
        k = max(bw / img.width, bh / img.height) * zoom
        img = img.resize((round(img.width * k), round(img.height * k)))
        fx, fy = focus or (0.5, 0.5)
        left = min(max(round(img.width * fx - bw / 2), 0), max(0, img.width - bw))
        up = min(max(round(img.height * fy - bh / 2), 0), max(0, img.height - bh))
        crop = img.crop((left, up, left + bw, up + bh))
        y0 = (H - bh) // 2 if top is None else top
        if radius:
            mask = Image.new("L", crop.size, 0)
            ImageDraw.Draw(mask).rounded_rectangle([0, 0, *crop.size], radius=radius, fill=255)
            self.img.paste(crop, (0, y0), mask)
        else:
            self.img.paste(crop, (0, y0))
        if dim:
            veil = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            ImageDraw.Draw(veil).rectangle([0, y0, W, y0 + bh], fill=(0, 0, 0, round(255 * dim)))
            self.img = Image.alpha_composite(self.img.convert("RGBA"), veil).convert("RGB")
        self.chrome_d = ImageDraw.Draw(self.img)
        return y0, bh

    def inset(self, path, x, y, w, radius=22, shadow=True):
        """Capture posée en carte sur la photo de fond, façon Nik Setting.

        Le décor est une photo plein cadre (`shot()` sans height, avec dim) ; la
        preuve est une capture réduite à `w` px de large, coins arrondis, ombre
        douce, posée à (x, y). Retourne (x, y, w, h) pour placer l'annotation.
        """
        img = Image.open(path).convert("RGB")
        h = round(img.height * w / img.width)
        img = img.resize((w, h), Image.LANCZOS)
        mask = Image.new("L", (w, h), 0)
        ImageDraw.Draw(mask).rounded_rectangle([0, 0, w - 1, h - 1], radius=radius, fill=255)
        if shadow:
            sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            ImageDraw.Draw(sh).rounded_rectangle([x + 6, y + 14, x + w + 6, y + h + 14],
                                                 radius=radius, fill=(0, 0, 0, 140))
            self.img = Image.alpha_composite(
                self.img.convert("RGBA"), sh.filter(ImageFilter.GaussianBlur(22))).convert("RGB")
        self.img.paste(img, (x, y), mask)
        self.chrome_d = ImageDraw.Draw(self.img)
        return x, y, w, h

    def block(self, lines, x=64, y=None, size=44, fill=(0, 0, 0), color=WHITE, gap=8):
        """Blocs de texte noirs natifs IG, une ligne par rectangle, ragged right.

        Dessinés sur le chrome (pas sur le calque recentré) : en mode screenshot
        on place le texte à la main, autour de ce qu'on montre.
        """
        d = self.chrome_d
        f = insta(size)
        y = SAFE_TOP if y is None else y
        pad_x, pad_y = 18, 12
        for ln in lines:
            box = d.textbbox((0, 0), ln, font=f)
            tw, th = box[2] - box[0], box[3] - box[1]
            d.rounded_rectangle([x - pad_x, y, x + tw + pad_x, y + th + 2 * pad_y],
                                radius=12, fill=fill)
            d.text((x - box[0], y + pad_y - box[1]), ln, font=f, fill=color)
            y += th + 2 * pad_y + gap
        return y

    def circle(self, cx, cy, rx, ry, color=MARKER, width=7):
        """Cercle tracé main : deux ellipses légèrement décalées."""
        for dx, dy, dr in [(0, 0, 0), (6, 4, 5)]:
            self.chrome_d.ellipse([cx - rx + dx - dr, cy - ry + dy,
                                   cx + rx + dx, cy + ry + dy + dr],
                                  outline=color, width=width)

    def arrow(self, p1, p2, bend=90, color=MARKER, width=8):
        """Flèche courbe tracée main, du texte vers l'élément qu'il désigne."""
        d = self.chrome_d
        (x1, y1), (x2, y2) = p1, p2
        mx, my = (x1 + x2) / 2 + bend, (y1 + y2) / 2
        pts = []
        for i in range(29):
            s = i / 28
            pts.append(((1 - s) ** 2 * x1 + 2 * (1 - s) * s * mx + s ** 2 * x2,
                        (1 - s) ** 2 * y1 + 2 * (1 - s) * s * my + s ** 2 * y2))
        d.line(pts, fill=color, width=width, joint="curve")
        ang = math.atan2(pts[-1][1] - pts[-4][1], pts[-1][0] - pts[-4][0])
        for da in (0.45, -0.45):
            d.line([x2, y2, x2 - 38 * math.cos(ang + da), y2 - 38 * math.sin(ang + da)],
                   fill=color, width=width)

    def underline(self, x1, x2, y, color=MARKER, width=8, tilt=6):
        self.chrome_d.line([(x1, y), (x2, y + tilt)], fill=color, width=width)

    # --- sortie -----------------------------------------------------------
    def save(self, path, quality=94):
        """Centre le calque de contenu dans la zone sûre puis aplatit."""
        box = self.layer.getbbox()
        if box:
            band = H - SAFE_TOP - SAFE_BOTTOM
            dy = round(SAFE_TOP + (band - (box[3] - box[1])) / 2 - box[1])
            shifted = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            shifted.paste(self.layer, (0, dy))
            self.layer = shifted
        self.img = Image.alpha_composite(self.img.convert("RGBA"), self.layer).convert("RGB")
        self.img.save(path, quality=quality)
        print(path, "ok")
