<script>
  import { onMount, getContext } from 'svelte';
  import { goto } from '$app/navigation';
  const i18n = getContext('i18n');

  let message = $i18n.t('Verifying the effectiveness of face detection');
  
  let ws;
  let status = null;

  // 在组件挂载时打开 WebSocket 连接
  onMount(() => {
    // 获取URL中的参数
    const params = new URLSearchParams(window.location.search);
    const userId = params.get("user_id");

    ws = new WebSocket(`wss://test.degpt.ai/api/v1/auths/ws/${userId}`);

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

      if (event.data.startsWith("True")) {
        message = $i18n.t('verification_success');
        status = 'success';
        goto("/?verifyAgain=true");
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
  <p>{message}</p>

  {#if status==='success'}
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
  {/if}
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
  button {
    margin-top: 20px;
    padding: 10px 20px;
    font-size: 1rem;
  }
</style>

