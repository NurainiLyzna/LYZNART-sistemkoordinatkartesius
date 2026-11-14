"""Membuat sprite ikon LYZNART (templates/_icons.html).

Gaya: ubin app-icon bergradasi + simbol putih bersih (dengan bayangan lembut).
Avatar karakter & objek game memakai gaya ilustrasi tersendiri.

    python tools/make_icon_sprite.py
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "templates", "_icons.html")

# warna ubin (atas-kiri → bawah-kanan)
TILES = {
    "v": ("#b794ff", "#6d28d9"), "c": ("#5ee7f7", "#0e93b5"), "s": ("#8fd3ff", "#3b6cf0"),
    "p": ("#ffa9d6", "#e0337f"), "m": ("#7beac0", "#0a9b6b"), "y": ("#ffd66b", "#f08c00"),
    "o": ("#ffb57a", "#f2622b"), "i": ("#aab4ff", "#4f46e5"), "g": ("#d5dbe5", "#7b8798"),
    "l": ("#d6c8ff", "#8b6cf0"),
}

S = 'fill="none" stroke="currentColor" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"'
F = 'fill="currentColor"'
GOLD = "#ffe27a"

# nama ikon: (warna ubin, isi simbol)
ICONS = {
    "book": ("v", f'<path {S} d="M32 22 C27 18 20 17 14 18 V45 C20 44 27 45 32 49 C37 45 44 44 50 45 V18 C44 17 37 18 32 22 Z M32 22 V49"/>'),
    "compass": ("c", f'<path {S} d="M20 46 H50 M24 50 V16"/><path d="M40 26 V46 M40 26 H24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-dasharray="2.5 4" stroke-linecap="round"/>'
                     f'<circle cx="40" cy="26" r="5.5" fill="{GOLD}" stroke="currentColor" stroke-width="3"/>'),
    "pencil": ("p", f'<path {S} d="M40 15 L49 24 L27 46 L15 49 L18 37 Z M35 20 L44 29"/>'),
    "gamepad": ("i", f'<path {S} d="M23 23 H41 a11 11 0 0 1 11 11 v4 a6 6 0 0 1 -11 3.5 L38 37 H26 l-3 4.5 A6 6 0 0 1 12 38 v-4 a11 11 0 0 1 11 -11 Z M23 29 v8 M19 33 h8"/>'
                     f'<circle cx="40" cy="30.5" r="2.4" {F}/><circle cx="45" cy="35.5" r="2.4" {F}/>'),
    "home": ("s", f'<path {S} d="M15 31 L32 17 L49 31 M20 27 V47 H44 V27 M28 47 V37 H36 V47"/>'),
    "logout": ("o", f'<path {S} d="M30 16 H21 a4 4 0 0 0 -4 4 V44 a4 4 0 0 0 4 4 H30 M27 32 H49 M42 25 L49 32 L42 39"/>'),
    "install": ("c", f'<path {S} d="M32 15 V37 M24 29 L32 37 L40 29 M17 39 V44 a4 4 0 0 0 4 4 H43 a4 4 0 0 0 4 -4 V39"/>'),
    "bulb": ("y", f'<path {S} d="M26 39 a12.5 12.5 0 1 1 12 0 V43 H26 Z M27 48 H37"/><path d="M32 23 l-3 7 h6 l-3 7" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>'),
    "clipboard": ("s", f'<path {S} d="M25 18 H21 a4 4 0 0 0 -4 4 V45 a4 4 0 0 0 4 4 H43 a4 4 0 0 0 4 -4 V22 a4 4 0 0 0 -4 -4 H39 M26 14 H38 V21 H26 Z M25 35 L30 40 L39 30"/>'),
    "cap": ("v", f'<path {S} d="M10 28 L32 18 L54 28 L32 38 Z M20 33 V42 C26 47 38 47 44 42 V33 M50 30 V40"/><circle cx="50" cy="42" r="2.5" fill="{GOLD}"/>'),
    "chart": ("c", f'<path {S} d="M16 47 H48"/><path d="M23 40 V32 M32 40 V22 M41 40 V27" fill="none" stroke="currentColor" stroke-width="6" stroke-linecap="round"/>'),
    "chartup": ("m", f'<path {S} d="M15 45 L26 33 L34 39 L48 23 M40 23 H48 V31"/>'),
    "medal": ("y", f'<path {S} d="M24 13 L29 27 M40 13 L35 27"/><circle cx="32" cy="38" r="11" {S}/>'
                   f'<path d="M32 32 l1.9 3.8 4.2 .6 -3 3 .7 4.2 -3.8 -2 -3.8 2 .7 -4.2 -3 -3 4.2 -.6 Z" {F}/>'),
    "star": ("y", f'<path d="M32 16 L36.6 26.6 L48 27.8 L39.4 35.4 L41.9 46.6 L32 40.8 L22.1 46.6 L24.6 35.4 L16 27.8 L27.4 26.6 Z" {F} stroke="currentColor" stroke-width="3" stroke-linejoin="round"/>'),
    "target": ("p", f'<circle cx="32" cy="32" r="14" {S}/><circle cx="32" cy="32" r="6.5" {S}/><circle cx="32" cy="32" r="2" {F}/>'
                    f'<path {S} d="M32 11 V17 M32 47 V53 M11 32 H17 M47 32 H53"/>'),
    "bolt": ("y", f'<rect x="16" y="16" width="12" height="12" rx="3" {F} opacity=".35"/><rect x="36" y="36" width="12" height="12" rx="3" {F} opacity=".35"/>'
                  f'<path d="M35 13 L21 35 H31 L28 51 L43 28 H33 Z" {F} stroke="currentColor" stroke-width="2.5" stroke-linejoin="round"/>'),
    "robot": ("s", f'<path {S} d="M32 23 V16"/><circle cx="32" cy="14" r="3" {F}/><rect x="16" y="23" width="32" height="24" rx="7" {S}/>'
                   f'<circle cx="26" cy="34" r="3.2" {F}/><circle cx="38" cy="34" r="3.2" {F}/><path {S} d="M28 41 H36 M12 31 V39 M52 31 V39"/>'),
    "ship": ("c", f'<path {S} d="M31 14 V40"/><path d="M34 15 L47 37 H34 Z M29 20 L18 37 H29 Z" {F} stroke="currentColor" stroke-width="2.5" stroke-linejoin="round"/>'
                  f'<path {S} d="M13 41 H51 L45.5 49 H18.5 Z"/>'),
    "trophy": ("y", f'<path {S} d="M22 16 H42 V26 a10 10 0 0 1 -20 0 Z M22 19 H16 a5.5 5.5 0 0 0 6.5 9.5 M42 19 H48 a5.5 5.5 0 0 1 -6.5 9.5 M32 36 V43 M24 48 H40"/>'),
    "map": ("m", f'<path {S} d="M14 20 L25 16 L39 20 L50 16 V44 L39 48 L25 44 L14 48 Z M25 16 V44 M39 20 V48"/>'),
    "pin": ("p", f'<path {S} d="M32 50 C24 40 19 34 19 27 a13 13 0 0 1 26 0 c0 7 -5 13 -13 23 Z"/><circle cx="32" cy="27" r="4.5" {F}/>'),
    "rocket": ("v", f'<path {S} d="M32 12 C39.5 17 42.5 27 39 38 H25 C21.5 27 24.5 17 32 12 Z M25 31 L18 39 L25 41 M39 31 L46 39 L39 41"/>'
                    f'<circle cx="32" cy="25" r="3.5" {F}/><path d="M28.5 43 L32 51 L35.5 43 Z" fill="{GOLD}"/>'),
    "key": ("y", f'<circle cx="24" cy="27" r="8.5" {S}/><path {S} d="M30 33 L47 50 M41 44 L45.5 39.5 M45 48 L49.5 43.5"/>'),
    "user": ("l", f'<circle cx="32" cy="25" r="8" {S}/><path {S} d="M17 49 a15 12 0 0 1 30 0"/>'),
    "check": ("m", f'<path d="M18 33 L28 43 L46 22" fill="none" stroke="currentColor" stroke-width="5.5" stroke-linecap="round" stroke-linejoin="round"/>'),
    "folder": ("y", f'<path {S} d="M14 22 a3 3 0 0 1 3 -3 H27 l4 4 H47 a3 3 0 0 1 3 3 V44 a3 3 0 0 1 -3 3 H17 a3 3 0 0 1 -3 -3 Z"/>'),
    "clock": ("c", f'<circle cx="32" cy="33" r="16" {S}/><path {S} d="M32 24 V33 L38 37 M27 13 H37"/>'),
    "gem": ("c", f'<path {S} d="M20 26 L26 17 H38 L44 26 L32 48 Z"/><path d="M20 26 H44 M28 26 L32 48 L36 26 M26 17 L28 26 M38 17 L36 26" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linejoin="round"/>'),
    "rock": ("g", f'<path {S} d="M16 44 C14 36 20 29 27 30 C31 23 42 25 44 33 C50 35 50 44 44 45 H19 Z"/>'),
    "fire": ("o", f'<path {S} d="M32 13 C36 21 44 26 44 36 a12 12 0 0 1 -24 0 C20 30 24 26 26 21 C28 26 30 27 32 13 Z"/><path d="M32 33 c2 3 5 4.5 5 8 a5 5 0 0 1 -10 0 c0 -3 3 -4.5 5 -8 Z" {F}/>'),
    "drop": ("s", f'<path {S} d="M32 14 C38 24 44 30 44 37 a12 12 0 0 1 -24 0 C20 30 26 24 32 14 Z"/><path d="M26 38 a6 6 0 0 0 4 5" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round"/>'),
    "sparkle": ("p", f'<path d="M28 13 C29 23 31 25 41 26 C31 27 29 29 28 39 C27 29 25 27 15 26 C25 25 27 23 28 13 Z" {F}/>'
                     f'<path d="M44 35 c.6 4.4 1.6 5.4 6 6 c-4.4 .6 -5.4 1.6 -6 6 c-.6 -4.4 -1.6 -5.4 -6 -6 c4.4 -.6 5.4 -1.6 6 -6 Z" {F}/>'),
    "lock": ("g", f'<path {S} d="M24 30 V24 a8 8 0 0 1 16 0 V30"/><rect x="18" y="30" width="28" height="19" rx="5" {S}/><circle cx="32" cy="39.5" r="2.6" {F}/>'),
    "crown": ("y", f'<path {S} d="M16 42 L18 22 L26 31 L32 18 L38 31 L46 22 L48 42 Z M18 48 H46"/>'),
    "dumbbell": ("v", f'<path {S} d="M22 32 H42"/><rect x="16" y="23" width="7" height="18" rx="2.5" {F}/><rect x="41" y="23" width="7" height="18" rx="2.5" {F}/>'
                      f'<rect x="10" y="27" width="5" height="10" rx="2" {F}/><rect x="49" y="27" width="5" height="10" rx="2" {F}/>'),
    "hundred": ("p", f'<text x="32" y="38" text-anchor="middle" font-family="Baloo 2, Nunito, Arial, sans-serif" font-weight="800" font-size="20" {F}>100</text>'
                     f'<path {S} stroke-width="3" d="M19 44 H45"/>'),
    "heart": ("p", f'<path d="M32 47 C20 39 15 33 15 26 a8.5 8.5 0 0 1 17 -3.5 a8.5 8.5 0 0 1 17 3.5 c0 7 -5 13 -17 21 Z" {F}/>'),
    "warn": ("o", f'<path {S} d="M32 15 L49 46 H15 Z M32 26 V35"/><circle cx="32" cy="41" r="2.4" {F}/>'),
    "chat": ("c", f'<path {S} d="M16 20 a4 4 0 0 1 4 -4 H44 a4 4 0 0 1 4 4 V36 a4 4 0 0 1 -4 4 H28 L20 47 V40 a4 4 0 0 1 -4 -4 Z"/>'
                  f'<circle cx="25" cy="28" r="2.4" {F}/><circle cx="32" cy="28" r="2.4" {F}/><circle cx="39" cy="28" r="2.4" {F}/>'),
    "eye": ("l", f'<path {S} d="M11 32 C18 21 46 21 53 32 C46 43 18 43 11 32 Z"/><circle cx="32" cy="32" r="5.5" {F}/>'),
    "refresh": ("c", f'<path {S} d="M45 25 A14 14 0 1 0 46.5 37 M46 15 V25 H36"/>'),
    "play": ("m", f'<path d="M25 18 L46 32 L25 46 Z" {F} stroke="currentColor" stroke-width="3" stroke-linejoin="round"/>'),
    "save": ("i", f'<path {S} d="M18 16 H40 L47 23 V46 a2 2 0 0 1 -2 2 H19 a2 2 0 0 1 -2 -2 V17 Z M24 16 V24 H37 V16 M24 48 V37 H40 V48"/>'),
    "signal": ("l", f'<path {S} d="M15 28 a24 24 0 0 1 34 0 M21.5 34.5 a15 15 0 0 1 21 0 M28 41 a5.5 5.5 0 0 1 8 0"/><circle cx="32" cy="47" r="2.8" {F}/>'),
    "question": ("c", f'<path {S} stroke-width="4.5" d="M25 25 a7 7 0 1 1 10 6.3 c-2 1 -3 2.5 -3 5"/><circle cx="32" cy="45" r="2.8" {F}/>'),
    "ladder": ("v", f'<path {S} d="M15 47 H25 V39 H34 V31 H43 V23 H49"/><path d="M43 12 l1.5 3.5 3.5 1.5 -3.5 1.5 -1.5 3.5 -1.5 -3.5 -3.5 -1.5 3.5 -1.5 Z" fill="{GOLD}"/>'),
    "scroll": ("o", f'<rect x="17" y="14" width="30" height="36" rx="5" {S}/><path {S} stroke-width="3.5" d="M24 24 H40 M24 32 H40 M24 40 H34"/>'),
    "pointer": ("i", f'<path d="M21 15 L45 33 L34 35.5 L40 47.5 L35 50 L29 38 L21 45 Z" {F} stroke="currentColor" stroke-width="2.5" stroke-linejoin="round"/>'),
    "ruler": ("y", f'<path {S} d="M14 38 L38 14 L50 26 L26 50 Z"/><path d="M20 32 L24 36 M25.5 26.5 L28.5 29.5 M31 21 L35 25 M36.5 15.5 L39.5 18.5" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round"/>'),
    "flag": ("p", f'<path {S} d="M20 49 V15"/><path d="M20 16 C28 12 34 20 44 16 V33 C34 37 28 29 20 33 Z" {F}/>'),
}


def tile_symbol(name, color, glyph):
    a, b = TILES[color]
    return (f'<symbol id="ci-{name}" viewBox="0 0 64 64">'
            f'<rect x="3" y="4" width="58" height="58" rx="18" fill="{b}" opacity=".35"/>'
            f'<rect x="3" y="2" width="58" height="58" rx="18" fill="url(#t-{color})"/>'
            f'<path d="M21 2 H43 A18 18 0 0 1 61 20 V22 C46 14 18 14 3 24 V20 A18 18 0 0 1 21 2 Z" fill="#fff" opacity=".18"/>'
            f'<rect x="4" y="3" width="56" height="56" rx="17" fill="none" stroke="#fff" stroke-opacity=".35" stroke-width="1.5"/>'
            f'<use href="#gl-{name}" color="#1e1b4b" opacity=".22" y="2"/>'
            f'<use href="#gl-{name}" color="#ffffff"/></symbol>\n'
            f'<symbol id="gl-{name}" viewBox="0 0 64 64">{glyph}</symbol>\n')


# ---- avatar karakter & objek game (gaya ilustrasi) ----
EXTRA = """
<symbol id="ci-face" viewBox="0 0 20 12">
  <ellipse cx="2.2" cy="8" rx="2" ry="1.2" fill="#f9a8d4"/><ellipse cx="17.8" cy="8" rx="2" ry="1.2" fill="#f9a8d4"/>
  <ellipse cx="5.5" cy="4.2" rx="1.8" ry="2.2" fill="#2e1065"/><ellipse cx="14.5" cy="4.2" rx="1.8" ry="2.2" fill="#2e1065"/>
  <circle cx="6.1" cy="3.4" r=".7" fill="#fff"/><circle cx="15.1" cy="3.4" r=".7" fill="#fff"/>
  <path d="M8.4 7.2 q1.6 1.8 3.2 0" fill="none" stroke="#2e1065" stroke-width="1.2" stroke-linecap="round"/>
</symbol>
<symbol id="ci-av-robot" viewBox="0 0 64 64"><g stroke="#3b1a78" stroke-width="2.6" stroke-linejoin="round" stroke-linecap="round">
  <path d="M32 17 V10" fill="none"/><circle cx="32" cy="8" r="4" fill="url(#a-p)"/>
  <rect x="5" y="28" width="7" height="13" rx="3.5" fill="url(#a-l)"/><rect x="52" y="28" width="7" height="13" rx="3.5" fill="url(#a-l)"/>
  <rect x="21" y="49" width="22" height="10" rx="4" fill="url(#a-l)"/>
  <rect x="11" y="17" width="42" height="34" rx="13" fill="url(#a-s)"/>
  <rect x="17" y="24" width="30" height="19" rx="9" fill="#2e1065"/></g>
  <ellipse cx="25.5" cy="32.5" rx="3" ry="3.6" fill="#67e8f9"/><ellipse cx="38.5" cy="32.5" rx="3" ry="3.6" fill="#67e8f9"/>
  <circle cx="26.5" cy="31.3" r="1" fill="#fff"/><circle cx="39.5" cy="31.3" r="1" fill="#fff"/>
  <path d="M29 38 q3 2.6 6 0" fill="none" stroke="#67e8f9" stroke-width="2" stroke-linecap="round"/>
  <ellipse cx="15" cy="44" rx="2.4" ry="1.4" fill="#f9a8d4"/><ellipse cx="49" cy="44" rx="2.4" ry="1.4" fill="#f9a8d4"/></symbol>
<symbol id="ci-av-astronot" viewBox="0 0 64 64"><g stroke="#3b1a78" stroke-width="2.6" stroke-linejoin="round" stroke-linecap="round">
  <path d="M32 9 V4" fill="none"/><circle cx="32" cy="4" r="2.6" fill="#fcd34d" stroke-width="2"/>
  <rect x="3" y="28" width="8" height="14" rx="4" fill="url(#a-p)"/><rect x="53" y="28" width="8" height="14" rx="4" fill="url(#a-p)"/>
  <circle cx="32" cy="34" r="25" fill="#fff"/>
  <rect x="13" y="22" width="38" height="27" rx="13.5" fill="url(#a-s)"/></g>
  <path d="M19 31 a8 8 0 0 1 6 -5" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round"/>
  <use href="#ci-face" x="22" y="30" width="20" height="12"/></symbol>
<symbol id="ci-av-kucing" viewBox="0 0 64 64"><g stroke="#3b1a78" stroke-width="2.6" stroke-linejoin="round" stroke-linecap="round">
  <path d="M10 28 L12 6 L26 17 Q32 15 38 17 L52 6 L54 28 Q60 44 48 52 Q32 61 16 52 Q4 44 10 28 Z" fill="url(#a-o)"/>
  <path d="M15 13 L16 22 L22 17 Z M49 13 L48 22 L42 17 Z" fill="#f9a8d4" stroke-width="1.6"/>
  <path d="M5 38 h9 M6 44 l8 -2 M59 38 h-9 M58 44 l-8 -2" fill="none" stroke-width="2"/></g>
  <use href="#ci-face" x="21" y="30" width="22" height="13"/></symbol>
<symbol id="ci-av-burung" viewBox="0 0 64 64"><g stroke="#3b1a78" stroke-width="2.6" stroke-linejoin="round" stroke-linecap="round">
  <path d="M13 22 L10 6 L24 15 Z M51 22 L54 6 L40 15 Z" fill="url(#a-v)"/>
  <ellipse cx="32" cy="36" rx="24" ry="23" fill="url(#a-v)"/>
  <ellipse cx="32" cy="45" rx="13" ry="11" fill="url(#a-l)" stroke-width="2"/>
  <circle cx="23" cy="30" r="8.5" fill="#fff" stroke-width="2.2"/><circle cx="41" cy="30" r="8.5" fill="#fff" stroke-width="2.2"/>
  <path d="M28.5 37 H35.5 L32 42 Z" fill="#fcd34d" stroke-width="2"/></g>
  <circle cx="24" cy="31" r="4.2" fill="#2e1065"/><circle cx="40" cy="31" r="4.2" fill="#2e1065"/>
  <circle cx="25.4" cy="29.6" r="1.4" fill="#fff"/><circle cx="41.4" cy="29.6" r="1.4" fill="#fff"/>
  <ellipse cx="14" cy="40" rx="2.6" ry="1.5" fill="#f9a8d4"/><ellipse cx="50" cy="40" rx="2.6" ry="1.5" fill="#f9a8d4"/></symbol>

<symbol id="ci-obj-rock" viewBox="0 0 64 64">
  <ellipse cx="32" cy="54" rx="22" ry="4" fill="#1e1b4b" opacity=".12"/>
  <path d="M8 47 C6 35 15 25 25 27 C31 15 50 18 52 31 C60 35 59 50 48 52 H14 C10 52 8 50 8 47 Z" fill="url(#o-rock)"/>
  <path d="M27 31 C30 24 40 23 45 29" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round" opacity=".55"/>
  <path d="M18 44 l6 -4 M38 46 l7 -3" stroke="#64748b" stroke-width="2" stroke-linecap="round" opacity=".6"/></symbol>
<symbol id="ci-obj-gem" viewBox="0 0 64 64">
  <ellipse cx="32" cy="58" rx="16" ry="3" fill="#1e1b4b" opacity=".12"/>
  <path d="M12 22 L22 8 H42 L52 22 L32 56 Z" fill="url(#o-gem)"/>
  <path d="M12 22 H52 L32 56 Z" fill="#0e7490" opacity=".25"/>
  <path d="M22 8 L27 22 L32 56 M42 8 L37 22 L32 56 M27 22 L32 8 L37 22" fill="none" stroke="#fff" stroke-width="1.6" opacity=".7" stroke-linejoin="round"/>
  <path d="M50 4 l1.6 4 4 1.6 -4 1.6 -1.6 4 -1.6 -4 -4 -1.6 4 -1.6 Z" fill="#fff"/></symbol>
<symbol id="ci-obj-fire" viewBox="0 0 64 64">
  <path d="M32 3 C41 17 54 23 52 41 C50 53 42 60 32 60 C22 60 14 53 12 41 C11 30 19 24 23 14 C26 23 30 25 32 3 Z" fill="url(#o-fire)"/>
  <path d="M32 26 C37 33 43 37 42 46 C41 52 37 55 32 55 C27 55 23 52 22 46 C22 39 28 36 32 26 Z" fill="#ffe27a"/>
  <path d="M32 40 c2.5 3.5 5 5 5 8.5 a5 5 0 0 1 -10 0 c0 -3.5 2.5 -5 5 -8.5 Z" fill="#fff" opacity=".85"/></symbol>
<symbol id="ci-obj-drop" viewBox="0 0 64 64">
  <path d="M32 4 C43 21 52 30 52 42 a20 20 0 0 1 -40 0 C12 30 21 21 32 4 Z" fill="url(#o-drop)"/>
  <path d="M21 40 a11 11 0 0 0 5 10" fill="none" stroke="#fff" stroke-width="4" stroke-linecap="round" opacity=".8"/>
  <circle cx="40" cy="30" r="3" fill="#fff" opacity=".6"/></symbol>
<symbol id="ci-obj-ship" viewBox="0 0 64 64">
  <path d="M31 6 V40" stroke="#4c1d95" stroke-width="3" stroke-linecap="round"/>
  <path d="M34 8 L52 36 H34 Z" fill="url(#o-sail)"/><path d="M28 14 L13 36 H28 Z" fill="#ede9fe"/>
  <path d="M6 40 H58 L50 54 H14 Z" fill="url(#o-hull)"/>
  <path d="M10 44 H54" stroke="#fff" stroke-width="2.4" opacity=".6"/>
  <path d="M2 60 q5 -4 10 0 t10 0 t10 0 t10 0 t10 0 t10 0" fill="none" stroke="#38bdf8" stroke-width="3" stroke-linecap="round"/></symbol>
"""

DEFS = "".join(f'<linearGradient id="t-{k}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{a}"/><stop offset="1" stop-color="{b}"/></linearGradient>'
               for k, (a, b) in TILES.items())
DEFS += """
<linearGradient id="a-l" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f5f3ff"/><stop offset="1" stop-color="#c4b5fd"/></linearGradient>
<linearGradient id="a-v" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#c4b5fd"/><stop offset="1" stop-color="#8b5cf6"/></linearGradient>
<linearGradient id="a-s" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f0f9ff"/><stop offset="1" stop-color="#7dd3fc"/></linearGradient>
<linearGradient id="a-p" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fdf2f8"/><stop offset="1" stop-color="#f9a8d4"/></linearGradient>
<linearGradient id="a-o" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff7ed"/><stop offset="1" stop-color="#fdba74"/></linearGradient>
<linearGradient id="o-rock" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e2e8f0"/><stop offset="1" stop-color="#94a3b8"/></linearGradient>
<linearGradient id="o-gem" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#a5f3fc"/><stop offset=".5" stop-color="#22d3ee"/><stop offset="1" stop-color="#8b5cf6"/></linearGradient>
<linearGradient id="o-fire" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fb923c"/><stop offset="1" stop-color="#e11d48"/></linearGradient>
<linearGradient id="o-drop" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7dd3fc"/><stop offset="1" stop-color="#2563eb"/></linearGradient>
<linearGradient id="o-sail" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#c4b5fd"/></linearGradient>
<linearGradient id="o-hull" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#a78bfa"/><stop offset="1" stop-color="#6d28d9"/></linearGradient>
"""

if __name__ == "__main__":
    body = "".join(tile_symbol(n, c, g) for n, (c, g) in ICONS.items())
    html = ('<svg id="ci-sprite" xmlns="http://www.w3.org/2000/svg" width="0" height="0" '
            'style="position:absolute;width:0;height:0;overflow:hidden" aria-hidden="true" focusable="false">\n'
            f"<defs>{DEFS}</defs>\n{body}{EXTRA}</svg>\n")
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write(html)
    print(f"{OUT}: {len(ICONS)} ikon ubin + avatar & objek game")
