"""Export a sheet source (*.src.svg) for GitHub: convert every <text> to outlined paths, since GitHub loads no web fonts, and bake the
wobble filter (filter="url(#wob)") into the linework itself, since browsers render feDisplacementMap unevenly and break thin lines apart.

Usage: python text2path.py FONT_DIR SRC.svg [...]   writes each SRC's sibling without the .src infix.
Needs fontTools and these TTFs in FONT_DIR, from github.com/google/fonts: PatrickHandSC-Regular.ttf, Caveat-Bold.ttf (Caveat[wght] instanced at 700),
BarlowCondensed-{Regular,SemiBold,Bold}.ttf, IBMPlexMono-Regular.ttf. Glyphs a face lacks (✓, →) fall back to IBM Plex Mono.
"""
import math
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

from fontTools.pens.basePen import BasePen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.svgLib.path import parse_path
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

SVG = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG)
INHERITED = ("font-family", "font-weight", "font-size", "letter-spacing", "fill", "text-anchor", "fill-opacity", "opacity")
KEEP = ("fill", "fill-opacity", "opacity", "stroke", "stroke-width", "stroke-linejoin", "paint-order", "transform")


class Face:
    def __init__(self, path):
        self.font = TTFont(path)
        self.cmap = self.font.getBestCmap()
        self.glyphs = self.font.getGlyphSet()
        self.upm = self.font["head"].unitsPerEm
        self.hmtx = self.font["hmtx"]


def load_faces(font_dir):
    d = Path(font_dir)
    return {
        ("barlow", 400): Face(d / "BarlowCondensed-Regular.ttf"),
        ("barlow", 600): Face(d / "BarlowCondensed-SemiBold.ttf"),
        ("barlow", 700): Face(d / "BarlowCondensed-Bold.ttf"),
        ("patrick", 400): Face(d / "PatrickHandSC-Regular.ttf"),
        ("caveat", 700): Face(d / "Caveat-Bold.ttf"),
        ("mono", 400): Face(d / "IBMPlexMono-Regular.ttf"),
    }


def pick(faces, family, weight):
    f = family.lower()
    key = "barlow" if "barlow" in f else "patrick" if "patrick" in f else "caveat" if "caveat" in f else "mono" if "mono" in f else None
    if key is None:
        raise ValueError(f"no face for font-family {family!r}")
    weights = sorted(w for (k, w) in faces if k == key)
    return faces[(key, min(weights, key=lambda w: abs(w - weight)))]


def outline(text, face, fallback, size, spacing):
    """Return (path data, advance width) for a string set at the origin, baseline y=0."""
    pieces, x = [], 0.0
    for ch in text:
        f = face if ord(ch) in face.cmap else fallback
        name = f.cmap.get(ord(ch))
        if name is None:
            raise ValueError(f"no glyph for {ch!r}")
        s = size / f.upm
        pen = SVGPathPen(f.glyphs, ntos=lambda v: f"{v:.1f}".rstrip("0").rstrip("."))
        f.glyphs[name].draw(TransformPen(pen, (s, 0, 0, -s, x, 0)))
        pieces.append(pen.getCommands())
        x += f.hmtx[name][0] * s + spacing
    return " ".join(p for p in pieces if p), x - spacing


def num(v, default=0.0):
    return float(re.sub(r"px$", "", v)) if v not in (None, "") else default


def convert(root, faces):
    fallback = faces[("mono", 400)]

    def walk(el, inherited):
        ctx = dict(inherited)
        for a in INHERITED:
            if el.get(a) is not None:
                ctx[a] = el.get(a)
        for i, child in enumerate(list(el)):
            if child.tag != f"{{{SVG}}}text":
                walk(child, ctx)
                continue
            c = dict(ctx)
            for a in INHERITED:
                if child.get(a) is not None:
                    c[a] = child.get(a)
            face = pick(faces, c.get("font-family", ""), int(num(c.get("font-weight"), 400)))
            size = num(c.get("font-size"), 16)
            d, width = outline(child.text or "", face, fallback, size, num(c.get("letter-spacing")))
            x, y = num(child.get("x")), num(child.get("y"))
            x -= {"middle": width / 2, "end": width}.get(c.get("text-anchor", "start"), 0)
            p = ET.Element(f"{{{SVG}}}path", {"d": d})
            for a in KEEP:
                v = child.get(a) if a not in ("fill", "fill-opacity", "opacity") else c.get(a)
                if v is not None:
                    p.set(a, v)
            p.set("transform", f"{child.get('transform', '')} translate({x:.2f} {y:.2f})".strip())
            el.remove(child)
            el.insert(i, p)
        for a in ("font-family", "font-weight", "font-size", "letter-spacing", "text-anchor"):
            el.attrib.pop(a, None)

    walk(root, {})


WOBBLE_STEP = 3.0  # px between resampled points
WOBBLE_WAVES = [  # (amplitude, wavelength, direction, phase): a smooth field ~±1.5px with 40-90px wavelengths, like feTurbulence at .018
    (0.8, 90, 0.4, 1.3), (0.5, 57, 2.1, 4.0), (0.3, 41, 3.6, 2.2),
]


def wobble(x, y, axis):
    total = 0.0
    for amp, wave, ang, ph in WOBBLE_WAVES:
        a = ang + axis * 1.7
        total += amp * math.sin((x * math.cos(a) + y * math.sin(a)) * 2 * math.pi / wave + ph + axis * 2.9)
    return total


class Flattener(BasePen):
    """Collect contours as dense polylines."""

    def __init__(self):
        super().__init__(None)
        self.contours, self.pts, self.closed = [], [], False

    def _moveTo(self, pt):
        self._flush()
        self.pts = [pt]

    def _lineTo(self, pt):
        a = self.pts[-1]
        n = max(1, math.ceil(math.dist(a, pt) / WOBBLE_STEP))
        self.pts += [(a[0] + (pt[0] - a[0]) * i / n, a[1] + (pt[1] - a[1]) * i / n) for i in range(1, n + 1)]

    def _curveToOne(self, p1, p2, p3):
        p0 = self.pts[-1]
        n = max(2, math.ceil((math.dist(p0, p1) + math.dist(p1, p2) + math.dist(p2, p3)) / WOBBLE_STEP))
        for i in range(1, n + 1):
            t = i / n
            u = 1 - t
            self.pts.append(tuple(u**3 * a + 3 * u * u * t * b + 3 * u * t * t * c + t**3 * d for a, b, c, d in zip(p0, p1, p2, p3)))

    def _closePath(self):
        if self.pts and self.pts[0] != self.pts[-1]:
            self._lineTo(self.pts[0])
        self.closed = True
        self._flush()

    def _endPath(self):
        self._flush()

    def _flush(self):
        if len(self.pts) > 1:
            self.contours.append((self.pts, self.closed))
        self.pts, self.closed = [], False


def shape_path(el):
    """Return path data for a basic shape or path element, or None."""
    tag = el.tag.split("}")[1]
    g = lambda a: num(el.get(a))
    if tag == "path":
        return el.get("d")
    if tag == "line":
        return f"M{g('x1')} {g('y1')} L{g('x2')} {g('y2')}"
    if tag == "rect":
        x, y, w, h = g("x"), g("y"), g("width"), g("height")
        return f"M{x} {y} H{x + w} V{y + h} H{x} Z"
    if tag in ("circle", "ellipse"):
        cx, cy = g("cx"), g("cy")
        rx, ry = (g("r"), g("r")) if tag == "circle" else (g("rx"), g("ry"))
        n = max(24, math.ceil(2 * math.pi * max(rx, ry) / WOBBLE_STEP))
        pts = [(cx + rx * math.cos(2 * math.pi * i / n), cy + ry * math.sin(2 * math.pi * i / n)) for i in range(n)]
        return "M" + " L".join(f"{x} {y}" for x, y in pts) + " Z"
    return None


GEOMETRY = ("d", "x", "y", "width", "height", "x1", "y1", "x2", "y2", "cx", "cy", "r", "rx", "ry")


def bake_wobble(root):
    def bake(el):
        for i, child in enumerate(list(el)):
            d = shape_path(child)
            if d is None:
                bake(child)
                continue
            pen = Flattener()
            parse_path(d, pen)
            pen._flush()
            out = []
            for pts, closed in pen.contours:
                moved = [(x + wobble(x, y, 0), y + wobble(x, y, 1)) for x, y in pts]
                out.append("M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in moved) + (" Z" if closed else ""))
            p = ET.Element(f"{{{SVG}}}path", {k: v for k, v in child.attrib.items() if k not in GEOMETRY})
            p.set("d", " ".join(out))
            el.remove(child)
            el.insert(i, p)

    for el in root.iter():
        if el.get("filter") == "url(#wob)":
            del el.attrib["filter"]
            bake(el)


def main():
    faces = load_faces(sys.argv[1])
    for src in map(Path, sys.argv[2:]):
        tree = ET.parse(src)
        convert(tree.getroot(), faces)
        bake_wobble(tree.getroot())
        out = src.with_name(src.name.replace(".src.svg", ".svg"))
        tree.write(out, encoding="unicode")
        print(f"{src} -> {out}")


if __name__ == "__main__":
    main()
