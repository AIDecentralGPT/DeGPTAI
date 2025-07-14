<script lang="ts">
  import { onMount, getContext } from 'svelte';
  import { facelivenessBindRes } from "$lib/apis/auths";
  import { copyToClipboard } from "$lib/utils";
  import { toast } from "svelte-sonner";
  import { goto } from '$app/navigation';
  const i18n = getContext('i18n');
  
  let status: any = null;
  let loading = true;
  let httpStatus = true;
  let message = "";
  let address = "";
  
  let userId = null;

  onMount(() => {
    // 获取URL中的参数
    const params = new URLSearchParams(window.location.search);
    userId = params.get("user_id");
    facelivenesdsBind();
  });

  // 用于发送消息的函数
  function facelivenesdsBind() {
    facelivenessBindRes({user_id: userId}).then(async (res) => {
      if (res) {
        loading = false;
        if (res.passed) {
          status = 'success';
          message = res.message;
        } else {
          status = 'fail';
          message = res.message;
          address = res.address;
        }
      } else {
        httpStatus = false;
      }
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
    window.location.href = "https://test.degpt.ai"
  }

</script>

<div class="container-main">
  {#if httpStatus}
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
      <p>{$i18n.t(message)}</p>
      {#if status==='success'}
        <p>{$i18n.t("Your kyc rewards have been credited.")}</p>
        <p>{$i18n.t("Please return to the software interface and click Complete.")}</p>
      {/if}
      {#if address}
        <div class="flex">
          <p class="w-[300px] dark:text-gray-500 dark:bg-gray-650 text-ellipsis overflow-hidden whitespace-nowrap">Wallet Adress: { address }</p>
          <button
            on:click={async () => {
              const res = await copyToClipboard(address);
              if (res) {
                toast.success($i18n.t("Copying to clipboard was successful!"));
              }
            }}
            type="button"
            class="px-3 py-2 text-sm-12 dark:text-gray-300 dark:bg-gray-650 rounded-md fs12"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="1em"
              height="1em"
              viewBox="0 0 512 512"
              ><rect
                width="336"
                height="336"
                x="128"
                y="128"
                fill="none"
                stroke="currentColor"
                stroke-linejoin="round"
                stroke-width="32"
                rx="57"
                ry="57"
              /><path
                fill="none"
                stroke="currentColor"
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="32"
                d="m383.5 128l.5-24a56.16 56.16 0 0 0-56-56H112a64.19 64.19 0 0 0-64 64v216a56.16 56.16 0 0 0 56 56h24"
              /></svg
            >
          </button>
        </div>        
      {/if}
      {#if status==='fail'}
        <button
          disabled={loading}
          class={" px-4 py-1 mt-2 primaryButton text-gray-100 transition rounded-lg fs-16"}
          style={loading ? "background: rgba(184, 142, 86, 0.6)" : ""}
          type="submit"
          on:click={async () => {
            gotoHome()
          }}
        >
          <span>{$i18n.t("Home")}</span>
        </button>
      {/if}
    {/if}
  {:else}
    <p>{$i18n.t('Request Exception, Please Retry')}</p>
    <button
      class="px-4 py-2 primaryButton text-gray-100 transition rounded-lg fs-16"
      on:click={refreshBind}>{$i18n.t('Refresh')}</button>
  {/if}
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

