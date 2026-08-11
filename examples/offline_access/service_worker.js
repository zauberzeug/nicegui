// Service worker that makes the app usable offline.
//
// It pre-caches a self-contained "/offline" page. While online, requests go to
// the network as usual (so the live NiceGUI app works normally). When a
// navigation fails because the device or server is offline, the cached offline
// page is served instead.

const CACHE = 'offline-access-v1';
const PRECACHE = ['/offline', '/manifest.webmanifest'];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE)
      .then((cache) => cache.addAll(PRECACHE))
      .then(() => self.skipWaiting()),
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((key) => key !== CACHE).map((key) => caches.delete(key))))
      .then(() => self.clients.claim()),
  );
});

self.addEventListener('fetch', (event) => {
  const { request } = event;
  if (request.method !== 'GET') return;
  // Page navigations: try the live app first, fall back to the cached offline page.
  if (request.mode === 'navigate') {
    event.respondWith(fetch(request).catch(() => caches.match('/offline')));
    return;
  }
  // Other GET requests (e.g. the manifest): fall back to the cache when offline.
  event.respondWith(fetch(request).catch(() => caches.match(request)));
});
