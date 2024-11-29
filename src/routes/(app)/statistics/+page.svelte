<script lang="ts">
  import { getContext, onMount } from "svelte";
  import { getDisperTotal, getThirdTotal, getdisperVip } from "$lib/apis/users";
  import { goto } from "$app/navigation";
  import BarChart from "$lib/components/common/echarts/BarChart.svelte";
  import LineChart from "$lib/components/common/echarts/LineChart.svelte";
  import { showSidebar } from "$lib/stores";

  const i18n = getContext("i18n");

  let userTotal: number = 0;
  let walletTotal: number = 0;
  let channelTotal: number = 0;
  let vipTotal: number = 0;
  let visitorTotal: number = 0;

  let thirdLoaded = false;
  let thirdXdata: any[] = [];
  let thirdSeries: any[] = [];
  let thirdTitle = $i18n.t("Channel Distribution");

  let vipLoaded = false;
  let vipXdata: any[] = [];
  let vipSeries: any[] = [];
  let vipTitle = "VIP分布图";

  const initInfo = () => {
    getDisperTotal(localStorage.getItem("token") || "").then((res) => {
      userTotal = res.total;
      walletTotal = res.wallet_total;
      channelTotal = res.channel_total;
      vipTotal = res.vip_total;
      visitorTotal = res.visitor_total;
    });
    getThirdTotal(localStorage.getItem("token") || "").then((res) => {
      res.forEach((item: any) => {
        thirdXdata.push(item?.channel);
        thirdSeries.push(item?.total);
      });
      thirdLoaded = true;
    });
    getdisperVip(localStorage.getItem("token") || "").then((res) => {
      vipXdata = ['VIP TOTAL', 'EXPIRE Total', 'RENEW TOTAL'];
      vipSeries.push(res.vip_total);
      vipSeries.push(res.expire_total);
      vipSeries.push(res.renew_total);
      vipLoaded = true;
    });
  };

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

<div class=" flex flex-col w-full min-h-screen">
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
        class="flex text-base text-gray-800 dark:text-gray-50 font-bold mt-2"
      >
        用户总数
      </div>
      <div
        class="flex text-3xl font-medium text-gray-800 dark:text-gray-50 mt-1 mb-2"
      >
        {userTotal}
      </div>
    </div>
    <div
      class="flex flex-col flex-1 min-w-[200px] items-center bg-teal-100 dark:bg-teal-300 rounded-lg px-2 py-4 m-3"
    >
      <div
        class="flex text-base text-gray-800 dark:text-gray-50 font-bold mt-2"
      >
        钱包用户数
      </div>
      <div
        class="flex text-3xl font-medium text-gray-800 dark:text-gray-50 mt-1 mb-2"
      >
        {walletTotal}
      </div>
    </div>
    <div
      class="flex flex-col flex-1 min-w-[200px] items-center bg-blue-100 dark:bg-blue-300 rounded-lg px-2 py-4 m-3"
    >
      <div
        class="flex text-base text-gray-800 dark:text-gray-50 font-bold mt-2"
      >
        渠道用户数
      </div>
      <div
        class="flex text-3xl font-medium text-gray-800 dark:text-gray-50 mt-1 mb-2"
      >
        {channelTotal}
      </div>
    </div>
    <div
      class="flex flex-col flex-1 min-w-[200px] items-center bg-violet-100 dark:bg-violet-300 rounded-lg px-2 py-4 m-3"
    >
      <div
        class="flex text-base text-gray-800 dark:text-gray-50 font-bold mt-2"
      >
        VIP用户数
      </div>
      <div
        class="flex text-3xl font-medium text-gray-800 dark:text-gray-50 mt-1 mb-2"
      >
        {vipTotal}
      </div>
    </div>
    <div
      class="flex flex-col flex-1 min-w-[200px] items-center bg-pink-100 dark:bg-pink-300 rounded-lg px-2 py-4 m-3"
    >
      <div
        class="flex text-base text-gray-800 dark:text-gray-50 font-bold mt-2"
      >
        访客数
      </div>
      <div
        class="flex text-3xl font-medium text-gray-800 dark:text-gray-50 mt-1 mb-2"
      >
        {visitorTotal}
      </div>
    </div>
  </div>

  <hr class=" my-2 dark:border-gray-850 w-full" />

  <div class="px-5">
    <div class="w-full bg-gray-100 dark:bg-gray-50 rounded-lg p-5">
      <LineChart
        bind:xData={thirdXdata}
        bind:seriesData={thirdSeries}
        bind:resize
      />
    </div>
  </div>

  <div
    class="flex justify-between flex-wrap text-gray-700 dark:text-gray-100 pt-1 pb-4"
  >
    <div
      class="flex-1 min-w-[200px] bg-gray-100 dark:bg-gray-50 rounded-lg p-5 m-5"
    >
      {#if thirdLoaded}
        <BarChart
          bind:xData={thirdXdata}
          bind:seriesData={thirdSeries}
          bind:title={thirdTitle}
          bind:resize
        />
      {/if}
    </div>
    <div
      class="flex-1 min-w-[200px] bg-gray-100 dark:bg-gray-50 rounded-lg p-5 m-5"
    >
      {#if vipLoaded}
        <BarChart
          bind:xData={vipXdata}
          bind:seriesData={vipSeries}
          bind:title={vipTitle}
          bind:resize
        />
      {/if}
    </div>
  </div>
</div>

<style>
</style>
