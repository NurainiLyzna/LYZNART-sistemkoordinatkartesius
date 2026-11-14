"""LYZNART - Explore. Learn. Play. Master!
Media pembelajaran Sistem Koordinat Kartesius untuk siswa kelas VIII SMP/MTs.
"""
import json
import os
import re
from datetime import datetime, timezone
from functools import wraps

from dotenv import load_dotenv

load_dotenv()  # harus sebelum import db agar DATABASE_URL terbaca

from flask import (Flask, abort, flash, g, jsonify, redirect, render_template,  # noqa: E402
                   request, send_from_directory, session, url_for)
from werkzeug.middleware.proxy_fix import ProxyFix  # noqa: E402
from werkzeug.security import check_password_hash, generate_password_hash  # noqa: E402

import db  # noqa: E402
from content.gamify import BADGES, GAMES, LEVELS, MATERI_SECTIONS, game_xp, level_info  # noqa: E402
from content.questions import QUIZZES, grade, public_items  # noqa: E402

APP_VERSION = "1.1.0"
IS_PRODUCTION = os.environ.get("FLASK_ENV") == "production" or bool(os.environ.get("RENDER"))
# STATIC_SITE=1 dipakai tools/build_static.py untuk membuat versi GitHub Pages
# (tanpa server: profil & progres disimpan di browser lewat static/js/local.js)
STATIC_SITE = os.environ.get("STATIC_SITE") == "1"

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)
app.config.update(
    SECRET_KEY=os.environ.get("SECRET_KEY") or "dev-only-ganti-di-production",
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=IS_PRODUCTION,
    PERMANENT_SESSION_LIFETIME=60 * 60 * 24 * 30,
    SEND_FILE_MAX_AGE_DEFAULT=60 * 60 * 24 if IS_PRODUCTION else 0,
)
if IS_PRODUCTION and not os.environ.get("SECRET_KEY"):
    raise RuntimeError("SECRET_KEY wajib diisi di environment production.")

app.teardown_appcontext(db.close_db)
db.init_db()


def now_iso():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


# ---------------------------------------------------------------- helpers
def current_user():
    if STATIC_SITE:
        return None
    if "user" not in g:
        uid = session.get("uid")
        g.user = db.query("SELECT * FROM users WHERE id = ?", (uid,), one=True) if uid else None
    return g.user


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if STATIC_SITE:
            return view(*args, **kwargs)
        if not current_user():
            if request.path.startswith("/api/"):
                return jsonify({"error": "Silakan masuk terlebih dahulu."}), 401
            flash("Masuk dulu yuk, supaya progresmu tersimpan!", "info")
            return redirect(url_for("login", next=request.path))
        return view(*args, **kwargs)
    return wrapped


def award_badge(uid, code):
    """Memberi badge bila belum dimiliki. Mengembalikan data badge baru atau None."""
    if db.query("SELECT 1 AS x FROM badges WHERE user_id = ? AND code = ?", (uid, code), one=True):
        return None
    db.execute("INSERT INTO badges (user_id, code, earned_at) VALUES (?, ?, ?) ON CONFLICT DO NOTHING",
               (uid, code, now_iso()))
    return {"code": code, **BADGES[code]}


def add_xp(uid, amount):
    if amount > 0:
        db.execute("UPDATE users SET xp = xp + ? WHERE id = ?", (amount, uid))
    return db.query("SELECT xp FROM users WHERE id = ?", (uid,), one=True)["xp"]


def check_xp_badges(uid, xp):
    new = []
    if xp >= 500:
        new.append(award_badge(uid, "xp500"))
    if level_info(xp)["level"] >= 6:
        new.append(award_badge(uid, "master"))
    return [b for b in new if b]


def best_result(uid, kind):
    return db.query("SELECT MAX(correct) AS best FROM results WHERE user_id = ? AND kind = ?",
                    (uid, kind), one=True)["best"]


def latest_result(uid, kind):
    return db.query("SELECT * FROM results WHERE user_id = ? AND kind = ? ORDER BY id DESC LIMIT 1",
                    (uid, kind), one=True)


@app.context_processor
def inject_globals():
    user = current_user()
    return {
        "user": user,
        "lvl": level_info(user["xp"]) if user else None,
        "app_version": APP_VERSION,
        "GAMES": GAMES,
        "static_site": STATIC_SITE,
        "base": request.script_root,
    }


@app.route("/kunci.js")
def static_keys():
    """Data untuk versi statis (GitHub Pages): kunci jawaban, badge, level, game."""
    if not STATIC_SITE:
        abort(404)
    data = {
        "quizzes": {k: {"rate": v["xp_per_correct"],
                        "items": [{"id": q["id"], "answer": q["answer"], "explanation": q["explanation"],
                                   "topic": q["topic"]} for q in v["items"]]} for k, v in QUIZZES.items()},
        "badges": BADGES, "levels": LEVELS, "games": GAMES, "materi": MATERI_SECTIONS,
    }
    body = "window.LYZ_DATA = " + json.dumps(data, ensure_ascii=False) + ";"
    return app.response_class(body, mimetype="application/javascript")


# ---------------------------------------------------------------- pages
@app.route("/")
def index():
    return render_template("index.html", games=GAMES, quizzes=QUIZZES)


@app.route("/daftar", methods=["GET", "POST"])
def register():
    if STATIC_SITE:
        return render_template("local_auth.html")
    if current_user():
        return redirect(url_for("dashboard"))
    form = {}
    if request.method == "POST":
        form = {k: request.form.get(k, "").strip() for k in ("name", "username", "kelas", "sekolah", "avatar")}
        password = request.form.get("password", "")
        username = form["username"].lower()
        error = None
        if not (2 <= len(form["name"]) <= 60):
            error = "Nama lengkap harus 2–60 karakter."
        elif not re.fullmatch(r"[a-z0-9_.]{3,20}", username):
            error = "Username 3–20 karakter: huruf kecil, angka, titik, atau garis bawah."
        elif len(password) < 6:
            error = "Kata sandi minimal 6 karakter."
        elif db.query("SELECT id FROM users WHERE username = ?", (username,), one=True):
            error = "Username sudah dipakai, coba yang lain ya."
        if error:
            flash(error, "error")
        else:
            avatar = form["avatar"] if form["avatar"] in ("robot", "astronot", "kucing", "burung") else "robot"
            db.execute(
                "INSERT INTO users (username, name, kelas, sekolah, avatar, password_hash, xp, created_at)"
                " VALUES (?, ?, ?, ?, ?, ?, 0, ?)",
                (username, form["name"], form["kelas"][:20], form["sekolah"][:80], avatar,
                 generate_password_hash(password), now_iso()))
            user = db.query("SELECT id FROM users WHERE username = ?", (username,), one=True)
            session.clear()
            session.permanent = True
            session["uid"] = user["id"]
            award_badge(user["id"], "welcome")
            add_xp(user["id"], 10)
            flash("Selamat datang di LYZNART! Kamu dapat badge Langkah Pertama 🚀 dan +10 XP.", "success")
            return redirect(url_for("dashboard"))
    return render_template("auth.html", mode="register", form=form)


@app.route("/masuk", methods=["GET", "POST"])
def login():
    if STATIC_SITE:
        return render_template("local_auth.html")
    if current_user():
        return redirect(url_for("dashboard"))
    form = {}
    if request.method == "POST":
        username = request.form.get("username", "").strip().lower()
        form = {"username": username}
        user = db.query("SELECT * FROM users WHERE username = ?", (username,), one=True)
        if user and check_password_hash(user["password_hash"], request.form.get("password", "")):
            session.clear()
            session.permanent = True
            session["uid"] = user["id"]
            nxt = request.args.get("next", "")
            return redirect(nxt if nxt.startswith("/") and not nxt.startswith("//") else url_for("dashboard"))
        flash("Username atau kata sandi salah.", "error")
    return render_template("auth.html", mode="login", form=form)


@app.route("/keluar")
def logout():
    session.clear()
    flash("Sampai jumpa lagi! 👋", "info")
    return redirect(url_for("index"))


@app.route("/dashboard")
@login_required
def dashboard():
    if STATIC_SITE:
        return render_template("local_dashboard.html")
    uid = current_user()["id"]
    done = {r["item"] for r in db.query("SELECT item FROM progress WHERE user_id = ?", (uid,))}
    played = {r["kind"][5:] for r in db.query(
        "SELECT DISTINCT kind FROM results WHERE user_id = ? AND kind LIKE 'game:%'", (uid,))}
    status = {k: latest_result(uid, k) for k in QUIZZES}
    badges = db.query("SELECT code FROM badges WHERE user_id = ?", (uid,))
    leaders = db.query("SELECT name, kelas, xp, avatar FROM users ORDER BY xp DESC, id ASC LIMIT 5")
    steps = [
        ("Pre-test", url_for("quiz", kind="pretest"), bool(status["pretest"])),
        ("Pelajari materi", url_for("materi"), len(done & set(MATERI_SECTIONS)) == len(MATERI_SECTIONS)),
        ("Contoh soal", url_for("contoh"), "contoh" in done),
        ("Visualisasi", url_for("visualisasi"), "visual" in done),
        ("Latihan 40 soal", url_for("quiz", kind="latihan"), bool(status["latihan"])),
        ("Main game", url_for("games"), len(played) > 0),
        ("Post-test", url_for("quiz", kind="posttest"), bool(status["posttest"])),
    ]
    return render_template("dashboard.html", steps=steps, status=status, done=done, played=played,
                           badge_count=len(badges), leaders=leaders, total_badges=len(BADGES))


@app.route("/materi")
def materi():
    done = set()
    if current_user():
        done = {r["item"] for r in db.query("SELECT item FROM progress WHERE user_id = ?", (current_user()["id"],))}
    return render_template("materi.html", done=done)


@app.route("/contoh-soal")
def contoh():
    return render_template("contoh.html")


@app.route("/visualisasi")
def visualisasi():
    return render_template("visualisasi.html")


@app.route("/kuis/<kind>")
def quiz(kind):
    if kind not in QUIZZES:
        abort(404)
    meta = QUIZZES[kind]
    return render_template("quiz.html", kind=kind, title=meta["title"], items=public_items(kind),
                           xp_rate=meta["xp_per_correct"])


@app.route("/game")
def games():
    return render_template("games.html", games=GAMES)


@app.route("/game/<gid>")
def game(gid):
    if gid not in GAMES:
        abort(404)
    best = None
    if current_user():
        best = db.query("SELECT MAX(score) AS best FROM results WHERE user_id = ? AND kind = ?",
                        (current_user()["id"], f"game:{gid}"), one=True)["best"]
    return render_template("game.html", gid=gid, game=GAMES[gid], best=best)


@app.route("/profil", methods=["GET", "POST"])
@login_required
def profil():
    if STATIC_SITE:
        return render_template("local_profil.html", badges=BADGES, levels=LEVELS)
    user = current_user()
    uid = user["id"]
    if request.method == "POST":
        name = request.form.get("name", "").strip()[:60]
        kelas = request.form.get("kelas", "").strip()[:20]
        sekolah = request.form.get("sekolah", "").strip()[:80]
        avatar = request.form.get("avatar", "robot")
        if avatar not in ("robot", "astronot", "kucing", "burung"):
            avatar = "robot"
        if len(name) < 2:
            flash("Nama minimal 2 karakter.", "error")
        else:
            db.execute("UPDATE users SET name = ?, kelas = ?, sekolah = ?, avatar = ? WHERE id = ?",
                       (name, kelas, sekolah, avatar, uid))
            flash("Profil berhasil diperbarui ✨", "success")
        return redirect(url_for("profil"))
    owned = {r["code"]: r["earned_at"] for r in db.query("SELECT code, earned_at FROM badges WHERE user_id = ?", (uid,))}
    history = db.query("SELECT kind, score, correct, total, xp_gained, created_at FROM results"
                       " WHERE user_id = ? ORDER BY id DESC LIMIT 15", (uid,))
    return render_template("profil.html", badges=BADGES, owned=owned, history=history, levels=LEVELS,
                           game_names={f"game:{k}": v["name"] for k, v in GAMES.items()},
                           quiz_names={k: v["title"] for k, v in QUIZZES.items()})


@app.route("/instal")
def install():
    return render_template("install.html")


@app.route("/offline")
def offline():
    return render_template("offline.html")


# ---------------------------------------------------------------- API
def _json():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        abort(400)
    return data


@app.post("/api/quiz/<kind>")
def api_quiz(kind):
    if kind not in QUIZZES:
        abort(404)
    answers = _json().get("answers", {})
    if not isinstance(answers, dict):
        abort(400)
    result = grade(kind, answers)
    response = {**result, "xp_gained": 0, "new_badges": [], "saved": False}
    user = current_user()
    if user:
        uid = user["id"]
        prev_best = best_result(uid, kind) or 0
        # XP hanya untuk soal benar yang melampaui rekor sebelumnya (mencegah farming)
        xp = max(0, result["correct"] - prev_best) * QUIZZES[kind]["xp_per_correct"]
        db.execute("INSERT INTO results (user_id, kind, score, correct, total, xp_gained, created_at)"
                   " VALUES (?, ?, ?, ?, ?, ?, ?)",
                   (uid, kind, result["score"], result["correct"], result["total"], xp, now_iso()))
        total_xp = add_xp(uid, xp)
        new = []
        if kind == "pretest":
            new.append(award_badge(uid, "pretest"))
        if kind == "posttest":
            if result["score"] >= 75:
                new.append(award_badge(uid, "posttest"))
            pre = db.query("SELECT MAX(score) AS s FROM results WHERE user_id = ? AND kind = 'pretest'",
                           (uid,), one=True)["s"]
            if pre is not None and result["score"] > pre:
                new.append(award_badge(uid, "improve"))
        if kind == "latihan" and result["score"] >= 80:
            new.append(award_badge(uid, "practice"))
        if result["score"] == 100:
            new.append(award_badge(uid, "perfect"))
        new += check_xp_badges(uid, total_xp)
        response.update(xp_gained=xp, new_badges=[b for b in new if b], saved=True,
                        level=level_info(total_xp))
    return jsonify(response)


@app.post("/api/game/<gid>")
def api_game(gid):
    if gid not in GAMES:
        abort(404)
    try:
        score = max(0, min(2000, int(_json().get("score", 0))))
    except (TypeError, ValueError):
        abort(400)
    user = current_user()
    if not user:
        return jsonify({"saved": False, "xp_gained": 0, "new_badges": []})
    uid = user["id"]
    xp = game_xp(score)
    db.execute("INSERT INTO results (user_id, kind, score, correct, total, xp_gained, created_at)"
               " VALUES (?, ?, ?, 0, 0, ?, ?)", (uid, f"game:{gid}", score, xp, now_iso()))
    total_xp = add_xp(uid, xp)
    played = db.query("SELECT COUNT(DISTINCT kind) AS n FROM results WHERE user_id = ? AND kind LIKE 'game:%'",
                      (uid,), one=True)["n"]
    new = []
    if played >= len(GAMES):
        new.append(award_badge(uid, "gamer"))
    new += check_xp_badges(uid, total_xp)
    return jsonify({"saved": True, "xp_gained": xp, "new_badges": [b for b in new if b],
                    "level": level_info(total_xp)})


@app.post("/api/progress")
@login_required
def api_progress():
    item = str(_json().get("item", ""))
    if item not in MATERI_SECTIONS + ["contoh", "visual"]:
        abort(400)
    uid = current_user()["id"]
    exists = db.query("SELECT 1 AS x FROM progress WHERE user_id = ? AND item = ?", (uid, item), one=True)
    xp, new = 0, []
    if not exists:
        db.execute("INSERT INTO progress (user_id, item, done_at) VALUES (?, ?, ?) ON CONFLICT DO NOTHING",
                   (uid, item, now_iso()))
        xp = 15 if item in MATERI_SECTIONS else 10
        done = {r["item"] for r in db.query("SELECT item FROM progress WHERE user_id = ?", (uid,))}
        if set(MATERI_SECTIONS) <= done:
            new.append(award_badge(uid, "reader"))
        if item == "visual":
            new.append(award_badge(uid, "explorer"))
    total_xp = add_xp(uid, xp)
    new += check_xp_badges(uid, total_xp)
    return jsonify({"saved": True, "xp_gained": xp, "new_badges": [b for b in new if b],
                    "level": level_info(total_xp)})


@app.get("/api/stats")
@login_required
def api_stats():
    uid = current_user()["id"]
    rows = db.query("SELECT kind, score, created_at FROM results WHERE user_id = ? ORDER BY id ASC", (uid,))
    pre = [r for r in rows if r["kind"] == "pretest"]
    post = [r for r in rows if r["kind"] == "posttest"]
    latihan = [r for r in rows if r["kind"] == "latihan"]
    games_best = {}
    for r in rows:
        if r["kind"].startswith("game:"):
            key = r["kind"][5:]
            games_best[key] = max(games_best.get(key, 0), r["score"])
    return jsonify({
        "pre": pre[-1]["score"] if pre else None,
        "post": post[-1]["score"] if post else None,
        "latihan": [{"score": r["score"], "date": r["created_at"][:10]} for r in latihan[-10:]],
        "games": [{"name": GAMES[k]["name"], "score": games_best.get(k)} for k in GAMES],
    })


@app.get("/healthz")
def healthz():
    db.query("SELECT 1 AS ok", one=True)
    return jsonify({"status": "ok", "db": db.backend_name(), "version": APP_VERSION})


# ---------------------------------------------------------------- PWA
@app.route("/sw.js")
def service_worker():
    resp = send_from_directory(app.static_folder, "sw.js", mimetype="application/javascript")
    resp.headers["Cache-Control"] = "no-cache"
    resp.headers["Service-Worker-Allowed"] = "/"
    return resp


@app.route("/manifest.webmanifest")
def manifest():
    with open(os.path.join(app.static_folder, "manifest.webmanifest"), encoding="utf-8") as fh:
        body = fh.read()
    if request.script_root:  # mis. GitHub Pages: /LYZNART-sistemkoordinatkartesius
        body = body.replace('"/', '"' + request.script_root + '/')
    resp = app.response_class(body, mimetype="application/manifest+json")
    resp.headers["Cache-Control"] = "no-cache"
    return resp


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(os.path.join(app.static_folder, "icons"), "icon-192.png", mimetype="image/png")


@app.errorhandler(404)
def not_found(_e):
    if request.path.startswith("/api/"):
        return jsonify({"error": "Tidak ditemukan"}), 404
    return render_template("error.html", code=404, message="Halaman tidak ditemukan. Mungkin titiknya di luar bidang? 😅"), 404


@app.errorhandler(500)
def server_error(_e):
    return render_template("error.html", code=500, message="Ups, terjadi kesalahan di server. Coba lagi sebentar ya."), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="127.0.0.1", port=port, debug=os.environ.get("FLASK_DEBUG") == "1")
