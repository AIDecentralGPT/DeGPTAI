<script lang="ts">
  import { onMount, getContext } from 'svelte';
  import { WEBUI_API_BASE_URL } from '$lib/constants';
  import { goto } from '$app/navigation';
  const i18n = getContext('i18n');
  
  let status: any = null;
  let loading = true;
  let httpStatus = true;
  let message = "";
  let address = "";
  
  let userId:any = null;

  onMount(() => {
    // 获取URL中的参数
    const params = new URLSearchParams(window.location.search);
    userId = params.get("user_id");
    console.log("===========================");
    facelivenesdsBind();
  });

  // 用于发送消息的函数
  function facelivenesdsBind() {
    fetch(`${WEBUI_API_BASE_URL}/auths/faceliveness_bind`, {
      method: "POST",
      headers: {
        "Accept": "text/event-stream"
      },
      body: JSON.stringify({user_id: userId}),
    }).then(response => {
      console.log("====================", response);
      // setTimeout(() => {
      //   facelivenesdsBind();
      // }, 500);
    })
  }

  // 重新加载页面
  function refreshBind() {
    status = null;
    loading = true;
    httpStatus = true;
    message = "";
    facelivenesdsBind();
  }

  // 返回首页
  function gotoHome() {
    goto(`/`);
  }

</script>

<div class="container-main">
  
</div>

<style>
  .container-main {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 100vh;
    width: 100%;
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
  .fs-16 {
    font-size: 16px;
  }
</style>

