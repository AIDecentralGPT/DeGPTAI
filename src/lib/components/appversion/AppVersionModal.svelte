<script lang="ts">
  import { getContext } from "svelte";
  import { Browser } from '@capacitor/browser';

  import Modal from "../common/Modal.svelte";

  const i18n = getContext("i18n");

  let mousedownValid = false;
  let size = "sm";

  export let show = false;
  export let versionData = {versionName:"", desc:[], url: ""}
</script>

<Modal bind:show bind:mousedownValid bind:size>
  <div class="flex justify-center my-6">
    <div
      class="w-20 h-20 rounded-full bg-primary/10 flex items-center justify-center animate-float"
    >
      <svg
        class="icon"
        viewBox="0 0 1024 1024"
        version="1.1"
        xmlns="http://www.w3.org/2000/svg"
        width="45"
        height="45"
        ><path
          d="M584.064 560.2048l-72.1792 72.1792-48.128 48.128v72.1792l-72.1792 120.3072 48.128 24.064L608.128 728.6272l-24.064-168.4224z m-120.3072-120.3072l-168.4352-24.064L126.8992 584.2688l24.064 48.128 120.3072-72.1792h72.1792l48.128-48.128 72.1792-72.192z"
          fill="#CCCCCC"
        /><path
          d="M247.2064 656.448c-47.3984 69.1584-119.9872 154.4064-120.3072 192.4864-0.2432 28.928 18.9568 48.3584 48.128 48.128 38.6944-0.3328 120.4352-72.5632 192.4864-120.3072l-120.3072-120.3072z"
          fill="#FFCC66"
        /><path
          d="M319.3856 632.384c-47.3984 69.1584-144.3712 154.4064-144.3712 192.4992 0 25.1392 2.4192 24.064 24.064 24.064 38.6944 0 120.4352-96.6272 192.4864-144.3712l-72.1792-72.192z"
          fill="#ED7161"
        /><path
          d="M848.7424 127.0912C773.12 131.7632 642.56 140.7744 487.8208 295.5264 373.9904 409.344 274.1376 574.8608 227.328 684.6976l112.6912 112.6912c109.2224-46.3616 273.6256-146.4576 388.416-261.248C882.176 382.4 890.9312 251.392 896.8704 175.2192c2.6368-34.0096-16.6784-50.0736-48.128-48.128z"
          fill="#387AA7"
        /><path
          d="M848.7424 127.0912C773.12 131.7632 642.56 140.7744 487.8208 295.5264c-92.9152 92.9152-176.4224 220.2368-229.5296 323.6736l147.2 147.2128c102.8096-52.9664 229.3632-136.704 322.944-230.272C882.176 382.4 890.9312 251.392 896.8704 175.2192c2.6368-34.0096-16.6784-50.0736-48.128-48.128z"
          fill="#48A0DC"
        /><path
          d="M704.3712 319.5904m-96.2432 0a96.2432 96.2432 0 1 0 192.4864 0 96.2432 96.2432 0 1 0-192.4864 0Z"
          fill="#4D4D4D"
        /><path
          d="M704.3712 319.5904m-48.128 0a48.128 48.128 0 1 0 96.256 0 48.128 48.128 0 1 0-96.256 0Z"
          fill="#FFFFFF"
        /></svg
      >
    </div>
  </div>
  <!-- 标题区域 -->
  <div class="text-center mb-6">
    <h2 class="text-[clamp(1.5rem,5vw,2rem)] font-bold text-dark dark:text-white mb-2">
      {$i18n.t("Discovered a new version!")}
    </h2>
    <p class="text-gray-600 dark:text-gray-100">{versionData.versionName} {$i18n.t("Released. Upgrade now to experience more features")}</p>
  </div>
  <!-- 新功能列表 -->
  <div class="flex flex-col mx-8 mb-8 space-y-3">
    {#each JSON.parse(versionData?.desc) as item, index}
      <div class="flex items-center">
      <div
        class="mt-0.5 mr-3 w-5 h-5 rounded-full bg-[#B88E56] flex items-center justify-center flex-shrink-0
        text-gray-100"
      >
        {index + 1}
      </div>
      <div>
        <p class="text-gray-800 dark:text-gray-100 text-xl">{item[$i18n.language]}</p>
      </div>
    </div>
    {/each}
  </div>
  <div class="flex w-full">
    <button class="primaryButton w-full p-3 m-8 text-gray-50 rounded-lg"
    on:click={() => {
      Browser.open({ url: versionData?.url, presentationStyle: 'fullscreen' });
    }}>{$i18n.t("Upgrade now")}</button>
  </div>
</Modal>
