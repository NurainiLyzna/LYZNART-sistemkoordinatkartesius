/* LYZNART service worker */
const VERSION = "lyznart-v1.0.0";
const STATIC_CACHE = VERSION + "-static";
const PAGE_CACHE = VERSION + "-pages";
const PRECACHE = [
  "/", "/offline", "/materi", "/contoh-soal", "/visualisasi", "/game", "/instal",
  "/static/css/style.css?v=1.0.0",
  "/static/js/main.js?v=1.0.0", "/static/js/plane.js?v=1.0.0", "/static/js/hero.js?v=1.0.0",
  "/static/js/visualisasi.js?v=1.0.0", "/static/js/quiz.js?v=1.0.0", "/static/js/games.js?v=1.0.0",
  "/static/js/charts.js?v=1.0.0",
  "/static/icons/icon-192.png", "/static/icons/icon-512.png", "/manifest.webmanifest",
];

// halaman pribadi (dashboard, profil, login) TIDAK disimpan di cache
const PUBLIC_PAGES = ["/", "/offline", "/materi", "/contoh-soal", "/visualisasi", "/game", "/instal"];

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
  if (url.pathname === "/keluar") {
    // hapus halaman tersimpan saat keluar (aman untuk perangkat bersama)
    event.waitUntil(caches.delete(PAGE_CACHE));
    return;
  }
  if (url.pathname.startsWith("/api/") || url.pathname === "/healthz") return;

  if (url.pathname.startsWith("/static/")) {
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
        const isPublic = PUBLIC_PAGES.includes(url.pathname) || /^\/(game|kuis)\//.test(url.pathname);
        if (res.ok && !res.redirected && isPublic) { const copy = res.clone(); caches.open(PAGE_CACHE).then((c) => c.put(req, copy)); }
        return res;
      }).catch(() => caches.match(req).then((hit) => hit || caches.match("/offline")))
    );
  }
});
