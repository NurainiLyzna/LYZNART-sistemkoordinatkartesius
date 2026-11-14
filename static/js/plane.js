/* Plane: bidang koordinat Kartesius berbasis canvas (dipakai visualisasi & game) */
(function () {
  "use strict";
  const C = {
    grid: "#efeafd", grid5: "#ddd6fe", axis: "#4c1d95", label: "#6b7280",
    q1: "rgba(196,181,253,.20)", q2: "rgba(103,232,249,.18)", q3: "rgba(56,189,248,.14)", q4: "rgba(240,171,252,.16)",
    point: "#7c3aed", ink: "#1e1b4b",
  };

  class Plane {
    constructor(canvas, opts) {
      this.canvas = canvas;
      this.ctx = canvas.getContext("2d");
      this.range = (opts && opts.range) || 10;
      this.shade = opts && opts.shade !== undefined ? opts.shade : true;
      this.labels = opts && opts.labels !== undefined ? opts.labels : true;
      this.resize();
      canvas._plane = this;
      if (!canvas._resizeBound) {
        canvas._resizeBound = true;
        window.addEventListener("resize", () => {
          const p = canvas._plane;
          p.resize();
          if (p.onResize) p.onResize(); else p.draw();
        });
      }
    }
    resize() {
      const rect = this.canvas.getBoundingClientRect();
      const size = Math.max(200, Math.round(rect.width || this.canvas.width));
      const dpr = Math.min(window.devicePixelRatio || 1, 2);
      this.canvas.width = size * dpr;
      this.canvas.height = size * dpr;
      this.ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      this.size = size;
      this.pad = size * 0.06;
      this.unit = (size - 2 * this.pad) / (2 * this.range);
    }
    sx(x) { return this.size / 2 + x * this.unit; }
    sy(y) { return this.size / 2 - y * this.unit; }
    toWorld(px, py) { return { x: (px - this.size / 2) / this.unit, y: (this.size / 2 - py) / this.unit }; }
    eventToWorld(e) {
      const r = this.canvas.getBoundingClientRect();
      const t = e.touches ? e.touches[0] || e.changedTouches[0] : e;
      return this.toWorld((t.clientX - r.left) * (this.size / r.width), (t.clientY - r.top) * (this.size / r.height));
    }
    clear() { this.ctx.clearRect(0, 0, this.size, this.size); }
    draw() {
      const { ctx, range: R } = this;
      this.clear();
      const lo = this.sx(-R), hi = this.sx(R);
      if (this.shade) {
        const m = this.size / 2;
        ctx.fillStyle = C.q1; ctx.fillRect(m, lo, hi - m, m - lo);
        ctx.fillStyle = C.q2; ctx.fillRect(lo, lo, m - lo, m - lo);
        ctx.fillStyle = C.q3; ctx.fillRect(lo, m, m - lo, hi - m);
        ctx.fillStyle = C.q4; ctx.fillRect(m, m, hi - m, hi - m);
        ctx.font = `800 ${Math.round(this.unit * 1.1)}px "Baloo 2", sans-serif`;
        ctx.fillStyle = "rgba(76,29,149,.16)"; ctx.textAlign = "center"; ctx.textBaseline = "middle";
        const o = R / 2;
        ctx.fillText("I", this.sx(o), this.sy(o)); ctx.fillText("II", this.sx(-o), this.sy(o));
        ctx.fillText("III", this.sx(-o), this.sy(-o)); ctx.fillText("IV", this.sx(o), this.sy(-o));
      }
      for (let i = -R; i <= R; i++) {
        ctx.strokeStyle = i % 5 === 0 ? C.grid5 : C.grid; ctx.lineWidth = 1;
        ctx.beginPath(); ctx.moveTo(this.sx(i), lo); ctx.lineTo(this.sx(i), hi); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(lo, this.sy(i)); ctx.lineTo(hi, this.sy(i)); ctx.stroke();
      }
      // sumbu
      ctx.strokeStyle = C.axis; ctx.fillStyle = C.axis; ctx.lineWidth = 2;
      const m = this.size / 2, a = 8;
      ctx.beginPath(); ctx.moveTo(lo - 4, m); ctx.lineTo(hi + 6, m); ctx.stroke();
      ctx.beginPath(); ctx.moveTo(m, hi + 4); ctx.lineTo(m, lo - 6); ctx.stroke();
      ctx.beginPath(); ctx.moveTo(hi + 10, m); ctx.lineTo(hi + 10 - a, m - a / 2); ctx.lineTo(hi + 10 - a, m + a / 2); ctx.fill();
      ctx.beginPath(); ctx.moveTo(m, lo - 10); ctx.lineTo(m - a / 2, lo - 10 + a); ctx.lineTo(m + a / 2, lo - 10 + a); ctx.fill();
      ctx.font = `800 ${Math.max(12, this.unit * 0.55)}px Nunito, sans-serif`;
      ctx.textAlign = "right"; ctx.textBaseline = "bottom"; ctx.fillText("x", hi + 8, m - 6);
      ctx.textAlign = "left"; ctx.textBaseline = "top"; ctx.fillText("y", m + 8, lo - 8);
      if (this.labels) {
        const step = this.unit < 18 ? 2 : 1;
        ctx.fillStyle = C.label; ctx.font = `600 ${Math.max(9, Math.min(13, this.unit * 0.42))}px Nunito, sans-serif`;
        for (let i = -R; i <= R; i++) {
          if (i === 0 || i % step) continue;
          ctx.textAlign = "center"; ctx.textBaseline = "top"; ctx.fillText(i, this.sx(i), m + 4);
          ctx.textAlign = "right"; ctx.textBaseline = "middle"; ctx.fillText(i, m - 5, this.sy(i));
        }
        ctx.textAlign = "right"; ctx.textBaseline = "top"; ctx.fillText("O", m - 4, m + 3);
      }
    }
    point(x, y, opts) {
      const o = Object.assign({ color: C.point, r: 7, label: "", ring: true }, opts || {});
      const { ctx } = this;
      ctx.beginPath(); ctx.arc(this.sx(x), this.sy(y), o.r, 0, Math.PI * 2);
      ctx.fillStyle = o.color; ctx.fill();
      if (o.ring) { ctx.lineWidth = 3; ctx.strokeStyle = "#fff"; ctx.stroke(); }
      if (o.label) {
        ctx.font = `800 ${Math.max(12, this.unit * 0.5)}px Nunito, sans-serif`;
        const tx = this.sx(x) + o.r + 4, ty = this.sy(y) - o.r - 2;
        const w = ctx.measureText(o.label).width;
        const right = tx + w > this.size - 4;
        ctx.textAlign = right ? "right" : "left"; ctx.textBaseline = "bottom";
        ctx.lineWidth = 4; ctx.strokeStyle = "rgba(255,255,255,.92)";
        const lx = right ? this.sx(x) - o.r - 4 : tx;
        ctx.strokeText(o.label, lx, ty); ctx.fillStyle = C.ink; ctx.fillText(o.label, lx, ty);
      }
    }
    line(x1, y1, x2, y2, opts) {
      const o = Object.assign({ color: C.point, width: 2, dash: [] }, opts || {});
      const { ctx } = this;
      ctx.save(); ctx.setLineDash(o.dash); ctx.strokeStyle = o.color; ctx.lineWidth = o.width; ctx.lineCap = "round";
      ctx.beginPath(); ctx.moveTo(this.sx(x1), this.sy(y1)); ctx.lineTo(this.sx(x2), this.sy(y2)); ctx.stroke();
      ctx.restore();
    }
    text(str, x, y, opts) {
      const o = Object.assign({ color: C.ink, size: 14, align: "center", base: "middle", weight: 800 }, opts || {});
      const { ctx } = this;
      ctx.font = `${o.weight} ${o.size}px Nunito, sans-serif`; ctx.textAlign = o.align; ctx.textBaseline = o.base;
      ctx.lineWidth = 4; ctx.strokeStyle = "rgba(255,255,255,.9)"; ctx.strokeText(str, this.sx(x), this.sy(y));
      ctx.fillStyle = o.color; ctx.fillText(str, this.sx(x), this.sy(y));
    }
    emoji(ch, x, y, scale) {
      const { ctx } = this;
      ctx.font = `${Math.round(this.unit * (scale || 1.1))}px "Segoe UI Emoji","Apple Color Emoji","Noto Color Emoji",sans-serif`;
      ctx.textAlign = "center"; ctx.textBaseline = "middle";
      ctx.fillText(ch, this.sx(x), this.sy(y));
    }
  }

  function quadrantOf(x, y) {
    if (x === 0 && y === 0) return "titik asal O";
    if (x === 0) return "sumbu-y";
    if (y === 0) return "sumbu-x";
    if (x > 0 && y > 0) return "kuadran I";
    if (x < 0 && y > 0) return "kuadran II";
    if (x < 0 && y < 0) return "kuadran III";
    return "kuadran IV";
  }
  const fmt = (n) => (n < 0 ? "−" + Math.abs(n) : String(n));

  window.Plane = Plane;
  window.PlaneUtil = { quadrantOf, fmt, colors: C };
})();
