/* Grafik hasil belajar (SVG murni) */
(function () {
  "use strict";
  const NS = "http://www.w3.org/2000/svg";
  const VIOLET = "#7c3aed", CYAN = "#0891b2";

  function el(tag, attrs, parent) {
    const n = document.createElementNS(NS, tag);
    Object.entries(attrs || {}).forEach(([k, v]) => n.setAttribute(k, v));
    if (parent) parent.appendChild(n);
    return n;
  }
  function empty(box) { box.innerHTML = `<div class="empty">${box.dataset.empty}</div>`; }
  function tooltip(box) {
    const tip = document.createElement("div");
    tip.className = "chart-tip";
    box.appendChild(tip);
    return {
      show(text, x, y, svg) {
        const r = svg.getBoundingClientRect(), vb = svg.viewBox.baseVal;
        tip.textContent = text;
        tip.style.left = (x * r.width / vb.width) + "px";
        tip.style.top = (y * r.height / vb.height) + "px";
        tip.classList.add("show");
      },
      hide() { tip.classList.remove("show"); },
    };
  }
  // batang dengan ujung data membulat 4px, dasar tetap rata pada baseline
  function barPath(x, y, w, h, horizontal) {
    const r = Math.min(4, horizontal ? h / 2 : w / 2, horizontal ? w : h);
    if (horizontal) return `M${x},${y} H${x + w - r} Q${x + w},${y} ${x + w},${y + r} V${y + h - r} Q${x + w},${y + h} ${x + w - r},${y + h} H${x} Z`;
    return `M${x},${y + h} V${y + r} Q${x},${y} ${x + r},${y} H${x + w - r} Q${x + w},${y} ${x + w},${y + r} V${y + h} Z`;
  }
  function yGrid(svg, L, T, W, H) {
    [0, 25, 50, 75, 100].forEach((v) => {
      const y = T + H - (v / 100) * H;
      el("line", { x1: L, x2: L + W, y1: y, y2: y, class: v === 0 ? "baseline" : "gridline" }, svg);
      const t = el("text", { x: L - 8, y: y + 4, "text-anchor": "end", class: "axis-text" }, svg); t.textContent = v;
    });
  }

  function prePost(box, pre, post) {
    if (pre === null && post === null) return empty(box);
    box.innerHTML = "";
    const Wt = 420, Ht = 260, L = 40, T = 24, W = Wt - L - 16, H = Ht - T - 40;
    const svg = el("svg", { viewBox: `0 0 ${Wt} ${Ht}`, role: "img", "aria-label": `Nilai pre-test ${pre ?? "belum ada"}, post-test ${post ?? "belum ada"}` }, box);
    const tip = tooltip(box);
    yGrid(svg, L, T, W, H);
    const data = [["Pre-test", pre], ["Post-test", post]];
    const bw = 64, gap = W / 2;
    data.forEach(([name, v], i) => {
      const cx = L + gap * i + gap / 2;
      const lbl = el("text", { x: cx, y: T + H + 22, "text-anchor": "middle", class: "axis-text" }, svg); lbl.textContent = name;
      if (v === null) { const t = el("text", { x: cx, y: T + H - 10, "text-anchor": "middle", class: "axis-text" }, svg); t.textContent = "belum dikerjakan"; return; }
      const h = Math.max(2, (v / 100) * H);
      el("path", { d: barPath(cx - bw / 2, T + H - h, bw, h), fill: VIOLET, opacity: i === 0 ? 0.55 : 1 }, svg);
      const t = el("text", { x: cx, y: T + H - h - 8, "text-anchor": "middle", class: "label-text" }, svg); t.textContent = v;
      const hit = el("rect", { x: cx - gap / 2 + 6, y: T, width: gap - 12, height: H, class: "hit" }, svg);
      hit.addEventListener("mouseenter", () => tip.show(`${name}: ${v}`, cx, T + H - h, svg));
      hit.addEventListener("mouseleave", tip.hide);
      hit.addEventListener("touchstart", () => tip.show(`${name}: ${v}`, cx, T + H - h, svg), { passive: true });
    });
    if (pre !== null && post !== null) {
      const d = post - pre;
      const p = document.createElement("p");
      p.className = "muted center";
      p.innerHTML = d > 0 ? `${window.LYZ.icon("chartup")} Nilaimu naik ${d} poin. Keren!` : d === 0 ? "Nilaimu tetap. Ayo latihan lagi!" : `Nilaimu turun ${-d} poin. Pelajari lagi materinya, ya!`;
      box.appendChild(p);
    }
  }

  function latihanLine(box, rows) {
    if (!rows.length) return empty(box);
    box.innerHTML = "";
    const Wt = 420, Ht = 260, L = 40, T = 24, W = Wt - L - 24, H = Ht - T - 40;
    const svg = el("svg", { viewBox: `0 0 ${Wt} ${Ht}`, role: "img", "aria-label": "Riwayat nilai latihan: " + rows.map((r) => r.score).join(", ") }, box);
    const tip = tooltip(box);
    yGrid(svg, L, T, W, H);
    const n = rows.length;
    const px = (i) => (n === 1 ? L + W / 2 : L + 12 + (i * (W - 24)) / (n - 1));
    const py = (v) => T + H - (v / 100) * H;
    if (n > 1) el("polyline", { points: rows.map((r, i) => `${px(i)},${py(r.score)}`).join(" "), fill: "none", stroke: VIOLET, "stroke-width": 2, "stroke-linejoin": "round", "stroke-linecap": "round" }, svg);
    rows.forEach((r, i) => {
      const x = px(i), y = py(r.score);
      el("circle", { cx: x, cy: y, r: 5, fill: VIOLET, stroke: "#fff", "stroke-width": 2 }, svg);
      const lbl = el("text", { x, y: T + H + 22, "text-anchor": "middle", class: "axis-text" }, svg); lbl.textContent = "ke-" + (i + 1);
      if (i === n - 1 || r.score === Math.max(...rows.map((q) => q.score))) {
        const t = el("text", { x, y: y - 12, "text-anchor": "middle", class: "label-text" }, svg); t.textContent = r.score;
      }
      const hit = el("circle", { cx: x, cy: y, r: 16, class: "hit" }, svg);
      const text = `Latihan ke-${i + 1}: ${r.score} (${r.date})`;
      hit.addEventListener("mouseenter", () => tip.show(text, x, y, svg));
      hit.addEventListener("mouseleave", tip.hide);
      hit.addEventListener("touchstart", () => tip.show(text, x, y, svg), { passive: true });
    });
  }

  function gameBars(box, games) {
    if (!games.some((g) => g.score !== null && g.score !== undefined)) return empty(box);
    box.innerHTML = "";
    const max = Math.max(50, ...games.map((g) => g.score || 0));
    const Wt = 760, rowH = 46, T = 10, L = 170, W = Wt - L - 60, Ht = T + rowH * games.length + 10;
    const svg = el("svg", { viewBox: `0 0 ${Wt} ${Ht}`, role: "img", "aria-label": "Skor terbaik game: " + games.map((g) => `${g.name} ${g.score ?? "belum dimainkan"}`).join(", ") }, box);
    const tip = tooltip(box);
    el("line", { x1: L, x2: L, y1: T, y2: Ht - 10, class: "baseline" }, svg);
    games.forEach((g, i) => {
      const y = T + i * rowH + 8, h = rowH - 18;
      const name = el("text", { x: L - 12, y: y + h / 2 + 5, "text-anchor": "end", class: "axis-text", style: "font-size:14px;font-weight:700" }, svg); name.textContent = g.name;
      if (g.score === null || g.score === undefined) { const t = el("text", { x: L + 10, y: y + h / 2 + 5, class: "axis-text" }, svg); t.textContent = "belum dimainkan"; return; }
      const w = Math.max(3, (g.score / max) * W);
      el("path", { d: barPath(L, y, w, h, true), fill: CYAN }, svg);
      const t = el("text", { x: L + w + 8, y: y + h / 2 + 5, class: "label-text" }, svg); t.textContent = g.score;
      const hit = el("rect", { x: L, y: y - 4, width: W + 40, height: h + 8, class: "hit" }, svg);
      hit.addEventListener("mouseenter", () => tip.show(`${g.name}: skor terbaik ${g.score}`, L + w, y, svg));
      hit.addEventListener("mouseleave", tip.hide);
    });
  }

  const pp = document.getElementById("chartPrePost");
  if (!pp) return;
  window.LYZ.api("/api/stats").then((s) => {
    prePost(pp, s.pre, s.post);
    latihanLine(document.getElementById("chartLatihan"), s.latihan);
    gameBars(document.getElementById("chartGames"), s.games);
  }).catch(() => {
    document.querySelectorAll(".chart").forEach((b) => (b.innerHTML = '<div class="empty">Grafik belum bisa dimuat (offline?).</div>'));
  });
})();
