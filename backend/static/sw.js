console.log('Service Worker script started execution');

self.addEventListener('install', (event) => {
  console.log('Before entering install event listener');
  event.waitUntil(
    // 可以在这里添加一些安装时需要执行的操作，例如缓存资源
    Promise.resolve()
      .then(() => {
        // 跳过等待阶段，立即激活新的 Service Worker
        return self.skipWaiting();
      })
  );
});

// self.addEventListener('fetch', (event) => {
//   const url = new URL(event.request.url);
//   if (url.pathname === '/api/v0/chat/completion/proxy') {
//     event.respondWith(
//       fetch(event.request).then(response => {
//         // 保持流式连接
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
        // 通过定期心跳保持活跃
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