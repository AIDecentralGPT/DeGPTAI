<script lang="ts">
  import { getContext, onMount } from "svelte";
  import dayjs from "dayjs";
  import * as echarts from "echarts";
  import { theme } from "$lib/stores";
  import Modal from "../common/Modal.svelte";
  import { getThirdTotal, getThirdPage } from "$lib/apis/users";
  import { copyToClipboard } from "$lib/utils";
  import { toast } from "svelte-sonner";

  const i18n = getContext("i18n");

  export let show = false;

  let chartInstance: echarts.ECharts | null = null;
  let chartRef: HTMLElement | null = null;

  // 定义指定的颜色数组
  const specifiedColors = ["#5470C6", "#91CC75", "#FAC858"];

  let option = {
    textStyle: {
      color: "#ffffff",
    },
    grid: {
      left: "10",
      right: "50",
      top: "35",
      bottom: "5",
      containLabel: true,
    },
    title: {
      text: $i18n.t("Third registration"),
      textStyle: {
        fontSize: 16,
        color: "#ffffff",
      },
    },
    tooltip: {
      trigger: "axis",
    },
    toolbox: {
      show: true,
      itemSize: 10,
      iconStyle: {
        color: "#ffffff",
        borderColor: "#ffffff",
      },
      feature: {
        // 自定义按钮配置
        myButton: {
          show: true,
          icon: "path://M912.082824 60.235294l42.586352 42.586353-404.60047 404.660706 404.60047 404.600471-42.586352 42.586352-404.600471-404.60047-404.660706 404.60047L60.235294 912.082824l404.660706-404.600471L60.235294 102.821647 102.821647 60.235294l404.660706 404.660706L912.082824 60.235294z",
          onclick: function () {
            show = false;
          },
        },
      },
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
    const textColor = $theme.indexOf("dark") >= 0 ? "#fff" : "#000";
    option.textStyle.color = textColor;
    option.title.textStyle.color = textColor;
    option.toolbox.iconStyle.color = textColor;
    option.toolbox.iconStyle.borderColor = textColor;
    const res = await getThirdTotal(localStorage.getItem("token") || "");
    if (res) {
      let total = 0;
      res.forEach((item: any) => {
        total += item?.total;
        option.yAxis[0].data.push(item?.channel);
        option.series[0].data.push(item?.total);
      });
      option.yAxis[0].data.push($i18n.t("Total"));
      option.series[0].data.push(total);
    }
    option.title.text = $i18n.t("Third registration");
    chartInstance.setOption(option);
  };

  onMount(async () => {
    if (show && chartRef) {
      await initChart();
    }
  });

  $: if (show) {
    (async () => {
      if (chartRef) {
        if (!chartInstance) {
          await initChart();
          fetchData();
        }
      } else {
        if (chartInstance) {
          chartInstance.dispose();
          chartInstance = null;
        }
      }
    })();
  }

  // 分页功能
  let currentPage = 1;
  let prePage = 1;
  let pageSize = 10;
  let loading = false;
  let firstCtrl = true;
  let thirdList = { row: [], total: 1 };

  $: pageTotal =
    Math.ceil(thirdList?.total / pageSize) == 0
      ? "1"
      : Math.ceil(thirdList?.total / pageSize);
  $: if (currentPage != prePage) {
    (async () => {
      await fetchData();
    })();
  }

  function previousPage() {
    if (currentPage > 1) {
      currentPage--;
    }
  }

  function nextPage() {
    if (currentPage < Math.ceil(thirdList?.total / pageSize)) {
      currentPage++;
    }
  }

  function fetchData() {
    loading = true;
    if (firstCtrl) {
      firstCtrl = false;
      thirdList = { row: [], total: 1 };
    }
    prePage = currentPage;
    getThirdPage(localStorage.token, {
      pageSize: pageSize,
      pageNum: currentPage,
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

<Modal bind:show size="lg">
  <div class="text-gray-700 dark:text-gray-100 px-5 pt-4 pb-4">
    <div
      class="chart w-full h-[200px] text-gray-300 dark:text-gray-800"
      bind:this={chartRef}
    />
  </div>
  <div
    class=" m-auto rounded-2xl max-w-full min-h-[50vh] max-h-[60vh] mx-2 bg-gray-50 dark:bg-gray-900 shadow-3xl p-4 overflow-auto relative"
  >
    <table class="min-w-full divide-y divide-gray-200 overflow-auto">
      <thead class="dark:border-gray-200 border-b">
        <tr>
          <th
            class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider whitespace-nowrap"
          >
            {$i18n.t("id")}
          </th>
          <th
            class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider whitespace-nowrap"
          >
            {$i18n.t("verified")}
          </th>
          <th
            class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider whitespace-nowrap"
          >
            {$i18n.t("channel")}
          </th>
          <th
            class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider whitespace-nowrap"
          >
            {$i18n.t("create_at")}
          </th>
        </tr>
      </thead>
      <tbody
        class="bg-white dark:bg-gray-900 text-gray-800 dark:text-gray-300 text-xs"
      >
        {#each thirdList?.row as thirdItem}
          <tr>
            <td class="px-6 py-4 whitespace-nowrap">
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
            <td class="px-6 py-4 whitespace-nowrap">
              {#if thirdItem?.verified}
                {$i18n.t("Yes")}
              {:else}
                {$i18n.t("No")}
              {/if}
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              {thirdItem?.channel}
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              {dayjs(thirdItem?.created_at).format("YYYY-MM-DD HH:mm:ss")}
            </td>
          </tr>
        {/each}
      </tbody>
    </table>
    {#if loading}
      <div
        class="flex items-center justify-center inset-0 z-10 bg-opacity-50 w-full absolute"
      >
        <div
          class="flex items-center justify-center bg-gray-300 w-[100px] h-[100px] rounded-xl opacity-60"
        >
          <svg
            class="animate-spin"
            xmlns="http://www.w3.org/2000/svg"
            width="30"
            height="30"
            viewBox="0 0 24 24"
          >
            <path
              fill="white"
              d="M12 20q-3.35 0-5.675-2.325T4 12t2.325-5.675T12 4q1.725 0 3.3.712T18 6.75V4h2v7h-7V9h4.2q-.8-1.4-2.187-2.2T12 6Q9.5 6 7.75 7.75T6 12t1.75 4.25T12 18q1.925 0 3.475-1.1T17.65 14h2.1q-.7 2.65-2.85 4.325T12 20"
            />
          </svg>
        </div>
      </div>
    {/if}
  </div>
  <div
    class="flex justify-center items-center h-[50px] pt-5 pb-10 text-gray-800 dark:text-gray-300"
  >
    <button
      class="px-1.5 py-1.5 mr-4 bg-gray-300 dark:bg-white dark:text-zinc-950 text-gray-100 rounded-full"
      on:click={previousPage}
    >
      <svg
        class="icon"
        viewBox="0 0 1024 1024"
        version="1.1"
        xmlns="http://www.w3.org/2000/svg"
        width="12"
        height="12"
      >
        <path
          d="M510.0475173 510.0475173l3.9049654 3.9049654-3.9049654-3.9049654zM514.38636775 509.61363225l-4.7727355 4.7727355c1.73554016-1.51859766 3.25413782-3.03719531 4.7727355-4.7727355z"
          fill="#515151"
        />
        <path
          d="M216.74122852 512.21694254c0 18.00622928 6.72521815 34.27691837 18.00622926 46.64264205l4.77273549 4.77273547 46.64264205 46.64264208L689.0250974 1013.13722421c26.90087265 26.90087265 71.157147 26.90087265 98.27496213 0 26.90087265-26.90087265 26.90087265-71.157147 0-98.27496216L384.22085499 512l402.86226199-403.07920455c26.90087265-26.90087265 26.90087265-71.157147 0-98.27496217-26.90087265-26.90087265-71.157147-26.90087265-98.05801958 0.21694251L286.16283532 413.72503786l-47.29346962 47.29346962-3.90496539 3.90496538c-11.49795361 12.3657237-18.44011431 29.07029783-18.22317179 47.29346968z"
          fill="#515151"
        />
      </svg>
    </button>
    <div class="fs-16">{currentPage} / {pageTotal}</div>
    <button
      class="px-1.5 py-1.5 ml-4 bg-gray-300 dark:bg-white dark:text-zinc-950 text-gray-100 rounded-full"
      on:click={nextPage}
    >
      <svg
        class="icon"
        viewBox="0 0 1024 1024"
        version="1.1"
        xmlns="http://www.w3.org/2000/svg"
        width="12"
        height="12"
      >
        <path
          d="M784.246262 454.443749L360.714443 30.88935a85.577949 85.577949 0 0 0-120.983285 121.005865l363.062756 363.040176-363.085336 362.995017a85.577949 85.577949 0 0 0 120.983285 120.983285l423.554399-423.464079a85.510209 85.510209 0 0 0 0-121.005865z"
          fill="#515151"
        />
      </svg>
    </button>
  </div>
</Modal>

<style>
</style>
