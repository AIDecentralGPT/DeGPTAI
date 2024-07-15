<script lang="ts">
  import { onMount, getContext } from "svelte";
  import { copyToClipboard, findWordIndices } from "$lib/utils";
  import { toast } from "svelte-sonner";
  import {
    showSettings,
    showNewWalletModal,
    showOpenWalletModal,
    currentWalletData,
    showExportWalletJsonModal,
    showTransferModal,
    showPriceModal,
    showBuyCoinModal,
    showShareModal,
    chats,
    chatId,
    pageUpdateNumber,
    showRewardsModal,
    threesideAccount,
  } from "$lib/stores";
  import { DefaultCurrentWalletData } from "$lib/constants.js";
  import // dbcPriceOcw, exportAccountForKeystore, getCurrentPair, removePair

  "$lib/utils/wallet/dbc";
  import { goto } from "$app/navigation";
  import { closeWallet } from "$lib/utils/wallet/walletUtils";
  import { getUsersInvited } from "$lib/apis/users";
  const i18n = getContext("i18n");


  function floorToFixed(num, digits) {
    let pow = Math.pow(10, digits);
    return (Math.floor(num * pow) / pow).toFixed(digits);
  }

  onMount(() => {
    // fetchPrice();
    // const interval = setInterval(fetchPrice, 5000); // 每5秒获取一次价格数据
    // return () => clearInterval(interval);
  });

  // // 在页面初始化时请求数据
  // onMount(async () => {
  //   try {
  //     // 假设你有一个获取钱包数据的 API
  //     // const response = await fetch('/api/get-wallet-data');
  //     // const data = await response.json();
  //     const data = await dbcPriceOcw();
  //     // 更新 currentWalletData 的值
  //     // currentWalletData.set(data);
  //     console.log("data", data);

  //   const interval = setInterval(fetchPrice, 5000); // 每5秒获取一次价格数据
  //   return () => clearInterval(interval);

  //   } catch (error) {
  //     console.error("Failed to fetch wallet data:", error);
  //   }
  // });
</script>

<div class="py-2 flex flex-col gap-2">



  {#if $threesideAccount?.address}
  <!-- <div class="py-2 px-3"> -->
  <!-- 升级计划 -->
  <button
    on:click={() => {
      $showPriceModal = true;
    }}
    class=" px-4 py-2 primaryButton text-gray-100 transition rounded-lg"
  >
    <span class="relative">{$i18n.t("Upgrade Plan")}</span>
  </button>



  <hr class="dark:border-gray-800 my-2 p-0" />

  <div>
    <!-- ------------ -->
    <!-- 钱包余额 -->
    <!-- 标题 -->
    <div class="flex justify-between items-center">

      <button
        class="flex gap-2 items-center cursor-pointer"
        on:click={() => {
          $showShareModal = true;
        }}
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="1em"
          height="1em"
          viewBox="0 0 24 24"
          ><path
            fill="none"
            stroke="currentColor"
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M10 4H6a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-4m-8-2l8-8m0 0v5m0-5h-5"
          /></svg
        >

        <span> {$i18n.t("Share to Obtain DGC")} </span>
      </button>
    </div>


    <!-- 二级按钮 -->
    <div class="flex justify-start gap-2">
      <!-- <button
        class=" px-4 py-2 dark:bg-white dark:text-zinc-950 bg-black text-gray-100 transition rounded-lg"
        type="submit"
        on:click={async () => {
          $showBuyCoinModal = true;
        }}
      >
        {$i18n.t("Buy")}
      </button> -->
      <button
        class=" px-4 py-2 dark:bg-white dark:text-zinc-950 bg-black text-gray-100 transition rounded-lg"
        type="submit"
        on:click={async () => {
          // toast.warning("Coming soon")

          $showRewardsModal = true;
        }}
      >
        {$i18n.t("Rewards")}
      </button>
    </div>
  </div>
{/if}
</div>

<style>
</style>
