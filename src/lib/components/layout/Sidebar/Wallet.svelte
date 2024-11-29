<script lang="ts">
  import { getContext } from "svelte";
  import {
    showSidebar,
    showNewWalletModal,
    showOpenWalletModal,
    showPriceModal,
    showLoginInfoModal,
    user,
    mobile
  } from "$lib/stores";
  import DbcAccountDetail from "$lib/components/wallet/DbcAccountDetail.svelte";
  import WalletConnect from "$lib/components/wallet/WalletConnect.svelte";
  import { goto } from "$app/navigation";
  
  const i18n = getContext("i18n");

  export let show = false;
  export let role = "";
  export let className = "max-w-[240px]";
</script>

<div name="content">
  <hr class=" dark:border-gray-800 my-1 p-0" />

  {#if $showLoginInfoModal}
    <div class="flex flex-row gap-2 px-3">
      <!-- 升级计划 -->
      <button
        on:click={() => {
          $showPriceModal = true;
        }}
        class="w-full px-4 py-2 primaryButton text-gray-100 transition rounded-lg mt-2 mb-2"
      > 
        {#if $user?.isPro}
          <div class="text-white text-center text-sm leading-4">VIP</div>       
          <div class="flex-1 flex flex-row text-xs justify-center items-center leading-3">
            {$i18n.t("Valid until")} {$user?.proEndDate}
          </div>
        {:else}
          <span class="relative">{$i18n.t("Upgrade Plan")}</span>
        {/if}
      </button>
      <button class="w-[50px] px-4 py-2 primaryButton text-gray-100 transition rounded-lg mt-2 mb-2"
        on:click={async () => {
          await goto("/");
          const newChatButton = document.getElementById("new-chat-button");
          setTimeout(() => {
            newChatButton?.click();
            if ($mobile) {
              showSidebar.set(false);
            }
          }, 0);
        }}>
        <svg class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" width="20" height="20">
          <path d="M786.88711111 644.43733333c45.51111111-58.70933333 72.81777778-132.43733333 72.81777778-212.53688888 0-192.05688889-155.648-347.70488889-347.70488889-347.7048889s-347.70488889 155.648-347.70488889 347.7048889c0 80.09955555 27.30666667 153.37244445 72.81777778 212.53688888L84.19555555 797.80977778h142.44977778v142.44977777l177.49333334-177.49333333c33.67822222 10.92266667 70.08711111 17.29422222 107.40622222 17.29422223s73.728-5.91644445 107.40622222-17.29422223l177.49333334 177.49333333v-142.44977777H939.80444445l-152.91733334-153.37244445z m-162.92977778-66.90133333L512 519.28177778l-111.95733333 58.70933333 21.39022222-124.70044444-91.02222222-88.29155556 125.15555555-18.20444444 55.97866667-113.77777778 55.97866666 113.77777778 125.15555556 18.20444444-90.112 88.29155556 21.39022222 124.24533333z" fill="#ffffff"></path>
        </svg>
      </button>
    </div>
  {/if}
  
  <!-- 第三方方式登录钱包 -->
  <WalletConnect />

  <!-- 创建，连接，打开钱包，三个按钮 -->
  {#if !($user?.id && $user?.id?.startsWith('0x'))}
    <div>
      <button
        class="flex rounded-md py-2 px-3 w-full hover:bg-gray-50 dark:hover:bg-gray-800 transition"
        on:click={async () => {
          $showNewWalletModal = true;
        }}
      >
        <div class=" self-center mr-3">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="1.4em"
            height="1.4em"
            viewBox="0 0 24 24"
            ><path
              fill="currentColor"
              d="M20 6h-8l-2-2H4c-1.11 0-1.99.89-1.99 2L2 18c0 1.11.89 2 2 2h16c1.11 0 2-.89 2-2V8c0-1.11-.89-2-2-2m0 12H4V6h5.17l2 2H20zm-8-4h2v2h2v-2h2v-2h-2v-2h-2v2h-2z"
            /></svg
          >
        </div>
        <div class=" self-center font-medium">{$i18n.t("Create Wallet")}</div>
      </button>

      <button
        class="flex rounded-md py-2 px-3 w-full hover:bg-gray-50 dark:hover:bg-gray-800 transition"
        on:click={async () => {
          $showOpenWalletModal = true;
        }}
      >
        <div class=" self-center mr-3">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="1.4em"
            height="1.4em"
            viewBox="0 0 512 512"
            ><rect
              width="416"
              height="288"
              x="48"
              y="144"
              fill="none"
              stroke="currentColor"
              stroke-linejoin="round"
              stroke-width="32"
              rx="48"
              ry="48"
            /><path
              fill="none"
              stroke="currentColor"
              stroke-linejoin="round"
              stroke-width="32"
              d="M411.36 144v-30A50 50 0 0 0 352 64.9L88.64 109.85A50 50 0 0 0 48 159v49"
            /><path
              fill="currentColor"
              d="M368 320a32 32 0 1 1 32-32a32 32 0 0 1-32 32"
            /></svg
          >
        </div>
        <div class=" self-center font-medium">{$i18n.t("Open Wallet")}</div>
      </button>
    </div>
  {/if}

  <!-- 钱包数据面板 -->
  <!-- {#if $user?.id?.startsWith('0x') && $user?.address_type === 'dbc'} -->
  {#if $user?.id?.startsWith('0x')}
    <DbcAccountDetail />
  {/if}
</div>

<style>

</style>
