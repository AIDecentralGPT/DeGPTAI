<script lang="ts">
  import { getContext, tick } from "svelte";
  import { showSidebar } from "$lib/stores";
  import { RealTimeSpeech } from "../../../../plugins/rtspeech";

  const i18n = getContext("i18n");

  export let show = false;
  export let prompt: string = "";

  let isRecording = false;
  let isListening = false;
  let isSend = false;
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

  let spanload = "...";
  let spanLoadTimer = null;
  const textLoading = () => {
    if (spanLoadTimer) {
      clearInterval(spanLoadTimer);
    }
    spanLoadTimer = setInterval(() => {
      switch (spanload) {
        case "...": // 3个点 → 1个点
          spanload = ".";
          break;
        case ".": // 1个点 → 2个点
          spanload = "..";
          break;
        case "..": // 2个点 → 3个点
          spanload = "...";
          break;
      }
    }, 200);
  };
  const textEndLoading = () => {
    if (spanLoadTimer) {
      clearInterval(spanLoadTimer);
    }
    spanload = "...";
  };

  // =========== 新语音识别代码 ============
  // 开始语音识别
  let volumeListener: any = null;
  let textListener: any = null;
  const startListening = async () => {
    if (!isListening) {
      textLoading();
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
        textEndLoading();
      }, 200);
    }
  };
</script>

<div
  class="fixed bottom-0 shadow-[0_-4px_15px_rgba(0,0,0,0.15)] rounded-2xl mx-4 mb-20 {$showSidebar
    ? 'left-0 md:left-[246px]'
    : 'left-0'} right-0"
>
  <!-- 语音录入界面 -->
  <div class="bg-white dark:bg-gray-800 rounded-2xl shadow-md w-full p-8">
    <!-- 声音波动动画容器 -->
    <div class="flex flex-col rounded-lg px-3 pt-3 pb-2 mb-2">
      <span class="text-gray-800 dark:text-gray-50">{prompt} {spanload}</span>
      <div class="flex justify-end">
        <div bind:clientWidth={divWidth} 
          class={`flex justify-center items-center gap-1 h-12`}>
          {#each soundBars as bar}
            <div class="bg-gray-800 dark:bg-gray-50 {bar.width}" style="height: {bar.height}" />
          {/each}
        </div>
      </div>
    </div>
    <p class="text-center text-gray-500 text-sm">
      {$i18n.t(
        "Hold down the microphone to speak, and release it to end the recording"
      )}
    </p>
  </div>
</div>

<style>
  .record-animation {
    animation: pulse 0.6s infinite;
  }
  @keyframes pulse {
    0% {
      transform: translate(-50%, -50%) scale(1);
      opacity: 0.8;
    }
    25% {
      transform: translate(-50%, -50%) scale(1.1);
      opacity: 0.6;
    }
    50% {
      transform: translate(-50%, -50%) scale(1.2);
      opacity: 0.4;
    }
    75% {
      transform: translate(-50%, -50%) scale(1.3);
      opacity: 0.2;
    }
    100% {
      transform: translate(-50%, -50%) scale(1.4);
      opacity: 0;
    }
  }
</style>
