<script lang="ts">
  import { createEventDispatcher, getContext, onMount } from 'svelte';
  import Tooltip from '$lib/components/common/Tooltip.svelte';
  import { config } from '$lib/stores';

  export let message;
  export let siblings;
  export let isLastMessage = true;
  export let readOnly = false;
  export let isContinuing = false;
  export let loadingSpeech = false;
  export let speaking = false;
  export let generatingImage = false;

  const i18n: any = getContext('i18n');
  const dispatch = createEventDispatcher();

  $: rating = message?.annotation?.rating;

  // ================= 1. 定义 SVG 图标常量 (复用 & 清洁) =================
  const ICONS = {
    prev: `<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-3.5"><path stroke-linecap="round" stroke-linejoin="round" d="M15.75 19.5 8.25 12l7.5-7.5" /></svg>`,
    next: `<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-3.5"><path stroke-linecap="round" stroke-linejoin="round" d="m8.25 4.5 7.5 7.5-7.5 7.5" /></svg>`,
    pencil: `<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-4 h-4"><path stroke-linecap="round" stroke-linejoin="round" d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L6.832 19.82a4.5 4.5 0 0 1-1.897 1.13l-2.685.8.8-2.685a4.5 4.5 0 0 1 1.13-1.897L16.863 4.487Zm0 0L19.5 7.125" /></svg>`,
    copy: `<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-4 h-4"><path stroke-linecap="round" stroke-linejoin="round" d="M15.75 17.25v3.375c0 .621-.504 1.125-1.125 1.125h-9.75a1.125 1.125 0 0 1-1.125-1.125V7.875c0-.621.504-1.125 1.125-1.125H6.75a9.06 9.06 0 0 1 1.5.124m7.5 10.376h3.375c.621 0 1.125-.504 1.125-1.125V11.25c0-4.46-3.243-8.161-7.5-8.876a9.06 9.06 0 0 0-1.5-.124H9.375c-.621 0-1.125.504-1.125 1.125v3.5m7.5 10.375H9.375a1.125 1.125 0 0 1-1.125-1.125v-9.25m12 6.625v-1.875a3.375 3.375 0 0 0-3.375-3.375h-1.5" /></svg>`,
    loading: `<svg width="24" height="24" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" class="w-4 h-4 text-gray-500 fill-current"><style>.spinner_S1WN{animation:spinner_MGfb .8s linear infinite;animation-delay:-.8s}.spinner_Km9P{animation-delay:-.65s}.spinner_JApP{animation-delay:-.5s}@keyframes spinner_MGfb{93.75%,100%{opacity:.2}}</style><circle class="spinner_S1WN" cx="4" cy="12" r="3"/><circle class="spinner_S1WN spinner_Km9P" cx="12" cy="12" r="3"/><circle class="spinner_S1WN spinner_JApP" cx="20" cy="12" r="3"/></svg>`,
    speakStop: `<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-4 h-4"><path stroke-linecap="round" stroke-linejoin="round" d="M19.114 5.636a9 9 0 0 1 0 12.728M16.463 8.288a5.25 5.25 0 0 1 0 7.424M6.75 8.25l4.72-4.72a.75.75 0 0 1 1.28.53v15.88a.75.75 0 0 1-1.28.53l-4.72-4.72H4.51c-.88 0-1.704-.507-1.938-1.354A9.009 9.009 0 0 1 2.25 12c0-.83.112-1.633.322-2.396C2.806 8.756 3.63 8.25 4.51 8.25H6.75Z" /><path stroke-linecap="round" stroke-linejoin="round" d="M15 15l6-6m0 6l-6-6" opacity="0.8" /></svg>`,
    speakWave: `<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-4 h-4"><path stroke-linecap="round" stroke-linejoin="round" d="M19.114 5.636a9 9 0 0 1 0 12.728M16.463 8.288a5.25 5.25 0 0 1 0 7.424M6.75 8.25l4.72-4.72a.75.75 0 0 1 1.28.53v15.88a.75.75 0 0 1-1.28.53l-4.72-4.72H4.51c-.88 0-1.704-.507-1.938-1.354A9.009 9.009 0 0 1 2.25 12c0-.83.112-1.633.322-2.396C2.806 8.756 3.63 8.25 4.51 8.25H6.75Z" /></svg>`,
    photo: `<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-4 h-4"><path stroke-linecap="round" stroke-linejoin="round" d="m2.25 15.75 5.159-5.159a2.25 2.25 0 0 1 3.182 0l5.159 5.159m-1.5-1.5 1.409-1.409a2.25 2.25 0 0 1 3.182 0l2.909 2.909m-18 3.75h16.5a1.5 1.5 0 0 0 1.5-1.5V6a1.5 1.5 0 0 0-1.5-1.5H3.75A1.5 1.5 0 0 0 2.25 6v12a1.5 1.5 0 0 0 1.5 1.5Zm10.5-11.25h.008v.008h-.008V8.25Zm.375 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Z" /></svg>`,
    info: `<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-4 h-4"><path stroke-linecap="round" stroke-linejoin="round" d="M11.25 11.25l.041-.02a.75.75 0 011.063.852l-.708 2.836a.75.75 0 001.063.853l.041-.021M21 12a9 9 0 11-18 0 9 9 0 0118 0zm-9-3.75h.008v.008H12V8.25z" /></svg>`,
    thumbUp: `<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-4 h-4"><path stroke-linecap="round" stroke-linejoin="round" d="M6.633 10.05c.806 0 1.533-.446 2.031-1.08a9.04 9.04 0 0 1 2.861-2.4c.723-.384 1.35-.956 1.653-1.715a4.498 4.498 0 0 0 .322-1.672V3a.75.75 0 0 1 .75-.75A2.25 2.25 0 0 1 16.5 4.5c0 1.152-.26 2.243-.723 3.218-.266.558.107 1.282.725 1.282h3.126c1.026 0 1.945.694 2.054 1.715.045.422.068.85.068 1.285a11.95 11.95 0 0 1-2.649 7.521c-.388.482-.987.729-1.605.729H13.48c-.483 0-.964-.078-1.423-.23l-3.114-1.04a4.501 4.501 0 0 0-1.423-.23H5.904M14.25 9h2.25M5.904 18.75c.083.205.173.405.27.602.197.4-.077.898-.521.898h-.908c-.889 0-1.713-.518-1.972-1.368a12 12 0 0 1-.521-3.507c0-1.553.295-3.036.831-4.396C3.387 9.6 4.167 9.5 5 9.5h1.053c.472 0 .745.556.5.96a8.958 8.958 0 0 0-1.302 4.665c0 1.194.232 2.333.654 3.375Z" /></svg>`,
    thumbDown: `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24"><!-- Icon from HeroIcons by Refactoring UI Inc - https://github.com/tailwindlabs/heroicons/blob/master/LICENSE --><path fill="none" stroke="#888888" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M7.498 15.25H4.372c-1.026 0-1.945-.694-2.054-1.715a12 12 0 0 1-.068-1.285c0-2.848.992-5.464 2.649-7.521C5.287 4.247 5.886 4 6.504 4h4.016a4.5 4.5 0 0 1 1.423.23l3.114 1.04a4.5 4.5 0 0 0 1.423.23h1.294M7.499 15.25c.618 0 .991.724.725 1.282A7.5 7.5 0 0 0 7.5 19.75A2.25 2.25 0 0 0 9.75 22a.75.75 0 0 0 .75-.75v-.633c0-.573.11-1.14.322-1.672c.304-.76.93-1.33 1.653-1.715a9 9 0 0 0 2.86-2.4c.498-.634 1.226-1.08 2.032-1.08h.384m-10.253 1.5H9.7m8.075-9.75q.015.075.05.148a8.95 8.95 0 0 1 .925 3.977a8.95 8.95 0 0 1-.999 4.125m.023-8.25c-.076-.365.183-.75.575-.75h.908c.889 0 1.713.518 1.972 1.368c.339 1.11.521 2.287.521 3.507c0 1.553-.295 3.036-.831 4.398c-.306.774-1.086 1.227-1.918 1.227h-1.053c-.472 0-.745-.556-.5-.96a9 9 0 0 0 .303-.54"/></svg>`,
    play: `<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-4 h-4"><path stroke-linecap="round" stroke-linejoin="round" d="M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" /><path stroke-linecap="round" stroke-linejoin="round" d="M15.91 11.672a.375.375 0 0 1 0 .656l-5.603 3.113a.375.375 0 0 1-.557-.328V8.887c0-.286.307-.466.557-.327l5.603 3.112Z" /></svg>`,
    refresh: `<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-4 h-4"><path stroke-linecap="round" stroke-linejoin="round" d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0l3.181 3.183a8.25 8.25 0 0 0 13.803-3.7M4.031 9.865a8.25 8.25 0 0 1 13.803-3.7l3.181 3.182m0-4.991v4.99" /></svg>`,
  };

  // ================= 2. 数据驱动：构建按钮配置数组 =================
  // 使用 $: 响应式声明，确保状态变化时按钮属性自动更新
  $: actionButtons = [
    {
      id: 'edit',
      tooltip: $i18n.t('Edit'),
      icon: ICONS.pencil,
      visible: !readOnly,
      onClick: () => dispatch('edit'),
    },
    {
      id: 'copy',
      tooltip: $i18n.t('Copy'),
      icon: ICONS.copy,
      visible: true,
      onClick: () => dispatch('copy'),
      class: 'copy-response-button',
    },
    {
      id: 'speak',
      tooltip: $i18n.t('Read Aloud'),
      // 动态图标逻辑：Loading -> Stop -> Speak
      icon: loadingSpeech ? ICONS.loading : speaking ? ICONS.speakStop : ICONS.speakWave,
      visible: true,
      onClick: () => {
        if (!loadingSpeech) dispatch('speak');
      },
    },
    {
      id: 'image',
      tooltip: 'Generate Image',
      // 动态图标逻辑：Loading -> Photo
      icon: generatingImage ? ICONS.loading : ICONS.photo,
      visible: $config.images && !readOnly,
      onClick: () => {
        if (!generatingImage) dispatch('image');
      },
    },
    {
      id: 'info',
      tooltip: $i18n.t('Generation Info'),
      icon: ICONS.info,
      visible: !!message.info,
      onClick: () => console.log(message),
      extraAttr: { id: `info-${message.id}` }, // 这种按钮有特殊ID需求
      class: 'whitespace-pre-wrap', // 特殊样式
    },
    {
      id: 'good',
      tooltip: $i18n.t('Good Response'),
      icon: ICONS.thumbUp,
      visible: !readOnly,
      onClick: () => dispatch('rate', 1),
      // 动态样式：选中时变灰
      class: rating === 1 ? 'bg-gray-100 dark:bg-gray-800' : '',
    },
    {
      id: 'bad',
      tooltip: $i18n.t('Bad Response'),
      icon: ICONS.thumbDown,
      visible: !readOnly,
      onClick: () => dispatch('rate', -1),
      class: rating === -1 ? 'bg-gray-100 dark:bg-gray-800' : '',
    },
    {
      id: 'continue',
      tooltip: $i18n.t('Continue Response'),
      icon: ICONS.play,
      visible: isLastMessage && !readOnly,
      onClick: () => dispatch('continue'),
      class: 'regenerate-response-button',
    },
    {
      id: 'regenerate',
      tooltip: $i18n.t('Regenerate'),
      icon: ICONS.refresh,
      visible: isLastMessage && !readOnly, // 注意：你的原代码里这个逻辑有点怪，通常 regenerate 也是最后一条才显示，但我按原逻辑保留
      onClick: () => dispatch('regenerate'),
      class: 'regenerate-response-button',
    },
  ];
</script>

<div class="w-full fade-in" class:hidden={isContinuing}>
  <div class="w-full fade-in">
    {#if message.done || siblings.length > 1}
      <div class="flex flex-col overflow-x-auto buttons text-gray-600 dark:text-gray-500">
        {#if siblings.length > 1}
          <div class="flex justify-start min-w-fit mr-4" dir="ltr">
            <button
              class="self-center p-1 hover:bg-black/5 dark:hover:bg-white/5 dark:hover:text-white hover:text-black rounded-md transition"
              on:click={() => dispatch('showPrevious', message)}
            >
              {@html ICONS.prev}
            </button>

            <div class="text-sm tracking-widest font-semibold self-center dark:text-gray-100 min-w-fit">
              {siblings.indexOf(message.id) + 1}/{siblings.length}
            </div>

            <button
              class="self-center p-1 hover:bg-black/5 dark:hover:bg-white/5 dark:hover:text-white hover:text-black rounded-md transition"
              on:click={() => dispatch('showNext', message)}
            >
              {@html ICONS.next}
            </button>

            <div class="truncate">
              {message.done ? $i18n.t('Generated by') : $i18n.t('Generating by')}
              {siblings.length}
              {siblings.length > 1 ? 'LLMs' : 'LLM'}
            </div>
          </div>
        {/if}

        {#if message.done}
          <div class="flex justify-start min-w-fit mr-4">
            {#each actionButtons as btn (btn.id)}
              {#if btn.visible}
                <Tooltip content={btn.tooltip} placement="bottom">
                  <button
                    type="button"
                    class="{isLastMessage
                      ? 'visible'
                      : 'invisible group-hover:visible'} p-1.5 hover:bg-black/5 dark:hover:bg-white/5 rounded-lg dark:hover:text-white hover:text-black transition {btn.class ||
                      ''}"
                    on:click={btn.onClick}
                    {...btn.extraAttr || {}}
                  >
                    {@html btn.icon}
                  </button>
                </Tooltip>
              {/if}
            {/each}
          </div>
        {/if}
      </div>
    {/if}
  </div>
</div>

<style>
  .fade-in {
    animation: fadeIn 0.2s ease-in-out;
  }
  @keyframes fadeIn {
    from {
      opacity: 0;
    }
    to {
      opacity: 1;
    }
  }
</style>
