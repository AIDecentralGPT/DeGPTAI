console.log('Service Worker script started execution');

self.addEventListener('install', (event) => {
  console.log('Before entering install event listener');
});
// self.addEventListener('fetch', (event) => {
//   console.log("============================");
//   const url = new URL(event.request.url);
//   if (url.pathname === '/api/stream') {
//     event.respondWith(
//       fetch(event.request).then(response => {
//         // 保持流式连接
//         return response;
//       })
//     );
//   }
// });