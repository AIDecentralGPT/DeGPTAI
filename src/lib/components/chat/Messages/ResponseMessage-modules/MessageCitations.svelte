<!-- MessageCitations.svelte -->
<script lang="ts">
  import { createEventDispatcher } from 'svelte';

  export let message;

  const dispatch = createEventDispatcher();

  // 将复杂的 reduce 逻辑移到这里，利用 Svelte 的响应式特性
  // 只有当 message 变化时，才会重新计算 citationsList
  $: citationsList = message?.citations
    ? message.citations.reduce((acc, citation) => {
        citation.document.forEach((document, index) => {
          const metadata = citation.metadata?.[index];
          const id = metadata?.source ?? 'N/A';

          const existingSource = acc.find((item) => item.id === id);

          if (existingSource) {
            existingSource.document.push(document);
            existingSource.metadata.push(metadata);
          } else {
            acc.push({
              id: id,
              source: citation?.source,
              document: [document],
              metadata: metadata ? [metadata] : [],
            });
          }
        });
        return acc;
      }, [])
    : [];
</script>

{#if citationsList.length > 0}
  <div class="mt-1 mb-2 w-full flex gap-1 items-center flex-wrap">
    {#each citationsList as citation, idx}
      <div class="flex gap-1 text-xs font-semibold">
        <button
          class="flex items-center dark:text-gray-300 py-1 px-1 bg-gray-50 hover:bg-gray-100 dark:bg-gray-850 dark:hover:bg-gray-800 transition rounded-xl border border-transparent hover:border-gray-200 dark:hover:border-gray-700"
          on:click={() => {
            // 将点击事件派发给父组件，把当前点击的 citation 传出去
            dispatch('click', citation);
          }}
        >
          <div class="bg-white dark:bg-gray-700 rounded-full w-4 h-4 flex items-center justify-center text-[10px]">
            {idx + 1}
          </div>
          <div class="flex-1 mx-2 line-clamp-1 max-w-[150px]">
            {citation.source.name}
          </div>
        </button>
      </div>
    {/each}
  </div>
{/if}
