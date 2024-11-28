<script lang="ts">
  import { getContext, onMount } from "svelte";
  import dayjs from "dayjs";
  import * as echarts from "echarts";
  import { theme, showSidebar } from "$lib/stores";
  import { getThirdTotal, getThirdPage } from "$lib/apis/users";
  import { copyToClipboard } from "$lib/utils";
  import { toast } from "svelte-sonner";
  import { goto } from "$app/navigation";
  import Pagination from "$lib/components/common/Pagination.svelte";
  import DatePicker from "$lib/components/common/DatePicker.svelte";

  const i18n = getContext("i18n");

  let loaded = false;

  let chartInstance: echarts.ECharts | null = null;
  let chartRef: HTMLElement | null = null;

  // 定义指定的颜色数组
  const specifiedColors = ["#5470C6", "#91CC75", "#FAC858"];

  let option = {
    textStyle: {
      color: "#ffffff",
    },
    grid: {
      left: "2",
      right: "10",
      top: "0",
      bottom: "0",
      containLabel: true,
    },
    tooltip: {
      trigger: "axis",
    },
    calculable: true,
    xAxis: [
      {
        type: "value",
        boundaryGap: [0, 0.01],
      },
    ],
    yAxis: [
      {
        type: "category",
        data: [],
      },
    ],
    series: [
      {
        name: $i18n.t("Total"),
        type: "bar",
        data: [],
        itemStyle: {
          // 通过回调函数根据索引来获取对应的颜色，实现颜色循环使用
          color: function (params: any) {
            return specifiedColors[params.dataIndex % specifiedColors.length];
          },
        },
      },
    ],
  };

  const initChart = async () => {
    option.yAxis[0].data = [];
    option.series[0].data = [];
    chartInstance = echarts.init(chartRef);
    $theme = $theme ?? "dark";
    const textColor = $theme.indexOf("dark") >= 0 ? "#fff" : "#000";
    option.textStyle.color = textColor;
    const res = await getThirdTotal(localStorage.getItem("token") || "");
    if (res) {
      let total = 0;
      channelList = [];
      res.forEach((item: any) => {
        total += item?.total;
        option.yAxis[0].data.push(item?.channel);
        option.series[0].data.push(item?.total);
        channelList.push(item?.channel);
      });
      option.yAxis[0].data.push($i18n.t("Total"));
      option.series[0].data.push(total);
    }
    chartInstance.setOption(option);
  };

  onMount(async () => {
    if (loaded && chartRef) {
      await initChart();
    }
    loaded = true;
  });

  $: if (loaded) {
    (async () => {
      if (chartRef) {
        if (!chartInstance) {
          await initChart();
        }
      } else {
        if (chartInstance) {
          chartInstance.dispose();
          chartInstance = null;
        }
      }
    })();
  }

  // 监听窗口大小改变事件
  window.onresize = function () {
    chartInstance?.resize();
  };
  $: if ($showSidebar) {
    setTimeout(() => {
      chartInstance?.resize();
    }, 200);
  }
  $: if (!$showSidebar) {
    setTimeout(() => {
      chartInstance?.resize();
    }, 200);
  }

  // 分页功能
  let loading = false;
  let page = 1;
  let pageSize = 10;
  let channelList: string[] = ["simitalk", "telegram", "discord"];
  let channel = "";
  let selectedDate: Date;
  let firstCtrl = true;
  let thirdList = { row: [], total: 1 };

  $: if (page || channel) {
    fetchData();
  }

  function fetchData() {
    loading = true;
    if (firstCtrl) {
      firstCtrl = false;
      thirdList = { row: [], total: 0 };
    }
    getThirdPage(localStorage.token, {
      pageSize: pageSize,
      pageNum: page,
      channel: channel
    })
      .then((result) => {
        loading = false;
        thirdList = result;
        console.log("rewardsHistory", thirdList);
      })
      .catch((error) => {
        loading = false;
      });
  }

  function formateAddress(val: string) {
    return val.substring(0, 6) + "*****" + val.substring(val.length - 2);
  }
</script>

<div class=" flex flex-col w-full min-h-screen">
  {#if loaded}
    <div class="flex justify-between px-4 pt-3 mt-0.5 mb-1 w-full">
      <div class="flex items-center text-xl font-semibold">
        {$i18n.t("Third registration")}
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

    <div class="text-gray-700 dark:text-gray-100 px-5 pt-4 pb-4">
      <div
        class="chart w-full h-[160px] text-gray-300 dark:text-gray-800"
        bind:this={chartRef}
      />
    </div>

    <hr class=" my-2 dark:border-gray-850 w-full" />

    <div
      class="mt-0.5 mb-2 gap-1 flex flex-col md:flex-row justify-between px-4"
    >
      <div class="flex md:self-center text-base font-medium px-0.5">
        {$i18n.t("All Users")}
        <div
          class="flex self-center w-[2px] h-4 mx-2.5 bg-gray-200 dark:bg-gray-700"
        />
        <span class="text-base font-medium text-gray-600 dark:text-gray-300"
          >{thirdList?.total}</span
        >
      </div>
      <div class="flex">
        <div class="flex">
          <select
            class="w-[100px] rounded-lg py-1.5 px-4 text-sm bg-gray-200 dark:bg-gray-850 dark:text-gray-300 disabled:text-gray-500 dark:disabled:text-gray-500 outline-none"
            on:change={(e) => {
              page = 1;
              channel = e.target?.value;
            }}
          >
            <option value=""> {$i18n.t("Channel")} </option>
            {#each channelList as item}
              <option value={item}>{item}</option>
            {/each}
          </select>
          <!-- <DatePicker bind:selectedDate={selectedDate} /> -->
        </div>
      </div>
    </div>

    <div
      class="max-w-full min-h-[30vh] bg-gray-50 dark:bg-gray-900 shadow-3xl px-4 overflow-auto relative"
    >
      <table
        class="w-full text-sm text-left text-gray-500 dark:text-gray-400 table-auto"
      >
        <thead
          class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-850 dark:text-gray-400"
        >
          <tr>
            <th scope="col" class="px-3 py-2">
              {$i18n.t("User Id")}
            </th>
            <th scope="col" class="px-3 py-2">
              {$i18n.t("Verified")}
            </th>
            <th scope="col" class="px-3 py-3">
              {$i18n.t("Channel")}
            </th>
            <th scope="col" class="px-3 py-2">
              {$i18n.t("Created at")}
            </th>
          </tr>
        </thead>
        {#if loading}
          <tr>
            <td colspan="6">
              <div class="py-[100px] w-full text-center text-lg">
                Loading...
              </div>
            </td>
          </tr>
        {:else}
          <tbody
            class="bg-white dark:bg-gray-900 text-gray-800 dark:text-gray-300 text-xs"
          >
            {#each thirdList?.row as thirdItem}
              <tr
                class="bg-white border-b dark:bg-gray-900 dark:border-gray-700 text-xs"
              >
                <td class="px-6 py-3 whitespace-nowrap">
                  {formateAddress(thirdItem?.id)}
                  <button
                    on:click={async () => {
                      const res = await copyToClipboard(thirdItem?.id);
                      if (res) {
                        toast.success(
                          $i18n.t("Copying to clipboard was successful!")
                        );
                      }
                    }}
                    type="button"
                    class="px-3 py-2 text-sm-12 dark:text-gray-300 dark:bg-gray-650 rounded-md fs12"
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
                </td>
                <td class="px-6 py-3 whitespace-nowrap">
                  {#if thirdItem?.verified}
                    {$i18n.t("Yes")}
                  {:else}
                    {$i18n.t("No")}
                  {/if}
                </td>
                <td class="px-6 py-3 whitespace-nowrap">
                  {thirdItem?.channel}
                </td>
                <td class="px-6 py-3 whitespace-nowrap">
                  {dayjs(thirdItem?.created_at * 1000).format("YYYY-MM-DD HH:mm:ss")}
                </td>
              </tr>
            {/each}
          </tbody>
        {/if}
      </table>
    </div>

    {#if !loading && thirdList?.row?.length > 0}
      <Pagination bind:page count={thirdList?.total} />
    {/if}
  {/if}
</div>

<style>
</style>
