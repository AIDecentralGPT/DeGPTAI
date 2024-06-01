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
  } from "$lib/stores";
  import { DefaultCurrentWalletData } from '$lib/constants.js';
  import { removePair } from "$lib/utils/wallet/dbc";
  const i18n = getContext("i18n");




</script>

<div class="py-2 flex flex-col gap-2">
  <!-- <div class="py-2 px-3"> -->
  <!-- 升级计划 -->
  <button
    on:click={() => {}}
    class=" px-4 py-2 primaryButton text-gray-100 transition rounded-lg"
  >
    <span class="relative">{$i18n.t("Upgrade Plan")}</span>
  </button>

  <!-- 地址展示 -->
  <div
    class="opacity-80 text-white text-lg font-medium font-['Gilroy'] leading-normal"
  >
    Wallet Address
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
            const res = await copyToClipboard("1");
            if (res) {
              toast.success($i18n.t("Copying to clipboard was successful!"));
            }
          }}
          type="button"
          class="absolute inset-y-0 right-0 px-3 py-2 text-sm dark:text-gray-300 dark:bg-gray-850 rounded-md"
        >
          <svg
            width="12"
            height="12"
            viewBox="0 0 12 12"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <g id="copy" clip-path="url(#clip0_0_29)">
              <path
                id="Vector"
                d="M0.75 10.6875V5.0625C0.75 4.75183 1.00184 4.5 1.3125 4.5H4.6875H6.9375C7.24817 4.5 7.5 4.75183 7.5 5.0625V7.3125V10.6875C7.5 10.9982 7.24817 11.25 6.9375 11.25H1.3125C1.00184 11.25 0.75 10.9982 0.75 10.6875Z"
                stroke="white"
                stroke-linecap="round"
                stroke-linejoin="round"
              />
              <path
                id="Vector_2"
                d="M7.875 7.5H10.6875C10.9982 7.5 11.25 7.24817 11.25 6.9375V1.3125C11.25 1.00184 10.9982 0.75 10.6875 0.75H5.0625C4.75183 0.75 4.5 1.00184 4.5 1.3125V4.125"
                stroke="white"
                stroke-linecap="round"
                stroke-linejoin="round"
              />
            </g>
            <defs>
              <clipPath id="clip0_0_29">
                <rect width="12" height="12" fill="white" />
              </clipPath>
            </defs>
          </svg>
        </button>
      </div>
    </div>
  </div>

  <!-- 二级按钮 -->
  <div class="flex justify-between">
    <button
      class=" px-4 py-2 dark:bg-white dark:text-zinc-950 bg-black text-gray-100 transition rounded-lg"
      type="submit"
      on:click={async () => {}}
    >
      {$i18n.t(" Transfer ")}
    </button>
    <button
      class=" px-4 py-2 dark:bg-white dark:text-zinc-950 bg-black text-gray-100 transition rounded-lg"
      type="submit"
      on:click={async () => {
        console.log("showExportWalletJsonModal", $showExportWalletJsonModal);
        
        $showExportWalletJsonModal = true
      }}
    >
      {$i18n.t(" Export Wallet ")}
    </button>
    <button
      class=" px-4 py-2 dark:bg-white dark:text-zinc-950 bg-black text-gray-100 transition rounded-lg"
      type="submit"
      on:click={async () => {
        // $currentWalletData = DefaultCurrentWalletData
        
        removePair($currentWalletData?.pair?.address)
        console.log($currentWalletData,DefaultCurrentWalletData);
        currentWalletData.set({})

      }}
    >
      {$i18n.t(" Close Wallet ")}
    </button>
  </div>
  <!-- ------------ -->

  <hr class="dark:border-gray-800 my-2 p-0" />

  <!-- ------------ -->
  <!-- 钱包余额 -->
  <!-- 标题 -->
  <div class="flex justify-between items-end">
    <div
      class="opacity-80 text-white text-lg font-medium font-['Gilroy'] leading-normal"
    >
      Wallet Balance
    </div>

    <div class="flex gap-2 items-center">
      <svg
        xmlns="http://www.w3.org/2000/svg"
        width="10"
        height="10"
        viewBox="0 0 10 10"
        fill="none"
      >
        <g opacity="0.5" clip-path="url(#clip0_0_42)">
          <path
            d="M6 0.5H9.5V4"
            stroke="white"
            stroke-linecap="round"
            stroke-linejoin="round"
          />
          <path
            d="M9.5 6.36842V8.75C9.5 9.16423 9.16423 9.5 8.75 9.5H1.25C0.835788 9.5 0.5 9.16423 0.5 8.75V1.25C0.5 0.835788 0.835788 0.5 1.25 0.5H3.5"
            stroke="white"
            stroke-linecap="round"
            stroke-linejoin="round"
          />
          <path
            d="M5.44995 4.54998L9.27495 0.724976"
            stroke="white"
            stroke-linecap="round"
            stroke-linejoin="round"
          />
        </g>
        <defs>
          <clipPath id="clip0_0_42">
            <rect width="10" height="10" fill="white" />
          </clipPath>
        </defs>
      </svg>
      <span> Share to Obtain DGC </span>
    </div>
  </div>
  <!-- 余额详情 -->
  <div class="flex flex-col gap-2">
    <div
      class="flex justify-between px-5 py-3 rounded-md w-full text-sm outline-none border dark:border-none dark:bg-gray-850"
    >
      <div class="flex gap-1">
        <div
          class="opacity-50 text-white text-xs font-medium font-['Gilroy'] leading-normal"
        >
          DLC
        </div>
        <div
          class="opacity-80 text-white text-xs font-medium font-['Gilroy'] leading-normal"
        >
          10119.000
        </div>
        <div
          class="opacity-50 text-white text-xs font-medium font-['Gilroy'] leading-normal"
        >
          ≈ ＄505
        </div>
      </div>
      <div
        class="opacity-50 text-right text-white text-xs font-medium font-['Gilroy'] leading-normal"
      >
        DLC price ＄0.05
      </div>
    </div>

    <div
      class="flex justify-between px-5 py-3 rounded-md w-full text-sm outline-none border dark:border-none dark:bg-gray-850"
    >
      <div class="flex gap-1">
        <div
          class="opacity-50 text-white text-xs font-medium font-['Gilroy'] leading-normal"
        >
          DBC
        </div>
        <div
          class="opacity-80 text-white text-xs font-medium font-['Gilroy'] leading-normal"
        >
          10119.000
        </div>
        <div
          class="opacity-50 text-white text-xs font-medium font-['Gilroy'] leading-normal"
        >
          ≈ ＄505
        </div>
      </div>
      <div
        class="opacity-50 text-right text-white text-xs font-medium font-['Gilroy'] leading-normal"
      >
        DBC price ＄0.05
      </div>
    </div>
  </div>

  <!-- 二级按钮 -->
  <div class="flex justify-start gap-2">
    <button
      class=" px-4 py-2 dark:bg-white dark:text-zinc-950 bg-black text-gray-100 transition rounded-lg"
      type="submit"
      on:click={async () => {}}
    >
      {$i18n.t(" Buy ")}
    </button>
    <button
      class=" px-4 py-2 dark:bg-white dark:text-zinc-950 bg-black text-gray-100 transition rounded-lg"
      type="submit"
      on:click={async () => {}}
    >
      {$i18n.t(" Rewards ")}
    </button>
  </div>

</div>

<style>
</style>
