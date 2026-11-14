# LYZNART · Explore. Learn. Play. Master!

**LYZNART** adalah website pembelajaran interaktif untuk materi **Sistem Koordinat Kartesius**, ditujukan bagi siswa **kelas VIII SMP/MTs**. Dibangun dengan **Python Flask, HTML, CSS, dan JavaScript**, serta bisa dipasang sebagai aplikasi (PWA). Website ini tetap bisa dipakai langsung lewat browser tanpa instalasi.

## ✨ Fitur

| Fitur | Keterangan |
|---|---|
| 🏠 Landing page & dashboard siswa | Peta belajar, ringkasan nilai, papan peringkat XP |
| 📘 Materi lengkap | 6 bagian materi + tujuan pembelajaran + rangkuman |
| 💡 Contoh soal | 8 contoh soal dengan pembahasan langkah demi langkah |
| 🧭 Visualisasi interaktif | Mode titik, titik acuan, jarak dua titik, dan tantangan |
| ✏️ Latihan | 40 soal pilihan ganda (6 topik) dengan pembahasan |
| 📝 Pre-test & 🎓 post-test | Masing-masing 15 soal paralel |
| 🎮 4 game edukasi | Tembak Titik, Kuadran Kilat, Robot Harta Karun, Kapal Koordinat |
| ✅ Penilaian otomatis | Kunci jawaban hanya disimpan di server |
| 👤 Profil & progres | Ubah profil, avatar, riwayat aktivitas |
| 📊 Grafik hasil belajar | Pre vs post-test, riwayat latihan, skor game |
| ⭐ XP, level & badge | 7 level, 11 badge, XP anti-farming |
| 📲 PWA | Manifest, service worker, ikon, tombol **Install LYZNART**, halaman offline |

## 🗂️ Struktur Proyek

```
LYZNART/
├── app.py                 # Aplikasi Flask (rute, API, PWA)
├── db.py                  # Database: SQLite (lokal) / PostgreSQL (online)
├── content/
│   ├── questions.py       # Bank soal latihan, pre-test, post-test
│   └── gamify.py          # XP, level, badge, daftar game
├── templates/             # Halaman HTML (Jinja2)
├── static/
│   ├── css/style.css
│   ├── js/                # main, plane, visualisasi, quiz, games, charts, hero
│   ├── icons/             # Ikon PWA
│   ├── manifest.webmanifest
│   └── sw.js              # Service worker
├── tests/test_app.py      # Pengujian otomatis
├── tools/
│   ├── make_icons.py      # Pembuat ikon PWA
│   └── git_sync.py        # Commit & push tanpa git.exe (dulwich)
├── render.yaml            # Blueprint deployment Render
├── gunicorn.conf.py, Procfile, .python-version
├── requirements.txt, requirements-dev.txt
└── .env.example, .gitignore
```

## 💻 Menjalankan di VS Code (lokal)

1. **Buka folder** `LYZNART` di VS Code.
2. **Buat virtual environment** (sekali saja). Buka Terminal (`Ctrl + ` `):
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements-dev.txt
   ```
   > Jika muncul error *running scripts is disabled*, jalankan dulu: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`
3. **Pilih interpreter**: `Ctrl+Shift+P` → *Python: Select Interpreter* → pilih `.venv`. File `.vscode/settings.json` sudah mengaturnya otomatis.
4. **(Opsional)** salin `.env.example` menjadi `.env`.
5. **Jalankan**:
   ```powershell
   python app.py
   ```
   atau tekan **F5** (konfigurasi *LYZNART (Flask)*). Buka **http://127.0.0.1:5000**.

Secara lokal data tersimpan di `instance/lyznart.db` (SQLite) dan **tidak hilang** saat server dimatikan.

### Pengujian otomatis
```powershell
python -m unittest discover -s tests -v
```

## 🌐 Deployment Online (Render, satu klik)

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/NurainiLyzna/LYZNART-sistemkoordinatkartesius)

Render menjalankan Flask dengan Gunicorn dan HTTPS otomatis. File `render.yaml` sekaligus membuat **database PostgreSQL Render** (`lyznart-db`), sehingga akun dan progres siswa **tidak hilang saat aplikasi restart atau di-deploy ulang**. Tidak ada isian manual.

1. Klik tombol **Deploy to Render** di atas, lalu login dengan akun GitHub.
2. Izinkan Render mengakses repository `LYZNART-sistemkoordinatkartesius`.
3. Klik **Apply**. Tunggu ±5 menit sampai status **Live**.
4. Website aktif di `https://lyznart.onrender.com` (atau nama lain yang diberikan Render).
5. Cek kesehatan: `https://<nama>.onrender.com/healthz` harus menampilkan `"db": "PostgreSQL"`.

> **Catatan paket gratis Render:** web service "tidur" setelah ±15 menit tanpa pengunjung (akses pertama ±30–60 detik), dan database gratis berlaku **30 hari**. Agar data permanen, upgrade database ke paket berbayar di Render, atau ganti `DATABASE_URL` dengan PostgreSQL gratis permanen seperti Neon (https://neon.tech).

### Memperbarui website
`autoDeploy: true` sudah aktif. Setiap push ke branch `main` akan otomatis di-deploy ulang oleh Render.

```powershell
# dengan git biasa
git add . ; git commit -m "Perbarui materi" ; git push

# jika git.exe diblokir Windows (Application Control)
python tools/git_sync.py "Perbarui materi"
```

## 🔐 Environment Variables

| Variabel | Fungsi |
|---|---|
| `SECRET_KEY` | Kunci sesi login (wajib di production) |
| `DATABASE_URL` | URL PostgreSQL; kosong = SQLite lokal |
| `FLASK_ENV` | `production` di server |
| `PORT` | Port server (diatur otomatis oleh Render) |

## 📐 Cakupan Materi

1. Bidang Kartesius: sumbu-x, sumbu-y, titik asal, absis, ordinat
2. Kuadran I–IV dan titik pada sumbu
3. Posisi titik terhadap sumbu-x dan sumbu-y (|y| dan |x|)
4. Posisi titik terhadap titik asal dan titik acuan (x − p, y − q), pergeseran titik
5. Garis sejajar, tegak lurus, dan memotong sumbu
6. Jarak dua titik (mendatar, tegak, Pythagoras) dan bangun datar pada bidang koordinat

---
© 2026 LYZNART · Explore. Learn. Play. Master!
