/* LYZNART - skrip umum */
(function () {
  "use strict";

  // ---------- menu HP ----------
  const toggle = document.querySelector(".nav-toggle");
  const nav = document.getElementById("mainnav");
  if (toggle && nav) {
    toggle.addEventListener("click", () => {
      const open = nav.classList.toggle("open");
      toggle.setAttribute("aria-expanded", String(open));
      toggle.textContent = open ? "✕" : "☰";
    });
  }

  // ---------- toast ----------
  function toast(msg, cls, html) {
    const zone = document.getElementById("toast-zone");
    if (!zone) return;
    const el = document.createElement("div");
    el.className = "toast " + (cls || "");
    if (html) el.innerHTML = msg; else el.textContent = msg;
    zone.appendChild(el);
    setTimeout(() => { el.style.opacity = "0"; el.style.transition = "opacity .4s"; }, 3200);
    setTimeout(() => el.remove(), 3700);
  }

  async function api(url, data) {
    if (window.LYZ.isStatic && window.LYZ.localApi) return window.LYZ.localApi(url, data);
    const res = await fetch((window.LYZ.base || "") + url, {
      method: data === undefined ? "GET" : "POST",
      headers: { "Content-Type": "application/json", "X-Requested-With": "LYZNART" },
      credentials: "same-origin",
      body: data === undefined ? undefined : JSON.stringify(data),
    });
    if (!res.ok) throw new Error("HTTP " + res.status);
    return res.json();
  }

  function showRewards(r) {
    if (!r) return;
    const ic = window.LYZ.icon;
    const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", "\"": "&quot;" }[c]));
    if (r.xp_gained > 0) toast(ic("star") + " +" + r.xp_gained + " XP", "", true);
    (r.new_badges || []).forEach((b, i) => setTimeout(() => toast(ic(b.icon) + " Badge baru: <b>" + esc(b.name) + "</b>", "badge-toast", true), 600 * (i + 1)));
    if (r.level) {
      const meta = document.querySelector(".nav-meta small");
      if (meta) meta.textContent = "Lv " + r.level.level + " · " + r.level.xp + " XP";
    }
  }

  window.LYZ = Object.assign(window.LYZ || {}, { toast, api, showRewards });

  // ---------- tandai selesai (materi, contoh, visualisasi) ----------
  document.querySelectorAll(".mark-done").forEach((btn) => {
    btn.addEventListener("click", async () => {
      if (!window.LYZ.loggedIn) { toast(window.LYZ.icon("key") + " Masuk dulu supaya progresmu tersimpan", "", true); return; }
      if (btn.classList.contains("is-done")) return;
      btn.disabled = true;
      try {
        const r = await api("/api/progress", { item: btn.dataset.item });
        btn.classList.add("is-done");
        btn.textContent = "✓ Sudah selesai";
        showRewards(r);
      } catch (e) {
        toast("Gagal menyimpan. Periksa koneksi internet.");
      } finally { btn.disabled = false; }
    });
  });

  // ---------- tombol lihat pembahasan ----------
  document.querySelectorAll(".reveal").forEach((btn) => {
    btn.addEventListener("click", () => {
      const sol = btn.nextElementSibling;
      const show = sol.hidden;
      sol.hidden = !show;
      btn.setAttribute("aria-expanded", String(show));
      btn.innerHTML = window.LYZ.icon("eye") + (show ? " Sembunyikan pembahasan" : " Lihat pembahasan");
    });
  });

  // ---------- PWA: service worker ----------
  if ("serviceWorker" in navigator) {
    window.addEventListener("load", () => {
      navigator.serviceWorker.register((window.LYZ.base || "") + "/sw.js", { scope: (window.LYZ.base || "") + "/" }).catch(() => {});
    });
  }

  // ---------- PWA: tombol Install ----------
  let deferredPrompt = null;
  const installBtns = document.querySelectorAll(".install-btn");
  const state = document.getElementById("installState");
  const standalone = window.matchMedia("(display-mode: standalone)").matches || window.navigator.standalone === true;
  const isIOS = /iphone|ipad|ipod/i.test(navigator.userAgent);

  if (state) {
    if (standalone) state.innerHTML = window.LYZ.icon("check") + " LYZNART sudah terpasang dan sedang berjalan sebagai aplikasi.";
    else if (isIOS) state.textContent = "Di iPhone/iPad, gunakan Safari → Bagikan → Tambah ke Layar Utama.";
    else state.textContent = "Jika tombol Install tidak muncul, gunakan menu browser sesuai petunjuk di bawah.";
  }

  window.addEventListener("beforeinstallprompt", (e) => {
    e.preventDefault();
    deferredPrompt = e;
    installBtns.forEach((b) => (b.hidden = false));
    if (state) state.innerHTML = "Perangkatmu mendukung instalasi. Tekan tombol di atas! " + window.LYZ.icon("sparkle");
  });

  installBtns.forEach((b) => b.addEventListener("click", async () => {
    if (!deferredPrompt) { location.href = (window.LYZ.base || "") + "/instal" + (window.LYZ.isStatic ? "/" : ""); return; }
    deferredPrompt.prompt();
    const choice = await deferredPrompt.userChoice;
    deferredPrompt = null;
    installBtns.forEach((x) => (x.hidden = true));
    toast(choice.outcome === "accepted" ? window.LYZ.icon("install") + " Mantap! LYZNART sedang dipasang" : window.LYZ.icon("heart") + " Tidak apa-apa, LYZNART tetap bisa dipakai di browser", "", true);
  }));

  window.addEventListener("appinstalled", () => {
    installBtns.forEach((b) => (b.hidden = true));
    toast(window.LYZ.icon("sparkle") + " LYZNART berhasil dipasang!", "", true);
  });
})();
