<script lang="ts">
  import { onMount, getContext } from 'svelte';
  import { copyToClipboard } from "$lib/utils";
  import { faceUrl } from "$lib/stores"
  import { toast } from "svelte-sonner";
  const i18n = getContext('i18n');

  onMount(() => {
  
  });

  // 返回首页
  function gotoHome() {
    window.location.href = "https://test.degpt.ai"
  }

</script>

<div class="w-full flex flex-col">
  <div class="flex flex-col items-center w-full mt-8">
    <img class="w-[200px]" src="./icon/faceError.png" alt="icon"/>
    <span class="font-bold mt-2">{$i18n.t("KYC Certification Instructions")}</span>
  </div>
  <div class="flex flex-col mt-6 m-2 bg-gray-100 p-4 rounded-md">
    <span class="text-">{$i18n.t("Please follow the steps below:")}</span>
    <div class="flex flex-row items-center mt-2">
      <img class="size-8" src="./icon/copytip.png" alt=""/>
      <span class="text-sm ml-2">{$i18n.t("Click \"Copy Link\".")}</span>
    </div>
    <div class="flex flex-row items-center mt-2">
      <img class="size-8" src="./icon/browser.png" alt=""/>
      <span class="text-sm ml-2">{$i18n.t("Open your browser. Chrome, Firefox, Microsoft Edge and Safari on iOS 14.3 or later are all supported.")}</span>
    </div>
    <div class="flex flex-row items-center mt-2">
      <img class="size-8" src="./icon/miniocr.png" alt=""/>
      <span class="text-sm ml-2">{$i18n.t("Paste the copied link and enable identity certificate recognition.")}</span>
    </div>
    <div class="flex flex-row items-center mt-2">
      <img class="size-8" src="./icon/over.png" alt=""/>
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
    <button class="primaryButton text-lg text-white py-3 rounded-lg"
      on:click={() => {
        gotoHome()
      }}>
        {$i18n.t("Complete Authentication")}
      </button>
  </div>
</div>

