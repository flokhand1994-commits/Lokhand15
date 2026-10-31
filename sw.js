const CACHE = 'dutch-v10';
const ASSETS = [
  './',
  './index.html',
  './stories.html',
  './gutenberg.html',
  './wablieft.html',
  './dutch_nouns.js',
  './dutch_stories.js',
  './gutenberg_stories.js',
  './manifest.webmanifest',
  './icons/icon.svg'
];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(ASSETS)));
  self.skipWaiting();
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  const url = new URL(e.request.url);
  // Only handle this site's own GET requests; let translation calls etc. go straight to the network
  if (e.request.method !== 'GET' || url.origin !== self.location.origin) return;
  // Network first, so new versions of pages and stories appear; fall back to cache when offline
  e.respondWith(
    fetch(e.request)
      .then(res => {
        if (res.ok) { const copy = res.clone(); caches.open(CACHE).then(c => c.put(e.request, copy)); }
        return res;
      })
      .catch(() => caches.match(e.request).then(r => r || caches.match('./index.html')))
  );
});

self.addEventListener('message', e => {
  if (e.data === 'skipWaiting') self.skipWaiting();
});
