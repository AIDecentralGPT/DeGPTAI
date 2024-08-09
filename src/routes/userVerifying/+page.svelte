<script>
  import { onMount } from "svelte";
	import { goto } from '$app/navigation';

  let message = "正在验证中...";
  let ws;

  // 在组件挂载时打开 WebSocket 连接
  onMount(() => {
    // 获取URL中的参数
    const params = new URLSearchParams(window.location.search);
    const userId = params.get("user_id");

    ws = new WebSocket(`ws://43.242.202.166:8080/api/v1/auths/ws/${userId}`);

    ws.onopen = () => {
      console.log("WebSocket connection established");
      // 连接成功后立即发送验证请求
      sendMessage("开始验证");
    };

    ws.onerror = (error) => {
      console.error("WebSocket error: ", error);
      message = "连接错误，请稍后重试。";
    };

    // 监听 WebSocket 消息事件
    ws.addEventListener("message", (event) => {
      // 将收到的消息添加到 messages 列表中
      console.log("Received:", event.data);

			if (event.data === "True") {
				message = "验证成功，请返回 OllamaHub 继续操作。";
			}
			 else if (event.data === "False") {
				message = "验证失败，请重新验证。";
				goto("/");

			}
			
			else {
				message = "验证中...";
			}

      
      // messages = [...messages, event.data];
    });

    ws.onclose = () => {
      console.log("WebSocket connection closed");
    };
  });

  // 用于发送消息的函数
  function sendMessage(data) {
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(data);
      console.log("Sent:", data);
    } else {
      console.error("WebSocket is not open");
    }
  }

  // 示例：当用户点击按钮时发送消息
  function handleSendVerification() {
    sendMessage("验证请求数据");
    message = "验证请求已发送，请稍等...";
  }
</script>

<div class="container">
  <p>{message}</p>
  <button on:click={handleSendVerification}>发送验证请求</button>
</div>

<!-- <script lang="ts">

	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';

	onMount(async () => {
		window.addEventListener('message', async (event) => {
			if (
				![
					'https://ollamahub.com',
					'https://www.ollamahub.com',
					'https://openwebui.com',
					'https://www.openwebui.com',
					'http://localhost:5173'
				].includes(event.origin)
			)
				return;
			const prompts = JSON.parse(event.data);
			sessionStorage.modelfile = JSON.stringify(prompts);

			goto('/workspace/prompts/create');
		});

		if (window.opener ?? false) {
			window.opener.postMessage('loaded', '*');
		}
	});
</script> -->

<style>
  .container {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 100vh;
    font-size: 1.5rem;
    text-align: center;
  }
  button {
    margin-top: 20px;
    padding: 10px 20px;
    font-size: 1rem;
  }
</style>
