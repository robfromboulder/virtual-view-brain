"""Convert every <text> in a sheet source (*.src.svg) to outlined paths, so GitHub renders the lettering without web fonts.

Usage: python text2path.py FONT_DIR SRC.svg [...]   writes each SRC's sibling without the .src infix.
Needs fontTools and these TTFs in FONT_DIR, from github.com/google/fonts: PatrickHandSC-Regular.ttf, Caveat-Bold.ttf (Caveat[wght] instanced at 700),
BarlowCondensed-{Regular,SemiBold,Bold}.ttf, IBMPlexMono-Regular.ttf. Glyphs a face lacks (✓, →) fall back to IBM Plex Mono.
"""
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

from fontTools.pens.svgPathPen import SVGPathPen
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


def main():
    faces = load_faces(sys.argv[1])
    for src in map(Path, sys.argv[2:]):
        tree = ET.parse(src)
        convert(tree.getroot(), faces)
        out = src.with_name(src.name.replace(".src.svg", ".svg"))
        tree.write(out, encoding="unicode")
        print(f"{src} -> {out}")


if __name__ == "__main__":
    main()
