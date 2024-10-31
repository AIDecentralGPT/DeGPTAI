<script lang="ts">
  import { onMount, getContext } from "svelte";
  import { copyToClipboard } from "$lib/utils";
  import { toast } from "svelte-sonner";
  import {
    currentWalletData,
    showExportWalletJsonModal,
    showTransferModal,
    showShareModal,
    user,
    showTransactionsModal,
    showUserVerifyModal,
    showLoginInfoModal,
    showCoinIntruModal,
    showCoinIntruType
  } from "$lib/stores";
  import // dbcPriceOcw, exportAccountForKeystore, getCurrentPair, removePair

  "$lib/utils/wallet/dbc";
  import { closeWallet, updateWalletData } from "$lib/utils/wallet/walletUtils";
  import { getDbcRate } from "$lib/apis/wallet/index";

  const i18n = getContext("i18n");

  function floorToFixed(num, digits) {
    let pow = Math.pow(10, digits);
    return (Math.floor(num * pow) / pow).toFixed(digits);
  }

  let dbcRate = 0.0003;

  let updateWalletLoad = false;

  onMount(async () => {
    let dbc_rate = await getDbcRate(localStorage.token);
    if (dbc_rate) {
      dbcRate = dbc_rate;
    }
  });
</script>

<div class="flex flex-col gap-2 px-3">
  <!-- <div class="py-2 px-3"> -->
  {#if $showLoginInfoModal}
    <!-- 地址展示 -->
    <div class="opacity-80 text-base font-medium leading-6">
      {$i18n.t("Wallet Address")}
    </div>
    <div class="pt-0.5">
      <div class="flex flex-col w-full">
        <div class="flex-1 relative">
          <p
            class="text-ellipsis overflow-hidden whitespace-nowrap pr-[35px] opacity-50
            px-5 py-3 rounded-md w-full leading-3 outline-none border dark:border-none dark:bg-gray-850 text-xs"
          >
            <!-- {$currentWalletData?.walletInfo?.address} -->
            {$user?.id}

          </p>
          <button
            on:click={async () => {
              const res = await copyToClipboard($user?.id);
              if (res) {
                toast.success($i18n.t("Copying to clipboard was successful!"));
              }
            }}
            type="button"
            class="absolute inset-y-0 right-0 px-3 py-2 leading-3 dark:text-gray-300 dark:bg-gray-650 rounded-md text-xs"
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
    {#if $user?.address_type === 'threeSide'}
      <div class="flex justify-center">
        <w3m-button class="v-btn" label="组件方式打开"/>
      </div>
      
    {:else}
      <div class="flex justify-start gap-2 mt-1 mb5">
        <button
          class=" px-4 py-2 dark:bg-white dark:text-zinc-950 bg-black text-gray-100 transition rounded-lg text-xs"
          type="submit"
          on:click={async () => {
            $showTransferModal = true;
          }}
        >
          {$i18n.t("Transfer")}
        </button>
        <button
          class=" px-4 py-2 dark:bg-white dark:text-zinc-950 bg-black text-gray-100 transition rounded-lg text-xs"
          type="submit"
          on:click={async () => {
            $showExportWalletJsonModal = true;
          }}
        >
          {$i18n.t("Export Wallet")}
        </button>
        <button
          class=" px-4 py-2 dark:bg-white dark:text-zinc-950 bg-black text-gray-100 transition rounded-lg text-xs"
          type="submit"
          on:click={async () => {
            closeWallet();
          }}
        >
          {$i18n.t("Close Wallet")}
        </button>
      </div>
    {/if}
    <!-- ------------ -->

    <hr class="dark:border-gray-800 my-1 p-0" />
  {/if}

  <!-- ------------ -->
  <!-- 钱包余额 -->
  <!-- 标题 -->
  <div class="flex justify-between items-center">
    <div
      class="opacity-80 text-base font-medium leading-6 flex items-center"
    >
      {$i18n.t("Wallet Balance")}
    </div>
    <div class="flex">
      <button
        class="flex gap-2 items-center cursor-pointer opacity-50 text-xs mr-2"
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

      <button
        on:click={ async () => {
          updateWalletLoad = true;
          await updateWalletData($currentWalletData?.walletInfo);
          updateWalletLoad = false;
        }}>
          <svg class="{updateWalletLoad? 'animate-spin' : 'animate-none'}"
            xmlns="http://www.w3.org/2000/svg"
            width="1em"
            height="1em"
            viewBox="0 0 24 24"
            >
              <path fill="currentColor"
                d="M12 20q-3.35 0-5.675-2.325T4 12t2.325-5.675T12 4q1.725 0 3.3.712T18 6.75V4h2v7h-7V9h4.2q-.8-1.4-2.187-2.2T12 6Q9.5 6 7.75 7.75T6 12t1.75 4.25T12 18q1.925 0 3.475-1.1T17.65 14h2.1q-.7 2.65-2.85 4.325T12 20"/>
          </svg>
      </button>
    </div>
  </div>
  <!-- 余额详情 -->
  <div class="flex flex-col gap-2">
    <div
      class="flex justify-between px-5 py-2 pe-2 rounded-md w-full text-sm outline-none border dark:border-none dark:bg-gray-850"
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
          {floorToFixed(Number($currentWalletData?.dgcBalance), 2)}
        </div>
      </div>

      <div class="flex flex-row opacity-50 leading-normal text-xs">
        1DGC=0.0005u
        <button class="ml-1 size-4 primaryButton saturate-200 text-white rounded-full"
          on:click={ async () => {
              $showCoinIntruModal = true;
              $showCoinIntruType = 'dgc';
          }}>
            ?
        </button>
      </div>

      <div class="opacity-50 leading-normal text-xs">
        Total ${floorToFixed(Number($currentWalletData?.dgcBalance) * 0.0005, 4)}u
      </div>
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
      <div class="flex flex-row opacity-50 leading-normal text-xs">
        1DBC={floorToFixed(dbcRate, 4)}u
        <button class="ml-1 size-4 primaryButton saturate-200 text-white rounded-full"
          on:click={ async () => {
            $showCoinIntruModal = true;
            $showCoinIntruType = 'dbc';
          }}>
            ?
        </button>
      </div>
      <div class="opacity-50 leading-normal text-xs">
        Total ${floorToFixed(Number($currentWalletData?.dbcBalance) * dbcRate, 4)}u
      </div>
    </div>
  </div>

  <!-- 二级按钮 -->
  {#if $showLoginInfoModal}
    <div class="flex justify-start gap-2 mt-1 mb-2">
      <button
        class=" px-4 py-2 dark:bg-white dark:text-zinc-950 bg-black text-gray-100 transition rounded-lg text-xs"
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
        class=" px-4 py-2 dark:bg-white dark:text-zinc-950 bg-black text-gray-100 transition rounded-lg text-xs"
        type="submit"
        on:click={async () => {
          $showTransactionsModal = true;
        }}
      >
        {$i18n.t("Transactions")}
      </button>
      {#if $user?.verified}
        <button
          class=" px-4 py-2 primaryButton text-gray-800 transition rounded-lg text-xs"
          type="submit"
        >
          {$i18n.t("Authed KYC")}
        </button>
      {:else}
        <button
          class=" px-4 py-2 primaryButton text-gray-100 transition rounded-lg text-xs"
          type="submit"
          on:click={async () => {
            $showUserVerifyModal = true;
          }}
        >
          {$i18n.t("Complete KYC")}
        </button>
      {/if}
    </div>
  {/if}
</div>

<style>

</style>
