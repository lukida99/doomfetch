#!/usr/bin/env python3
"""Build doomfetch's ANSI colorscripts from a WAD.

    python3 build/build.py --wad /path/to/DOOM2.WAD

Writes ~/.local/share/doomfetch/{colorscripts,index.json} by default.
"""

import argparse
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from render import DEFAULTS, to_ansi          # noqa: E402
from sprites import SPRITES                   # noqa: E402
from PIL import ImageOps                       # noqa: E402
from wad import (Wad, WadError, decode_lump,   # noqa: E402
                 resolve_sprite)

DEFAULT_OUT = Path.home() / ".local/share/doomfetch"


def parse_args(argv=None):
    p = argparse.ArgumentParser(
        description="Extract Doom sprites from a WAD and render them as "
                    "ANSI colorscripts.")
    p.add_argument("--wad", required=True, type=Path,
                   help="IWAD to read, e.g. DOOM.WAD, DOOM2.WAD, freedoom2.wad")
    p.add_argument("--out", type=Path, default=DEFAULT_OUT,
                   help=f"output directory (default: {DEFAULT_OUT})")
    p.add_argument("--max-rows", type=int, default=DEFAULTS["max_rows"],
                   help="maximum height in terminal rows")
    p.add_argument("--max-cols", type=int, default=DEFAULTS["max_cols"],
                   help="maximum width in columns")
    p.add_argument("--max-scale", type=float, default=DEFAULTS["max_scale"],
                   help="maximum upscale factor for small sprites")
    p.add_argument("--keep-png", action="store_true",
                   help="also write the extracted sprites as PNG")
    p.add_argument("-q", "--quiet", action="store_true")
    return p.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)

    try:
        wad = Wad(args.wad)
        palette = wad.palette()
    except WadError as exc:
        sys.exit(f"error: {exc}")

    csdir = args.out / "colorscripts"
    if csdir.exists():
        shutil.rmtree(csdir)
    csdir.mkdir(parents=True)

    pngdir = args.out / "png"
    if args.keep_png:
        if pngdir.exists():
            shutil.rmtree(pngdir)
        pngdir.mkdir(parents=True)

    index, missing, broken = {}, [], []
    for name, (lump, title, category, since) in sorted(SPRITES.items()):
        actual, mirrored = resolve_sprite(wad, lump)
        if actual is None:
            missing.append(name)
            continue
        img = decode_lump(wad.get(actual), palette)
        if img is None:
            broken.append(name)
            continue
        if mirrored:
            img = ImageOps.mirror(img)
        (csdir / name).write_text(
            to_ansi(img, max_rows=args.max_rows, max_cols=args.max_cols,
                    max_scale=args.max_scale))
        if args.keep_png:
            img.save(pngdir / f"{name}.png")
        index[name] = {"title": title, "category": category,
                       "lump": lump, "since": since}

    (args.out / "index.json").write_text(
        json.dumps(index, indent=2, ensure_ascii=False) + "\n")
    (args.out / "source.json").write_text(json.dumps({
        "wad": args.wad.name,
        "kind": wad.kind,
        "lumps": len(wad.order),
        "sprites": len(index),
    }, indent=2) + "\n")

    if not args.quiet:
        print(f"{len(index)} sprites from {args.wad.name} -> {csdir}")
        if missing:
            print(f"{len(missing)} not present in this IWAD "
                  f"(a different one would add them): {', '.join(missing[:8])}"
                  + (" …" if len(missing) > 8 else ""))
        if broken:
            print(f"warning: could not decode: {', '.join(broken)}",
                  file=sys.stderr)

    if not index:
        sys.exit("error: no sprites found at all - is this really a Doom IWAD?")
    return 0


if __name__ == "__main__":
    sys.exit(main())
