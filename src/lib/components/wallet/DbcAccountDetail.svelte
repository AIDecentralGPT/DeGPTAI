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
    user,
    showTransactionsModal,
    showUserVerifyModal,
  } from "$lib/stores";
  import { DefaultCurrentWalletData } from "$lib/constants.js";
  import // dbcPriceOcw, exportAccountForKeystore, getCurrentPair, removePair

  "$lib/utils/wallet/dbc";
  import { goto } from "$app/navigation";
  import { closeWallet, updateWalletData } from "$lib/utils/wallet/walletUtils";
  import { getUsersInvited } from "$lib/apis/users";
  const i18n = getContext("i18n");

  // const fetchPrice = async () => {
  //   try {

  //     const dbcPriceData = await dbcPriceOcw();
  //     console.log("dbcPriceData", dbcPriceData);
  //     // $currentWalletData.price.dbc = priceData / 1000000

  //     currentWalletData.update((data) => {
  //       return {
  //         ...data,
  //         price: {
  //           dbc: dbcPriceData / 1000000,
  //           dlc: dbcPriceData / 1000000,
  //         },
  //       };
  //     });
  //   } catch (error) {
  //     console.error("Failed to fetch DBC price:", error);
  //   }
  // };

  let showPrice = false

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

<div class="flex flex-col gap-2 padding-l-r-10">
  <!-- <div class="py-2 px-3"> -->

  <!-- 地址展示 -->
  <div class="opacity-80 text-lg font-medium font-['Gilroy'] leading-normal">
    {$i18n.t("Wallet Address")}
  </div>

  <div class="pt-0.5">
    <div class="flex flex-col w-full">
      <div class="flex-1 relative">
        <p
          class="text-ellipsis overflow-hidden whitespace-nowrap pr-[35px] opacity-50
          px-5 py-3 rounded-md w-full text-sm-12 outline-none border dark:border-none dark:bg-gray-850 fs12"
        >
          <!-- {$currentWalletData?.walletInfo?.address} -->
          {$user?.id}

        </p>
        <button
          on:click={async () => {
            const res = await copyToClipboard($user?.id);
            alert(res);
            if (res) {
              toast.success($i18n.t("Copying to clipboard was successful!"));
            }
          }}
          type="button"
          class="absolute inset-y-0 right-0 px-3 py-2 text-sm-12 dark:text-gray-300 dark:bg-gray-650 rounded-md fs12"
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
  <div class="flex justify-start gap-2 mt6 mb10">
    <button
      class=" px-4 py-2 dark:bg-white dark:text-zinc-950 bg-black text-gray-100 transition rounded-lg fs12"
      type="submit"
      on:click={async () => {
        $showTransferModal = true;
      }}
    >
      {$i18n.t("Transfer")}
    </button>
    <button
      class=" px-4 py-2 dark:bg-white dark:text-zinc-950 bg-black text-gray-100 transition rounded-lg fs12"
      type="submit"
      on:click={async () => {
        console.log("showExportWalletJsonModal", $showExportWalletJsonModal);
        // const pair = getCurrentPair()
        // exportAccountForKeystore(pair)

        $showExportWalletJsonModal = true;
      }}
    >
      {$i18n.t("Export Wallet")}
    </button>
    <button
      class=" px-4 py-2 dark:bg-white dark:text-zinc-950 bg-black text-gray-100 transition rounded-lg fs12"
      type="submit"
      on:click={async () => {
        closeWallet();
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
    <div
      class="opacity-80 text-lg font-medium font-['Gilroy'] leading-normal flex items-center"
    >
      {$i18n.t("Wallet Balance")}
    </div>
    <div class="flex">
      <button
        class="flex gap-2 items-center cursor-pointer opacity-50 fs12 mr-2"
        on:click={() => {
          // const pair = getCurrentPair()
          // console.log("pair?.address", pair?.address);

          // if(!pair?.address) {
          //   toast.error($i18n.t("Please log in to your wallet first"))
          // }
          // else {
          //   $showShareModal = true;
          // }

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

      <button
        on:click={() => {
          updateWalletData($currentWalletData?.walletInfo);
        }}
        ><svg
          xmlns="http://www.w3.org/2000/svg"
          width="1em"
          height="1em"
          viewBox="0 0 24 24"
          ><path
            fill="currentColor"
            d="M12 20q-3.35 0-5.675-2.325T4 12t2.325-5.675T12 4q1.725 0 3.3.712T18 6.75V4h2v7h-7V9h4.2q-.8-1.4-2.187-2.2T12 6Q9.5 6 7.75 7.75T6 12t1.75 4.25T12 18q1.925 0 3.475-1.1T17.65 14h2.1q-.7 2.65-2.85 4.325T12 20"
          /></svg
        >
      </button>
    </div>
  </div>
  <!-- 余额详情 -->
  <div class="flex flex-col gap-2">
    <div
      class="flex justify-between px-5 py-2 pe-2 rounded-md w-full text-sm outline-none border dark:border-none dark:bg-gray-850"
    >
      <!-- <div class="flex gap-1">
        <div
          class="opacity-50 text-xs font-medium font-['Gilroy'] leading-normal"
        >
          DBC:
        </div>
        {#if showPrice == true}
        <div
          class="opacity-80 text-xs font-medium font-['Gilroy'] leading-normal"
        >
          {floorToFixed(Number($currentWalletData?.dbcBalance), 2)}
        </div>
        {:else}
        <div
          class="opacity-80 text-xs font-medium font-['Gilroy'] leading-normal"
        >
          *****
        </div>
        {/if}
      </div> -->
      <div class="flex gap-1">
        <div
          class="opacity-50 text-xs font-medium font-['Gilroy'] leading-normal"
        >
          DGC 
        </div>
        <div
          class="opacity-80 text-xs font-medium font-['Gilroy'] leading-normal"
        >
          {floorToFixed(Number($currentWalletData?.dgcBalance), 2)}
        </div>
        <!-- {#if showPrice == true}
        <div
          class="opacity-80 text-xs font-medium font-['Gilroy'] leading-normal"
        >
          {floorToFixed(Number($currentWalletData?.dgcBalance), 2)}
        </div>
        {:else}
        <div
          class="opacity-80 text-xs font-medium font-['Gilroy'] leading-normal"
        >
          *****
        </div>
        {/if} -->
      </div>

      <div class="opacity-50 leading-normal fs12">
        1DGC=0.0005u
      </div>

      <div class="opacity-50 leading-normal fs12">
        Total ${floorToFixed(Number($currentWalletData?.dgcBalance) * 0.0005, 4)}u
      </div>
      
      <!-- <div on:click={()=>showPrice=!showPrice}>
        {#if showPrice === true}
        <svg
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 16 16"
          fill="currentColor"
          class="w-4 h-4"
        >
          <path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z" />
          <path
            fill-rule="evenodd"
            d="M1.38 8.28a.87.87 0 0 1 0-.566 7.003 7.003 0 0 1 13.238.006.87.87 0 0 1 0 .566A7.003 7.003 0 0 1 1.379 8.28ZM11 8a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z"
            clip-rule="evenodd"
          />
        </svg>
    
        {:else}
          <svg
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 16 16"
            fill="currentColor"
            class="w-4 h-4"
          >
            <path
              fill-rule="evenodd"
              d="M3.28 2.22a.75.75 0 0 0-1.06 1.06l10.5 10.5a.75.75 0 1 0 1.06-1.06l-1.322-1.323a7.012 7.012 0 0 0 2.16-3.11.87.87 0 0 0 0-.567A7.003 7.003 0 0 0 4.82 3.76l-1.54-1.54Zm3.196 3.195 1.135 1.136A1.502 1.502 0 0 1 9.45 8.389l1.136 1.135a3 3 0 0 0-4.109-4.109Z"
              clip-rule="evenodd"
            />
            <path
              d="m7.812 10.994 1.816 1.816A7.003 7.003 0 0 1 1.38 8.28a.87.87 0 0 1 0-.566 6.985 6.985 0 0 1 1.113-2.039l2.513 2.513a3 3 0 0 0 2.806 2.806Z"
            />
          </svg>
        {/if}
      </div> -->
     
    </div>
    <div
      class="flex justify-between px-5 py-2 pe-2 rounded-md w-full text-sm outline-none border dark:border-none dark:bg-gray-850"
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
          {floorToFixed(Number($currentWalletData?.dbcBalance), 2)}
        </div>
      </div>
      <div class="opacity-50 leading-normal fs12">
        Total ${floorToFixed(Number($currentWalletData?.dbcBalance) * 0.0005, 4)}u
      </div>
    </div>
  </div>

  <!-- 二级按钮 -->
  <div class="flex justify-start gap-2 mt6 mb30">
    <button
      class=" px-4 py-2 dark:bg-white dark:text-zinc-950 bg-black text-gray-100 transition rounded-lg fs12"
      type="submit"
      on:click={async () => {
        // $showBuyCoinModal = true;
        // 用新标签打开
        window.open("https://www.drcpad.io/project?name=DeGPT", "_blank");
      }}
    >
      {$i18n.t("Buy")}
    </button>
    <!-- <button
      class=" px-4 py-2 dark:bg-white dark:text-zinc-950 bg-black text-gray-100 transition rounded-lg fs12"
      type="submit"
      on:click={async () => {
        $showRewardsModal = true;
      }}
    >
      {$i18n.t("Rewards")}
    </button> -->
    <button
      class=" px-4 py-2 dark:bg-white dark:text-zinc-950 bg-black text-gray-100 transition rounded-lg fs12"
      type="submit"
      on:click={async () => {
        $showTransactionsModal = true;
      }}
    >
      {$i18n.t("Transactions")}
    </button>
    {#if $user?.verified}
      <button
        class=" px-4 py-2 primaryButton text-gray-800 transition rounded-lg fs12"
        type="submit"
      >
        {$i18n.t("Authed KYC")}
      </button>
    {:else}
      <button
        class=" px-4 py-2 primaryButton text-gray-100 transition rounded-lg fs12"
        type="submit"
        on:click={async () => {
          $showUserVerifyModal = true;
        }}
      >
        {$i18n.t("JOIN KYC")}
      </button>
    {/if}
  </div>
</div>

<style>
.padding-l-r-10 {
  padding-left: 10px;
  padding-right: 10px;
}
.text-sm-12 {
  line-height: 12px;
}
.fs12 {
  font-size: 12px;
}
.mt6 {
  margin-top: 6px;
}
.mb10 {
  margin-bottom: 10px;
}
.mb30 {
  margin-bottom: 30px;
}
</style>
