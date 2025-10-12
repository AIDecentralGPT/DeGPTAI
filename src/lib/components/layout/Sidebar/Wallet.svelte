<script lang="ts">
  import { onMount, getContext } from "svelte";
  import {
    showSidebar,
    showNewWalletModal,
    showOpenWalletModal,
    showPriceModal,
    user,
    mobile,
    binanceFlag,
    channel
  } from "$lib/stores";
  import DbcAccountDetail from "$lib/components/wallet/DbcAccountDetail.svelte";
  import { handleWalletSignIn } from "$lib/utils/wallet/ether/utils";
  // import WalletConnect from "$lib/components/wallet/WalletConnect.svelte";
  // import { goto } from "$app/navigation";
  import { binanceprovider } from "$lib/utils/wallet/ether/binance";

  const i18n = getContext("i18n");

  export let show = false;
  export let role = "";
  export let className = "max-w-[240px]";

  async function connectBinanceWallet() {
    try {
      // 切换到BSC主网
      await binanceprovider.request({
        method: 'wallet_switchEthereumChain',
        params: [{ chainId: '0x38' }] // BSC主网
      });
      let accounts = await binanceprovider.enable();
      // 调用 connect 方法，会唤起钱包授权
      accounts = await binanceprovider.request({
        method: 'eth_accounts' 
      });
      if (accounts?.length) {
        console.log("TON 账户地址:", accounts[0]);
        await handleWalletSignIn({
          walletImported: {
            address: accounts[0],
          },
          address_type: "threeSide",
          channel: $channel,
        });
      }
    } catch (error) {
      console.error("connection rejected:", error);
    }
  }

  onMount(async () => {
    if ($binanceFlag) {
      await connectBinanceWallet();
    } 
  });
</script>

<div name="content">
  <hr class=" dark:border-gray-800 my-1 p-0" />

  <div class="flex flex-row gap-2 px-2">
    <!-- 升级计划 -->
    <button
      on:click={() => {
        $showPriceModal = true;
      }}
      class="w-full px-4 py-2 primaryButton text-gray-100 transition rounded-lg mt-2 mb-2"
    >
      {#if $user?.vipInfo && $user?.vipInfo?.length > 0}
        {#if $user?.vipInfo?.length > 0}
          <div class="text-white text-center text-sm leading-4">
            {$user?.vipInfo[0]?.vip == "basic"
              ? $i18n.t("Basic VIP")
              : $user?.vipInfo[0]?.vip == "pro"
              ? $i18n.t("Pro VIP")
              : $i18n.t("Standard VIP")}
          </div>
          <div
            class="flex-1 flex flex-row text-xs justify-center items-center leading-3 mt-1"
          >
            {$i18n.t("Valid until")}
            {$user?.vipInfo[0].end_date}
          </div>
        {/if}
      {:else}
        <span class="relative">{$i18n.t("Upgrade Plan")}</span>
      {/if}
    </button>
  </div>

  <!-- 第三方方式登录钱包 -->
  <!-- <WalletConnect /> -->

  <!-- 创建，连接，打开钱包，三个按钮 -->
  {#if !($user?.id && $user?.id?.startsWith("0x"))}
    <div>
      {#if $binanceFlag}
        <button
          class="flex rounded-md py-2 px-2 w-full hover:bg-gray-50 dark:hover:bg-gray-800 transition"
          on:click={async () => {
            await connectBinanceWallet();
          }}
        >
          <div class=" self-center mr-3">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="1.4em"
              height="1.4em"
              viewBox="0 0 512 512"
            >
              <rect
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
              />
              <path
                fill="none"
                stroke="currentColor"
                stroke-linejoin="round"
                stroke-width="32"
                d="M411.36 144v-30A50 50 0 0 0 352 64.9L88.64 109.85A50 50 0 0 0 48 159v49"
              />
              <path
                fill="currentColor"
                d="M368 320a32 32 0 1 1 32-32a32 32 0 0 1-32 32"
              />
            </svg>
          </div>
          <div class=" self-center font-medium">
            {$i18n.t("Connect Wallet")}
          </div>
        </button>
      {:else}
        <button
          class="flex rounded-md py-2 px-2 w-full hover:bg-gray-50 dark:hover:bg-gray-800 transition"
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
          class="flex rounded-md py-2 px-2 w-full hover:bg-gray-50 dark:hover:bg-gray-800 transition"
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
      {/if}
    </div>
  {/if}

  <!-- 钱包数据面板 -->
  <!-- {#if $user?.id?.startsWith('0x') && $user?.address_type === 'dbc'} -->
  {#if $user?.id?.startsWith("0x")}
    <DbcAccountDetail />
  {/if}
</div>

<style>
</style>
