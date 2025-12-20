<script lang="ts">
  import { getContext } from 'svelte';
  import Skeleton from '../Skeleton.svelte';
  import CodeBlock from '../CodeBlock.svelte';
  import { revertSanitizedResponseContent, sanitizeResponseContent } from '$lib/utils';
  import { marked } from 'marked';
  import {
    mobile,
    modelfiles,
    models,
    settings,
    showNewWalletModal,
    showOpenWalletModal,
    showSidebar,
    toolflag,
    tooltype,
  } from '$lib/stores';

  export let message;
  export let isLastMessage = false;
  export let resentMessage: Function;
  // 1. 新增：接收父组件传来的 loading 状态
  export let isContinuing = false;

  let thinkHiden = false;
  const i18n: any = getContext('i18n');

  // 响应式计算 Tokens
  $: tokens = thinkAnalysis((message?.think_content ?? '') + message?.content);

  function thinkAnalysis(content: any) {
    if (!content) return [];

    if (content.startsWith('<think>')) {
      let firstIndex = content.indexOf('</think>');
      if (firstIndex == -1) {
        return [{ type: 'thinking', raw: content.replace('<think>', '') }];
      } else {
        let token = content.split('</think>');
        let thinkObj = {
          type: 'thinking',
          raw: token[0].replace('<think>', ''),
        };

        if (token.length > 1 && token[1]) {
          return [thinkObj, ...marked.lexer(sanitizeResponseContent(token[1]))];
        } else {
          return [thinkObj];
        }
      }
    } else {
      return marked.lexer(sanitizeResponseContent(content));
    }
  }

  const renderer = new marked.Renderer();
  renderer.codespan = (code) => {
    return `<code>${code.replaceAll('&amp;', '&')}</code>`;
  };

  const { extensions, ...defaults } = marked.getDefaults() as any & {
    extensions: any;
  };
</script>

<div class="message-content-wrapper w-full">
  {#if message?.error === true}
    <div class="flex mt-2 mb-4 space-x-2 border px-4 py-3 border-red-800 bg-red-800/30 font-medium rounded-lg">
      <div class="self-center flex-1">
        {$i18n.t('It seems that you are offline. Please reconnect to send messages.')}
      </div>
      {#if isLastMessage}
        <button
          class="hover:text-white transition"
          on:click={() => {
            resentMessage(message?.parentId);
          }}
        >
          <svg
            class="w-4 h-4"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            stroke-width="1.5"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0l3.181 3.183a8.25 8.25 0 0 0 13.803-3.7M4.031 9.865a8.25 8.25 0 0 1 13.803-3.7l3.181 3.182m0-4.991v4.99"
            />
          </svg>
        </button>
      {/if}
    </div>
  {:else if message?.warning === true}
    <div class="flex mt-2 mb-4 space-x-2 border px-4 py-3 border-amber-600 bg-amber-600/30 font-medium rounded-lg">
      <div class="self-center">
        {message.content}

        <button
          class=" px-2 py-1.5 text-xs primaryButton text-gray-100 transition rounded-lg"
          on:click={async () => {
            $showOpenWalletModal = true;
          }}
        >
          {$i18n.t('Open Wallet')}
        </button>
        <button
          class=" px-2 py-1.5 text-xs primaryButton text-gray-100 transition rounded-lg"
          on:click={async () => {
            $showNewWalletModal = true;
          }}
        >
          {$i18n.t('Create Wallet')}
        </button>
      </div>
    </div>
  {:else if message.content === '' && !message?.done}
    {#if message.search}
      {#if message?.parseInfo?.web || message?.parseInfo?.videos || message?.parseInfo?.content}
        <Skeleton />
      {/if}
    {:else}
      <Skeleton />
    {/if}
  {:else}
    <div class="markdown-content">
      {#each tokens as token, tokenIdx (tokenIdx)}
        {#if token.type === 'thinking'}
          <button
            class="flex items-center bg-gray-50 dark:bg-gray-800/50 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg px-2 py-1 transition mt-1"
            on:click={() => {
              thinkHiden = !thinkHiden;
            }}
          >
            {#if message.done}
              <div class="flex flex-wrap text-xs text-gray-500">
                <span class="flex-start font-medium">{$i18n.t('have thought deeply')} </span>
                <span class="flex-start ml-1"
                  >({$i18n.t('Last for {{ time }} seconds', {
                    time: (message?.replytime - message?.timestamp) % 60,
                  })})</span
                >
              </div>
            {:else}
              <span class="text-xs text-gray-500 animate-pulse">{$i18n.t('thinking...')}</span>
            {/if}

            <svg class="w-5 h-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
              <path
                fill-rule="evenodd"
                d="M5.23 7.21a.75.75 0 011.06.02L10 11.168l3.71-3.938a.75.75 0 111.08 1.04l-4.25 4.5a.75.75 0 01-1.08 0l-4.25-4.5a.75.75 0 01.02-1.06z"
                clip-rule="evenodd"
              />
            </svg>
          </button>

          <div
            class="border-l-2 border-slate-200 dark:border-slate-700 pl-3 my-2 transition duration-150 {thinkHiden
              ? 'hidden'
              : ''}"
          >
            {@html marked.parse(token.raw || '', {
              ...defaults,
              gfm: true,
              breaks: true,
              renderer,
            })}
          </div>
        {:else if token.type === 'code'}
          <CodeBlock
            id={`${message.id}-${tokenIdx}`}
            lang={token.lang}
            code={revertSanitizedResponseContent(token.text)}
          />
        {:else}
          {@html marked.parse(token.raw || '', {
            ...defaults,
            gfm: true,
            breaks: true,
            renderer,
          })}
        {/if}
      {/each}

      {#if isContinuing}
        <div class="mt-2 text-sm text-gray-500 dark:text-gray-400 animate-pulse flex items-center select-none">
          <span>Continuing generation...</span>
        </div>
      {/if}
    </div>
  {/if}
</div>
