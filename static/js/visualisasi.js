/* Visualisasi koordinat interaktif */
(function () {
  "use strict";
  const { quadrantOf, fmt, colors } = window.PlaneUtil;
  const canvas = document.getElementById("vizCanvas");
  const plane = new Plane(canvas, { range: 10 });
  const help = document.getElementById("vizHelp");
  const out = document.getElementById("vizReadout");
  const shadeBox = document.getElementById("vizShade");
  const guideBox = document.getElementById("vizGuides");
  const inX = document.getElementById("vizX"), inY = document.getElementById("vizY");

  const R = 10;
  const clamp = (v) => Math.max(-R, Math.min(R, Math.round(v)));
  const CYAN = "#0891b2", PINK = "#db2777";

  const state = {
    mode: "titik",
    pts: { P: { x: 3, y: -2 }, A: { x: 5, y: 4 }, Ref: { x: 2, y: 1 }, B: { x: -3, y: -2 } },
    drag: null,
    challenge: { target: null, round: 0, score: 0, last: null },
  };
  let tracked = false;

  const HELP = {
    titik: "📍 <b>Mode Titik.</b> Ketuk atau geser titik <b>P</b>. Lihat absis, ordinat, kuadran, dan jaraknya ke sumbu.",
    acuan: "🎯 <b>Mode Titik Acuan.</b> Geser titik acuan <b style='color:#0891b2'>R</b> dan titik <b style='color:#7c3aed'>A</b>. Koordinat A terhadap R = (x − p, y − q).",
    jarak: "📏 <b>Mode Jarak.</b> Geser titik <b style='color:#7c3aed'>A</b> dan <b style='color:#db2777'>B</b>. Lihat jarak mendatar, tegak, dan jarak lurusnya (Pythagoras).",
    tantangan: "🏁 <b>Tantangan.</b> Ketuk posisi titik yang diminta. 10 soal, ayo dapatkan skor sempurna!",
  };

  function track() {
    if (tracked || !window.LYZ.loggedIn) return;
    tracked = true;
    window.LYZ.api("/api/progress", { item: "visual" }).then(window.LYZ.showRewards).catch(() => {});
  }

  function activeKeys() {
    if (state.mode === "titik") return ["P"];
    if (state.mode === "acuan") return ["A", "Ref"];
    if (state.mode === "jarak") return ["A", "B"];
    return [];
  }

  function guides(p, color) {
    if (!guideBox.checked) return;
    plane.line(p.x, p.y, p.x, 0, { color, dash: [6, 5], width: 2 });
    plane.line(p.x, p.y, 0, p.y, { color, dash: [6, 5], width: 2 });
  }

  function row(k, v) { return `<div class="ro"><span>${k}</span><b>${v}</b></div>`; }

  function render() {
    plane.shade = shadeBox.checked;
    plane.draw();
    const { P, A, Ref, B } = state.pts;
    let html = "";
    if (state.mode === "titik") {
      guides(P, colors.point);
      plane.point(P.x, P.y, { label: `P(${fmt(P.x)}, ${fmt(P.y)})`, r: 9 });
      html = `<div class="big-coord">P(${fmt(P.x)}, ${fmt(P.y)})</div>` +
        row("Absis (x)", fmt(P.x)) + row("Ordinat (y)", fmt(P.y)) + row("Letak", quadrantOf(P.x, P.y)) +
        row("Jarak ke sumbu-x", `|${fmt(P.y)}| = ${Math.abs(P.y)} satuan`) +
        row("Jarak ke sumbu-y", `|${fmt(P.x)}| = ${Math.abs(P.x)} satuan`) +
        `<div class="calc">Dari O: ${P.x === 0 ? "tidak bergeser mendatar" : Math.abs(P.x) + " satuan ke " + (P.x > 0 ? "kanan" : "kiri")}, lalu ${P.y === 0 ? "tidak naik/turun" : Math.abs(P.y) + " satuan ke " + (P.y > 0 ? "atas" : "bawah")}.</div>`;
    } else if (state.mode === "acuan") {
      const dx = A.x - Ref.x, dy = A.y - Ref.y;
      if (guideBox.checked) {
        plane.line(Ref.x, Ref.y, A.x, Ref.y, { color: CYAN, width: 3, dash: [8, 5] });
        plane.line(A.x, Ref.y, A.x, A.y, { color: colors.point, width: 3, dash: [8, 5] });
        if (dx) plane.text(`${dx > 0 ? "→" : "←"} ${Math.abs(dx)}`, (Ref.x + A.x) / 2, Ref.y - 0.6, { color: CYAN, size: 13 });
        if (dy) plane.text(`${dy > 0 ? "↑" : "↓"} ${Math.abs(dy)}`, A.x + 0.9, (Ref.y + A.y) / 2, { color: colors.point, size: 13 });
      }
      plane.point(Ref.x, Ref.y, { color: CYAN, label: `R(${fmt(Ref.x)}, ${fmt(Ref.y)})`, r: 9 });
      plane.point(A.x, A.y, { label: `A(${fmt(A.x)}, ${fmt(A.y)})`, r: 9 });
      html = `<div class="big-coord">(${fmt(dx)}, ${fmt(dy)})</div>` +
        row("A terhadap O", `(${fmt(A.x)}, ${fmt(A.y)})`) + row("Titik acuan R", `(${fmt(Ref.x)}, ${fmt(Ref.y)})`) +
        row("A terhadap R", `(${fmt(dx)}, ${fmt(dy)})`) +
        `<div class="calc">(x − p, y − q) = (${fmt(A.x)} − ${Ref.x < 0 ? "(" + fmt(Ref.x) + ")" : Ref.x}, ${fmt(A.y)} − ${Ref.y < 0 ? "(" + fmt(Ref.y) + ")" : Ref.y}) = (${fmt(dx)}, ${fmt(dy)})<br>` +
        `Dari R: ${dx === 0 ? "tidak bergeser mendatar" : Math.abs(dx) + " satuan ke " + (dx > 0 ? "kanan" : "kiri")}, ${dy === 0 ? "tidak naik/turun" : Math.abs(dy) + " satuan ke " + (dy > 0 ? "atas" : "bawah")}.</div>`;
    } else if (state.mode === "jarak") {
      const dx = Math.abs(B.x - A.x), dy = Math.abs(B.y - A.y);
      const d2 = dx * dx + dy * dy, d = Math.sqrt(d2);
      if (guideBox.checked && dx && dy) {
        plane.line(A.x, A.y, B.x, A.y, { color: "#94a3b8", dash: [6, 5] });
        plane.line(B.x, A.y, B.x, B.y, { color: "#94a3b8", dash: [6, 5] });
      }
      plane.line(A.x, A.y, B.x, B.y, { color: "#6366f1", width: 3 });
      plane.point(A.x, A.y, { label: `A(${fmt(A.x)}, ${fmt(A.y)})`, r: 9 });
      plane.point(B.x, B.y, { color: PINK, label: `B(${fmt(B.x)}, ${fmt(B.y)})`, r: 9 });
      const rel = A.x === B.x && A.y === B.y ? "titik berimpit" : A.y === B.y ? "sejajar sumbu-x" : A.x === B.x ? "sejajar sumbu-y" : "miring (memotong kedua sumbu)";
      const exact = Number.isInteger(d) ? String(d) : `√${d2} ≈ ${d.toFixed(2)}`;
      html = `<div class="big-coord">AB = ${exact}</div>` +
        row("Jarak mendatar |x₂ − x₁|", dx) + row("Jarak tegak |y₂ − y₁|", dy) + row("Garis AB", rel) +
        `<div class="calc">AB = √(${dx}² + ${dy}²) = √${d2}${Number.isInteger(d) ? " = " + d : " ≈ " + d.toFixed(2)} satuan</div>`;
    } else {
      const ch = state.challenge;
      if (ch.last) plane.point(ch.last.x, ch.last.y, { color: ch.last.ok ? "#059669" : "#dc2626", label: `(${fmt(ch.last.x)}, ${fmt(ch.last.y)})`, r: 9 });
      if (ch.last && !ch.last.ok && ch.prev) plane.point(ch.prev.x, ch.prev.y, { color: "#059669", label: "jawaban", r: 7 });
      if (ch.round < 10) {
        html = `<div class="big-coord">Ketuk (${fmt(ch.target.x)}, ${fmt(ch.target.y)})</div>` +
          row("Soal", `${ch.round + 1} / 10`) + row("Benar", ch.score) +
          (ch.last ? `<div class="calc">${ch.last.ok ? "✅ Tepat sekali!" : `❌ Kamu mengetuk (${fmt(ch.last.x)}, ${fmt(ch.last.y)}). Ingat: x dulu (kanan/kiri), lalu y (atas/bawah).`}</div>` : "");
      } else {
        html = `<div class="big-coord">Skor ${ch.score}/10</div>` +
          `<div class="calc">${ch.score === 10 ? "🏆 Sempurna! Kamu Master Titik!" : ch.score >= 7 ? "🎉 Hebat! Sedikit lagi sempurna." : "💪 Terus berlatih ya!"}</div>` +
          `<button class="btn btn-primary btn-sm" id="chAgain">↺ Main lagi</button>`;
      }
    }
    out.innerHTML = html;
    const again = document.getElementById("chAgain");
    if (again) again.onclick = startChallenge;
  }

  function newTarget() {
    let t;
    do { t = { x: Math.floor(Math.random() * 17) - 8, y: Math.floor(Math.random() * 17) - 8 }; }
    while (state.challenge.target && t.x === state.challenge.target.x && t.y === state.challenge.target.y);
    state.challenge.target = t;
  }
  function startChallenge() {
    state.challenge = { target: null, round: 0, score: 0, last: null };
    newTarget(); render();
  }

  function setMode(m) {
    state.mode = m;
    document.querySelectorAll(".chip[data-mode]").forEach((c) => c.classList.toggle("active", c.dataset.mode === m));
    help.innerHTML = HELP[m];
    document.getElementById("vizInput").hidden = m === "tantangan";
    if (m === "tantangan") startChallenge(); else render();
  }

  function nearest(w) {
    let best = null, bd = 1.2;
    activeKeys().forEach((k) => {
      const p = state.pts[k], d = Math.hypot(p.x - w.x, p.y - w.y);
      if (d < bd) { bd = d; best = k; }
    });
    return best;
  }

  function down(e) {
    e.preventDefault();
    const w = plane.eventToWorld(e);
    track();
    if (state.mode === "tantangan") {
      const ch = state.challenge;
      if (ch.round >= 10) return;
      const x = clamp(w.x), y = clamp(w.y);
      const ok = x === ch.target.x && y === ch.target.y;
      ch.score += ok; ch.last = { x, y, ok }; ch.prev = ch.target; ch.round++;
      window.LYZ.toast(ok ? "Tepat! ✅" : `Belum tepat. Titik yang diminta (${fmt(ch.target.x)}, ${fmt(ch.target.y)})`);
      if (ch.round < 10) newTarget();
      render();
      return;
    }
    let key = nearest(w);
    if (!key) key = activeKeys()[0];
    state.drag = key;
    state.pts[key] = { x: clamp(w.x), y: clamp(w.y) };
    render();
  }
  function move(e) {
    if (!state.drag) return;
    e.preventDefault();
    const w = plane.eventToWorld(e);
    const p = { x: clamp(w.x), y: clamp(w.y) };
    const cur = state.pts[state.drag];
    if (p.x !== cur.x || p.y !== cur.y) { state.pts[state.drag] = p; render(); }
  }
  function up() { state.drag = null; }

  canvas.addEventListener("mousedown", down);
  window.addEventListener("mousemove", move);
  window.addEventListener("mouseup", up);
  canvas.addEventListener("touchstart", down, { passive: false });
  canvas.addEventListener("touchmove", move, { passive: false });
  canvas.addEventListener("touchend", up);

  document.querySelectorAll(".chip[data-mode]").forEach((c) => c.addEventListener("click", () => setMode(c.dataset.mode)));
  document.getElementById("vizReset").addEventListener("click", () => {
    state.pts = { P: { x: 3, y: -2 }, A: { x: 5, y: 4 }, Ref: { x: 2, y: 1 }, B: { x: -3, y: -2 } };
    setMode(state.mode);
  });
  shadeBox.addEventListener("change", render);
  guideBox.addEventListener("change", render);
  document.getElementById("vizInput").addEventListener("submit", (e) => {
    e.preventDefault();
    const x = clamp(Number(inX.value)), y = clamp(Number(inY.value));
    const key = state.mode === "titik" ? "P" : "A";
    state.pts[key] = { x, y };
    track(); render();
  });
  plane.onResize = render;
  setMode("titik");
})();
