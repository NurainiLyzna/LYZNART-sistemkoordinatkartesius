/* LYZNART versi statis (GitHub Pages): profil, penilaian, XP, badge, dan progres disimpan di browser.
   Meniru API Flask (/api/quiz, /api/game, /api/progress, /api/stats) agar skrip lain tetap sama. */
(function () {
  "use strict";
  const D = window.LYZ_DATA;
  if (!D) return;
  const LYZ = window.LYZ;
  const BASE = LYZ.base || "";
  const KEY = "lyznart:v2";   // { accounts: { username: {user, pw, salt, results, badges, progress} }, current }
  const AVA = { robot: "🤖", astronot: "🧑‍🚀", kucing: "🐱", burung: "🦉" };

  function loadAll() {
    try { const a = JSON.parse(localStorage.getItem(KEY)); if (a && a.accounts) return a; } catch (e) { /* abaikan */ }
    return { accounts: {}, current: null };
  }
  let ALL = loadAll();
  let S = ALL.current ? ALL.accounts[ALL.current] || null : null;
  function save() { try { localStorage.setItem(KEY, JSON.stringify(ALL)); return true; } catch (e) { return false; } }

  async function hashPw(pw, salt) {
    const text = salt + ":" + pw;
    if (window.crypto && crypto.subtle) {
      const h = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(text));
      return [...new Uint8Array(h)].map((b) => b.toString(16).padStart(2, "0")).join("");
    }
    let h = 2166136261;  // cadangan FNV-1a bila Web Crypto tidak tersedia
    for (let i = 0; i < text.length; i++) { h ^= text.charCodeAt(i); h = Math.imul(h, 16777619); }
    return "fnv" + (h >>> 0).toString(16);
  }
  function logout() { ALL.current = null; save(); location.href = page("/masuk"); }
  const hasUser = () => !!(S && S.user);
  LYZ.loggedIn = hasUser();
  const now = () => new Date().toISOString().slice(0, 19);
  const page = (p) => BASE + (p === "/" ? "/" : p + "/");
  LYZ.page = page;

  // ---------------------------------------------------------------- logika (sama dengan server)
  function levelInfo(xp) {
    let idx = 0;
    D.levels.forEach(([need], i) => { if (xp >= need) idx = i; });
    const [curNeed, name] = D.levels[idx];
    if (idx + 1 < D.levels.length) {
      const nxt = D.levels[idx + 1][0];
      return { level: idx + 1, name, xp, next: nxt, pct: Math.round(100 * (xp - curNeed) / (nxt - curNeed)) };
    }
    return { level: idx + 1, name, xp, next: null, pct: 100 };
  }
  function award(code) {
    if (S.badges[code]) return null;
    S.badges[code] = now();
    return Object.assign({ code }, D.badges[code]);
  }
  function addXp(n) { if (n > 0) S.user.xp += n; return S.user.xp; }
  function xpBadges() {
    const out = [];
    if (S.user.xp >= 500) out.push(award("xp500"));
    if (levelInfo(S.user.xp).level >= 6) out.push(award("master"));
    return out;
  }
  const clean = (arr) => arr.filter(Boolean);

  function grade(kind, answers) {
    const items = D.quizzes[kind].items;
    let correct = 0;
    const detail = items.map((q) => {
      let given = answers[q.id];
      given = Number.isInteger(given) ? given : null;
      const ok = given === q.answer;
      correct += ok;
      return { id: q.id, given, answer: q.answer, correct: ok, explanation: q.explanation, topic: q.topic };
    });
    const total = items.length;
    return { correct, total, score: total ? Math.round(100 * correct / total) : 0, detail };
  }

  function apiQuiz(kind, data) {
    if (!D.quizzes[kind]) throw new Error("404");
    const r = grade(kind, (data && data.answers) || {});
    const res = Object.assign({}, r, { xp_gained: 0, new_badges: [], saved: false });
    if (!hasUser()) return res;
    const prevBest = Math.max(0, ...S.results.filter((x) => x.kind === kind).map((x) => x.correct));
    const xp = Math.max(0, r.correct - prevBest) * D.quizzes[kind].rate;
    S.results.push({ kind, score: r.score, correct: r.correct, total: r.total, xp_gained: xp, created_at: now() });
    addXp(xp);
    const nb = [];
    if (kind === "pretest") nb.push(award("pretest"));
    if (kind === "posttest") {
      if (r.score >= 75) nb.push(award("posttest"));
      const pres = S.results.filter((x) => x.kind === "pretest").map((x) => x.score);
      if (pres.length && r.score > Math.max(...pres)) nb.push(award("improve"));
    }
    if (kind === "latihan" && r.score >= 80) nb.push(award("practice"));
    if (r.score === 100) nb.push(award("perfect"));
    nb.push(...xpBadges());
    save();
    return Object.assign(res, { xp_gained: xp, new_badges: clean(nb), saved: true, level: levelInfo(S.user.xp) });
  }

  function apiGame(gid, data) {
    if (!D.games[gid]) throw new Error("404");
    const score = Math.max(0, Math.min(2000, parseInt(data && data.score, 10) || 0));
    if (!hasUser()) return { saved: false, xp_gained: 0, new_badges: [] };
    const xp = Math.max(0, Math.min(40, Math.floor(score / 10)));
    S.results.push({ kind: "game:" + gid, score, correct: 0, total: 0, xp_gained: xp, created_at: now() });
    addXp(xp);
    const played = new Set(S.results.filter((x) => x.kind.startsWith("game:")).map((x) => x.kind));
    const nb = [];
    if (played.size >= Object.keys(D.games).length) nb.push(award("gamer"));
    nb.push(...xpBadges());
    save();
    return { saved: true, xp_gained: xp, new_badges: clean(nb), level: levelInfo(S.user.xp) };
  }

  function apiProgress(data) {
    const item = String((data && data.item) || "");
    if (!D.materi.concat(["contoh", "visual"]).includes(item)) throw new Error("400");
    if (!hasUser()) throw new Error("401");
    let xp = 0;
    const nb = [];
    if (!S.progress[item]) {
      S.progress[item] = now();
      xp = D.materi.includes(item) ? 15 : 10;
      if (D.materi.every((m) => S.progress[m])) nb.push(award("reader"));
      if (item === "visual") nb.push(award("explorer"));
    }
    addXp(xp);
    nb.push(...xpBadges());
    save();
    return { saved: true, xp_gained: xp, new_badges: clean(nb), level: levelInfo(S.user.xp) };
  }

  function apiStats() {
    const rows = (S && S.results) || [];
    const last = (k) => { const r = rows.filter((x) => x.kind === k); return r.length ? r[r.length - 1].score : null; };
    const best = {};
    rows.filter((x) => x.kind.startsWith("game:")).forEach((x) => { const k = x.kind.slice(5); best[k] = Math.max(best[k] || 0, x.score); });
    return {
      pre: last("pretest"), post: last("posttest"),
      latihan: rows.filter((x) => x.kind === "latihan").slice(-10).map((x) => ({ score: x.score, date: x.created_at.slice(0, 10) })),
      games: Object.entries(D.games).map(([k, g]) => ({ name: g.name, score: best[k] === undefined ? null : best[k] })),
    };
  }

  LYZ.localApi = function (url, data) {
    return new Promise((resolve, reject) => {
      try {
        let m;
        if ((m = url.match(/^\/api\/quiz\/(\w+)/))) resolve(apiQuiz(m[1], data));
        else if ((m = url.match(/^\/api\/game\/(\w+)/))) resolve(apiGame(m[1], data));
        else if (url.startsWith("/api/progress")) resolve(apiProgress(data));
        else if (url.startsWith("/api/stats")) resolve(apiStats());
        else reject(new Error("404"));
      } catch (e) { reject(e); }
    });
  };

  // ---------------------------------------------------------------- tampilan
  const $ = (s, r) => (r || document).querySelector(s);
  const $$ = (s, r) => [...(r || document).querySelectorAll(s)];
  const here = location.pathname.replace(BASE, "").replace(/\/$/, "") || "/";

  function fillCommon() {
    if (!hasUser()) return;
    const u = S.user, lv = levelInfo(u.xp);
    const set = (k, v) => $$(`[data-fill="${k}"]`).forEach((el) => (el.textContent = v));
    $$('[data-fill="avatar"]').forEach((el) => (el.innerHTML = LYZ.icon("av-" + (AVA[u.avatar] ? u.avatar : "robot"), "av")));
    set("first", u.name.split(" ")[0]);
    set("name", u.name);
    set("handle", "@" + (u.username || ALL.current));
    set("kelasline", (u.kelas || "Kelas VIII") + (u.sekolah ? " · " + u.sekolah : ""));
    set("lv", "Lv " + lv.level);
    set("lvname", lv.name);
    set("lvtext", `${u.xp} XP` + (lv.next ? ` · ${lv.next - u.xp} XP lagi ke level berikutnya` : " · Level maksimum!"));
    $$('[data-fill="lvbar"]').forEach((el) => (el.style.width = lv.pct + "%"));
  }

  function nav() {
    $$(".guest-only").forEach((el) => (el.hidden = hasUser()));
    if (!hasUser()) return;
    const navEl = $("#mainnav");
    if (!navEl) return;
    $$("a.btn", navEl).forEach((a) => a.remove());
    const u = S.user, lv = levelInfo(u.xp);
    const dash = document.createElement("a");
    dash.href = page("/dashboard"); dash.innerHTML = LYZ.icon("home") + " Dashboard";
    if (here === "/dashboard") dash.className = "active";
    const me = document.createElement("a");
    me.href = page("/profil"); me.className = "nav-user" + (here === "/profil" ? " active" : "");
    me.innerHTML = '<span class="nav-avatar"></span><span class="nav-meta"><b></b><small></small></span>';
    me.querySelector(".nav-avatar").innerHTML = LYZ.icon("av-" + (AVA[u.avatar] ? u.avatar : "robot"), "av");
    me.querySelector("b").textContent = u.name.split(" ")[0];
    me.querySelector("small").textContent = `Lv ${lv.level} · ${u.xp} XP`;
    const out = document.createElement("a");
    out.href = page("/masuk"); out.className = "nav-logout"; out.innerHTML = LYZ.icon("logout") + " Keluar";
    out.addEventListener("click", (e) => { e.preventDefault(); logout(); });
    const install = $(".install-btn", navEl);
    navEl.insertBefore(dash, install); navEl.insertBefore(me, install); navEl.insertBefore(out, install);
  }

  function markDone() {
    if (!hasUser()) return;
    $$(".mark-done").forEach((b) => {
      if (S.progress[b.dataset.item]) { b.classList.add("is-done"); b.textContent = "✓ Sudah selesai"; }
    });
  }

  function authPage() {
    const form = $("#localAuth");
    if (!form) return;
    if (hasUser()) { location.replace(page("/dashboard")); return; }
    const err = $("#authErr");
    const fail = (m) => { err.textContent = m; err.hidden = false; };
    const mode = form.dataset.mode;
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      err.hidden = true;
      const f = new FormData(form);
      const username = String(f.get("username") || "").trim().toLowerCase();
      const password = String(f.get("password") || "");
      if (mode === "login") {
        const acc = ALL.accounts[username];
        if (!acc || acc.pw !== await hashPw(password, acc.salt)) return fail("Username atau kata sandi salah.");
        ALL.current = username;
        if (!save()) return fail("Browser ini tidak mengizinkan penyimpanan data (mode privat?).");
        location.href = page("/dashboard");
        return;
      }
      const name = String(f.get("name") || "").trim().slice(0, 60);
      if (name.length < 2) return fail("Nama lengkap minimal 2 karakter.");
      if (!/^[a-z0-9_.]{3,20}$/.test(username)) return fail("Username 3–20 karakter: huruf kecil, angka, titik, atau garis bawah.");
      if (password.length < 6) return fail("Kata sandi minimal 6 karakter.");
      if (ALL.accounts[username]) return fail("Username sudah dipakai di perangkat ini, coba yang lain ya.");
      const salt = [...crypto.getRandomValues(new Uint8Array(8))].map((b) => b.toString(16).padStart(2, "0")).join("");
      ALL.accounts[username] = {
        user: { username, name, kelas: String(f.get("kelas") || "").trim().slice(0, 20), sekolah: String(f.get("sekolah") || "").trim().slice(0, 80),
                avatar: AVA[f.get("avatar")] ? f.get("avatar") : "robot", xp: 10, created_at: now() },
        pw: await hashPw(password, salt), salt,
        results: [], badges: { welcome: now() }, progress: {},
      };
      ALL.current = username;
      if (!save()) return fail("Browser ini tidak mengizinkan penyimpanan data (mode privat?). Progres tidak akan tersimpan.");
      location.href = page("/dashboard");
    });
  }

  function dashboardPage() {
    const path = $("#ldPath");
    if (!path || !hasUser()) return;
    const last = (k) => S.results.filter((x) => x.kind === k).slice(-1)[0];
    const played = new Set(S.results.filter((x) => x.kind.startsWith("game:")).map((x) => x.kind));
    const steps = [
      ["Pre-test", "/kuis/pretest", !!last("pretest")],
      ["Pelajari materi", "/materi", D.materi.every((m) => S.progress[m])],
      ["Contoh soal", "/contoh-soal", !!S.progress.contoh],
      ["Visualisasi", "/visualisasi", !!S.progress.visual],
      ["Latihan 40 soal", "/kuis/latihan", !!last("latihan")],
      ["Main game", "/game", played.size > 0],
      ["Post-test", "/kuis/posttest", !!last("posttest")],
    ];
    path.innerHTML = "";
    steps.forEach(([label, href, ok], i) => {
      const li = document.createElement("li");
      if (ok) li.className = "done";
      li.innerHTML = `<a href="${page(href)}"><span class="dot">${ok ? "✓" : i + 1}</span><span></span></a>`;
      li.querySelector("a span:last-child").textContent = label;
      path.appendChild(li);
    });
    $("#ldPathText").textContent = `Selesai ${steps.filter((s) => s[2]).length} dari ${steps.length} langkah.`;
    const sc = (k) => (last(k) ? last(k).score : "–");
    const stats = [["Pre-test", sc("pretest")], ["Post-test", sc("posttest")], ["Latihan", sc("latihan")],
      ["Badge", `${Object.keys(S.badges).length}/${Object.keys(D.badges).length}`],
      ["Materi", `${D.materi.filter((m) => S.progress[m]).length}/${D.materi.length}`],
      ["Game", `${played.size}/${Object.keys(D.games).length}`]];
    $("#ldStats").innerHTML = stats.map(([k, v]) => `<div><span>${k}</span><b>${v}</b></div>`).join("");
  }

  function profilPage() {
    const form = $("#lpForm");
    if (!form || !hasUser()) return;
    const u = S.user;
    form.name.value = u.name; form.kelas.value = u.kelas; form.sekolah.value = u.sekolah;
    const av = form.querySelector(`input[name=avatar][value="${u.avatar}"]`); if (av) av.checked = true;
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      const name = form.name.value.trim().slice(0, 60);
      if (name.length < 2) { LYZ.toast("Nama minimal 2 karakter."); return; }
      Object.assign(S.user, { name, kelas: form.kelas.value.trim().slice(0, 20), sekolah: form.sekolah.value.trim().slice(0, 80),
        avatar: (form.querySelector("input[name=avatar]:checked") || {}).value || "robot" });
      save(); location.reload();
    });
    $("#lpReset").addEventListener("click", () => {
      if (!confirm("Hapus akun ini beserta semua progresnya di perangkat ini? Tindakan ini tidak bisa dibatalkan.")) return;
      delete ALL.accounts[ALL.current];
      logout();
    });
    $("#lpLogout").addEventListener("click", logout);
    // badge
    const grid = $("#lpBadges");
    $("#lpBadgeCount").textContent = Object.keys(S.badges).length;
    grid.innerHTML = "";
    Object.entries(D.badges).forEach(([code, b]) => {
      const own = !!S.badges[code];
      const d = document.createElement("div");
      d.className = "badge " + (own ? "owned" : "locked"); d.title = b.desc;
      d.innerHTML = `<span class="b-icon">${LYZ.icon(own ? b.icon : "lock")}</span><b></b><small></small>`;
      d.querySelector("b").textContent = b.name; d.querySelector("small").textContent = b.desc;
      grid.appendChild(d);
    });
    // tangga level
    $("#lpLadder").innerHTML = D.levels.map(([need, name], i) =>
      `<li class="${u.xp >= need ? "reached" : ""}"><span>Lv ${i + 1}</span><b>${name}</b><small>${need} XP</small></li>`).join("");
    // riwayat
    const names = { latihan: "Latihan Soal", pretest: "Pre-test", posttest: "Post-test" };
    Object.entries(D.games).forEach(([k, g]) => (names["game:" + k] = g.name));
    const rows = S.results.slice(-15).reverse();
    $("#lpHistory").innerHTML = rows.length
      ? `<div class="table-scroll"><table class="tbl"><thead><tr><th>Aktivitas</th><th>Nilai/Skor</th><th>Benar</th><th>XP</th><th>Tanggal</th></tr></thead><tbody>${
        rows.map((h) => `<tr><td>${names[h.kind] || h.kind}</td><td><b>${h.score}</b></td><td>${h.total ? h.correct + "/" + h.total : "–"}</td><td>+${h.xp_gained}</td><td>${h.created_at.slice(0, 10)}</td></tr>`).join("")
      }</tbody></table></div>`
      : `<p class="muted">Belum ada aktivitas. Yuk mulai dari <a href="${page("/kuis/pretest")}">pre-test</a>!</p>`;
  }

  // halaman yang butuh profil
  if ($("[data-need-profile]") && !hasUser()) { location.replace(page("/masuk")); return; }
  function heroCta() {
    const cta = $(".hero-cta");
    if (!cta || !hasUser()) return;
    cta.innerHTML = `<a class="btn btn-primary btn-lg" href="${page("/dashboard")}">${LYZ.icon("rocket")} Lanjut Belajar</a>` +
      `<a class="btn btn-ghost btn-lg" href="${page("/materi")}">${LYZ.icon("book")} Lihat Materi</a>`;
  }
  nav(); fillCommon(); markDone(); authPage(); dashboardPage(); profilPage(); heroCta();
})();
