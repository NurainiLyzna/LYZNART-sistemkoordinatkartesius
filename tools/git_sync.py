"""Commit & push LYZNART ke GitHub tanpa git.exe (memakai dulwich, Git berbasis Python murni).

Berguna bila Windows memblokir git.exe ("An Application Control policy has blocked this file").

Pemakaian (dari folder proyek, dengan .venv aktif):
    python tools/git_sync.py "pesan commit"

Token GitHub (Personal Access Token, izin "Contents: Read and write") dibaca dari:
    1. variabel lingkungan GITHUB_TOKEN, atau
    2. file .github_token di folder proyek (sudah di-.gitignore), atau
    3. ditanyakan saat dijalankan (tidak ditampilkan di layar).
"""
import getpass
import os
import sys

from dulwich import porcelain
from dulwich.repo import Repo

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REMOTE = "https://github.com/NurainiLyzna/LYZNART-sistemkoordinatkartesius.git"
BRANCH = b"main"
AUTHOR = os.environ.get("GIT_AUTHOR", "LYZNART Dev <lyznart@users.noreply.github.com>").encode()


def get_token():
    tok = os.environ.get("GITHUB_TOKEN", "").strip()
    path = os.path.join(ROOT, ".github_token")
    if not tok and os.path.exists(path):
        tok = open(path, encoding="utf-8").read().strip()
    if not tok:
        tok = getpass.getpass("Tempel GitHub token (tidak terlihat): ").strip()
    return tok


def main():
    msg = sys.argv[1] if len(sys.argv) > 1 else "Update LYZNART"
    if not os.path.isdir(os.path.join(ROOT, ".git")):
        repo = porcelain.init(ROOT)
        repo.refs.set_symbolic_ref(b"HEAD", b"refs/heads/main")
        print("Repository Git baru dibuat.")
    repo = Repo(ROOT)
    cfg = repo.get_config()
    cfg.set((b"remote", b"origin"), b"url", REMOTE.encode())
    cfg.set((b"remote", b"origin"), b"fetch", b"+refs/heads/*:refs/remotes/origin/*")
    cfg.write_to_path()

    porcelain.add(repo)  # menghormati .gitignore
    st = porcelain.status(repo)
    staged = sum(len(v) for v in st.staged.values())
    if staged:
        porcelain.commit(repo, message=msg.encode(), author=AUTHOR, committer=AUTHOR)
        print(f"Commit dibuat: {msg} ({staged} perubahan)")
    else:
        print("Tidak ada perubahan baru untuk di-commit.")

    if "--no-push" in sys.argv:
        return
    token = get_token()
    porcelain.push(repo, REMOTE, refspecs=[b"refs/heads/main:refs/heads/main"],
                   username="x-access-token", password=token)
    print("Berhasil push ke", REMOTE)


if __name__ == "__main__":
    main()
