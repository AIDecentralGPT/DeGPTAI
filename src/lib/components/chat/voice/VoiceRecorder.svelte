<script lang="ts">
  import { getContext, tick } from "svelte";
  import { showSidebar } from "$lib/stores";
  import { VoiceRecord } from "../../../../plugins/voice";
  import { toast } from "svelte-sonner";

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

  let filePath = "";
  $: if (show) {
    filePath = "";
    prompt = "";
  }

  // =========== 新语音识别代码 ============
  // 开始语音识别
  let volumeListener: any = null;
  const startListening = async () => {
    if (!isListening) {
      try {
        const perState = await VoiceRecord.checkPermissions();
        if (perState.audio != "granted") {
          const perState = await VoiceRecord.requestPermissions();
          if (perState.audio != "granted") {
            return;
          }
        }
        const ret = await VoiceRecord.startRecording({filePath});
        if (ret?.status) {
          filePath = ret.filePath;
          isRecording = true;
          isListening = true;
          volumeListener = await VoiceRecord.addListener(
            "volumeChange",
            async (data) => {
              if (data?.db && data.db > 53) {
                console.log("进入db", data.db, data.level);
                await assignSoundBars(Math.floor((data.db - 50) / 2.5) + 3);
              } else {
                await assignSoundBars(3);
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

  // 暂停语音识别
  const pauseListening = async () => {
    if (isListening) {
      const timerId = setTimeout(async () => {
        const ret = await VoiceRecord.pauseRecording();
        if (ret?.status) {
          isListening = false;
          if (volumeListener) {
            volumeListener.remove();
          }
        }
        clearInterval(timerId);
      }, 200);
    }
  };

  // 发送录音
  const sendRecoding = async () => {
    if (isRecording) {
      isSend = true;
      const timerId = setTimeout(async () => {
        const ret = await VoiceRecord.sendRecording();
        if (ret?.status) {   
          if (volumeListener) {
            volumeListener.remove();
          }
          if (ret?.message) {
            prompt = ret?.message;
          } else {
            toast.error($i18n.t("No text recognized"));
          }
          isRecording = false;
        }
        clearInterval(timerId);
        show = false;
      }, 200);
    } else {
      toast.error($i18n.t("No text recognized"));
      show = false;
    }
  };

  // 取消录音
  const cancleRecoding = async () => {
    if (isRecording) {
      const timerId = setTimeout(async () => {
        const ret = await VoiceRecord.cancelRecording();
        if (ret?.status) {
          if (volumeListener) {
            volumeListener.remove();
          }
          isRecording = false;
        }
        clearInterval(timerId);
        show = false;
      }, 200);
    } else {
      show = false;
    }
  };
</script>

<div
  class="fixed bottom-0 shadow-[0_-4px_15px_rgba(0,0,0,0.15)] rounded-t-2xl {$showSidebar
    ? 'left-0 md:left-[246px]'
    : 'left-0'} right-0"
>
  <!-- 语音录入界面 -->
  <div class="bg-white dark:bg-gray-800 rounded-t-2xl shadow-md w-full p-8">
    <!-- 声音波动动画容器 -->
    <div
      bind:clientWidth={divWidth}
      class={`flex justify-center items-center gap-1 h-12 mb-10 rounded-lg bg-green-600`}
    >
      {#each soundBars as bar}
        <div class="bg-gray-50 {bar.width}" style="height: {bar.height}" />
      {/each}
    </div>

    <!-- 底部操作区 -->
    <div class="flex justify-between items-center">
      <div class="text-gray-500 flex flex-col items-center">
        <button
          class="text-sm ml-2 text-gray-600 dark:text-gray-400"
          on:click={ async () => {
            await cancleRecoding();
          }}>{$i18n.t("Cancel")}</button
        >
      </div>

      <div class="flex justify-center items-center w-20 h-20 relative">
        <div
          class="absolute top-1/2 left-1/2 w-20 h-20 rounded-full bg-primary/50 opacity-0 z-20
          {isListening ? 'record-animation' : ''}"
        />
        <!-- 中心按钮 -->
        <button
          class="rounded-full w-20 h-20 flex items-center justify-center border border-gray-100 shadow-lg bg-white dark:bg-gray-800 z-40"
          on:mousedown={async () => {
            await startListening();
          }}
          on:mouseup={async () => {
            await pauseListening();
          }}
          on:mouseleave={async () => {
            await pauseListening();
          }}
          on:touchstart|preventDefault={async () => {
            await startListening();
          }}
          on:touchend={async () => {
            await pauseListening();
          }}
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 20 20"
            fill="currentColor"
            class="w-10 h-10 translate-y-[0.5px] s-Fb8Dy0t5csK5"
            ><path
              d="M7 4a3 3 0 016 0v6a3 3 0 11-6 0V4z"
              class="s-Fb8Dy0t5csK5"
            /><path
              d="M5.5 9.643a.75.75 0 00-1.5 0V10c0 3.06 2.29 5.585 5.25 5.954V17.5h-1.5a.75.75 0 000 1.5h4.5a.75.75 0 000-1.5h-1.5v-1.546A6.001 6.001 0 0016 10v-.357a.75.75 0 00-1.5 0V10a4.5 4.5 0 01-9 0v-.357z"
              class="s-Fb8Dy0t5csK5"
            /></svg
          >
        </button>
      </div>

      <div class="text-wechat-red flex flex-col items-center">
        <button disabled={isSend}
          class="text-sm mr-2 text-gray-900 dark:text-gray-50 "
          on:click={async () => {
            await sendRecoding();
          }}>{$i18n.t("Done")}{isSend ? '...' : ''}</button
        >
      </div>
    </div>
    <p class="text-center text-gray-500 text-sm mt-6">
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
