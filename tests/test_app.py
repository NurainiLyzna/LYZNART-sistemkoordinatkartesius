"""Pengujian otomatis LYZNART.  Jalankan:  python -m unittest discover -s tests -v"""
import json
import os
import sys
import tempfile
import unittest

TMP = tempfile.mkdtemp()
os.environ["SQLITE_PATH"] = os.path.join(TMP, "test.db")
os.environ["DATABASE_URL"] = ""
os.environ.pop("RENDER", None)
os.environ["FLASK_ENV"] = "testing"
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app  # noqa: E402
from content.questions import QUIZZES  # noqa: E402
from content.gamify import level_info  # noqa: E402


class LyznartTest(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.c = app.test_client()

    def register(self, username="siswa1", password="rahasia1"):
        return self.c.post("/daftar", data={"name": "Siswa Uji", "username": username, "kelas": "VIII A",
                                            "sekolah": "SMP Uji", "avatar": "kucing", "password": password},
                           follow_redirects=True)

    def post_json(self, url, data):
        return self.c.post(url, data=json.dumps(data), content_type="application/json")

    # ------------------------------------------------------------ konten
    def test_question_counts(self):
        self.assertGreaterEqual(len(QUIZZES["latihan"]["items"]), 40)
        self.assertGreaterEqual(len(QUIZZES["pretest"]["items"]), 15)
        self.assertGreaterEqual(len(QUIZZES["posttest"]["items"]), 15)
        for kind, meta in QUIZZES.items():
            for q in meta["items"]:
                self.assertEqual(len(q["options"]), 4, q["id"])
                self.assertEqual(len(set(q["options"])), 4, f"opsi ganda di {q['id']}")
                self.assertTrue(0 <= q["answer"] < 4)

    def test_level_info(self):
        self.assertEqual(level_info(0)["level"], 1)
        self.assertEqual(level_info(100)["level"], 2)
        self.assertEqual(level_info(5000)["pct"], 100)

    # ------------------------------------------------------------ halaman publik
    def test_public_pages(self):
        for url in ["/", "/materi", "/contoh-soal", "/visualisasi", "/kuis/latihan", "/kuis/pretest",
                    "/kuis/posttest", "/game", "/game/titik", "/game/kuadran", "/game/robot", "/game/kapal",
                    "/instal", "/offline", "/masuk", "/daftar", "/healthz"]:
            r = self.c.get(url)
            self.assertEqual(r.status_code, 200, url)

    def test_quiz_pages_hide_answers(self):
        html = self.c.get("/kuis/latihan").get_data(as_text=True)
        self.assertNotIn("Pembahasan", html.split("quizForm")[1].split("resultDialog")[0][:200])
        self.assertEqual(html.count('class="card question"'), 40)
        self.assertNotIn(QUIZZES["latihan"]["items"][0]["explanation"], html)

    def test_pwa_files(self):
        r = self.c.get("/manifest.webmanifest")
        self.assertEqual(r.status_code, 200)
        m = json.loads(r.data)
        r.close()
        self.assertEqual(m["short_name"], "LYZNART")
        self.assertTrue(any(i["sizes"] == "512x512" for i in m["icons"]))
        r = self.c.get("/sw.js")
        self.assertEqual(r.status_code, 200)
        self.assertIn("javascript", r.content_type)
        r.close()
        for icon in ["icon-192.png", "icon-512.png", "icon-maskable-512.png", "apple-touch-icon.png"]:
            r = self.c.get(f"/static/icons/{icon}")
            self.assertEqual(r.status_code, 200, icon)
            r.close()

    def test_404(self):
        self.assertEqual(self.c.get("/tidak-ada").status_code, 404)
        self.assertEqual(self.c.get("/kuis/xyz").status_code, 404)
        self.assertEqual(self.c.get("/game/xyz").status_code, 404)

    def test_protected_redirect(self):
        r = self.c.get("/dashboard")
        self.assertEqual(r.status_code, 302)
        self.assertIn("/masuk", r.headers["Location"])
        self.assertEqual(self.c.get("/api/stats").status_code, 401)

    # ------------------------------------------------------------ alur siswa
    def test_full_student_flow(self):
        r = self.register("alur1")
        self.assertIn("Hai, Siswa!", r.get_data(as_text=True))
        # pre-test: semua salah
        pre = QUIZZES["pretest"]["items"]
        wrong = {q["id"]: (q["answer"] + 1) % 4 for q in pre}
        d = self.post_json("/api/quiz/pretest", {"answers": wrong}).get_json()
        self.assertEqual(d["score"], 0)
        self.assertTrue(d["saved"])
        self.assertIn("pretest", [b["code"] for b in d["new_badges"]])
        # post-test: semua benar
        post = QUIZZES["posttest"]["items"]
        right = {q["id"]: q["answer"] for q in post}
        d = self.post_json("/api/quiz/posttest", {"answers": right}).get_json()
        self.assertEqual(d["score"], 100)
        self.assertEqual(d["xp_gained"], 15 * QUIZZES["posttest"]["xp_per_correct"])
        codes = [b["code"] for b in d["new_badges"]]
        for c in ("posttest", "improve", "perfect"):
            self.assertIn(c, codes)
        # mengulang tidak menambah XP (anti farming)
        d = self.post_json("/api/quiz/posttest", {"answers": right}).get_json()
        self.assertEqual(d["xp_gained"], 0)
        # latihan sebagian
        lat = QUIZZES["latihan"]["items"]
        ans = {q["id"]: q["answer"] for q in lat[:32]}
        d = self.post_json("/api/quiz/latihan", {"answers": ans}).get_json()
        self.assertEqual(d["correct"], 32)
        self.assertEqual(d["score"], 80)
        self.assertIn("practice", [b["code"] for b in d["new_badges"]])
        # progres materi
        for item in ["m1", "m2", "m3", "m4", "m5", "m6"]:
            d = self.post_json("/api/progress", {"item": item}).get_json()
        self.assertIn("reader", [b["code"] for b in d["new_badges"]])
        d = self.post_json("/api/progress", {"item": "m1"}).get_json()
        self.assertEqual(d["xp_gained"], 0)
        self.assertEqual(self.post_json("/api/progress", {"item": "hack"}).status_code, 400)
        # game
        for g in ["titik", "kuadran", "robot"]:
            self.post_json(f"/api/game/{g}", {"score": 120})
        d = self.post_json("/api/game/kapal", {"score": 99999}).get_json()
        self.assertEqual(d["xp_gained"], 40)  # dibatasi
        self.assertIn("gamer", [b["code"] for b in d["new_badges"]])
        self.assertEqual(self.post_json("/api/game/kapal", {"score": "abc"}).status_code, 400)
        # statistik
        s = self.c.get("/api/stats").get_json()
        self.assertEqual(s["pre"], 0)
        self.assertEqual(s["post"], 100)
        self.assertEqual(len(s["latihan"]), 1)
        self.assertEqual(len(s["games"]), 4)
        # halaman pribadi
        for url in ["/dashboard", "/profil"]:
            self.assertEqual(self.c.get(url).status_code, 200, url)
        html = self.c.get("/profil").get_data(as_text=True)
        self.assertIn("Sempurna!", html)
        # edit profil
        r = self.c.post("/profil", data={"name": "Nama Baru", "kelas": "VIII B", "sekolah": "MTs", "avatar": "robot"},
                        follow_redirects=True)
        self.assertIn("Nama Baru", r.get_data(as_text=True))

    def test_login_logout(self):
        self.register("masuk1", "sandi123")
        self.c.get("/keluar")
        self.assertEqual(self.c.get("/dashboard").status_code, 302)
        r = self.c.post("/masuk", data={"username": "masuk1", "password": "salah"}, follow_redirects=True)
        self.assertIn("salah", r.get_data(as_text=True))
        r = self.c.post("/masuk?next=/profil", data={"username": "MASUK1", "password": "sandi123"})
        self.assertEqual(r.headers["Location"], "/profil")
        r = self.c.post("/masuk?next=//evil.com", data={"username": "masuk1", "password": "sandi123"})
        self.assertNotIn("evil", r.headers.get("Location", ""))

    def test_register_validation(self):
        r = self.c.post("/daftar", data={"name": "A", "username": "x", "password": "1"}, follow_redirects=True)
        self.assertIn("Nama lengkap harus", r.get_data(as_text=True))
        self.register("dup1")
        self.c.get("/keluar")
        r = self.register("dup1")
        self.assertIn("sudah dipakai", r.get_data(as_text=True))

    def test_guest_quiz_not_saved(self):
        d = self.post_json("/api/quiz/latihan", {"answers": {}}).get_json()
        self.assertFalse(d["saved"])
        self.assertEqual(d["score"], 0)
        self.assertEqual(self.post_json("/api/quiz/latihan", {"answers": []}).status_code, 400)


if __name__ == "__main__":
    unittest.main()
