/* LYZNART service worker (bekerja di root "/" maupun sub-folder GitHub Pages) */
const VERSION = "lyznart-v1.4.0";
const STATIC_CACHE = VERSION + "-static";
const PAGE_CACHE = VERSION + "-pages";
const BASE = new URL(self.registration.scope).pathname.replace(/\/$/, "");
const V = "?v=1.4.0";
const IS_STATIC = self.location.hostname.endsWith("github.io");
const PRECACHE = [
  IS_STATIC ? "/offline/" : "/offline",
  "/static/css/style.css" + V,
  "/static/js/main.js" + V, "/static/js/plane.js" + V, "/static/js/hero.js" + V,
  "/static/js/visualisasi.js" + V, "/static/js/quiz.js" + V, "/static/js/games.js" + V,
  "/static/js/charts.js" + V,
  "/static/icons/icon-192.png", "/static/icons/icon-512.png", "/manifest.webmanifest",
].map((p) => BASE + p);
// halaman pribadi versi server (dashboard, profil, login) TIDAK disimpan di cache
const PUBLIC_PAGES = ["", "/offline", "/materi", "/contoh-soal", "/visualisasi", "/game", "/instal"];
// versi statis (GitHub Pages) tidak memiliki data pribadi di HTML, jadi semua halaman aman di-cache

function pagePath(url) {
  let p = url.pathname;
  if (p.startsWith(BASE)) p = p.slice(BASE.length);
  return p.replace(/\/(index\.html)?$/, "");
}

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(STATIC_CACHE)
      // credentials: "omit" → versi tamu (tanpa data akun) yang disimpan
      .then((cache) => Promise.all(PRECACHE.map((url) => cache.add(new Request(url, { credentials: "omit" })).catch(() => null))))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => !k.startsWith(VERSION)).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", (event) => {
  const req = event.request;
  if (req.method !== "GET") return;               // POST (jawaban, skor) selalu ke server
  const url = new URL(req.url);
  if (url.origin !== location.origin) {
    // font Google: cache-first
    if (url.hostname.endsWith("gstatic.com") || url.hostname.endsWith("googleapis.com")) {
      event.respondWith(caches.match(req).then((hit) => hit || fetch(req).then((res) => {
        const copy = res.clone(); caches.open(STATIC_CACHE).then((c) => c.put(req, copy)); return res;
      }).catch(() => hit)));
    }
    return;
  }
  const path = pagePath(url);
  if (path === "/keluar") {
    // hapus halaman tersimpan saat keluar (aman untuk perangkat bersama)
    event.waitUntil(caches.delete(PAGE_CACHE));
    return;
  }
  if (path.startsWith("/api/") || path === "/healthz") return;

  if (path.startsWith("/static/")) {
    // aset statis: cache-first
    event.respondWith(caches.match(req).then((hit) => hit || fetch(req).then((res) => {
      if (res.ok) { const copy = res.clone(); caches.open(STATIC_CACHE).then((c) => c.put(req, copy)); }
      return res;
    })));
    return;
  }

  if (req.mode === "navigate" || (req.headers.get("accept") || "").includes("text/html")) {
    // halaman: network-first, fallback ke cache lalu halaman offline
    event.respondWith(
      fetch(req).then((res) => {
        const isPublic = IS_STATIC || PUBLIC_PAGES.includes(path) || /^\/(game|kuis)\//.test(path);
        if (res.ok && isPublic) { const copy = res.clone(); caches.open(PAGE_CACHE).then((c) => c.put(req, copy)); }
        return res;
      }).catch(() => caches.match(req).then((hit) => hit || caches.match(BASE + "/offline")
        .then((off) => off || caches.match(BASE + "/offline/"))))
    );
  }
});
