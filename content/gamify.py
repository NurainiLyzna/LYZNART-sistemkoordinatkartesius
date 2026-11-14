"""XP, level, dan badge LYZNART."""

LEVELS = [
    (0, "Penjelajah Pemula"),
    (100, "Pencari Titik"),
    (250, "Navigator Sumbu"),
    (450, "Penakluk Kuadran"),
    (700, "Kapten Koordinat"),
    (1000, "Master Kartesius"),
    (1400, "Legenda LYZNART"),
]

BADGES = {
    "welcome":    {"icon": "🚀", "name": "Langkah Pertama", "desc": "Bergabung dengan LYZNART"},
    "reader":     {"icon": "📘", "name": "Pembaca Rajin", "desc": "Menyelesaikan semua bagian materi"},
    "explorer":   {"icon": "🧭", "name": "Penjelajah Bidang", "desc": "Mencoba visualisasi koordinat interaktif"},
    "pretest":    {"icon": "📝", "name": "Siap Belajar", "desc": "Menyelesaikan pre-test"},
    "posttest":   {"icon": "🎓", "name": "Lulus Post-test", "desc": "Nilai post-test minimal 75"},
    "improve":    {"icon": "📈", "name": "Makin Hebat", "desc": "Nilai post-test lebih tinggi dari pre-test"},
    "practice":   {"icon": "💪", "name": "Pejuang Latihan", "desc": "Nilai latihan minimal 80"},
    "perfect":    {"icon": "💯", "name": "Sempurna!", "desc": "Mendapat nilai 100 pada latihan atau tes"},
    "gamer":      {"icon": "🎮", "name": "Gamer Koordinat", "desc": "Memainkan keempat game edukasi"},
    "xp500":      {"icon": "⭐", "name": "Bintang 500 XP", "desc": "Mengumpulkan 500 XP"},
    "master":     {"icon": "👑", "name": "Master Kartesius", "desc": "Mencapai level Master Kartesius"},
}

GAMES = {
    "titik":   {"name": "Tembak Titik", "icon": "🎯", "desc": "Klik posisi titik secepat mungkin sebelum waktu habis!", "color": "violet"},
    "kuadran": {"name": "Kuadran Kilat", "icon": "⚡", "desc": "Tebak kuadran atau sumbu tempat titik berada.", "color": "cyan"},
    "robot":   {"name": "Robot Harta Karun", "icon": "🤖", "desc": "Program robot agar sampai ke harta karun dengan langkah tepat.", "color": "sky"},
    "kapal":   {"name": "Kapal Koordinat", "icon": "🚢", "desc": "Temukan kapal tersembunyi dengan menebak koordinatnya.", "color": "lavender"},
}

MATERI_SECTIONS = ["m1", "m2", "m3", "m4", "m5", "m6"]


def level_info(xp):
    idx = 0
    for i, (need, _) in enumerate(LEVELS):
        if xp >= need:
            idx = i
    cur_need, name = LEVELS[idx]
    if idx + 1 < len(LEVELS):
        nxt = LEVELS[idx + 1][0]
        pct = round(100 * (xp - cur_need) / (nxt - cur_need))
    else:
        nxt, pct = None, 100
    return {"level": idx + 1, "name": name, "xp": xp, "next": nxt, "pct": pct}


def game_xp(score):
    """XP dari skor game dibatasi agar adil (maks 40 XP per permainan)."""
    return max(0, min(40, int(score) // 10))
