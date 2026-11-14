"""Membangun LYZNART versi statis dan (opsional) mem-publish-nya ke GitHub Pages.

    python tools/build_static.py            # build ke folder _site/
    python tools/build_static.py --deploy   # build + push ke branch gh-pages

Website online:  https://nurainilyzna.github.io/LYZNART-sistemkoordinatkartesius/
Versi statis menyimpan profil & progres siswa di browser (localStorage) melalui static/js/local.js.
"""
import os
import re
import shutil
import sys
import tempfile
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "_site")
REPO_NAME = "LYZNART-sistemkoordinatkartesius"
BASE = "/" + REPO_NAME
REMOTE = f"https://github.com/NurainiLyzna/{REPO_NAME}.git"

os.environ["STATIC_SITE"] = "1"
os.environ["DATABASE_URL"] = ""
os.environ["SQLITE_PATH"] = os.path.join(tempfile.mkdtemp(), "build.db")
sys.path.insert(0, ROOT)

from app import app  # noqa: E402
from content.gamify import GAMES  # noqa: E402

PAGES = ["/", "/materi", "/contoh-soal", "/visualisasi", "/kuis/latihan", "/kuis/pretest", "/kuis/posttest",
         "/game", *[f"/game/{g}" for g in GAMES], "/instal", "/offline", "/daftar", "/masuk", "/dashboard", "/profil"]
FILES = {"/sw.js": "sw.js", "/manifest.webmanifest": "manifest.webmanifest", "/kunci.js": "kunci.js"}


def add_trailing_slashes(html):
    # /BASE/materi → /BASE/materi/  (menghindari redirect GitHub Pages)
    for p in sorted(PAGES, key=len, reverse=True):
        if p == "/":
            continue
        html = re.sub(rf'(href="{re.escape(BASE + p)})(["?#])', r"\1/\2", html)
    return html


def build():
    shutil.rmtree(OUT, ignore_errors=True)
    os.makedirs(OUT)
    client = app.test_client()
    base_url = "https://nurainilyzna.github.io" + BASE
    for p in PAGES:
        r = client.get(p, base_url=base_url)
        assert r.status_code == 200, (p, r.status_code)
        html = add_trailing_slashes(r.get_data(as_text=True))
        target = os.path.join(OUT, "index.html") if p == "/" else os.path.join(OUT, *p.strip("/").split("/"), "index.html")
        os.makedirs(os.path.dirname(target), exist_ok=True)
        with open(target, "w", encoding="utf-8") as f:
            f.write(html)
    r = client.get("/halaman-tidak-ada", base_url=base_url)
    with open(os.path.join(OUT, "404.html"), "w", encoding="utf-8") as f:
        f.write(add_trailing_slashes(r.get_data(as_text=True)))
    for url, name in FILES.items():
        r = client.get(url, base_url=base_url)
        assert r.status_code == 200, (url, r.status_code)
        with open(os.path.join(OUT, name), "wb") as f:
            f.write(r.data)
        r.close()
    shutil.copytree(os.path.join(ROOT, "static"), os.path.join(OUT, "static"),
                    ignore=shutil.ignore_patterns("sw.js", "manifest.webmanifest"))
    open(os.path.join(OUT, ".nojekyll"), "w").close()
    n = sum(len(fs) for _, _, fs in os.walk(OUT))
    print(f"Build selesai: {n} file di {OUT}")


def deploy():
    from dulwich import porcelain
    from dulwich.objects import Blob, Commit, Tree
    from dulwich.repo import Repo

    repo = Repo(ROOT)
    store = repo.object_store

    def tree_of(path):
        t = Tree()
        for name in sorted(os.listdir(path)):
            full = os.path.join(path, name)
            if os.path.isdir(full):
                t.add(name.encode(), 0o040000, tree_of(full))
            else:
                with open(full, "rb") as f:
                    b = Blob.from_string(f.read())
                store.add_object(b)
                t.add(name.encode(), 0o100644, b.id)
        store.add_object(t)
        return t.id

    c = Commit()
    c.tree = tree_of(OUT)
    c.author = c.committer = b"LYZNART Dev <lyznart@users.noreply.github.com>"
    c.author_time = c.commit_time = int(time.time())
    c.author_timezone = c.commit_timezone = 7 * 3600
    c.encoding = b"UTF-8"
    c.message = b"Deploy LYZNART ke GitHub Pages"
    store.add_object(c)
    repo.refs[b"refs/heads/gh-pages"] = c.id

    sys.path.insert(0, os.path.join(ROOT, "tools"))
    from git_sync import get_token
    porcelain.push(repo, REMOTE, refspecs=[b"+refs/heads/gh-pages:refs/heads/gh-pages"],
                   username="x-access-token", password=get_token(), force=True)
    print("Deploy terkirim ke branch gh-pages:")
    print(f"  https://nurainilyzna.github.io{BASE}/")


if __name__ == "__main__":
    build()
    if "--deploy" in sys.argv:
        deploy()
