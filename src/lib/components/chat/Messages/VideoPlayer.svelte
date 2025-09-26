<script lang="ts">
  export let audioinfo = {type: "base", data: ""};
  
  let audioElement: any;
  let duration: number = 0;
  let currentTime: number = 0;
  let progress: number = 0;
  let isPlaying = false;

  // 格式化时间
  function formatTime(seconds: number) {
    if (isNaN(seconds)) return "00:00";
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  }

  // 处理元数据加载完成
  function handleMetadataLoaded() {
    duration = audioElement.duration;
  }

  // 更新播放进度
  function updateProgress() {
    if (!audioElement || !duration) return;
    currentTime = audioElement.currentTime;
    progress = (currentTime / duration) * 100;
  }

  // 通过进度条调整播放位置
  function seek(e: any) {
    if (!audioElement || !duration) return;
    const rect = e.currentTarget.getBoundingClientRect();
    const pos = (e.clientX - rect.left) / rect.width;
    audioElement.currentTime = pos * duration;
  }

  // 播放/暂停切换
  function togglePlay() {
    if (!audioElement) return;
    if (isPlaying) {
      audioElement.pause();
    } else {
      audioElement.play();
    }
    isPlaying = !isPlaying;
  }
</script>

<div class="w-full">
  <div class="flex items-center w-full">
    <button class="ml-1"
      on:click={() => {
        togglePlay();
      }}
    >
      {#if isPlaying}
        <svg
          viewBox="0 0 24 24"
          fill="currentColor"
          width="1.2em"
          height="1.2em"
        >
          <path
            d="M6.5 7.75C6.5 7.05964 7.05964 6.5 7.75 6.5H9.25C9.94036 6.5 10.5 7.05964 10.5 7.75V16.25C10.5 16.9404 9.94036 17.5 9.25 17.5H7.75C7.05964 17.5 6.5 16.9404 6.5 16.25V7.75Z"
          /><path
            d="M13.5 7.75C13.5 7.05964 14.0596 6.5 14.75 6.5H16.25C16.9404 6.5 17.5 7.05964 17.5 7.75V16.25C17.5 16.9404 16.9404 17.5 16.25 17.5H14.75C14.0596 17.5 13.5 16.9404 13.5 16.25V7.75Z"
          />
        </svg>
      {:else}
        <svg
          viewBox="0 0 24 24"
          fill="currentColor"
          width="1.2em"
          height="1.2em"
        >
          <path
            d="M8 16.7229V7.27711C8 6.29075 9.08894 5.69298 9.9211 6.22254L17.3428 10.9454C18.1147 11.4366 18.1147 12.5634 17.3428 13.0546L9.92109 17.7775C9.08894 18.3071 8 17.7093 8 16.7229Z"
          />
        </svg>
      {/if}
    </button>
    <!-- 进度条 -->
    <div class="flex-1 progress-container min-w-[90px] mx-2" on:click={seek}>
      <div class="progress-bar" style="width: {progress}%" />
      <!-- 进度指示器 -->
      <div class="progress-thumb" style="left: {progress}%" />
    </div>
    <div class="mx-1">{ isPlaying ? formatTime(currentTime) : formatTime(duration) }</div>
  </div>
  <audio
    on:loadedmetadata={handleMetadataLoaded}
    on:timeupdate={updateProgress}
    on:ended={togglePlay}
    bind:this={audioElement}
    src={ audioinfo.type == "base" ? `data:audio/wav;codecs=1;base64,${audioinfo.data}` : audioinfo.data}
    hidden
  />
</div>

<style>
  .progress-container {
    flex: 1;
    height: 6px;
    background: #8f9399;
    border-radius: 3px;
    position: relative;
    cursor: pointer;
  }

  .progress-bar {
    height: 100%;
    background: rgba(184, 142, 86, 1);
    border-radius: 3px;
    transition: width 0.1s ease;
  }
  .progress-thumb {
    position: absolute;
    top: 50%;
    transform: translate(-50%, -50%);
    width: 12px;
    height: 12px;
    background: rgba(184, 142, 86, 1);
    border-radius: 50%;
    box-shadow: 0 0 0 2px white;
    transition: background 0.2s;
  }
</style>
