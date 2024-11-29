<script lang="ts">
  import { getContext, onMount } from "svelte";
  import { getDisperTotal, getDisperUser, getThirdTotal, getdisperVip } from "$lib/apis/users";
  import { goto } from "$app/navigation";
  import BarChart from "$lib/components/common/echarts/BarChart.svelte";
  import LineChart from "$lib/components/common/echarts/LineChart.svelte";
  import { showSidebar } from "$lib/stores";

  const i18n = getContext("i18n");

  let userTotal: number = 0;
  let walletTotal: number = 0;
  let channelTotal: number = 0;
  let vipTotal: number = 0;
  let kycTotal: number = 0;

  let lineLoaded = false;
  let lineXdata: any[] = [];
  let lineSeries: any[] = [];
  let lineTitle = $i18n.t("Recent 15 Days User Data Distribution");

  let thirdLoaded = false;
  let thirdXdata: any[] = [];
  let thirdSeries: any[] = [];
  let thirdTitle = $i18n.t("Channel Distribution");

  let vipLoaded = false;
  let vipXdata: any[] = [];
  let vipSeries: any[] = [];
  let vipTitle = $i18n.t("VIP Distribution");

  const initInfo = () => {
    getDisperTotal(localStorage.getItem("token") || "").then((res) => {
      userTotal = res.total;
      walletTotal = res.wallet_total;
      channelTotal = res.channel_total;
      vipTotal = res.vip_total;
      kycTotal = res.kyc_total;
    });
    getDisperUser(localStorage.getItem("token") || "").then((res) => {
      lineXdata = res.date_list;
      lineSeries.push(
        {
          name: $i18n.t("Wallet User Total"),
          type: "line",
          data: res.wallet_list
        }
      );
      lineSeries.push(
        {
          name: $i18n.t("Channel User Total"),
          type: "line",
          data: res.channel_list
        }
      );
      lineSeries.push(
        {
          name: $i18n.t("KYC User Total"),
          type: "line",
          data: res.kyc_list
        }
      );
      lineLoaded = true;
    });
    getThirdTotal(localStorage.getItem("token") || "").then((res) => {
      res.forEach((item: any) => {
        thirdXdata.push(item?.channel);
        thirdSeries.push(item?.total);
      });
      thirdLoaded = true;
    });
    getdisperVip(localStorage.getItem("token") || "").then((res) => {
      vipXdata = [
        $i18n.t("VIP Total"),
        $i18n.t("Expired Total"),
        $i18n.t("Renew Total"),
      ];
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
    <div
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
    </div>
    <div
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

  <div class="px-5">
    {#if lineLoaded}
      <div class="w-full bg-gray-100 dark:bg-gray-50 rounded-lg p-5">
        <LineChart
          bind:title={lineTitle}
          bind:xData={lineXdata}
          bind:seriesData={lineSeries}
          bind:resize
        />
      </div>
    {/if}
  </div>

  <div
    class="flex justify-between flex-wrap text-gray-700 dark:text-gray-100 pt-1 pb-4"
  >
    {#if thirdLoaded && vipLoaded}
      <div
        class="flex-1 min-w-[200px] bg-gray-100 dark:bg-gray-50 rounded-lg p-5 m-5"
      >
        <BarChart
          bind:xData={thirdXdata}
          bind:seriesData={thirdSeries}
          bind:title={thirdTitle}
          bind:resize
        />
      </div>
      <div
        class="flex-1 min-w-[200px] bg-gray-100 dark:bg-gray-50 rounded-lg p-5 m-5"
      >
        <BarChart
          bind:xData={vipXdata}
          bind:seriesData={vipSeries}
          bind:title={vipTitle}
          bind:resize
        />
      </div>
    {/if}
  </div>
</div>

<style>
</style>
