<script lang="ts">
  import { getContext, onMount } from "svelte";
  import {
    getDisperTotal,
    getDisperUser,
    getThirdTotal,
    getdisperVip,
    getRewardsTotal,
    getDailyUserLine
  } from "$lib/apis/users";
  import {
    getInviteRewardTotal,
    syncRegisterReward,
    syncInviteReward,
  } from "$lib/apis/rewards";
  import { goto } from "$app/navigation";
  import BarChart from "$lib/components/common/echarts/BarChart.svelte";
  import LineChart from "$lib/components/common/echarts/LineChart.svelte";
  import { showSidebar } from "$lib/stores";
  import { toast } from "svelte-sonner";

  const i18n = getContext("i18n");

  let userTotal: number = 0;
  let walletTotal: number = 0;
  let channelTotal: number = 0;
  let vipTotal: number = 0;
  let activeToday: number = 0;
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

  let registLoaded = false;
  let regist_total = 0;
  let reward_total = 0;
  let issue_total = 0;
  let regist_reward_per = "0";

  let inviteLoaded = false;
  let invite_total = 0;
  let invite_reward_total = 0;
  let invite_issue_total = 0;
  let invite_reward_per = "0";

  // 日活跃用户数
  let dailyLoaded = false;
  let dailylineXdata: any[] = [];
  let dailylineSeries: any[] = [];
  let dailyTitle = $i18n.t("Daily Active Users Data Distribution");

  const initInfo = () => {
    getDisperTotal(localStorage.getItem("token") || "").then((res) => {
      userTotal = res.total;
      walletTotal = res.wallet_total;
      channelTotal = res.channel_total;
      vipTotal = res.vip_total;
      activeToday = res.active_today;
      kycTotal = res.kyc_total;
    });
    getDisperUser(localStorage.getItem("token") || "").then((res) => {
      lineXdata = res.date_list;
      lineSeries.push({
        name: $i18n.t("Wallet User Total"),
        type: "line",
        data: res.wallet_list,
      });
      lineSeries.push({
        name: $i18n.t("Channel User Total"),
        type: "line",
        data: res.channel_list,
      });
      lineSeries.push({
        name: $i18n.t("KYC User Total"),
        type: "line",
        data: res.kyc_list,
      });
      lineLoaded = true;
    });
    getDailyUserLine(localStorage.getItem("token") || "").then((res) => {
      dailylineXdata = res.date_list;
      dailylineSeries.push({
        name: $i18n.t("Daily Active Users"),
        type: "line",
        data: res.users_list,
      });
      dailyLoaded = true;
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
    rewardsTotal();
    inviteRewardTotal();
  };

  function rewardsTotal() {
    getRewardsTotal(localStorage.getItem("token") || "").then((res) => {
      regist_total = res.regist_total;
      reward_total = res.reward_total;
      issue_total = res.issue_total;
      if (issue_total == 0) {
        regist_reward_per = reward_total == 0 ? "100" : "0";
      } else {
        let reward_per = (issue_total * 100) / reward_total;
        if (reward_per >= 100) {
          regist_reward_per = "100";
        } else {
          regist_reward_per = reward_per.toFixed(1);
        }
      }
      registLoaded = true;
    });
  }

  function inviteRewardTotal() {
    getInviteRewardTotal(localStorage.getItem("token") || "").then((res) => {
      invite_total = res.invite_total;
      invite_reward_total = res.invite_reward_total;
      invite_issue_total = res.invite_issue_total;
      if (invite_issue_total == 0) {
        invite_reward_per = invite_reward_total == 0 ? "100" : "0";
      } else {
        let invitee_per = (invite_issue_total * 100) / invite_reward_total;
        if (invitee_per >= 100) {
          invite_reward_per = "100";
        } else {
          invite_reward_per = invitee_per.toFixed(1);
        }
      }
      inviteLoaded = true;
    });
  }

  function syncregisterreward() {
    syncRegisterReward(localStorage.getItem("token") || "").then((res) => {
      rewardsTotal();
    });
  }

  function syncinviteereward() {
    syncInviteReward(localStorage.getItem("token") || "").then((res) => {
      inviteRewardTotal();
    });
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
      class="flex flex-col flex-1 min-w-[300px] items-center bg-sky-100 dark:bg-sky-300 rounded-lg px-2 py-4 m-3"
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
      class="flex flex-col flex-1 min-w-[300px] items-center bg-teal-100 dark:bg-teal-300 rounded-lg px-2 py-4 m-3"
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
      class="flex flex-col flex-1 min-w-[300px] items-center bg-blue-100 dark:bg-blue-300 rounded-lg px-2 py-4 m-3"
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
      class="flex flex-col flex-1 min-w-[300px] items-center bg-violet-100 dark:bg-violet-300 rounded-lg px-2 py-4 m-3"
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
      class="flex flex-col flex-1 min-w-[300px] items-center bg-violet-100 dark:bg-violet-300 rounded-lg px-2 py-4 m-3"
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
      class="flex flex-col flex-1 min-w-[300px] items-center bg-pink-100 dark:bg-pink-300 rounded-lg px-2 py-4 m-3"
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

  <!-- <div class="px-5">
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
  </div> -->

  <div class="px-5 mt-2">
    {#if dailyLoaded}
      <div class="w-full bg-gray-100 dark:bg-gray-50 rounded-lg p-5">
        <LineChart
          bind:title={dailyTitle}
          bind:xData={dailylineXdata}
          bind:seriesData={dailylineSeries}
          bind:resize
        />
      </div>
    {/if}
  </div>

  <div
    class="flex justify-between flex-wrap text-gray-700 dark:text-gray-100 pt-1 pb-1"
  >
    {#if thirdLoaded && vipLoaded}
      <div
        class="flex-1 min-w-[300px] bg-gray-100 dark:bg-gray-50 rounded-lg p-5 mx-5 mt-5 mb-2"
      >
        <BarChart
          bind:xData={thirdXdata}
          bind:seriesData={thirdSeries}
          bind:title={thirdTitle}
          bind:resize
        />
      </div>
      <div
        class="flex-1 min-w-[300px] bg-gray-100 dark:bg-gray-50 rounded-lg p-5 mx-5 mt-5 mb-2"
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

  <div
    class="flex justify-between flex-wrap text-gray-700 dark:text-gray-100 pt-1 pb-4"
  >
    {#if registLoaded && inviteLoaded}
      <div
        class="flex-1 min-w-[300px] bg-gray-100 dark:bg-gray-50 rounded-lg p-5 mx-5 mt-2 mb-5"
      >
        <div class="flex justify-between">
          <div class="text-lg text-gray-900 font-semibold">
            {$i18n.t("Registration Rewards")}
          </div>
          <button
            class="text-sm text-gray-700 font-semibold"
            on:click={async () => {
              if (regist_reward_per == "100") {
                toast.success(
                  $i18n.t("There is no data that can be synchronized.")
                );
              } else {
                toast.success(
                  $i18n.t("The synchronous request was sent successfully.")
                );
                syncregisterreward();
              }
            }}
          >
            {$i18n.t("Sync Data")} >
          </button>
        </div>

        <hr class=" my-2 dark:border-gray-850 w-full" />
        <div class="flex justify-between">
          <div class="flex flex-col mt-2">
            <div class="flex flex-col text-gray-900">
              <div class="text-sm font-semibold">
                {$i18n.t("Total Of Rewards")}
              </div>
              <div class="text-3xl font-semibold">{regist_total}</div>
            </div>
            <div class="flex flex-col text-gray-900 mt-1">
              <div class="text-sm font-semibold">
                {$i18n.t("Should Be Issued")}
              </div>
              <div class="text-sm text-gray-600">
                ({$i18n.t("Total rewards for KYC-authenticated users")})
              </div>
              <div class="text-3xl font-semibold">{reward_total}</div>
            </div>
            <div class="flex flex-col text-gray-900 mt-1">
              <div class="text-sm font-semibold">
                {$i18n.t("Actually Issued")}
              </div>
              <div class="text-sm text-gray-600">
                ({$i18n.t(
                  "Total rewards actually for KYC-authenticated users."
                )})
              </div>
              <div class="text-3xl font-semibold">{issue_total}</div>
            </div>
          </div>
          <div class="flex-1 flex justify-center items-center">
            <div
              class="flex flex-col justify-center items-center w-[200px] h-[200px] bw-16 rounded-full
              {regist_reward_per == '100'
                ? 'border-green-800'
                : 'border-yellow-600'}"
            >
              <div class="text-gray-900">{$i18n.t("Completion Rate")}</div>
              <div class="text-3xl font-semibold text-gray-900">
                {regist_reward_per}%
              </div>
            </div>
          </div>
        </div>
      </div>
      <div
        class="flex-1 min-w-[300px] bg-gray-100 dark:bg-gray-50 rounded-lg p-5 mx-5 mt-2 mb-5"
      >
        <div class="flex justify-between">
          <div class="text-lg text-gray-900 font-semibold">
            {$i18n.t("Invite Rewards")}
          </div>
          <button
            class="text-sm text-gray-700 font-semibold"
            on:click={async () => {
              if (invite_reward_per == "100") {
                toast.success(
                  $i18n.t("There is no data that can be synchronized.")
                );
              } else {
                toast.success(
                  $i18n.t("The synchronous request was sent successfully.")
                );
                syncinviteereward();
              }
            }}
          >
            {$i18n.t("Sync Data")} >
          </button>
        </div>
        <hr class=" my-2 dark:border-gray-850 w-full" />
        <div class="flex justify-between">
          <div class="flex flex-col mt-2">
            <div class="flex flex-col text-gray-900">
              <div class="text-sm font-semibold">
                {$i18n.t("Total Of Rewards")}
              </div>
              <div class="text-3xl font-semibold">{invite_total}</div>
            </div>
            <div class="flex flex-col text-gray-900 mt-1">
              <div class="text-sm font-semibold">
                {$i18n.t("Should Be Issued")}
              </div>
              <div class="text-sm text-gray-600">
                ({$i18n.t("Total rewards for KYC-authenticated users")})
              </div>
              <div class="text-3xl font-semibold">{invite_reward_total}</div>
            </div>
            <div class="flex flex-col text-gray-900 mt-1">
              <div class="text-sm font-semibold">
                {$i18n.t("Actually Issued")}
              </div>
              <div class="text-sm text-gray-600">
                ({$i18n.t(
                  "Total rewards actually for KYC-authenticated users."
                )})
              </div>
              <div class="text-3xl font-semibold">{invite_issue_total}</div>
            </div>
          </div>
          <div class="flex-1 flex justify-center items-center">
            <div
              class="flex flex-col justify-center items-center w-[200px] h-[200px] bw-16 rounded-full
              {invite_reward_per == '100'
                ? 'border-green-800'
                : 'border-yellow-600'}"
            >
              <div class="text-gray-900">{$i18n.t("Completion Rate")}</div>
              <div class="text-3xl font-semibold text-gray-900">
                {invite_reward_per}%
              </div>
            </div>
          </div>
        </div>
      </div>
    {/if}
  </div>
</div>

<style>
  .bw-16 {
    border-width: 16px;
  }
</style>
