<script lang="ts">
  import { onMount, getContext } from 'svelte';
  import { WEBUI_API_BASE_URL } from '$lib/constants';
  import { copyToClipboard } from "$lib/utils";
  import { toast } from "svelte-sonner";
  import { goto } from '$app/navigation';
  const i18n = getContext('i18n');
  
  
  let userId:any = null;
  let httpStatus = true;
  let progress_finish = false;
  let progress_status = [
    {'type': 1, 'progress': 0, 'flag': false, 'passedInfo': {'message': '', 'address': ''}},
    {'type': 2, 'progress': 0, 'flag': false}
  ];
  // 用于发送消息的函数
  async function facelivenesdsBind() {
    const response = await fetch(`${WEBUI_API_BASE_URL}/auths/faceliveness_bind`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({user_id: userId, stream: true})
    }).catch(() => {
      httpStatus = false;
    });

    if (httpStatus) {
      const reader = response?.body.getReader();
      const decoder = new TextDecoder('utf-8');

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        const progressData = decoder.decode(value);
        const pattern = /\[([^\]]+)\]/;
        const match = progressData.match(pattern);
        if (match) {
          if (match[1] === 'done') {
            progress_finish = true;
          } else {
            progress_status = JSON.parse("[" + match[1] + "]");
          }
        }
      }
    }
    progress_finish = true;
  }

  // 重新加载页面
  async function initBind() {
    httpStatus = true;
    progress_finish = false;
    progress_status = [
      {'type': 1, 'progress': 0, 'flag': false, 'passedInfo': {'message': '', 'address': ''}},
      {'type': 2, 'progress': 0, 'flag': false}
    ];
    await facelivenesdsBind();
  }

  // 返回首页
  function gotoHome() {
    goto(`/`);
  }

  onMount(async () => {
    // 获取URL中的参数
    const params = new URLSearchParams(window.location.search);
    userId = params.get("user_id");
    await initBind();
  });

</script>

<div class="flex flex-col justify-center items-center mt-20">
  <img class="size-20" src='./static/logo.png' alt="logo"/>
  {#if progress_finish}
    <span class="font-bold text-3xl mt-2">{ $i18n.t("AUTHENTICATED") }</span>
  {:else}
    <span class="font-bold text-3xl mt-2">{ $i18n.t("AUTHENTICATING") }</span>
  {/if}
  
  <div class="flex flex-col w-full px-2 mt-8">
    <div class="flex justify-between px-1">
      <span class="text-base font-bold">{ $i18n.t("KYC AUTHENTICATION") }</span>
      {#if progress_finish}
        {#if progress_status[0].flag}
          <span class="text-sm font-bold text-green-600">{ $i18n.t("SUCCESS") }</span>
        {:else}
          <span class="text-sm font-bold text-red-600">{ $i18n.t("FAIL") }</span>
        {/if}
      {:else}
        <svg class="animate-spin ml-2"
          xmlns="http://www.w3.org/2000/svg"
          width="1em"
          height="1em"
          viewBox="0 0 24 24">
            <path fill="#000000"
              d="M12 20q-3.35 0-5.675-2.325T4 12t2.325-5.675T12 4q1.725 0 3.3.712T18 6.75V4h2v7h-7V9h4.2q-.8-1.4-2.187-2.2T12 6Q9.5 6 7.75 7.75T6 12t1.75 4.25T12 18q1.925 0 3.475-1.1T17.65 14h2.1q-.7 2.65-2.85 4.325T12 20"/>
        </svg>
      {/if}
    </div>
    <div class="w-full h-[20px] bg-gray-500 rounded-lg">
      <div class="h-[20px] bg-green-300 rounded-lg"
        style='{"width:" + progress_status[0].progress + "%"}'>
      </div>
    </div>
  </div>

  <div class="flex flex-col w-full px-2 mt-5">
    <div class="flex justify-between px-1">
      <span class="text-base font-bold">{ $i18n.t("REWARD CREDIT") }</span>
      {#if progress_finish}
        {#if progress_status[1].flag}
          <span class="text-sm font-bold text-green-600">{ $i18n.t("SUCCESS") }</span>
        {:else}
          <span class="text-sm font-bold text-red-600">{ $i18n.t("FAIL") }</span>
        {/if}
      {:else}
        <svg class="animate-spin ml-2"
          xmlns="http://www.w3.org/2000/svg"
          width="1em"
          height="1em"
          viewBox="0 0 24 24">
            <path fill="#000000"
              d="M12 20q-3.35 0-5.675-2.325T4 12t2.325-5.675T12 4q1.725 0 3.3.712T18 6.75V4h2v7h-7V9h4.2q-.8-1.4-2.187-2.2T12 6Q9.5 6 7.75 7.75T6 12t1.75 4.25T12 18q1.925 0 3.475-1.1T17.65 14h2.1q-.7 2.65-2.85 4.325T12 20"/>
        </svg>
      {/if}
    </div>
    <div class="w-full h-[20px] bg-gray-500 rounded-lg">
      <div class="h-[20px] bg-green-300 rounded-lg"
        style='{"width:" + progress_status[1].progress + "%"}'>
      </div>
    </div>
  </div>
  
  <div class="w-full px-2 py-5">
    {#if httpStatus}
      {#if progress_finish}
        <button class="w-full py-2 primaryButton text-gray-100 transition rounded-lg text-base"
          on:click={gotoHome}>{$i18n.t('Home')}</button>
      {/if}
    {:else}
      <button class="w-full py-2 primaryButton text-gray-100 transition rounded-lg text-base"
      on:click={initBind}>{$i18n.t('Refresh')}</button>
    {/if} 
  </div>
  

  <div class="w-full text-left px-2">
    {#if progress_finish}
      <span class="text-sm ml-1">{ $i18n.t("AUTHENTICATION RESULT") }:</span>
      <div class="flex flex-col border border-gray-300 rounded-lg p-2">
        {#if progress_status[0].flag}
          <span class="text-sm">{ $i18n.t("INFO") }: { $i18n.t(progress_status[0].passedInfo?.message) }</span>
        {:else}
          <span class="text-sm">{ $i18n.t("INFO") }: { $i18n.t(progress_status[0].passedInfo?.message) }</span>
          {#if progress_status[0]?.passedInfo?.address}
            <div class="flex items-center">
              <span class="w-[300px] text-sm text-ellipsis overflow-hidden whitespace-nowrap">{ $i18n.t("Wallet Adress") }: { progress_status[0].passedInfo?.address }</span>
              <button
                on:click={async () => {
                  const res = await copyToClipboard(progress_status[0].passedInfo?.address);
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
        {/if}
        {#if progress_status[1].flag}
          <span class="text-sm">{ $i18n.t("INFO") }: {$i18n.t("Your kyc rewards have been credited.")}</span>
        {:else}
          <span class="text-sm">{ $i18n.t("INFO") }: {$i18n.t("Your kyc rewards have not been credited.")}</span>
        {/if}
      </div>
    {/if}
  </div>
  
</div>

<style>
</style>