self.addEventListener('fetch', (event) => {
  const url = new URL(event.request.url);
  console.log("============================", event.request.url, url)
  if (url.pathname === '/api/stream') {
    event.respondWith(
      fetch(event.request).then(response => {
        // 保持流式连接
        return response;
      })
    );
  }
});