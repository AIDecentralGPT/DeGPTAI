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
  } from "$lib/stores";
  import { DefaultCurrentWalletData } from "$lib/constants.js";
  import { dbcPriceOcw, removePair } from "$lib/utils/wallet/dbc";
  import { goto } from "$app/navigation";
  import { closeWallet } from "$lib/utils/wallet/walletUtils";
  const i18n = getContext("i18n");

  const fetchPrice = async () => {
    try {
      const dbcPriceData = await dbcPriceOcw();
      console.log("dbcPriceData", dbcPriceData);
      // $currentWalletData.price.dbc = priceData / 1000000

      currentWalletData.update((data) => {
        return {
          ...data,
          price: {
            dbc: dbcPriceData / 1000000,
            dlc: dbcPriceData / 1000000,
          },
        };
      });
    } catch (error) {
      console.error("Failed to fetch DBC price:", error);
    }
  };

  onMount(() => {
    fetchPrice();
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

  <!-- 地址展示 -->
  <div class="opacity-80 text-lg font-medium font-['Gilroy'] leading-normal">
    
    {$i18n.t("Wallet Address")}
  </div>

  <div class="pt-0.5">
    <div class="flex flex-col w-full">
      <div class="flex-1 relative">
        <p
          class="
          text-ellipsis overflow-hidden whitespace-nowrap
          pr-[35px]
          px-5 py-3 rounded-md w-full text-sm outline-none border dark:border-none dark:bg-gray-850"
        >
          {$currentWalletData?.pair?.address}
        </p>
        <button
          on:click={async () => {
            const res = await copyToClipboard(
              $currentWalletData?.pair?.address
            );
            if (res) {
              toast.success($i18n.t("Copying to clipboard was successful!"));
            }
          }}
          type="button"
          class="absolute inset-y-0 right-0 px-3 py-2 text-sm dark:text-gray-300 dark:bg-gray-850 rounded-md"
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
    </div>
  </div>

  <!-- 二级按钮 -->
  <div class="flex justify-between">
    <button
      class=" px-4 py-2 dark:bg-white dark:text-zinc-950 bg-black text-gray-100 transition rounded-lg"
      type="submit"
      on:click={async () => {
        $showTransferModal = true;
      }}
    >
      {$i18n.t("Transfer")}
    </button>
    <button
      class=" px-4 py-2 dark:bg-white dark:text-zinc-950 bg-black text-gray-100 transition rounded-lg"
      type="submit"
      on:click={async () => {
        console.log("showExportWalletJsonModal", $showExportWalletJsonModal);

        $showExportWalletJsonModal = true;
      }}
    >
      {$i18n.t("Export Wallet")}
    </button>
    <button
      class=" px-4 py-2 dark:bg-white dark:text-zinc-950 bg-black text-gray-100 transition rounded-lg"
      type="submit"
      on:click={async () => {
        closeWallet()
      }}
    >
      {$i18n.t("Close Wallet")}
    </button>
  </div>
  <!-- ------------ -->

  <hr class="dark:border-gray-800 my-2 p-0" />

  <!-- ------------ -->
  <!-- 钱包余额 -->
  <!-- 标题 -->
  <div class="flex justify-between items-center">
    <div class="opacity-80 text-lg font-medium font-['Gilroy'] leading-normal">
      {$i18n.t("Wallet Balance")}

    </div>

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

      <span>     {$i18n.t("Share to Obtain DGC")}
      </span>
    </button>
  </div>
  <!-- 余额详情 -->
  <div class="flex flex-col gap-2">
    <div
      class="flex justify-between px-5 py-3 rounded-md w-full text-sm outline-none border dark:border-none dark:bg-gray-850"
    >
      <div class="flex gap-1">
        <div
          class="opacity-50 text-xs font-medium font-['Gilroy'] leading-normal"
        >
          DGC
        </div>
        <div
          class="opacity-80 text-xs font-medium font-['Gilroy'] leading-normal"
        >
          {Number($currentWalletData?.dlcBalance?.balance).toFixed(4) ||
            "0.0000"}
        </div>
        <div
          class="opacity-50 text-xs font-medium font-['Gilroy'] leading-normal"
        >
          ≈ ＄{Number(
            $currentWalletData?.dlcBalance?.balance *
              $currentWalletData?.price?.dlc
          ).toFixed(4)}
        </div>
      </div>
      <div
        class="opacity-50 text-right text-xs font-medium font-['Gilroy'] leading-normal"
      >
        DGC {$i18n.t("price")} ＄{Number($currentWalletData?.price?.dlc).toFixed(4)}
      </div>
    </div>

    <div
      class="flex justify-between px-5 py-3 rounded-md w-full text-sm outline-none border dark:border-none dark:bg-gray-850"
    >
      <div class="flex gap-1">
        <div
          class="opacity-50 text-xs font-medium font-['Gilroy'] leading-normal"
        >
          DBC
        </div>
        <div
          class="opacity-80 text-xs font-medium font-['Gilroy'] leading-normal"
        >
          {Number($currentWalletData?.balance?.count).toFixed(4)}
        </div>
        <div
          class="opacity-50 text-xs font-medium font-['Gilroy'] leading-normal"
        >
          ≈ ＄{Number(
            $currentWalletData?.balance?.count * $currentWalletData?.price?.dbc
          ).toFixed(4)}
        </div>
      </div>
      <div
        class="opacity-50 text-right text-xs font-medium font-['Gilroy'] leading-normal"
      >
        DBC     {$i18n.t("price")}
        ＄{Number($currentWalletData?.price?.dbc).toFixed(4)}
      </div>
    </div>
  </div>

  <!-- 二级按钮 -->
  <div class="flex justify-start gap-2">
    <button
      class=" px-4 py-2 dark:bg-white dark:text-zinc-950 bg-black text-gray-100 transition rounded-lg"
      type="submit"
      on:click={async () => {
        $showBuyCoinModal = true;
      }}
    >
      {$i18n.t("Buy")}
    </button>
    <button
      class=" px-4 py-2 dark:bg-white dark:text-zinc-950 bg-black text-gray-100 transition rounded-lg"
      type="submit"
      on:click={async () => {}}
    >
      {$i18n.t("Rewards")}
    </button>
  </div>
</div>

<style>
</style>
