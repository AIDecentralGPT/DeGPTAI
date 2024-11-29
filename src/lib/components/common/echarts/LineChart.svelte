<script lang="ts">
  import { getContext, onMount } from "svelte";
  import * as echarts from "echarts";
  import { theme } from "$lib/stores";

  const i18n = getContext("i18n");

  // 定义指定的颜色数组
  const specifiedColors = ["#5470C6", "#91CC75", "#FAC858"];

  export let xData: any[] = [];

  export let title: string = "";

  export let seriesData: any[] = [];

  let chartInstance: echarts.ECharts | null = null;
  let chartRef: HTMLElement | null = null;

  let option = {
    title: {
      text: "近30天用户注册分布图",
      textStyle: {
        color: "#ffffff",
      },
    },
    grid: {
      left: "10",
      right: "10",
      top: "50",
      bottom: "10",
      containLabel: true,
    },
    textStyle: {
      color: "#ffffff",
    },
    tooltip: {
      trigger: "axis",
    },
    calculable: true,
    xAxis: [
      {
        type: "category",
        boundaryGap: false,
        data: ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28"],
      },
    ],
    yAxis: [
      {
        type: "value",
        axisLabel: {
          formatter: "{value}",
        },
      },
    ],
    series: [
      {
        name: "渠道注册",
        type: "line",
        data: [11, 11, 15, 13, 12, 13, 10, 10, 11, 15, 13, 12, 13, 10, 11, 15, 13, 12, 13, 10, 10, 11, 15, 13, 12, 13, 10, 8],
      },
      {
        name: "钱包注册",
        type: "line",
        data: [1, 6, 2, 5, 3, 2, 0, 6, 2, 5, 3, 2, 0, 2, 5, 3, 2, 0, 6, 2, 5, 3, 2, 0, 2, 0, 2, 6],
      },
      {
        name: "访客数",
        type: "line",
        data: [2, 6, 3, 5, 2, 2, 5, 6, 3, 5, 2, 2, 1, 2, 6, 3, 1, 5, 8, 1, 5, 2, 2, 1, 2, 1, 2, 5],
      },
    ],
  };

  const initChart = () => {
    // option.xAxis[0].data = xData;
    // option.series[0].data = seriesData;
    $theme = $theme ?? "dark";
    const textColor = $theme.indexOf("dark") >= 0 ? "#000" : "#000";
    option.textStyle.color = textColor;
    option.title.textStyle.color = textColor;
    chartInstance?.setOption(option);
  };

  onMount(() => {
    if (chartRef) {
      chartInstance = echarts.init(chartRef);
    }
  });

  $: if (xData || seriesData) {
    if (chartRef) {
      initChart();
    } else {
      if (chartInstance) {
        chartInstance.dispose();
        chartInstance = null;
      }
    }
  }

  export let resize: number = 0;
  $: if(resize) {
    chartInstance?.resize();
  }
</script>

<div
  class="chart w-full h-[300px] text-gray-300 dark:text-gray-800"
  bind:this={chartRef}
/>
