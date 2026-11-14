/* LYZNART - 4 game edukasi koordinat */
(function () {
  "use strict";
  const shell = document.getElementById("gameShell");
  if (!shell) return;
  const gid = shell.dataset.game;
  const { quadrantOf, fmt } = window.PlaneUtil;
  const canvas = document.getElementById("gCanvas");
  const overlay = document.getElementById("gOverlay");
  const rulesEl = document.getElementById("gRules");
  const startBtn = document.getElementById("gStart");
  const scoreEl = document.getElementById("gScore");
  const midEl = document.getElementById("gHudMid");
  const rightEl = document.getElementById("gHudRight");
  const controls = document.getElementById("gControls");
  const msgEl = document.getElementById("gMsg");

  const I = (n) => window.LYZ.icon(n);
  const rnd = (a, b) => a + Math.floor(Math.random() * (b - a + 1));
  let score = 0;
  let timers = [];
  function setScore(v) { score = Math.max(0, v); scoreEl.textContent = score; }
  function msg(text, cls) { msgEl.innerHTML = text; msgEl.className = "game-msg " + (cls || ""); }
  function clearTimers() { timers.forEach(clearInterval); timers.forEach(clearTimeout); timers = []; }

  async function finish(summary) {
    clearTimers();
    overlay.hidden = false;
    rulesEl.innerHTML = `<p style="font-size:1.3rem"><b>Permainan selesai!</b></p><p>${summary}</p><p style="font-size:2rem;font-family:'Baloo 2'"><b>${I("star")} ${score}</b></p><p id="gSave" class="muted">Menyimpan skor...</p>`;
    overlay.querySelector("h2").innerHTML = score >= 100 ? "Luar biasa! " + I("trophy") : score >= 50 ? "Hebat! " + I("sparkle") : "Ayo coba lagi! " + I("heart");
    startBtn.innerHTML = I("refresh") + " Main Lagi";
    const save = document.getElementById("gSave");
    try {
      const r = await window.LYZ.api("/api/game/" + gid, { score });
      if (r.saved) {
        save.textContent = `Skor tersimpan · +${r.xp_gained} XP`;
        window.LYZ.showRewards(r);
      } else save.textContent = "Masuk untuk menyimpan skor dan mendapatkan XP.";
    } catch (e) { save.textContent = "Skor tidak tersimpan (offline)."; }
  }

  // =====================================================================
  // 1. TEMBAK TITIK
  // =====================================================================
  const titik = {
    rules: `<ul><li>Muncul perintah koordinat, misalnya <b>(3, −2)</b>.</li><li>Ketuk titik potong garis yang tepat pada bidang.</li><li>Benar: <b>+10</b>, plus bonus beruntun. Waktu: <b>60 detik</b>.</li></ul>`,
    start() {
      const plane = new Plane(canvas, { range: 8, shade: false });
      let target, time = 60, streak = 0, marks = [], hits = 0, tries = 0;
      const next = () => { do { target = { x: rnd(-7, 7), y: rnd(-7, 7) }; } while (target.x === 0 && target.y === 0); };
      const draw = () => {
        plane.draw();
        marks.forEach((m) => plane.point(m.x, m.y, { color: m.ok ? "#059669" : "#dc2626", r: 7 }));
        midEl.innerHTML = `${I("target")} Ketuk <b>(${fmt(target.x)}, ${fmt(target.y)})</b>`;
        rightEl.innerHTML = `${I("clock")} <b>${time}</b> dtk`;
      };
      plane.onResize = draw;
      next(); draw();
      const onTap = (e) => {
        e.preventDefault();
        if (time <= 0) return;
        const w = plane.eventToWorld(e);
        const x = Math.round(w.x), y = Math.round(w.y);
        tries++;
        const ok = x === target.x && y === target.y;
        marks.push({ x, y, ok });
        if (marks.length > 6) marks.shift();
        if (ok) {
          streak++; hits++;
          const bonus = Math.min(5, streak - 1);
          setScore(score + 10 + bonus);
          msg(`Tepat! +${10 + bonus}${bonus ? " (beruntun ×" + streak + ")" : ""}`, "ok");
          next();
        } else {
          streak = 0;
          msg(`Itu (${fmt(x)}, ${fmt(y)}). Cari (${fmt(target.x)}, ${fmt(target.y)}): x dulu, lalu y!`, "no");
        }
        draw();
      };
      canvas.onmousedown = onTap;
      canvas.ontouchstart = onTap;
      timers.push(setInterval(() => {
        time--; draw();
        if (time <= 0) { canvas.onmousedown = canvas.ontouchstart = null; finish(`Kamu mengenai <b>${hits}</b> titik dari ${tries} tembakan.`); }
      }, 1000));
    },
  };

  // =====================================================================
  // 2. KUADRAN KILAT
  // =====================================================================
  const kuadran = {
    rules: `<ul><li>Sebuah titik muncul di bidang koordinat.</li><li>Pilih letaknya: <b>Kuadran I–IV</b>, <b>sumbu-x</b>, atau <b>sumbu-y</b>.</li><li>15 soal. Benar <b>+10</b>, jawab di bawah 3 detik <b>+5</b> bonus kilat ${I("bolt")}.</li></ul>`,
    start() {
      const plane = new Plane(canvas, { range: 9, shade: false });
      const opts = ["kuadran I", "kuadran II", "kuadran III", "kuadran IV", "sumbu-x", "sumbu-y"];
      let round = 0, p, t0, correct = 0, locked = false;
      controls.innerHTML = opts.map((o) => `<button class="btn btn-ghost" data-a="${o}">${o.replace("kuadran", "Kuadran")}</button>`).join("");
      const next = () => {
        const r = Math.random();
        if (r < 0.12) p = { x: rnd(-8, 8) || 3, y: 0 };
        else if (r < 0.24) p = { x: 0, y: rnd(-8, 8) || -4 };
        else p = { x: (rnd(1, 8)) * (Math.random() < .5 ? -1 : 1), y: (rnd(1, 8)) * (Math.random() < .5 ? -1 : 1) };
        t0 = Date.now(); locked = false; draw();
      };
      const draw = () => {
        plane.draw();
        plane.point(p.x, p.y, { r: 10, label: `(${fmt(p.x)}, ${fmt(p.y)})` });
        midEl.innerHTML = `Soal <b>${Math.min(round + 1, 15)}</b>/15`;
        rightEl.innerHTML = `${I("check")} <b>${correct}</b>`;
      };
      plane.onResize = draw;
      controls.querySelectorAll("button").forEach((b) => b.addEventListener("click", () => {
        if (locked || round >= 15) return;
        locked = true;
        const ans = quadrantOf(p.x, p.y);
        const ok = b.dataset.a === ans;
        const fast = Date.now() - t0 < 3000;
        if (ok) { correct++; setScore(score + 10 + (fast ? 5 : 0)); msg(fast ? "Benar! " + I("bolt") + " Bonus kilat +5" : "Benar! " + I("check") + " +10", "ok"); }
        else msg(`Belum tepat. (${fmt(p.x)}, ${fmt(p.y)}) ada di ${ans}.`, "no");
        b.classList.add(ok ? "btn-primary" : "btn-cyan");
        timers.push(setTimeout(() => {
          b.classList.remove("btn-primary", "btn-cyan");
          round++;
          if (round >= 15) { controls.innerHTML = ""; finish(`Kamu benar <b>${correct}</b> dari 15 soal.`); }
          else next();
        }, ok ? 550 : 1300));
      }));
      next();
    },
  };

  // =====================================================================
  // 3. ROBOT HARTA KARUN
  // =====================================================================
  const robot = {
    rules: `<ul><li>Harta karun <b>tersembunyi</b>: hanya koordinatnya yang diberitahu.</li><li>Susun langkah robot dengan tombol panah (1 langkah = 1 satuan), lalu tekan <b>Jalankan</b>.</li><li>Hindari batu ${I("rock")}! 5 level. Berhasil pada percobaan pertama <b>+30</b>, rute terpendek <b>+10</b> bonus.</li></ul>`,
    start() {
      const R = 6;
      const plane = new Plane(canvas, { range: R, shade: false });
      let level = 0, start, pos, treasure, rocks = [], program = [], tries = 0, running = false, found = false, trail = [];
      const key = (x, y) => x + "," + y;
      const isRock = (x, y) => rocks.some((r) => r.x === x && r.y === y);
      const shortest = () => {
        const q = [[start.x, start.y, 0]], seen = new Set([key(start.x, start.y)]);
        while (q.length) {
          const [x, y, d] = q.shift();
          if (x === treasure.x && y === treasure.y) return d;
          [[1, 0], [-1, 0], [0, 1], [0, -1]].forEach(([dx, dy]) => {
            const nx = x + dx, ny = y + dy;
            if (Math.abs(nx) <= R && Math.abs(ny) <= R && !isRock(nx, ny) && !seen.has(key(nx, ny))) { seen.add(key(nx, ny)); q.push([nx, ny, d + 1]); }
          });
        }
        return Infinity;
      };
      const setup = () => {
        do {
          start = { x: rnd(-5, 5), y: rnd(-5, 5) };
          treasure = { x: rnd(-5, 5), y: rnd(-5, 5) };
          rocks = [];
          const nRocks = 2 + level * 2;
          while (rocks.length < nRocks) {
            const r = { x: rnd(-5, 5), y: rnd(-5, 5) };
            if ((r.x !== start.x || r.y !== start.y) && (r.x !== treasure.x || r.y !== treasure.y) && !isRock(r.x, r.y)) rocks.push(r);
          }
        } while (Math.abs(start.x - treasure.x) + Math.abs(start.y - treasure.y) < 4 + level || shortest() === Infinity);
        pos = { ...start }; program = []; tries = 0; found = false; trail = [];
        msg(`Level ${level + 1}: robot di (${fmt(start.x)}, ${fmt(start.y)}). Harta tersembunyi di (${fmt(treasure.x)}, ${fmt(treasure.y)})!`);
        draw(); renderProgram();
      };
      const draw = () => {
        plane.draw();
        trail.forEach((t) => plane.point(t.x, t.y, { color: "rgba(124,58,237,.35)", r: 4, ring: false }));
        rocks.forEach((r) => plane.sprite("rock", r.x, r.y, 1.05));
        if (found) plane.sprite("gem", treasure.x, treasure.y, 1.2);
        plane.sprite("robot", pos.x, pos.y, 1.25);
        plane.text(`(${fmt(pos.x)}, ${fmt(pos.y)})`, pos.x, pos.y + 0.85, { size: 12, color: "#5b21b6" });
        midEl.innerHTML = `${I("gem")} Harta di <b>(${fmt(treasure.x)}, ${fmt(treasure.y)})</b>`;
        rightEl.innerHTML = `Level <b>${Math.min(level + 1, 5)}</b>/5`;
      };
      plane.onResize = draw;
      const arrows = { R: "→", L: "←", U: "↑", D: "↓" };
      controls.innerHTML = `
        <div class="program" id="rProg" aria-label="Program robot"></div>
        <div class="pad">
          <button class="btn btn-ghost up" data-m="U" aria-label="Atas">↑</button>
          <button class="btn btn-ghost left" data-m="L" aria-label="Kiri">←</button>
          <button class="btn btn-ghost down" data-m="D" aria-label="Bawah">↓</button>
          <button class="btn btn-ghost right" data-m="R" aria-label="Kanan">→</button>
        </div>
        <button class="btn btn-ghost" id="rUndo">⌫ Hapus</button>
        <button class="btn btn-ghost" id="rClear">${I("warn")} Kosongkan</button>
        <button class="btn btn-primary" id="rRun">${I("play")} Jalankan</button>`;
      const progEl = document.getElementById("rProg");
      const renderProgram = () => {
        progEl.innerHTML = program.length ? program.map((m) => `<span class="step">${arrows[m]}</span>`).join("") : '<span class="muted" style="font-size:.9rem">Program kosong. Tekan tombol panah.</span>';
      };
      controls.querySelectorAll("[data-m]").forEach((b) => b.addEventListener("click", () => {
        if (running || program.length >= 30) return;
        program.push(b.dataset.m); renderProgram();
      }));
      document.getElementById("rUndo").onclick = () => { if (!running) { program.pop(); renderProgram(); } };
      document.getElementById("rClear").onclick = () => { if (!running) { program = []; renderProgram(); } };
      document.getElementById("rRun").onclick = () => {
        if (running || !program.length) return;
        running = true; tries++; pos = { ...start }; trail = []; draw();
        let i = 0, crashed = false;
        const step = setInterval(() => {
          const m = program[i];
          const n = { x: pos.x + (m === "R") - (m === "L"), y: pos.y + (m === "U") - (m === "D") };
          if (Math.abs(n.x) > R || Math.abs(n.y) > R) { crashed = "keluar bidang"; }
          else if (isRock(n.x, n.y)) { crashed = `menabrak batu di (${fmt(n.x)}, ${fmt(n.y)})`; }
          else { trail.push({ ...pos }); pos = n; }
          draw(); i++;
          if (crashed || i >= program.length) {
            clearInterval(step); running = false;
            if (!crashed && pos.x === treasure.x && pos.y === treasure.y) {
              found = true; draw();
              const pts = tries === 1 ? 30 : tries === 2 ? 20 : 10;
              const bonus = program.length === shortest() ? 10 : 0;
              setScore(score + pts + bonus);
              msg(`${I("gem")} Harta ditemukan! +${pts}${bonus ? " +10 rute terpendek" : ""}`, "ok");
              level++;
              timers.push(setTimeout(() => (level >= 5 ? (controls.innerHTML = "", finish("Kamu menemukan kelima harta karun! " + I("gem"))) : setup()), 1600));
            } else if (crashed) {
              msg(`${I("warn")} Robot ${crashed}. Perbaiki programmu lalu jalankan lagi.`, "no");
            } else {
              msg(`Robot berhenti di (${fmt(pos.x)}, ${fmt(pos.y)}), belum di (${fmt(treasure.x)}, ${fmt(treasure.y)}). Coba lagi!`, "no");
            }
          }
        }, 320);
        timers.push(step);
      };
      setup();
    },
  };

  // =====================================================================
  // 4. KAPAL KOORDINAT
  // =====================================================================
  const kapal = {
    rules: `<ul><li>Ada <b>3 kapal</b> tersembunyi (panjang 3, 2, dan 2 titik) pada bidang −5 sampai 5.</li><li>Ketik koordinat (x, y) lalu tekan <b>Tembak</b>. Mengetuk bidang juga mengisi koordinat.</li><li>Kena <b>+15</b>. Tenggelamkan semua kapal: bonus sisa peluru ×5. Kamu punya <b>25 peluru</b>.</li></ul>`,
    start() {
      const R = 5;
      const plane = new Plane(canvas, { range: R, shade: true });
      const key = (x, y) => x + "," + y;
      let ships = [], shots = new Map(), ammo = 25, aim = null, over = false;
      const occupied = new Set();
      [3, 2, 2].forEach((len) => {
        for (;;) {
          const horiz = Math.random() < .5;
          const x0 = rnd(-R, horiz ? R - len + 1 : R), y0 = rnd(-R, horiz ? R : R - len + 1);
          const cells = Array.from({ length: len }, (_, i) => ({ x: x0 + (horiz ? i : 0), y: y0 + (horiz ? 0 : i) }));
          if (cells.every((c) => !occupied.has(key(c.x, c.y)))) { cells.forEach((c) => occupied.add(key(c.x, c.y))); ships.push({ cells, len }); break; }
        }
      });
      const sunk = (s) => s.cells.every((c) => shots.get(key(c.x, c.y)) === "hit");
      const draw = () => {
        plane.draw();
        if (over) ships.forEach((s) => s.cells.forEach((c) => { if (!shots.has(key(c.x, c.y))) plane.sprite("ship", c.x, c.y, 0.95); }));
        shots.forEach((v, k) => { const [x, y] = k.split(",").map(Number); plane.sprite(v === "hit" ? "fire" : "drop", x, y, 0.95); });
        if (aim && !over) plane.point(aim.x, aim.y, { color: "rgba(124,58,237,.5)", r: 12, ring: false });
        const left = ships.filter((s) => !sunk(s)).length;
        midEl.innerHTML = `${I("ship")} Sisa kapal <b>${left}</b>/3`;
        rightEl.innerHTML = `${I("fire")} Peluru <b>${ammo}</b>`;
      };
      plane.onResize = draw;
      controls.innerHTML = `<form class="coord-form" id="kForm">
          <label>x<input type="number" id="kx" min="-5" max="5" step="1" required></label>
          <label>y<input type="number" id="ky" min="-5" max="5" step="1" required></label>
          <button class="btn btn-primary" type="submit">${I("fire")} Tembak</button></form>`;
      const kx = document.getElementById("kx"), ky = document.getElementById("ky");
      const tap = (e) => {
        e.preventDefault();
        if (over) return;
        const w = plane.eventToWorld(e);
        aim = { x: Math.max(-R, Math.min(R, Math.round(w.x))), y: Math.max(-R, Math.min(R, Math.round(w.y))) };
        kx.value = aim.x; ky.value = aim.y; draw();
        msg(`Bidikan di (${fmt(aim.x)}, ${fmt(aim.y)}). Tekan Tembak!`);
      };
      canvas.onmousedown = tap; canvas.ontouchstart = tap;
      document.getElementById("kForm").addEventListener("submit", (e) => {
        e.preventDefault();
        if (over) return;
        const x = Number(kx.value), y = Number(ky.value);
        if (!Number.isInteger(x) || !Number.isInteger(y) || Math.abs(x) > R || Math.abs(y) > R) { msg("Koordinat harus bilangan bulat dari −5 sampai 5.", "no"); return; }
        if (shots.has(key(x, y))) { msg(`(${fmt(x)}, ${fmt(y)}) sudah pernah ditembak. Pilih titik lain.`, "no"); return; }
        ammo--; aim = null;
        const ship = ships.find((s) => s.cells.some((c) => c.x === x && c.y === y));
        if (ship) {
          shots.set(key(x, y), "hit"); setScore(score + 15);
          msg(sunk(ship) ? `${I("trophy")} Kapal sepanjang ${ship.len} tenggelam! (+15)` : `${I("fire")} Kena di (${fmt(x)}, ${fmt(y)})! +15. Coba titik di sekitarnya.`, "ok");
        } else {
          shots.set(key(x, y), "miss");
          const rest = ships.filter((s) => !sunk(s)).flatMap((s) => s.cells.filter((c) => !shots.has(key(c.x, c.y))));
          const near = rest.sort((a, b) => Math.hypot(a.x - x, a.y - y) - Math.hypot(b.x - x, b.y - y))[0];
          msg(`${I("drop")} Meleset di (${fmt(x)}, ${fmt(y)}). Petunjuk: bagian kapal terdekat ada di ${quadrantOf(near.x, near.y)}.`, "no");
        }
        const allSunk = ships.every(sunk);
        if (allSunk || ammo <= 0) {
          over = true; canvas.onmousedown = canvas.ontouchstart = null;
          if (allSunk) setScore(score + ammo * 5);
          draw(); controls.innerHTML = "";
          timers.push(setTimeout(() => finish(allSunk ? `Semua kapal tenggelam! Bonus sisa peluru: ${ammo} × 5.` : "Peluru habis. Kapal yang tersisa ditampilkan " + I("ship")), 1200));
          return;
        }
        draw(); kx.focus();
      });
      draw();
      msg("Ketik koordinat atau ketuk bidang untuk membidik.");
    },
  };

  const GAMES = { titik, kuadran, robot, kapal };
  const game = GAMES[gid];
  rulesEl.innerHTML = game.rules;
  // gambar bidang kosong di belakang overlay
  const preview = new Plane(canvas, { range: gid === "kapal" ? 5 : gid === "robot" ? 6 : 8, shade: gid === "kapal" });
  preview.draw();

  startBtn.addEventListener("click", () => {
    clearTimers();
    overlay.hidden = true;
    controls.innerHTML = "";
    setScore(0);
    msg("");
    canvas.onmousedown = canvas.ontouchstart = null;
    game.start();
  });
})();
