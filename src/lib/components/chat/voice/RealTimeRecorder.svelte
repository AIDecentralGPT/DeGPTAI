<script lang="ts">
  import { getContext, tick } from "svelte";
  import { showSidebar } from "$lib/stores";
  import { RealTimeSpeech } from "../../../../plugins/rtspeech";

  const i18n = getContext("i18n");

  export let show = false;
  export let prompt: string = "";

  let isRecording = false;
  let isListening = false;
  let isCancel = false;
  let soundBars: any[] = [];

  // 发消息需要
  let user: any = null;
  let toolInfo: any = { url: "", trantip: "" };

  // 初始化声波柱数据
  let divWidth: any;
  $: if (divWidth !== undefined) {
    console.log("宽度变化了：", divWidth);
    // 这里可以添加你的逻辑，比如根据宽度调整其他元素
    handleWidthChange(divWidth);
    startListening();
  }

  const handleWidthChange = (width: any) => {
    // 更简洁的写法
    soundBars = Array.from({ length: Math.floor(width / 7) }, () => {
      return {
        width: "w-[2px]",
        height: "3px",
      };
    });
  };

  $: if (show) {
    prompt = "";
  }

  // =========== 新语音识别代码 ============
  // 开始语音识别
  let volumeListener: any = null;
  let textListener: any = null;
  const startListening = async () => {
    if (!isListening) {
      try {
        const perState = await RealTimeSpeech.checkPermissions();
        if (perState.audio != "granted") {
          const perState = await RealTimeSpeech.requestPermissions();
          if (perState.audio != "granted") {
            return;
          }
        }
        const ret = await RealTimeSpeech.startRecording();
        if (ret?.status) {
          isRecording = true;
          isListening = true;
          volumeListener = await RealTimeSpeech.addListener(
            "volumeChange",
            async (data) => {
              if (data?.db && data.db > 53) {
                await assignSoundBars(Math.floor((data.db - 50) / 2.5) + 3);
              } else {
                await assignSoundBars(3);
              }
            }
          );
          textListener = await RealTimeSpeech.addListener(
            "textChange",
            async (data) => {
              // if (data?.text) {
              //   prompt = prompt + data?.text;
              // }
              if (data?.content) {
                prompt = prompt + data?.content;
              }
            }
          );
        }
      } catch (error) {
        console.error("启动失败:", error);
      }
    }
  };
  const assignSoundBars = async (param: number) => {
    const newSoundBars = [...soundBars];
    newSoundBars.shift();
    newSoundBars.push({ width: "w-[2px]", height: `${param}px` });
    soundBars = newSoundBars;
    await tick();
  };

  // 停止语音识别
  const stopListening = async () => {
    console.log("=================stopListening===================");
    if (isListening) {
      const timerId = setTimeout(async () => {
        const ret = await RealTimeSpeech.stopRecording();
        if (ret?.status) {
          isListening = false;
          if (volumeListener) {
            volumeListener.remove();
          }
          if (textListener) {
            textListener.remove();
          }
        }
        clearInterval(timerId);
      }, 200);
    }
  };

  // 触摸结束
  document.addEventListener("touchend", () => {
    // if (isListening) {
    // }
    console.log("触摸结束");
  });
</script>

<div
  class="fixed bottom-0 shadow-[0_-4px_15px_rgba(0,0,0,0.15)] rounded-2xl mx-2.5 md:mx-20 mb-4 inset-x-0
  {$showSidebar ? 'left-0 md:left-[246px]' : 'left-0'} right-0 text-center"
>
  <div class="text-sm pt-10">
    {$i18n.t("Release to send, Swipe up to cancel")}
  </div>
  <!-- 语音录入界面 -->
  <div
    class="{isCancel
      ? 'bg-red-700'
      : 'bg-green-700'} rounded-2xl shadow-md w-full p-2 mt-4"
  >
    <!-- 声音波动动画容器 -->
    <div class="flex flex-col rounded-lg">
      <div class="flex justify-end">
        <div
          bind:clientWidth={divWidth}
          class={`flex justify-center items-center gap-1 w-full h-8`}
        >
          {#each soundBars as bar}
            <div class="bg-gray-50 {bar.width}" style="height: {bar.height}" />
          {/each}
        </div>
      </div>
    </div>
  </div>
</div>

<style>
</style>
