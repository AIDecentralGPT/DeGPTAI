<script lang="ts">
  import { getContext, onMount } from "svelte";
  import * as echarts from "echarts";
  import { theme } from "$lib/stores";

  const i18n = getContext("i18n");

  export let title: string = "";

  export let xData: any[] = [];

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
    grid: {
      left: "10",
      right: "20",
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
        data: xData,
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
    series: seriesData,
  };

  const initChart = () => {
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
