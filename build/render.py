"""Renders images as ANSI art using half blocks and 24-bit colour.

One terminal cell shows two stacked pixels: the upper one as the foreground
colour of "▀", the lower one as the background colour. When only one half is
visible, "▀" or "▄" is emitted without a background so the terminal's own
background shows through.
"""

from PIL import Image

RESET = "\033[0m"
UPPER, LOWER = "▀", "▄"

# Doom renders 320x200 onto a 4:3 screen, so its pixels are 1.2x taller than
# they are wide. Without this correction every sprite comes out squashed.
PIXEL_ASPECT = 1.2

DEFAULTS = {"max_rows": 24, "max_cols": 44, "max_scale": 3.0, "pad": 1}


def fit(img, max_rows, max_cols, max_scale):
    width, height = img.size
    height = round(height * PIXEL_ASPECT)
    factor = min(max_cols / width, (max_rows * 2) / height, max_scale)
    return img.resize((max(1, round(width * factor)),
                       max(1, round(height * factor))), Image.NEAREST)


def to_ansi(img, max_rows=None, max_cols=None, max_scale=None, pad=None,
            alpha_threshold=127):
    max_rows = DEFAULTS["max_rows"] if max_rows is None else max_rows
    max_cols = DEFAULTS["max_cols"] if max_cols is None else max_cols
    max_scale = DEFAULTS["max_scale"] if max_scale is None else max_scale
    pad = DEFAULTS["pad"] if pad is None else pad

    img = fit(img.convert("RGBA"), max_rows, max_cols, max_scale)
    width, height = img.size
    if height % 2:                       # odd height -> add a transparent row
        padded = Image.new("RGBA", (width, height + 1), (0, 0, 0, 0))
        padded.paste(img, (0, 0))
        img, height = padded, height + 1
    px = img.load()

    lines = []
    for y in range(0, height, 2):
        parts = [" " * pad]
        cur_fg = cur_bg = None
        for x in range(width):
            top, bottom = px[x, y], px[x, y + 1]
            top_on = top[3] > alpha_threshold
            bottom_on = bottom[3] > alpha_threshold

            if not top_on and not bottom_on:
                if cur_fg is not None or cur_bg is not None:
                    parts.append(RESET)
                    cur_fg = cur_bg = None
                parts.append(" ")
                continue

            if top_on and bottom_on:
                fg, bg, char = top[:3], bottom[:3], UPPER
            elif top_on:
                fg, bg, char = top[:3], None, UPPER
            else:
                fg, bg, char = bottom[:3], None, LOWER

            codes = []
            if fg != cur_fg:
                codes.append("38;2;%d;%d;%d" % fg)
                cur_fg = fg
            if bg != cur_bg:
                codes.append("49" if bg is None else "48;2;%d;%d;%d" % bg)
                cur_bg = bg
            if codes:
                parts.append("\033[" + ";".join(codes) + "m")
            parts.append(char)

        parts.append(RESET)
        line = "".join(parts)
        lines.append(line.rstrip() if line.strip() else "")

    while lines and not lines[0]:
        lines.pop(0)
    while lines and not lines[-1]:
        lines.pop()
    return "\n".join(lines) + "\n"
