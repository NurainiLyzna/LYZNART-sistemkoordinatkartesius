/* Animasi bidang koordinat di halaman beranda */
(function () {
  "use strict";
  const canvas = document.getElementById("heroPlane");
  if (!canvas || !window.Plane) return;
  const plane = new Plane(canvas, { range: 6 });
  const { fmt, quadrantOf } = window.PlaneUtil;
  const bubble = document.querySelector(".bubble");
  const pts = [[3, 2], [-4, 3], [-2, -4], [5, -3], [0, 4], [-5, 0], [2, 5]];
  let i = 0, t = 0, from = { x: 0, y: 0 }, to = { x: 3, y: 2 };
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function frame() {
    t = Math.min(1, t + 0.025);
    const e = t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2;
    const x = from.x + (to.x - from.x) * e, y = from.y + (to.y - from.y) * e;
    plane.draw();
    if (t >= 1) {
      plane.line(to.x, to.y, to.x, 0, { dash: [6, 5], color: "#a78bfa" });
      plane.line(to.x, to.y, 0, to.y, { dash: [6, 5], color: "#67e8f9" });
    }
    plane.point(x, y, { r: 10, label: t >= 1 ? `(${fmt(to.x)}, ${fmt(to.y)})` : "" });
    if (t < 1) requestAnimationFrame(frame);
    else if (bubble) bubble.innerHTML = `Titik <b>(${fmt(to.x)}, ${fmt(to.y)})</b> ada di <b>${quadrantOf(to.x, to.y)}</b>! ✨`;
  }
  function next() {
    from = to; i = (i + 1) % pts.length; to = { x: pts[i][0], y: pts[i][1] }; t = 0;
    requestAnimationFrame(frame);
  }
  plane.onResize = () => { t = 1; frame(); };
  if (reduce) { t = 1; frame(); return; }
  requestAnimationFrame(frame);
  setInterval(next, 3200);
})();
