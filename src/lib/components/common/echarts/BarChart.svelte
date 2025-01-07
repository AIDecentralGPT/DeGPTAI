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
      text: title,
      textStyle: {
        color: "#ffffff",
      },
    },
    textStyle: {
      color: "#ffffff",
    },
    grid: {
      left: "10",
      right: "10",
      top: "50",
      bottom: "10",
      containLabel: true,
    },
    tooltip: {
      trigger: "axis",
    },
    calculable: true,
    xAxis: [
      {
        type: "category",
        data: [],
      },
    ],
    yAxis: [
      {
        type: "value",
      },
    ],
    series: [
      {
        name: $i18n.t("Total"),
        type: "bar",
        data: [],
        barWidth: 30,
        itemStyle: {
          // 通过回调函数根据索引来获取对应的颜色，实现颜色循环使用
          color: function (params: any) {
            return specifiedColors[params.dataIndex % specifiedColors.length];
          },
        },
      },
    ],
  };

  const initChart = () => {
    option.xAxis[0].data = xData;
    option.series[0].data = seriesData;
    $theme = $theme ?? "light";
    // $theme = $theme ?? "dark";
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