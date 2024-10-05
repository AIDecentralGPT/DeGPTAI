<script>
  import { onMount, getContext } from 'svelte';
  import { goto } from '$app/navigation';
  import { WEBUI_API_BASE_URL } from "$lib/constants";
  const i18n = getContext('i18n');

  let message = $i18n.t('Loading ...');
  
  let ws;
  let status = null;
  let loading = true;

  // 在组件挂载时打开 WebSocket 连接
  onMount(() => {
    // 获取URL中的参数
    const params = new URLSearchParams(window.location.search);
    const userId = params.get("user_id");
    let socketUrl = '';
    if (WEBUI_API_BASE_URL.includes('https://')) {
      socketUrl = WEBUI_API_BASE_URL.replace('https://', 'wss://')
    } else {
      socketUrl = WEBUI_API_BASE_URL.replace('http://', 'ws://')
    }
    ws = new WebSocket(`${socketUrl}/auths/ws/${userId}`);

    ws.onopen = () => {
      console.log("WebSocket connection established");
      // 连接成功后立即发送验证请求
      sendMessage($i18n.t('start_verification'));
    };

    ws.onerror = (error) => {
      console.error("WebSocket error: ", error);
      message = $i18n.t('connection_error');
      status = 'error';
    };

    // 监听 WebSocket 消息事件
    ws.addEventListener("message", (event) => {
      // 将收到的消息添加到 messages 列表中
      console.log("Received:", event.data);
      loading = false;
      if (event.data.startsWith("True")) {
        message = $i18n.t('verification_success');
        status = 'success';
      } else if (event.data.startsWith("False")) {
        message = event.data.substring(6);
        status = 'fail';
      } else {
        message = $i18n.t('Verifying the effectiveness of face detection');
      }
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
    sendMessage($i18n.t('verification_request_data'));
    message = $i18n.t('verification_request_sent');
        goto("/?verifyAgain=true");
  }
</script>

<div class="container">
  {#if loading}
    <div class="loading-container">
      <div class="loading"></div>
      <div class="loading-tip">Loading...</div>
    </div>
  {:else}
    <p>{message}</p>
  {/if}

  <!-- {#if status==='success'}
    <button on:click={handleSendVerification}>{$i18n.t('return_home')}</button>
  {/if}
  {#if status==='fail'}
    <button
      class="px-4 py-2 primaryButton text-gray-100 transition rounded-lg"
      on:click={handleSendVerification}>{$i18n.t('try_again')}</button>
  {/if}
  {#if status==='error'}
    <button 
      class="px-4 py-2 primaryButton text-gray-100 transition rounded-lg"
      on:click={handleSendVerification}>{$i18n.t('try_again')}</button>
  {/if} -->
</div>

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
  .loading-container {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 200px;
    height: 200px;
    background: #9E9E9E;
    border-radius: 10px;
  }
  .loading {
    width: 80px;
    height: 80px;
    border: 10px solid #5F5F5F;
    border-top: 10px solid #ffffff;
    border-radius: 50%;
    animation: spin 2s linear infinite;
    margin-top: 50px;
    margin-left: 50px;
  }
  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
  .loading-tip {
    width: 200px;
    text-align: center;
    margin-top: 12px;
    color: #393939;
    font-size: 20px;
  }
</style>

