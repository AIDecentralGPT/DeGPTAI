<script lang="ts">
  import { getContext, onMount } from "svelte";
  import {
    getDisperTotal,
    getDailyUserLine
  } from "$lib/apis/users";
  import { goto } from "$app/navigation";
  import { showSidebar } from "$lib/stores";
  import Pagination from "$lib/components/common/Pagination.svelte";

  const i18n = getContext("i18n");

  let userTotal: number = 0;
  let walletTotal: number = 0;
  let activeToday: number = 0;
  let kycTotal: number = 0;

  // 日活跃用户数
  let page = 1;
  let total = 0;
  let perPage = 15
  let alldata = [];
  let paginatedData = []; 
  let dailyLoaded = true;

  const initInfo = () => {
    getDisperTotal(localStorage.getItem("token") || "").then((res) => {
      userTotal = res.total;
      walletTotal = res.wallet_total;
      // channelTotal = res.channel_total;
      // vipTotal = res.vip_total;
      activeToday = res.active_today;
      kycTotal = res.kyc_total;
    });
    getDailyUserLine(localStorage.getItem("token") || "").then((data) => {
      alldata = data;
      total = data.length;
      pageList();
    });
  };

  function pageList() {
    let startIndex = (page - 1) * perPage;
    let endIndex = startIndex + perPage; 
    paginatedData = alldata.slice(startIndex, endIndex);
  }

  $: if (page) {
    pageList();
  }

  onMount(() => {
    initInfo();
  });

  // 监听窗口大小改变事件
  let resize = 0;
  window.onresize = function () {
    resize == 0 ? (resize = 1) : (resize = 0);
  };
  $: if ($showSidebar) {
    setTimeout(() => {
      resize == 0 ? (resize = 1) : (resize = 0);
    }, 200);
  }
  $: if (!$showSidebar) {
    setTimeout(() => {
      resize == 0 ? (resize = 1) : (resize = 0);
    }, 200);
  }
</script>

<div class=" flex flex-col w-full max-h-screen overflow-auto">
  <div class="flex justify-between px-4 pt-3 mt-0.5 mb-1 w-full">
    <div class="flex items-center text-xl font-semibold">
      {$i18n.t("Dashboard")}
    </div>
    <button
      class="self-center"
      on:click={() => {
        goto("/");
      }}
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 20 20"
        fill="currentColor"
        class="w-5 h-5"
      >
        <path
          d="M6.28 5.22a.75.75 0 00-1.06 1.06L8.94 10l-3.72 3.72a.75.75 0 101.06 1.06L10 11.06l3.72 3.72a.75.75 0 101.06-1.06L11.06 10l3.72-3.72a.75.75 0 00-1.06-1.06L10 8.94 6.28 5.22z"
        />
      </svg>
    </button>
  </div>

  <hr class=" my-2 dark:border-gray-850 w-full" />

  <div
    class="flex justify-between flex-wrap text-gray-700 dark:text-gray-100 px-2"
  >
    <div
      class="flex flex-col flex-1 min-w-[200px] items-center bg-sky-100 dark:bg-sky-300 rounded-lg px-2 py-4 m-3"
    >
      <div
        class="flex text-base text-center text-gray-800 dark:text-gray-50 font-bold mt-2"
      >
        {$i18n.t("User Total")}
      </div>
      <div
        class="flex text-3xl font-medium text-center text-gray-800 dark:text-gray-50 mt-1 mb-2"
      >
        {userTotal}
      </div>
    </div>
    <div
      class="flex flex-col flex-1 min-w-[200px] items-center bg-teal-100 dark:bg-teal-300 rounded-lg px-2 py-4 m-3"
    >
      <div
        class="flex text-base text-center text-gray-800 dark:text-gray-50 font-bold mt-2"
      >
        {$i18n.t("Wallet User Total")}
      </div>
      <div
        class="flex text-3xl font-medium text-center text-gray-800 dark:text-gray-50 mt-1 mb-2"
      >
        {walletTotal}
      </div>
    </div>
    <!-- <div
      class="flex flex-col flex-1 min-w-[200px] items-center bg-blue-100 dark:bg-blue-300 rounded-lg px-2 py-4 m-3"
    >
      <div
        class="flex text-base text-center text-gray-800 dark:text-gray-50 font-bold mt-2"
      >
        {$i18n.t("Channel User Total")}
      </div>
      <div
        class="flex text-3xl font-medium text-center text-gray-800 dark:text-gray-50 mt-1 mb-2"
      >
        {channelTotal}
      </div>
    </div> -->
    <!-- <div
      class="flex flex-col flex-1 min-w-[200px] items-center bg-violet-100 dark:bg-violet-300 rounded-lg px-2 py-4 m-3"
    >
      <div
        class="flex text-base text-center text-gray-800 dark:text-gray-50 font-bold mt-2"
      >
        {$i18n.t("VIP User Total")}
      </div>
      <div
        class="flex text-3xl font-medium text-center text-gray-800 dark:text-gray-50 mt-1 mb-2"
      >
        {vipTotal}
      </div>
    </div> -->
    <div
      class="flex flex-col flex-1 min-w-[200px] items-center bg-violet-100 dark:bg-violet-300 rounded-lg px-2 py-4 m-3"
    >
      <div
        class="flex text-base text-center text-gray-800 dark:text-gray-50 font-bold mt-2"
      >
        {$i18n.t("Daily Active Users")}
      </div>
      <div
        class="flex text-3xl font-medium text-center text-gray-800 dark:text-gray-50 mt-1 mb-2"
      >
        {activeToday}
      </div>
    </div>
    <div
      class="flex flex-col flex-1 min-w-[200px] items-center bg-pink-100 dark:bg-pink-300 rounded-lg px-2 py-4 m-3"
    >
      <div
        class="flex text-base text-center text-gray-800 dark:text-gray-50 font-bold mt-2"
      >
        {$i18n.t("KYC User Total")}
      </div>
      <div
        class="flex text-3xl font-medium text-center text-gray-800 dark:text-gray-50 mt-1 mb-2"
      >
        {kycTotal}
      </div>
    </div>
  </div>

  <hr class=" my-2 dark:border-gray-850 w-full" />

  <div class="px-5 mt-2">
    {#if dailyLoaded}
      <div class="w-full flex flex-col p-5">
        <div class="text-gray-800 dark:text-gray-50 font-bold">{$i18n.t("Daily Active Users Data Distribution")}</div>
        <div class="mt-2">
          <table
            class="w-full text-sm text-left text-gray-500 dark:text-gray-400 table-auto"
          >
            <thead
              class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-850 dark:text-gray-400"
            >
              <tr>
                <th scope="col" class="px-3 py-3"> {$i18n.t("Number")} </th>
                <th scope="col" class="px-3 py-3"> {$i18n.t("Acitve User Total")} </th>
                <th scope="col" class="px-3 py-3"> {$i18n.t("Active Time")} </th>
                <th scope="col" class="px-3 py-3 text-right" />
              </tr>
            </thead>
            <tbody>
              {#each paginatedData as item, index}
                <tr class="bg-white border-b dark:bg-gray-900 dark:border-gray-700 text-xs">
                  <td class=" px-3 py-3">
                    { (page -1) * perPage + index + 1}
                  </td>
                  <td class=" px-3 py-3">
                    {item.user_num}
                  </td>
                  <td class=" px-3 py-3">
                    {item.active_time}
                  </td>
                </tr>
              {/each}
            </tbody>
          </table>
        </div>
        <Pagination bind:page bind:perPage count={total} />
      </div>
    {/if}
  </div>
</div>

<style>
  .bw-16 {
    border-width: 16px;
  }
</style>
