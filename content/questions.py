"""Bank soal LYZNART - Sistem Koordinat Kartesius (Kelas VIII).

Setiap soal: (teks, [jawaban_benar, pengecoh1, pengecoh2, pengecoh3], pembahasan, plot_opsional)
Opsi diacak secara deterministik (seed = id soal) sehingga kunci selalu konsisten.
plot = daftar titik [x, y, "label"] yang digambar pada bidang koordinat kecil di soal.
"""
import random

PLOT_A = [[2, 3, "A"], [-4, 1, "B"], [-2, -3, "C"], [3, -2, "D"]]

LATIHAN_RAW = [
    # --- A. Bidang Kartesius & pasangan berurutan ---
    ("Titik potong antara sumbu-x dan sumbu-y disebut ...",
     ["titik asal O(0, 0)", "titik puncak", "titik tengah (1, 1)", "kuadran I"],
     "Sumbu-x dan sumbu-y berpotongan tegak lurus di titik asal O dengan koordinat (0, 0).", None, "Bidang Kartesius"),
    ("Absis dari titik P(−3, 5) adalah ...",
     ["−3", "5", "3", "−5"],
     "Pada pasangan berurutan (x, y), absis adalah nilai x. Jadi absis P adalah −3.", None, "Bidang Kartesius"),
    ("Ordinat dari titik Q(4, −7) adalah ...",
     ["−7", "4", "7", "−4"],
     "Ordinat adalah nilai y pada pasangan berurutan (x, y). Ordinat Q adalah −7.", None, "Bidang Kartesius"),
    ("Titik yang memiliki absis 6 dan ordinat −2 ditulis ...",
     ["(6, −2)", "(−2, 6)", "(−6, 2)", "(2, −6)"],
     "Koordinat ditulis (absis, ordinat) = (x, y), sehingga titiknya (6, −2).", None, "Bidang Kartesius"),
    ("Perhatikan gambar. Koordinat titik B adalah ...",
     ["(−4, 1)", "(1, −4)", "(4, 1)", "(−4, −1)"],
     "Dari O, titik B berada 4 satuan ke kiri (x = −4) dan 1 satuan ke atas (y = 1). Jadi B(−4, 1).", PLOT_A, "Bidang Kartesius"),
    ("Titik berikut yang terletak pada sumbu-y adalah ...",
     ["(0, −5)", "(−5, 0)", "(5, 5)", "(−5, −5)"],
     "Titik pada sumbu-y memiliki absis 0, yaitu (0, −5).", None, "Bidang Kartesius"),
    ("Titik berikut yang terletak pada sumbu-x adalah ...",
     ["(7, 0)", "(0, 7)", "(7, 7)", "(−7, 7)"],
     "Titik pada sumbu-x memiliki ordinat 0, yaitu (7, 0).", None, "Bidang Kartesius"),
    ("Dari titik asal, Lyzy bergerak 3 satuan ke kiri lalu 4 satuan ke atas. Lyzy sampai di titik ...",
     ["(−3, 4)", "(3, −4)", "(4, −3)", "(−4, 3)"],
     "Ke kiri berarti x negatif (x = −3), ke atas berarti y positif (y = 4). Jadi (−3, 4).", None, "Bidang Kartesius"),

    # --- B. Kuadran ---
    ("Titik (−5, 2) terletak pada kuadran ...",
     ["II", "I", "III", "IV"],
     "x negatif dan y positif → kuadran II.", None, "Kuadran"),
    ("Titik (4, −6) terletak pada kuadran ...",
     ["IV", "I", "II", "III"],
     "x positif dan y negatif → kuadran IV.", None, "Kuadran"),
    ("Titik (−1, −8) terletak pada kuadran ...",
     ["III", "I", "II", "IV"],
     "x negatif dan y negatif → kuadran III.", None, "Kuadran"),
    ("Ciri titik yang berada di kuadran I adalah ...",
     ["x > 0 dan y > 0", "x < 0 dan y > 0", "x < 0 dan y < 0", "x > 0 dan y < 0"],
     "Kuadran I berada di kanan atas: absis dan ordinat sama-sama positif.", None, "Kuadran"),
    ("Ciri titik yang berada di kuadran IV adalah ...",
     ["absis positif, ordinat negatif", "absis negatif, ordinat positif",
      "absis dan ordinat negatif", "absis dan ordinat positif"],
     "Kuadran IV berada di kanan bawah: x positif, y negatif.", None, "Kuadran"),
    ("Titik (0, 9) terletak ...",
     ["pada sumbu-y, tidak di kuadran mana pun", "di kuadran I", "di kuadran II", "pada sumbu-x"],
     "Absisnya 0 sehingga titik berada tepat pada sumbu-y. Titik pada sumbu tidak termasuk kuadran mana pun.", None, "Kuadran"),
    ("Jika titik (a, 3) berada di kuadran II, maka nilai a yang mungkin adalah ...",
     ["a < 0", "a > 0", "a = 0", "a = 3"],
     "Di kuadran II absis negatif, sehingga a < 0.", None, "Kuadran"),
    ("Manakah titik yang berada di kuadran III?",
     ["(−2, −7)", "(2, −7)", "(−2, 7)", "(2, 7)"],
     "Kuadran III membutuhkan x < 0 dan y < 0. Hanya (−2, −7) yang memenuhi.", None, "Kuadran"),

    # --- C. Posisi titik terhadap sumbu ---
    ("Jarak titik A(−4, 6) terhadap sumbu-x adalah ...",
     ["6 satuan", "4 satuan", "10 satuan", "2 satuan"],
     "Jarak titik ke sumbu-x = |y| = |6| = 6 satuan.", None, "Jarak ke Sumbu"),
    ("Jarak titik A(−4, 6) terhadap sumbu-y adalah ...",
     ["4 satuan", "6 satuan", "−4 satuan", "10 satuan"],
     "Jarak titik ke sumbu-y = |x| = |−4| = 4 satuan. Jarak selalu bernilai positif.", None, "Jarak ke Sumbu"),
    ("Titik B(5, −3) memiliki jarak ...",
     ["3 satuan ke sumbu-x dan 5 satuan ke sumbu-y", "5 satuan ke sumbu-x dan 3 satuan ke sumbu-y",
      "−3 satuan ke sumbu-x dan 5 satuan ke sumbu-y", "8 satuan ke kedua sumbu"],
     "Jarak ke sumbu-x = |−3| = 3, jarak ke sumbu-y = |5| = 5.", None, "Jarak ke Sumbu"),
    ("Titik di kuadran III yang berjarak 2 satuan dari sumbu-x dan 7 satuan dari sumbu-y adalah ...",
     ["(−7, −2)", "(−2, −7)", "(7, 2)", "(−7, 2)"],
     "Jarak ke sumbu-y = |x| = 7 dan jarak ke sumbu-x = |y| = 2. Di kuadran III keduanya negatif → (−7, −2).", None, "Jarak ke Sumbu"),
    ("Jarak titik (0, −8) ke titik asal adalah ...",
     ["8 satuan", "−8 satuan", "0 satuan", "16 satuan"],
     "Titik berada di sumbu-y, 8 satuan di bawah O. Jaraknya 8 satuan.", None, "Jarak ke Sumbu"),
    ("Titik P di kuadran II berjarak 5 satuan dari sumbu-y dan 1 satuan dari sumbu-x. Koordinat P adalah ...",
     ["(−5, 1)", "(−1, 5)", "(5, −1)", "(1, −5)"],
     "Jarak ke sumbu-y menentukan |x| = 5, jarak ke sumbu-x menentukan |y| = 1. Kuadran II: x < 0, y > 0 → (−5, 1).", None, "Jarak ke Sumbu"),

    # --- D. Posisi titik terhadap titik acuan ---
    ("Koordinat titik A(5, 3) terhadap titik acuan B(2, 1) adalah ...",
     ["(3, 2)", "(7, 4)", "(2, 3)", "(−3, −2)"],
     "Terhadap titik acuan (p, q): (x − p, y − q) = (5 − 2, 3 − 1) = (3, 2).", None, "Titik Acuan"),
    ("Koordinat titik C(−2, 4) terhadap titik acuan P(1, −1) adalah ...",
     ["(−3, 5)", "(−1, 3)", "(3, −5)", "(−3, 3)"],
     "(x − p, y − q) = (−2 − 1, 4 − (−1)) = (−3, 5).", None, "Titik Acuan"),
    ("Koordinat titik Q terhadap titik R(3, 2) adalah (−4, 1). Koordinat Q terhadap titik asal adalah ...",
     ["(−1, 3)", "(−7, −1)", "(7, 1)", "(1, −3)"],
     "Q = (3 + (−4), 2 + 1) = (−1, 3).", None, "Titik Acuan"),
    ("Pada peta, rumah Dina di (2, 3) dan sekolah di (6, −1). Posisi sekolah terhadap rumah Dina adalah ...",
     ["(4, −4)", "(−4, 4)", "(8, 2)", "(4, 4)"],
     "Sekolah terhadap rumah: (6 − 2, −1 − 3) = (4, −4), artinya 4 satuan ke kanan dan 4 satuan ke bawah.", None, "Titik Acuan"),
    ("Koordinat titik asal O(0, 0) terhadap titik K(−3, 5) adalah ...",
     ["(3, −5)", "(−3, 5)", "(0, 0)", "(5, −3)"],
     "(0 − (−3), 0 − 5) = (3, −5).", None, "Titik Acuan"),
    ("Titik T(4, −2) digeser 3 satuan ke kiri lalu 5 satuan ke atas. Posisi T sekarang adalah ...",
     ["(1, 3)", "(7, 3)", "(1, −7)", "(7, −7)"],
     "Ke kiri 3: x = 4 − 3 = 1. Ke atas 5: y = −2 + 5 = 3. Jadi (1, 3).", None, "Titik Acuan"),

    # --- E. Garis sejajar & tegak lurus sumbu ---
    ("Garis yang melalui A(2, 5) dan B(−3, 5) adalah garis yang ...",
     ["sejajar sumbu-x", "sejajar sumbu-y", "melalui titik asal", "tegak lurus sumbu-x"],
     "Ordinat A dan B sama (y = 5), sehingga garis AB mendatar, sejajar sumbu-x (dan tegak lurus sumbu-y).", None, "Garis & Sumbu"),
    ("Garis yang melalui C(4, 1) dan D(4, −6) adalah garis yang ...",
     ["sejajar sumbu-y", "sejajar sumbu-x", "tegak lurus sumbu-y", "melalui titik asal"],
     "Absis C dan D sama (x = 4), sehingga garis CD tegak, sejajar sumbu-y (tegak lurus sumbu-x).", None, "Garis & Sumbu"),
    ("Garis k melalui titik (−2, 3) dan sejajar sumbu-x. Titik lain yang dilalui garis k adalah ...",
     ["(5, 3)", "(−2, 5)", "(3, −2)", "(0, 0)"],
     "Garis sejajar sumbu-x memiliki ordinat tetap y = 3. Titik (5, 3) memiliki y = 3.", None, "Garis & Sumbu"),
    ("Garis m melalui titik (−1, 4) dan tegak lurus sumbu-x. Titik lain yang dilalui garis m adalah ...",
     ["(−1, −2)", "(4, −1)", "(1, 4)", "(2, 4)"],
     "Garis tegak lurus sumbu-x berarti tegak (vertikal), absisnya tetap x = −1. Titik (−1, −2) memenuhi.", None, "Garis & Sumbu"),
    ("Garis yang melalui (1, 2) dan (3, 4) ...",
     ["tidak sejajar sumbu-x maupun sumbu-y", "sejajar sumbu-x", "sejajar sumbu-y", "berimpit dengan sumbu-x"],
     "Absis berbeda (1 ≠ 3) dan ordinat berbeda (2 ≠ 4), jadi garisnya miring: memotong kedua sumbu.", None, "Garis & Sumbu"),
    ("Semua titik pada garis yang melalui (3, −4) dan sejajar sumbu-x memiliki ...",
     ["ordinat −4", "absis 3", "absis −4", "ordinat 3"],
     "Garis sejajar sumbu-x memiliki ordinat yang sama di setiap titiknya, yaitu −4.", None, "Garis & Sumbu"),

    # --- F. Jarak dua titik & bangun datar ---
    ("Jarak titik A(1, 2) ke titik B(7, 2) adalah ...",
     ["6 satuan", "8 satuan", "4 satuan", "5 satuan"],
     "Ordinat sama, jadi jaraknya = |7 − 1| = 6 satuan.", None, "Jarak & Bangun"),
    ("Jarak titik C(−3, 5) ke titik D(−3, −4) adalah ...",
     ["9 satuan", "1 satuan", "6 satuan", "8 satuan"],
     "Absis sama, jadi jaraknya = |5 − (−4)| = 9 satuan.", None, "Jarak & Bangun"),
    ("Persegi panjang memiliki titik sudut (1, 1), (6, 1), (6, 4), dan (1, 4). Luasnya adalah ...",
     ["15 satuan luas", "16 satuan luas", "8 satuan luas", "24 satuan luas"],
     "Panjang = 6 − 1 = 5, lebar = 4 − 1 = 3. Luas = 5 × 3 = 15 satuan luas.",
     [[1, 1, "A"], [6, 1, "B"], [6, 4, "C"], [1, 4, "D"]], "Jarak & Bangun"),
    ("Tiga titik sudut sebuah persegi adalah (−2, −1), (2, −1), dan (2, 3). Titik sudut keempat adalah ...",
     ["(−2, 3)", "(3, −2)", "(−2, −3)", "(2, −3)"],
     "Sisi persegi 4 satuan. Titik keempat harus sejajar dengan (−2, −1) secara tegak dan dengan (2, 3) secara mendatar → (−2, 3).", None, "Jarak & Bangun"),
    ("Dengan teorema Pythagoras, jarak titik O(0, 0) ke titik Q(3, 4) adalah ...",
     ["5 satuan", "7 satuan", "1 satuan", "12 satuan"],
     "Jarak = √(3² + 4²) = √(9 + 16) = √25 = 5 satuan.", [[0, 0, "O"], [3, 4, "Q"]], "Jarak & Bangun"),
    ("Segitiga dengan titik sudut A(0, 0), B(6, 0), dan C(0, 4) memiliki luas ...",
     ["12 satuan luas", "24 satuan luas", "10 satuan luas", "20 satuan luas"],
     "Alas AB = 6, tinggi AC = 4. Luas = ½ × 6 × 4 = 12 satuan luas.",
     [[0, 0, "A"], [6, 0, "B"], [0, 4, "C"]], "Jarak & Bangun"),
]

PRETEST_RAW = [
    ("Garis bilangan mendatar pada bidang Kartesius disebut ...",
     ["sumbu-x", "sumbu-y", "titik asal", "kuadran"], "Sumbu mendatar adalah sumbu-x (absis).", None, "Bidang Kartesius"),
    ("Absis dari titik (8, −1) adalah ...",
     ["8", "−1", "1", "−8"], "Absis adalah nilai x, yaitu 8.", None, "Bidang Kartesius"),
    ("Titik (−6, −3) terletak pada kuadran ...",
     ["III", "II", "IV", "I"], "x < 0 dan y < 0 → kuadran III.", None, "Kuadran"),
    ("Titik (7, 2) terletak pada kuadran ...",
     ["I", "II", "III", "IV"], "x > 0 dan y > 0 → kuadran I.", None, "Kuadran"),
    ("Titik berikut yang terletak pada sumbu-x adalah ...",
     ["(−4, 0)", "(0, −4)", "(−4, −4)", "(4, 4)"], "Titik pada sumbu-x memiliki ordinat 0.", None, "Bidang Kartesius"),
    ("Jarak titik (3, −9) terhadap sumbu-x adalah ...",
     ["9 satuan", "3 satuan", "−9 satuan", "12 satuan"], "Jarak ke sumbu-x = |y| = 9.", None, "Jarak ke Sumbu"),
    ("Jarak titik (−6, 2) terhadap sumbu-y adalah ...",
     ["6 satuan", "2 satuan", "−6 satuan", "8 satuan"], "Jarak ke sumbu-y = |x| = 6.", None, "Jarak ke Sumbu"),
    ("Koordinat titik A(6, 4) terhadap titik acuan B(2, 1) adalah ...",
     ["(4, 3)", "(8, 5)", "(3, 4)", "(−4, −3)"], "(6 − 2, 4 − 1) = (4, 3).", None, "Titik Acuan"),
    ("Garis yang melalui (−1, 2) dan (5, 2) adalah garis yang ...",
     ["sejajar sumbu-x", "sejajar sumbu-y", "melalui titik asal", "tegak lurus sumbu-x"],
     "Ordinat kedua titik sama (y = 2), jadi garisnya mendatar dan sejajar sumbu-x.", None, "Garis & Sumbu"),
    ("Jarak titik (2, 3) ke titik (2, 10) adalah ...",
     ["7 satuan", "13 satuan", "5 satuan", "8 satuan"], "Absis sama, jarak = |10 − 3| = 7.", None, "Jarak & Bangun"),
    ("Dari titik asal bergerak 5 satuan ke kanan lalu 2 satuan ke bawah. Titik yang dicapai adalah ...",
     ["(5, −2)", "(−5, 2)", "(2, −5)", "(5, 2)"], "Kanan → x = 5, bawah → y = −2.", None, "Bidang Kartesius"),
    ("Jika titik (m, −4) berada di kuadran III, maka ...",
     ["m < 0", "m > 0", "m = 0", "m = −4 saja"], "Di kuadran III absis negatif, jadi m < 0.", None, "Kuadran"),
    ("Persegi panjang dengan titik sudut (0, 0), (4, 0), (4, 3), dan (0, 3) memiliki luas ...",
     ["12 satuan luas", "14 satuan luas", "7 satuan luas", "16 satuan luas"], "Luas = 4 × 3 = 12 satuan luas.", None, "Jarak & Bangun"),
    ("Titik K di kuadran IV berjarak 3 satuan dari sumbu-x dan 2 satuan dari sumbu-y. Koordinat K adalah ...",
     ["(2, −3)", "(3, −2)", "(−2, 3)", "(−3, 2)"], "|x| = 2, |y| = 3, kuadran IV: x > 0, y < 0 → (2, −3).", None, "Jarak ke Sumbu"),
    ("Titik P(1, 5) digeser 4 satuan ke kiri lalu 2 satuan ke bawah. Posisi P sekarang ...",
     ["(−3, 3)", "(5, 7)", "(−3, 7)", "(5, 3)"], "x = 1 − 4 = −3, y = 5 − 2 = 3.", None, "Titik Acuan"),
]

POSTTEST_RAW = [
    ("Garis bilangan tegak pada bidang Kartesius disebut ...",
     ["sumbu-y", "sumbu-x", "titik asal", "kuadran"], "Sumbu tegak adalah sumbu-y (ordinat).", None, "Bidang Kartesius"),
    ("Ordinat dari titik (−5, 9) adalah ...",
     ["9", "−5", "5", "−9"], "Ordinat adalah nilai y, yaitu 9.", None, "Bidang Kartesius"),
    ("Titik (4, −8) terletak pada kuadran ...",
     ["IV", "III", "II", "I"], "x > 0 dan y < 0 → kuadran IV.", None, "Kuadran"),
    ("Titik (−3, 6) terletak pada kuadran ...",
     ["II", "I", "III", "IV"], "x < 0 dan y > 0 → kuadran II.", None, "Kuadran"),
    ("Titik berikut yang terletak pada sumbu-y adalah ...",
     ["(0, 6)", "(6, 0)", "(6, 6)", "(−6, 6)"], "Titik pada sumbu-y memiliki absis 0.", None, "Bidang Kartesius"),
    ("Jarak titik (−7, 5) terhadap sumbu-x adalah ...",
     ["5 satuan", "7 satuan", "−7 satuan", "12 satuan"], "Jarak ke sumbu-x = |y| = 5.", None, "Jarak ke Sumbu"),
    ("Jarak titik (8, −1) terhadap sumbu-y adalah ...",
     ["8 satuan", "1 satuan", "−1 satuan", "9 satuan"], "Jarak ke sumbu-y = |x| = 8.", None, "Jarak ke Sumbu"),
    ("Koordinat titik A(−1, 3) terhadap titik acuan B(2, −2) adalah ...",
     ["(−3, 5)", "(1, 1)", "(3, −5)", "(−3, 1)"], "(−1 − 2, 3 − (−2)) = (−3, 5).", None, "Titik Acuan"),
    ("Garis yang melalui (3, −2) dan (3, 4) adalah garis yang ...",
     ["sejajar sumbu-y", "sejajar sumbu-x", "melalui titik asal", "tegak lurus sumbu-y"],
     "Absis kedua titik sama (x = 3), jadi garisnya tegak dan sejajar sumbu-y.", None, "Garis & Sumbu"),
    ("Jarak titik (−4, 1) ke titik (5, 1) adalah ...",
     ["9 satuan", "1 satuan", "6 satuan", "10 satuan"], "Ordinat sama, jarak = |5 − (−4)| = 9.", None, "Jarak & Bangun"),
    ("Dari titik asal bergerak 2 satuan ke kiri lalu 6 satuan ke atas. Titik yang dicapai adalah ...",
     ["(−2, 6)", "(2, −6)", "(6, −2)", "(−6, 2)"], "Kiri → x = −2, atas → y = 6.", None, "Bidang Kartesius"),
    ("Jika titik (5, n) berada di kuadran IV, maka ...",
     ["n < 0", "n > 0", "n = 0", "n = 5"], "Di kuadran IV ordinat negatif, jadi n < 0.", None, "Kuadran"),
    ("Segitiga dengan titik sudut (0, 0), (8, 0), dan (0, 5) memiliki luas ...",
     ["20 satuan luas", "40 satuan luas", "13 satuan luas", "26 satuan luas"], "Luas = ½ × 8 × 5 = 20 satuan luas.", None, "Jarak & Bangun"),
    ("Titik di kuadran II berjarak 4 satuan dari sumbu-x dan 1 satuan dari sumbu-y. Koordinatnya ...",
     ["(−1, 4)", "(−4, 1)", "(1, −4)", "(4, −1)"], "|x| = 1, |y| = 4, kuadran II: x < 0, y > 0 → (−1, 4).", None, "Jarak ke Sumbu"),
    ("Titik Q(−2, 0) digeser 5 satuan ke kanan lalu 3 satuan ke atas. Posisi Q sekarang ...",
     ["(3, 3)", "(−7, 3)", "(3, −3)", "(−7, −3)"], "x = −2 + 5 = 3, y = 0 + 3 = 3.", None, "Titik Acuan"),
]


def _build(raw, prefix):
    items = []
    for i, (text, opts, expl, plot, topic) in enumerate(raw, start=1):
        qid = f"{prefix}{i}"
        correct = opts[0]
        shuffled = list(opts)
        random.Random(qid).shuffle(shuffled)
        items.append({
            "id": qid,
            "no": i,
            "text": text,
            "options": shuffled,
            "answer": shuffled.index(correct),
            "explanation": expl,
            "plot": plot,
            "topic": topic,
        })
    return items


QUIZZES = {
    "latihan": {"title": "Latihan Soal", "items": _build(LATIHAN_RAW, "L"), "xp_per_correct": 5},
    "pretest": {"title": "Pre-test", "items": _build(PRETEST_RAW, "PRE"), "xp_per_correct": 4},
    "posttest": {"title": "Post-test", "items": _build(POSTTEST_RAW, "POST"), "xp_per_correct": 6},
}


def public_items(kind):
    """Soal tanpa kunci jawaban (dikirim ke browser)."""
    return [{k: v for k, v in q.items() if k not in ("answer", "explanation")} for q in QUIZZES[kind]["items"]]


def grade(kind, answers):
    """answers: {qid: index}. Mengembalikan detail penilaian."""
    items = QUIZZES[kind]["items"]
    detail, correct = [], 0
    for q in items:
        given = answers.get(q["id"])
        try:
            given = int(given) if given is not None else None
        except (TypeError, ValueError):
            given = None
        ok = given == q["answer"]
        correct += ok
        detail.append({"id": q["id"], "given": given, "answer": q["answer"], "correct": ok,
                       "explanation": q["explanation"], "topic": q["topic"]})
    total = len(items)
    score = round(100 * correct / total) if total else 0
    return {"correct": correct, "total": total, "score": score, "detail": detail}
