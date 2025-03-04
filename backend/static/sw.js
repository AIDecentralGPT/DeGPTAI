console.log('Service Worker script started execution');

self.addEventListener('install', (event) => {
  console.log('Before entering install event listener');
  event.waitUntil(
    // You can add some operations that need to be performed during installation here, such as caching resources
    Promise.resolve()
      .then(() => {
        // Skip the waiting phase and activate the new one immediately Service Worker
        return self.skipWaiting();
      })
  );
});

// self.addEventListener('fetch', (event) => {
//   const url = new URL(event.request.url);
//   if (url.pathname === '/api/v0/chat/completion/proxy') {
//     event.respondWith(
//       fetch(event.request).then(response => {
//         return response;
//       })
//     );
//   }
// });

self.addEventListener('fetch', (event) => {
  const url = new URL(event.request.url);
  if (url.pathname === '/api/v0/chat/completion/proxy') {
    event.respondWith(
      new Promise((resolve) => {
        // Maintain activity through regular heartbeats
        const heartbeat = setInterval(() => {
          new BroadcastChannel('sw-heartbeat').postMessage('ping');
        }, 5000);

        fetch(event.request)
          .then(resolve)
          .catch(() => caches.match(event.request))
          .finally(() => clearInterval(heartbeat));
      })
    );
  }
});