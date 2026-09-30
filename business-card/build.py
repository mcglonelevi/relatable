#!/usr/bin/env python3
"""Builds the Chaotick business card SVGs (front + back).

Card: US standard 3.5 x 2 in, plus 0.125 in bleed on every side (3.75 x 2.25 in).
Units: 300 per inch. Trim line sits 37.5 units in; keep text 75 units in (safe area).
All text is converted to outlines from Rubik so the printer needs no fonts.

Edit CONTACT / QR_URL below and run:  python3 build.py
Needs: pip3 install fonttools segno
"""
import re
from pathlib import Path

import segno
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

CONTACT = {
    "name": "Levi McGlone",
    "title": "Founder & Designer",
    "phone": "614-929-1853",
    "website": "chaotick.gg",
    "email": "levi@chaotick.gg",
}
QR_URL = "https://chaotick.gg"
TAGLINE = "Instantly familiar. Endlessly fun."

HERE = Path(__file__).parent
KIT = HERE.parent / "Chaotick-Brand-Kit"

CREAM, INK = "#F6F1E7", "#1F1B2E"
SURFACE_RAISED, LINE = "#FFFCF6", "#DDD3C2"   # light theme
INK_MUTED_LIGHT = "#5E5870"                   # ink-muted on cream
INK_MUTED_DARK = "#BEB6CC"                    # ink-muted on ink (dark theme)
DIVIDER = "#3A3452"                           # line on ink (dark theme)
SURFACE_RAISED_DARK = "#2A2540"               # front background (dark theme raised surface)
TOMATO_TEXT_LIGHT = "#B83A17"                 # tomato-text on cream
TOMATO_TEXT_DARK = "#F07A55"                  # tomato-text on ink
MUSTARD = "#F2B134"

W, H = 1125, 675          # full size incl. bleed
BLEED = 37.5
SAFE = 75 + 18            # a little extra breathing room inside the safe area

_fonts = {}


def font(weight):
    if weight not in _fonts:
        _fonts[weight] = TTFont(KIT / "fonts" / f"Rubik-{weight}.ttf")
    return _fonts[weight]


def text_path(s, x, y, size, weight, fill, tracking=0.0, anchor="start"):
    """Outline `s` as a single <path>. `tracking` is in em (e.g. 0.12)."""
    f = font(weight)
    gs, cmap = f.getGlyphSet(), f.getBestCmap()
    upm = f["head"].unitsPerEm
    scale = size / upm
    names = [cmap[ord(c)] for c in s]
    advances = [gs[n].width + tracking * upm for n in names]
    width = (sum(advances) - tracking * upm) * scale
    if anchor == "middle":
        x -= width / 2
    elif anchor == "end":
        x -= width
    pen = SVGPathPen(gs)
    cursor = 0.0
    for n, adv in zip(names, advances):
        gs[n].draw(TransformPen(pen, (scale, 0, 0, -scale, x + cursor * scale, y)))
        cursor += adv
    return f'<path fill="{fill}" d="{pen.getCommands()}"/>', width


def logo_inner(name, prefix):
    """Inner markup + viewBox of a brand-kit logo, with ids namespaced."""
    src = (KIT / "logos" / "svg" / f"{name}.svg").read_text()
    vb = [float(v) for v in re.search(r'viewBox="([^"]+)"', src).group(1).split()]
    body = re.search(r"<svg[^>]*>(.*)</svg>", src, re.S).group(1)
    body = re.sub(r"<title>.*?</title>", "", body)
    body = re.sub(r'id="([^"]+)"', lambda m: f'id="{prefix}-{m.group(1)}"', body)
    body = re.sub(r"url\(#([^)]+)\)", lambda m: f"url(#{prefix}-{m.group(1)})", body)
    return body.strip(), vb


def place(name, prefix, x, y, width):
    """Draw a brand-kit logo with its viewBox's top-left corner at (x, y), scaled to `width`."""
    body, (vx, vy, vw, vh) = logo_inner(name, prefix)
    s = width / vw
    return f'<g transform="translate({x - vx * s:.2f} {y - vy * s:.2f}) scale({s:.5f})">{body}</g>', vh * s


def svg(title, content):
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" width="3.75in" height="2.25in" viewBox="0 0 {W} {H}">\n'
        f"<title>{title}</title>\n"
        "<!-- 3.5 x 2 in business card with 0.125 in bleed on all sides. Trim 37.5 units in from each edge. -->\n"
        f"{content}\n</svg>\n"
    )


def qr_tile(url, right, bottom, size):
    """Raised rounded tile of `size` units whose bottom-right corner is at (right, bottom)."""
    qr = segno.make(url, error="m")
    rows = [list(r) for r in qr.matrix]
    n = len(rows)
    quiet = 3  # light modules around the code
    m = size / (n + 2 * quiet)
    x0, y0 = right - size, bottom - size
    d = []
    for y, row in enumerate(rows):
        x = 0
        while x < n:
            if row[x]:
                start = x
                while x < n and row[x]:
                    x += 1
                d.append(f"M{x0 + (quiet + start) * m:.2f} {y0 + (quiet + y) * m:.2f}"
                         f"h{(x - start) * m:.2f}v{m:.2f}h{-(x - start) * m:.2f}z")
            else:
                x += 1
    return (f'<rect x="{x0:.2f}" y="{y0:.2f}" width="{size}" height="{size}" rx="{size * 0.12:.1f}" fill="{SURFACE_RAISED}" stroke="{LINE}" stroke-width="3"/>\n'
            f'<path fill="{INK}" shape-rendering="crispEdges" d="{"".join(d)}"/>')


def front():
    # Dark scheme, two columns: logo + tagline on the left, a divider, then name and contact details.
    parts = [f'<rect width="{W}" height="{H}" fill="{SURFACE_RAISED_DARK}"/>']
    mid_y = H / 2

    # Left column: the logo, with the tagline underneath on two lines.
    # The logo's viewBox is its artwork bounds, so centring the viewBox centres the artwork.
    col_l, col_r = SAFE, 480
    col_cx = (col_l + col_r) / 2
    mark_w = 360
    mark_h = mark_w * 120.4 / 555.7
    group_h = mark_h + 44 + 17 + 34   # logo, gap, two tagline lines
    top = mid_y - group_h / 2
    mark, _ = place("chaotick-logo-on-dark", "fw", col_cx - mark_w / 2, top, mark_w)
    parts.append(mark)
    for i, line in enumerate(("INSTANTLY FAMILIAR.", "ENDLESSLY FUN.")):
        y = top + mark_h + 44 + 17 + i * 34
        parts.append(text_path(line, col_cx, y, 23, 600, MUSTARD, tracking=0.14, anchor="middle")[0])

    # Divider.
    div_x = 530
    parts.append(f'<rect x="{div_x - 1.5}" y="{mid_y - 150:.1f}" width="3" height="300" rx="1.5" fill="{DIVIDER}"/>')

    # Right column: name, title, then labelled contact lines, centred vertically.
    left = div_x + 52
    y0 = mid_y - 81
    parts.append(text_path(CONTACT["name"], left, y0, 52, 700, CREAM, tracking=-0.01)[0])
    parts.append(text_path(CONTACT["title"], left, y0 + 48, 32, 500, TOMATO_TEXT_DARK)[0])

    # "Phone:" / "Email:" / "Website:" labels in muted ink, values lined up in a column after them.
    rows = [
        ("Phone:", CONTACT["phone"], y0 + 112),
        ("Email:", CONTACT["email"], y0 + 156),
        ("Website:", CONTACT["website"], y0 + 200),
    ]
    labels = [text_path(lbl, left, y, 34, 400, INK_MUTED_DARK) for lbl, _, y in rows]
    value_x = left + max(w for _, w in labels) + 16
    for (lbl_path, _), (_, value, y) in zip(labels, rows):
        parts += [lbl_path, text_path(value, value_x, y, 34, 500, CREAM)[0]]

    return "\n".join(parts)


def back():
    # Light scheme: QR code centred on cream, with a short label and the URL underneath.
    parts = [f'<rect width="{W}" height="{H}" fill="{CREAM}"/>']
    size = 300
    top = 128
    parts.append(qr_tile(QR_URL, W / 2 + size / 2, top + size, size))
    label, _ = text_path("SCAN TO MEET THE GAMES", W / 2, top + size + 70, 25, 600, TOMATO_TEXT_LIGHT, tracking=0.12, anchor="middle")
    url, _ = text_path(QR_URL, W / 2, top + size + 118, 30, 400, INK_MUTED_LIGHT, anchor="middle")
    parts += [label, url]
    return "\n".join(parts)


# ---- Print sheet: US Letter, 10 cards per side (2 x 5), for printing at home and cutting by hand ----
# Cards touch edge to edge, so every cut is shared by two cards and nothing is wasted between them.
# Only the outside of the grid gets bleed; crop crosshairs sit in the page margins, lined up with each cut.

SHEET_W, SHEET_H = 2550, 3300      # 8.5 x 11 in at 300 units/in
TRIM_W, TRIM_H = W - 2 * BLEED, H - 2 * BLEED
COLS, ROWS = 2, 5
GRID_X = (SHEET_W - COLS * TRIM_W) / 2     # 0.75 in side margins
GRID_Y = (SHEET_H - ROWS * TRIM_H) / 2     # 0.5 in top and bottom margins


def card_origins():
    """Top-left corner of each card's trim box on the sheet."""
    return [(GRID_X + c * TRIM_W, GRID_Y + r * TRIM_H) for r in range(ROWS) for c in range(COLS)]


def marks():
    """A crosshair in the margin at both ends of every cut line (above and below each vertical cut,
    left and right of each horizontal cut), plus one on every card corner inside the grid."""
    xs = [GRID_X + c * TRIM_W for c in range(COLS + 1)]
    ys = [GRID_Y + r * TRIM_H for r in range(ROWS + 1)]
    off = 42                                   # gap from the bleed edge to the crosshair centre
    top, bottom = GRID_Y - BLEED - off, SHEET_H - GRID_Y + BLEED + off
    left, right = GRID_X - BLEED - off - 20, SHEET_W - GRID_X + BLEED + off + 20
    centres = [(x, top) for x in xs] + [(x, bottom) for x in xs] + [(left, y) for y in ys] + [(right, y) for y in ys]
    arm, ring = 30, 12
    d = "".join(
        f"M{cx - arm} {cy}H{cx + arm}M{cx} {cy - arm}V{cy + arm}"
        f"M{cx + ring} {cy}a{ring} {ring} 0 1 0 {-2 * ring} 0a{ring} {ring} 0 1 0 {2 * ring} 0"
        for cx, cy in centres
    )
    # Small white crosshairs on every card corner. They sit inside the area a corner rounder removes,
    # sized for a 1/8 in (37.5 unit) radius or larger: arms stay where the curve cuts deeper than the
    # stroke, and the ring stays inside the 0.41 r gap along the diagonal.
    c_arm, c_ring = 24, 9
    corners = "".join(
        f"M{x - c_arm} {y}H{x + c_arm}M{x} {y - c_arm}V{y + c_arm}"
        f"M{x + c_ring} {y}a{c_ring} {c_ring} 0 1 0 {-2 * c_ring} 0a{c_ring} {c_ring} 0 1 0 {2 * c_ring} 0"
        for x in xs for y in ys
    )
    return (f'<path d="{d}" fill="none" stroke="#000" stroke-width="2.5"/>\n'
            f'<path d="{corners}" fill="none" stroke="#fff" stroke-width="2.5"/>')


def sheet(title, card, bg, note, with_marks):
    # Each card is cropped to its trim box; one shared background rectangle supplies the outer bleed.
    uses = "\n".join(
        f'<use href="#card" x="{x}" y="{y}" width="{TRIM_W}" height="{TRIM_H}"/>' for x, y in card_origins()
    )
    grid_bg = (f'<rect x="{GRID_X - BLEED}" y="{GRID_Y - BLEED}" width="{COLS * TRIM_W + 2 * BLEED}" '
               f'height="{ROWS * TRIM_H + 2 * BLEED}" fill="{bg}"/>')
    # Caption sits in the bottom margin between the left and middle crosshairs.
    caption, _ = text_path(note, GRID_X + 80, SHEET_H - GRID_Y + BLEED + 52, 22, 400, "#8A8497")
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" width="8.5in" height="11in" viewBox="0 0 {SHEET_W} {SHEET_H}">\n'
        f"<title>{title}</title>\n"
        f'<defs><symbol id="card" viewBox="{BLEED} {BLEED} {TRIM_W} {TRIM_H}">{card}</symbol></defs>\n'
        f'<rect width="{SHEET_W}" height="{SHEET_H}" fill="#fff"/>\n{grid_bg}\n'
        f"{uses}\n{marks() if with_marks else ''}\n{caption}\n</svg>\n"
    )


if __name__ == "__main__":
    (HERE / "chaotick-business-card-front.svg").write_text(svg("Chaotick business card - front", front()))
    (HERE / "chaotick-business-card-back.svg").write_text(svg("Chaotick business card - back", back()))

    out = HERE / "print"
    out.mkdir(exist_ok=True)
    (out / "sheet-1-fronts.svg").write_text(sheet(
        "Chaotick business cards - fronts (letter)", front(), SURFACE_RAISED_DARK,
        "Page 1 of 2 \u00b7 Fronts \u00b7 Print at 100% / Actual size", True))
    # Backs line up with the fronts when printed double-sided, flipping on the long edge. The layout is
    # symmetric left-to-right, so the same positions work. No marks here: cut from the front side.
    (out / "sheet-2-backs.svg").write_text(sheet(
        "Chaotick business cards - backs (letter)", back(), CREAM,
        "Page 2 of 2 \u00b7 Backs \u00b7 Print double-sided, flip on long edge", False))
    print("Wrote card SVGs and print sheets to", HERE)
