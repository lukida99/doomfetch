"""Minimal reader for Doom WAD files.

Covers exactly what doomfetch needs: the lump directory, the palette, and
decoding of the Doom picture format. Deliberately free of external tools
such as SLADE or deutex.
"""

import io
import struct
from pathlib import Path

from PIL import Image, UnidentifiedImageError

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


class WadError(Exception):
    pass


class Wad:
    """An IWAD or PWAD held in memory."""

    def __init__(self, path):
        self.path = Path(path)
        try:
            self.data = self.path.read_bytes()
        except OSError as exc:
            raise WadError(f"cannot read {path}: {exc}") from exc

        if len(self.data) < 12:
            raise WadError(f"{path} is too small to be a WAD")

        magic, count, diroff = struct.unpack_from("<4sii", self.data, 0)
        if magic not in (b"IWAD", b"PWAD"):
            raise WadError(f"{path} is not a WAD (magic: {magic!r})")
        if not 0 < count < 100_000 or not 0 <= diroff < len(self.data):
            raise WadError(f"{path} has a corrupt directory")

        self.kind = magic.decode()
        self.lumps = {}
        self.order = []
        for i in range(count):
            base = diroff + i * 16
            if base + 16 > len(self.data):
                raise WadError(f"{path}: directory runs past end of file")
            off, size, raw = struct.unpack_from("<ii8s", self.data, base)
            name = raw.rstrip(b"\0").decode("ascii", "replace")
            # On duplicate names the first entry wins, same as Doom itself.
            self.lumps.setdefault(name, (off, size))
            self.order.append(name)

    def __contains__(self, name):
        return name in self.lumps

    def get(self, name):
        off, size = self.lumps[name]
        return self.data[off:off + size]

    def palette(self, index=0):
        """PLAYPAL holds 14 palettes of 256 RGB triples each."""
        if "PLAYPAL" not in self.lumps:
            raise WadError(f"{self.path}: PLAYPAL is missing")
        pal = self.get("PLAYPAL")[index * 768:(index + 1) * 768]
        if len(pal) < 768:
            raise WadError(f"{self.path}: PLAYPAL is truncated")
        return [tuple(pal[i * 3:i * 3 + 3]) for i in range(256)]

    def between(self, start, end):
        """Lump names between two markers, e.g. S_START and S_END."""
        if start not in self.order or end not in self.order:
            return []
        i, j = self.order.index(start), self.order.index(end)
        return [n for n in self.order[i + 1:j]
                if not n.endswith("_START") and not n.endswith("_END")]

    def sprite_names(self):
        return self.between("S_START", "S_END")


def decode_lump(raw, palette):
    """Decode a graphic lump, whichever of the two formats it uses.

    Vanilla Doom stores graphics in its own picture format. Ports of the
    ZDoom family also accept plain PNG lumps, and Freedoom has shipped PNGs
    since 0.13, so both need handling.
    """
    if raw[:8] == PNG_MAGIC:
        try:
            return Image.open(io.BytesIO(raw)).convert("RGBA")
        except (UnidentifiedImageError, OSError):
            return None
    return decode_picture(raw, palette)


def decode_picture(raw, palette):
    """Doom picture format -> RGBA image, or None if the lump is not one.

    Layout: a header (width, height, leftoffset, topoffset), then one 32-bit
    offset per column pointing at a chain of posts. A post is
    (topdelta, length, unused, `length` palette indices, unused); a topdelta
    of 0xFF ends the column. Pixels no post covers stay transparent.
    """
    if len(raw) < 8:
        return None
    width, height, _left, _top = struct.unpack_from("<hhhh", raw, 0)
    if not (0 < width <= 4096 and 0 < height <= 4096):
        return None
    if len(raw) < 8 + width * 4:
        return None

    columns = struct.unpack_from(f"<{width}I", raw, 8)
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    px = img.load()

    for x, offset in enumerate(columns):
        pos = offset
        if pos >= len(raw):
            return None
        while True:
            # The terminating 0xFF is a single byte and may be the very last
            # byte of the lump, so check for it before requiring a length.
            if pos >= len(raw):
                return None
            topdelta = raw[pos]
            if topdelta == 0xFF:
                break
            if pos + 1 >= len(raw):
                return None
            length = raw[pos + 1]
            pos += 3                       # topdelta, length, padding byte
            if pos + length > len(raw):
                return None
            for i in range(length):
                y = topdelta + i
                if 0 <= y < height:
                    px[x, y] = (*palette[raw[pos + i]], 255)
            pos += length + 1              # pixels + padding byte
    return img
