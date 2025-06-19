<script lang="ts">
  import { onMount, getContext } from 'svelte';
  import { copyToClipboard } from "$lib/utils";
  import { faceUrl, user, showUserVerifyModal } from "$lib/stores"
  import { toast } from "svelte-sonner";
  import { getUserInfo } from "$lib/apis/users";
  import { goto } from '$app/navigation';

  const i18n = getContext('i18n');

  onMount(() => {
  
  });

  // 上一页
  async function gotoLastPage() {
    $showUserVerifyModal = true;
    goto("/");
  }

  // 返回首页
  async function gotoHome() {
    const userInfo = await getUserInfo(localStorage.token);
    await user.set({
      ...$user,
      verified: userInfo?.verified,
    });
    $showUserVerifyModal = false;
    goto("/");
  }

</script>

<div class="w-full flex flex-col">
  <div class="flex flex-col items-center w-full mt-8">
    <img class="w-[160px]" src="/static/icon/faceError.png" alt="icon"/>
    <span class="font-bold mt-2">{$i18n.t("KYC Certification Instructions")}</span>
  </div>
  <div class="flex flex-col mt-6 m-2 bg-gray-100 p-4 rounded-md">
    <span class="text-">{$i18n.t("Please follow the steps below:")}</span>
    <div class="flex flex-row items-center mt-2">
      <img class="size-8" src="/static/icon/copytip.png" alt=""/>
      <span class="text-sm ml-2">{$i18n.t("Click \"Copy Link\".")}</span>
    </div>
    <div class="flex flex-row items-center mt-2">
      <img class="size-8" src="/static/icon/browser.png" alt=""/>
      <span class="text-sm ml-2">{$i18n.t("Open your browser. Chrome, Firefox, Microsoft Edge and Safari on iOS 14.3 or later are all supported.")}</span>
    </div>
    <div class="flex flex-row items-center mt-2">
      <img class="size-8" src="/static/icon/miniocr.png" alt=""/>
      <span class="text-sm ml-2">{$i18n.t("Paste the copied link and enable identity certificate recognition.")}</span>
    </div>
    <div class="flex flex-row items-center mt-2">
      <img class="size-8" src="/static/icon/over.png" alt=""/>
      <span class="text-sm ml-2">{$i18n.t("After authentication, return to the APP and click \"Complete Authentication\".")}</span>
    </div>
    <button class="primaryButton ml-2 text-sm text-white px-4 py-2 rounded-lg mt-6"
      on:click={async () => {
        const res = await copyToClipboard($faceUrl.url, false);
        if (res) {
          toast.success($i18n.t("Copying to clipboard was successful!"));
        }
      }}>
      {$i18n.t("Copy Link")}
    </button>
  </div>
  <div class="flex flex-col w-full py-4 px-6">
    <button class="primaryButton text-lg text-white py-2 rounded-lg"
      on:click={() => {
        gotoLastPage()
      }}>
      {$i18n.t("Previous")}
    </button>
    <button class="primaryButton text-lg text-white py-2 rounded-lg mt-2"
      on:click={() => {
        gotoHome()
      }}>
      {$i18n.t("Complete Authentication")}
    </button>
  </div>
</div>

