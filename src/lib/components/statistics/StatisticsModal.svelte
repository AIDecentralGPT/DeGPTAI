<script lang="ts">
  import { getContext } from "svelte";

  import * as echarts from "echarts";

  import Modal from "../common/Modal.svelte";

  const i18n = getContext("i18n");

  export let show = false;

  let chartInstance;
  let chartRef: any;

  let option = {
    // Echarts图表配置选项
    xAxis: {
      type: "category",
      data: ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"],
    },
    yAxis: {
      type: "value",
    },
    series: [
      {
        data: [5, 20, 36, 10, 10, 20],
        type: "bar",
      },
    ],
  };

  $: if (show) {
    console.log("=======================show====================");
    chartInstance = echarts.init(chartRef);
    chartInstance.setOption(option);
  }
</script>

<Modal bind:show>
  <div class="text-gray-700 dark:text-gray-100 px-5 pt-4 pb-4">
    <h2 class="text-2xl font-bold mb-4">Channel</h2>
    <div class="chart" bind:this={chartRef} />
  </div>
</Modal>

<style>
</style>
