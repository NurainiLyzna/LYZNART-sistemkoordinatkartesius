"""Membuat ikon PWA LYZNART (PNG) tanpa library eksternal.

Jalankan:  python tools/make_icons.py
"""
import math
import os
import struct
import zlib

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "static", "icons")
SS = 3  # supersampling untuk anti-aliasing


def lerp(a, b, t):
    return tuple(a[i] + (b[i] - a[i]) * t for i in range(3))


def render(size, maskable=False):
    big = size * SS
    c1, c2, c3 = (124, 58, 237), (99, 102, 241), (34, 211, 238)
    radius = 0 if maskable else big * 0.22
    scale = 0.78 if maskable else 1.0  # area aman ikon maskable
    cx = cy = big / 2
    pixels = []
    for y in range(big):
        row = []
        for x in range(big):
            # rounded square mask
            inside = True
            if radius:
                dx = max(radius - x, 0, x - (big - 1 - radius))
                dy = max(radius - y, 0, y - (big - 1 - radius))
                inside = dx * dx + dy * dy <= radius * radius
            if not inside:
                row.append((0, 0, 0, 0))
                continue
            t = (x + y) / (2 * big)
            col = lerp(c1, c2, t * 2) if t < 0.5 else lerp(c2, c3, (t - 0.5) * 2)
            # koordinat relatif (−1..1) di area ikon
            u = (x - cx) / (big / 2) / scale
            v = (cy - y) / (big / 2) / scale
            a = 1.0
            # grid tipis
            g = 0.25
            if abs(u) < 0.8 and abs(v) < 0.8 and (abs((u / g) - round(u / g)) < 0.025 or abs((v / g) - round(v / g)) < 0.025):
                col = lerp(col, (255, 255, 255), 0.18)
            # sumbu
            w = 0.035
            if (abs(v) < w and -0.78 < u < 0.7) or (abs(u) < w and -0.78 < v < 0.7):
                col = (255, 255, 255)
            # panah sumbu
            if 0.62 <= u <= 0.84 and abs(v) <= (0.84 - u) * 0.6:
                col = (255, 255, 255)
            if 0.62 <= v <= 0.84 and abs(u) <= (0.84 - v) * 0.6:
                col = (255, 255, 255)
            # titik di kuadran I (lingkar putih + isi cyan)
            d = math.hypot(u - 0.38, v - 0.38)
            if d < 0.17:
                col = (255, 255, 255)
            if d < 0.11:
                col = (34, 211, 238)
            # titik kecil di kuadran III
            d2 = math.hypot(u + 0.4, v + 0.36)
            if d2 < 0.09:
                col = (253, 224, 71)
            row.append((col[0], col[1], col[2], 255 * a))
        pixels.append(row)
    # downsample
    out = bytearray()
    for y in range(size):
        out.append(0)
        for x in range(size):
            acc = [0, 0, 0, 0]
            for sy in range(SS):
                for sx in range(SS):
                    p = pixels[y * SS + sy][x * SS + sx]
                    acc[0] += p[0] * p[3]
                    acc[1] += p[1] * p[3]
                    acc[2] += p[2] * p[3]
                    acc[3] += p[3]
            alpha = acc[3] / (SS * SS)
            if acc[3]:
                out += bytes([int(acc[0] / acc[3]), int(acc[1] / acc[3]), int(acc[2] / acc[3]), int(alpha)])
            else:
                out += bytes([0, 0, 0, 0])
    return bytes(out)


def write_png(path, size, raw):
    def chunk(tag, data):
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)

    png = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", size, size, 8, 6, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(png)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for name, size, mask in [("icon-192.png", 192, False), ("icon-512.png", 512, False),
                             ("icon-maskable-512.png", 512, True), ("apple-touch-icon.png", 180, True)]:
        write_png(os.path.join(OUT, name), size, render(size, mask))
        print("dibuat", name)
