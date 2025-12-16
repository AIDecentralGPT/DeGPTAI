<script lang="ts">
  import Bolt from '$lib/components/icons/Bolt.svelte';
  import { onMount, getContext } from 'svelte';
  import { toolflag, tooltype } from '$lib/stores';
  import Icon from '@iconify/svelte';

  const i18n = getContext('i18n');

  export let submitPrompt: Function;
  export let suggestionPrompts = [];

  let prompts = [];

  $: prompts = suggestionPrompts;
  // .reduce((acc, current) => [...acc, ...[current]], [])
  // .sort(() => Math.random() - 0.5);
  // suggestionPrompts.length <= 4
  // 	? suggestionPrompts
  // 	: suggestionPrompts.sort(() => Math.random() - 0.5).slice(0, 4);

  onMount(() => {
    const containerElement = document.getElementById('suggestions-container');

    if (containerElement) {
      containerElement.addEventListener('wheel', function (event) {
        if (event.deltaY !== 0) {
          // If scrolling vertically, prevent default behavior
          event.preventDefault();
          // Adjust horizontal scroll position based on vertical scroll
          containerElement.scrollLeft += event.deltaY;
        }
      });
    }
  });
</script>

{#if prompts.length > 0}
  <div
    class="mb-1.5 flex gap-1 text-xs font-medium uppercase tracking-widest items-center text-gray-500 dark:text-gray-400 px-1"
  >
    <Icon icon="lucide:sparkles" class="w-4 h-4" />

    {$i18n.t('Suggested')}
  </div>
{/if}

<div class="w-full">
  <div
    class="relative w-full flex gap-4 snap-x snap-mandatory md:snap-none overflow-x-auto pb-4 no-scrollbar"
    id="suggestions-container "
  >
    {#each prompts as prompt, promptIdx}
      <div class="snap-center shrink-0">
        <button
          class="flex flex-col flex-1 shrink-0 w-72 justify-between h-32 p-4 rounded-3xl transition-all duration-300 group
                 border border-gray-200 dark:border-white/5
                 bg-white dark:bg-[#1a1a1a]
                 hover:bg-gray-50 dark:hover:bg-[#252525]
                 active:scale-[0.98]"
          on:click={() => {
            if (promptIdx == 0) {
              $toolflag = true;
              $tooltype = 'webread';
            } else {
              $toolflag = false;
              $tooltype = '';
            }
            submitPrompt($i18n.t(prompt.content), promptIdx);
          }}
        >
          <div class="flex flex-col text-left space-y-1">
            {#if prompt.title && prompt.title[0] !== ''}
              <div
                class="text-base font-bold text-gray-800 dark:text-gray-100 group-hover:text-primary transition-colors"
              >
                {$i18n.t(prompt.title[0])}
              </div>
              <div class="text-sm text-gray-500 dark:text-gray-400 font-normal leading-relaxed line-clamp-2">
                {$i18n.t(prompt.title[1])}
              </div>
            {:else}
              <div
                class="self-center text-sm font-medium text-gray-800 dark:text-gray-200 group-hover:text-amber-600 dark:group-hover:text-amber-500 transition-colors line-clamp-3"
              >
                {$i18n.t(prompt.content)}
              </div>
            {/if}
          </div>

          <div class="w-full flex justify-between items-end">
            <div
              class="text-[10px] uppercase font-bold tracking-wider text-gray-400 dark:text-gray-600 group-hover:text-gray-500 dark:group-hover:text-gray-500 transition self-center"
            >
              {$i18n.t('Prompt')}
            </div>

            <div
              class="p-2 rounded-full bg-gray-100 dark:bg-white/5 text-gray-400 group-hover:bg-amber-100 group-hover:text-amber-600 dark:group-hover:bg-amber-500/20 dark:group-hover:text-amber-500 transition-all"
            >
              <Icon icon="mdi-light:arrow-up" class="w-3 h-3" />
            </div>
          </div>
        </button>
      </div>
    {/each}
  </div>
</div>

<style>
  /* 隐藏滚动条的核心代码 */
  .no-scrollbar::-webkit-scrollbar {
    display: none; /* Chrome, Safari, Opera */
  }

  .no-scrollbar {
    -ms-overflow-style: none; /* IE and Edge */
    scrollbar-width: none; /* Firefox */
  }
</style>
