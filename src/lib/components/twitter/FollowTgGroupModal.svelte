<script lang="ts">
  import Modal from "../common/Modal.svelte";
  export let show = false;
  import { getContext } from "svelte";
  import {
    user
  } from "$lib/stores";
  const i18n = getContext("i18n");
  
  // 显示初始化Socket
  $: if (show) {
    
  }
</script>

<Modal bind:show size="sm">
  <div class="max-h-[80dvh] xs:h-auto flex flex-col">
    <div class="flex justify-between dark:text-gray-300 px-5 pt-4 pb-2">
      <div class="text-lg font-medium self-center">{$i18n.t("Follow TG Group")}</div>
      <button
        class="self-center"
        on:click={() => {
          show = false;
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

    <div class="mx-auto max-w-7xl px-6 lg:px-8 flex-1 overflow-auto">
      
    </div>
  </div>
</Modal>

<style>
</style>
