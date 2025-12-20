<!-- MessageContent-edit.svelte -->
<script lang="ts">
  import { onMount, getContext, tick } from 'svelte';

  // 接收父组件的方法和数据
  export let message;
  export let editedContent; // 这里接收数据
  export let cancelEditMessage: () => void;
  export let editMessageConfirmHandler: () => void;

  const i18n: any = getContext('i18n');
  let textareaEl: HTMLTextAreaElement;

  // 辅助函数：调整高度
  const adjustHeight = () => {
    if (textareaEl) {
      textareaEl.style.height = '';
      textareaEl.style.height = `${textareaEl.scrollHeight}px`;
    }
  };

  // 组件挂载（显示）时，自动调整一次高度
  onMount(async () => {
    await tick();
    adjustHeight();
  });
</script>

<div class="w-full bg-gray-50 dark:bg-gray-800 rounded-3xl px-5 py-3 my-2">
  <textarea
    id="message-edit-{message.id}"
    bind:this={textareaEl}
    class="bg-transparent outline-none w-full resize-none"
    bind:value={editedContent}
    on:input={adjustHeight}
  />

  <div class="mt-2 mb-1 flex justify-end space-x-1.5 text-sm font-medium">
    <button
      id="close-edit-message-button"
      class="px-4 py-2 bg-gray-900 hover:bg-gray-850 text-gray-100 transition rounded-3xl"
      on:click={cancelEditMessage}
    >
      {$i18n.t('Cancel')}
    </button>

    <button
      id="save-edit-message-button"
      class="px-4 py-2 bg-white hover:bg-gray-100 text-gray-800 transition rounded-3xl"
      on:click={editMessageConfirmHandler}
    >
      {$i18n.t('Save')}
    </button>
  </div>
</div>
