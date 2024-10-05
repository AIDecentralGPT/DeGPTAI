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
      status = 'fail';
      if (event.data.startsWith("True")) {
        message = $i18n.t('verification_success');
        status = 'success';
      } else if (event.data.startsWith("False")) {
        message = event.data.substring(6);
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
    {#if status==='success'}
      <svg xmlns="http://www.w3.org/2000/svg"
        class="icon" 
        viewBox="0 0 1024 1024" 
        version="1.1"
        width="128" 
        height="128">
          <path d="M877.397333 240.170667c-110.762667-47.658667-208.512-105.173333-289.450666-170.410667a119.978667 119.978667 0 0 0-151.893334 0C355.114667 135.04 257.365333 192.512 146.602667 240.213333A31.317333 31.317333 0 0 0 128 269.056v257.109333C128 748.672 455.765333 981.333333 512 981.333333c56.234667 0 384-232.661333 384-455.168V269.056a31.317333 31.317333 0 0 0-18.602667-28.885333z m-176.170666 175.786666l-224.298667 236.288a28.842667 28.842667 0 0 1-20.992 9.130667 28.842667 28.842667 0 0 1-20.992-9.130667l-112.213333-118.186666a32.426667 32.426667 0 0 1-8.064-30.421334 30.549333 30.549333 0 0 1 21.205333-22.357333 28.714667 28.714667 0 0 1 28.885333 8.533333l91.178667 96.042667 203.264-214.186667a28.629333 28.629333 0 0 1 42.026667 0 32.469333 32.469333 0 0 1 0 44.245334z" fill="#11B648"></path>
      </svg>
    {:else}
      <svg xmlns="http://www.w3.org/2000/svg"
        class="icon" 
        viewBox="0 0 1024 1024" 
        version="1.1" 
        width="128" 
        height="128">
          <path d="M826.88 200.528c23.36 1.056 41.424 20.176 40.368 43.536v268.672c0 138.048-71.152 265.488-187.968 338.752l-82.832 52.032-59.472 37.168c-13.792 8.496-31.84 8.496-46.72 0l-59.472-37.168-82.816-52.032C231.152 778.208 160 650.784 160 512.736V245.12c0-23.36 18.048-43.552 41.408-44.608 59.472-4.24 117.888-19.12 173.104-42.48 33.984-14.864 84.96-48.848 114.688-70.08 14.864-10.624 36.096-10.624 50.976 0 29.728 21.232 80.704 55.216 113.616 70.08 55.216 23.36 113.632 38.24 173.104 42.48zM506.192 686.544a40.72 40.72 0 1 0 0-81.44 40.72 40.72 0 0 0 0 81.44zM508 288A28 28 0 0 0 480 316v229.088a28 28 0 0 0 56 0V316A28 28 0 0 0 508 288z" fill="#F36A5A"></path>
      </svg>
    {/if}
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
    width: 160px;
    height: 160px;
    background: #9E9E9E;
    border-radius: 10px;
  }
  .loading {
    width: 60px;
    height: 60px;
    border: 5px solid #5F5F5F;
    border-top: 5px solid #ffffff;
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
    width: 160px;
    text-align: center;
    margin-top: 12px;
    color: #393939;
    font-size: 16px;
  }
</style>

