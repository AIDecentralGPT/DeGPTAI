<script lang="ts">
  import { onMount, tick, getContext } from 'svelte';
  import TwitterEmbed from '$lib/components/twitter/TwitterEmbed.svelte';

  // ❌ 已移除 Iconify，防止 insertBefore 报错
  // import Icon from '@iconify/svelte';

  export let message;
  const i18n: any = getContext('i18n');

  let webFlag = true;
  $: webShow = webFlag;

  // 隐藏/展开 Web 搜索结果
  const handleWebHidden = () => {
    webFlag = !webFlag;
  };

  // 高亮关键词逻辑
  function highlightedText(content: string, keyword: string) {
    let keywords = keyword.split('/');
    if (content.length > 150) {
      content = content.substring(0, 150);
    }
    keywords.forEach((item) => {
      const regexText = /^[\s.,!?;:'"()[\]{}<>]+$/;
      if (!regexText.test(item)) {
        const regex = new RegExp(item, 'gi');
        content = content.replace(regex, (match) => `<span style="color: rgba(184, 142, 86, 1);">${match}</span>`);
      }
    });
    return content;
  }

  // ✅ 核心修改：将所有 SVG 路径提取为常量，数据驱动
  const ICONS = {
    // 1. 网页搜索图标 (mdi:web)
    // 用于：Web Search 标题左侧的圆形图标
    web: 'M16.36,14C16.44,13.34 16.5,12.68 16.5,12C16.5,11.32 16.44,10.66 16.36,10H19.74C19.9,10.64 20,11.31 20,12C20,12.69 19.9,13.36 19.74,14M12.45,10H15.55C15.41,9.5 15.18,9.07 14.95,8.68C14.1,7.24 13.12,6 12,6C10.88,6 9.9,7.24 9.05,8.68C8.82,9.07 8.59,9.5 8.45,10M4.26,14C4.1,13.36 4,12.69 4,12C4,11.31 4.1,10.64 4.26,10H7.64C7.56,10.66 7.5,11.32 7.5,12C7.5,12.68 7.56,13.34 7.64,14M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2Z',

    // 2. 下拉箭头 (heroicons-solid:chevron-down)
    // 用于：折叠/展开按钮，带旋转动画
    chevronDown:
      'M5.23 7.21a.75.75 0 011.06.02L10 11.168l3.71-3.938a.75.75 0 111.08 1.04l-4.25 4.5a.75.75 0 01-1.08 0l-4.25-4.5a.75.75 0 01.02-1.06z',

    // 3. 简单地球 (ph:globe-simple)
    // 用于：每个网页搜索结果左侧的小图标
    globeSimple:
      'M12,24c-6.6,0-12-5.4-12-12s5.4-12,12-12s12,5.4,12,12S18.6,24,12,24z M12,2c-5.5,0-10,4.5-10,10s4.5,10,10,10s10-4.5,10-10S17.5,2,12,2z M12,4c2.2,0,4,3.6,4,8s-1.8,8-4,8s-4-3.6-4-8S9.8,4,12,4z M12,20c0.9,0,2.1-1.6,2.9-4H9.1C9.9,18.4,11.1,20,12,20z M12,4C11.1,4,9.9,5.6,9.1,8h5.8C14.1,5.6,12.9,4,12,4z M2,12h6.2c0.2-1.6,0.6-3,1.3-4H3.8C2.6,9.1,2,10.5,2,12z M14.5,8c0.7,1,1.1,2.4,1.3,4h6.4c0-1.5-0.6-2.9-1.8-4H14.5z M20.2,16h-6.4c-0.2,1.6-0.6,3-1.3,4h5.7C19.4,18.9,20,17.5,20.2,16z M3.8,16h5.7c-0.7-1-1.1-2.4-1.3-4H2C2,13.5,2.6,14.9,3.8,16z',

    // 4. 外部链接箭头 (lucide:external-link)
    // 用于：网页链接旁边的跳转小箭头
    externalLink: 'M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6 M15 3h6v6 M10 14L21 3',

    // 5. YouTube 图标 (mdi:youtube)
    // 用于：视频搜索标题左侧
    youtube:
      'M10,15L15.19,12L10,9V15M21.56,7.17C21.69,7.64 21.78,8.27 21.84,9.07C21.91,9.87 21.94,10.56 21.94,11.16L22,12C22,14.19 21.84,15.8 21.56,16.83C21.31,17.73 20.73,18.31 19.83,18.56C19.36,18.69 18.5,18.78 17.18,18.84C15.88,18.91 14.69,18.94 13.59,18.94L12,19C7.81,19 5.2,18.84 4.17,18.56C3.27,18.31 2.69,17.73 2.44,16.83C2.31,16.36 2.22,15.73 2.16,14.93C2.09,14.13 2.06,13.44 2.06,12.84L2,12C2,9.81 2.16,8.2 2.44,7.17C2.69,6.27 3.27,5.69 4.17,5.44C4.64,5.31 5.5,5.22 6.82,5.16C8.12,5.09 9.31,5.06 10.41,5.06L12,5C16.19,5 18.8,5.16 19.83,5.44C20.73,5.69 21.31,6.27 21.56,7.17Z',

    // 6. 用户头像 (lucide:user-round)
    // 用于：YouTube 频道名称旁边的小人图标
    userRound: 'M12 2a5 5 0 1 0 5 5 5 5 0 0 0-5-5ZM12 14c-5.5 0-9 4.5-9 9h18c0-4.5-3.5-9-9-9Z',

    // 7. Twitter X 图标 (ri:twitter-x-fill)
    // 用于：推特搜索标题左侧
    twitterX:
      'M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z',
  };
</script>

{#if message?.tooltype == 'web' || message?.tooltype == 'bing'}
  {#if message?.parseInfo?.web}
    <div class="flex flex-col max-w-full rounded-2xl bg-gray-100 dark:bg-gray-800 my-2">
      <div class="flex justify-between items-center h-[55px] p-4">
        <div class="flex flex-row items-center text-sm font-bold">
          <div class="flex items-center justify-center bg-gray-50 dark:bg-gray-600 rounded-full size-[2rem] p-1.5">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
              fill="currentColor"
              class="text-[#D0A870] w-4 h-4"
            >
              <path d={ICONS.web} />
            </svg>
          </div>
          <div class="flex flex-col ml-1">
            <span class="text-sm">{$i18n.t('Web Search')}</span>
            <span class="text-xs"> {message?.parseInfo?.web.length} Results</span>
          </div>
        </div>
        <button on:click={handleWebHidden}>
          <svg
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 20 20"
            fill="currentColor"
            class="h-4 w-4 shrink-0 text-muted-foreground transition-transform duration-200 {webShow
              ? 'rotate-180'
              : 'rotate-0'}"
          >
            <path fill-rule="evenodd" d={ICONS.chevronDown} clip-rule="evenodd" />
          </svg>
        </button>
      </div>

      <div class="w-full transition ease-in-out delay-150 overflow-x-auto {webShow ? 'h-0' : 'h-auto'}">
        <div class="flex flex-row px-4 mr-2">
          {#each message?.parseInfo?.web ?? [] as item}
            <div class="flex flex-col rounded-2xl bg-white dark:bg-black mx-2 mb-4 p-4 min-w-[300px] max-w-[300px]">
              <div class="flex flex-row">
                <div
                  class="w-9 h-9 min-w-[2.25rem] rounded-lg bg-neutral-100 dark:bg-neutral-800 flex items-center justify-center overflow-hidden"
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 24 24"
                    fill="currentColor"
                    class="w-[1.2rem] h-[1.2rem]"
                  >
                    <path d={ICONS.globeSimple} />
                  </svg>
                </div>
                <div class="ml-2 overflow-hidden">
                  <div class="w-full text-sm font-bold line-clamp-1 text-ellipsis">
                    {@html highlightedText(item.title, message?.parseInfo?.keyword ?? '')}
                  </div>
                  <div class="flex flex-row items-center w-full text-xs mt-1">
                    <a
                      class="flex-start text-gray-500 font-bold line-clamp-1 text-ellipsis max-w-[200px]"
                      href={item.url}
                      target="_blank"
                    >
                      {item.url}
                    </a>
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      stroke-width="2"
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      class="h-3 w-3 ml-2"
                    >
                      <path d={ICONS.externalLink} />
                    </svg>
                  </div>
                </div>
              </div>
              <div class="text-xs text-gray-500 w-full line-clamp-3 text-ellipsis mt-2 h-[3rem]">
                {@html highlightedText(item.content, message?.parseInfo?.keyword ?? '')}
              </div>
            </div>
          {/each}
        </div>
      </div>
    </div>
  {/if}
{/if}

{#if message?.tooltype == 'youtube'}
  {#if message?.parseInfo?.videos}
    <div class="flex flex-col w-full rounded-xl bg-gray-100 dark:bg-gray-800 my-2">
      <div class="flex justify-between items-center h-[55px] p-4">
        <div class="flex flex-row items-center text-sm font-bold">
          <div class="flex items-center justify-center bg-gray-50 dark:bg-gray-600 rounded-full size-[2rem] p-1.5">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
              fill="currentColor"
              class="text-[#D0A870] w-5 h-5"
            >
              <path d={ICONS.youtube} />
            </svg>
          </div>
          <div class="flex flex-col ml-1">
            <span class="text-sm">{$i18n.t('YouTube Search')}</span>
            <span class="text-xs"> {message?.parseInfo?.videos.length} videos</span>
          </div>
        </div>
        <button on:click={handleWebHidden}>
          <svg
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 20 20"
            fill="currentColor"
            class="h-4 w-4 shrink-0 text-muted-foreground transition-transform duration-200 {webShow
              ? 'rotate-180'
              : 'rotate-0'}"
          >
            <path fill-rule="evenodd" d={ICONS.chevronDown} clip-rule="evenodd" />
          </svg>
        </button>
      </div>

      <div class="w-full transition ease-in-out delay-150 overflow-x-auto {webShow ? 'h-0' : 'h-auto'}">
        <div class="flex flex-row px-4 mr-2">
          {#each message?.parseInfo?.videos ?? [] as item}
            <div class="flex flex-col rounded-xl bg-white dark:bg-black mx-2 mb-4 pb-2 min-w-[230px]">
              <a class="flex flex-col w-[230px]" href={item.video_url} target="_blank">
                <img class="rounded-t-xl drag-none aspect-video object-cover" src={item.thumbnail_url} alt="" />
                <div class="px-3 py-2">
                  <span class="line-clamp-2 text-ellipsis text-sm font-medium">{item.title}</span>
                  <div class="flex flex-row items-center mt-2">
                    <div class="w-[20px]">
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        viewBox="0 0 24 24"
                        fill="currentColor"
                        class="h-4 w-4 text-red-500"
                      >
                        <path d={ICONS.userRound} />
                      </svg>
                    </div>
                    <span class="ml-1 line-clamp-1 text-ellipsis text-xs text-gray-500">{item.channel_title}</span>
                  </div>
                </div>
              </a>
            </div>
          {/each}
        </div>
      </div>
    </div>
  {/if}
{/if}

{#if message?.tooltype == 'twitter'}
  {#if message?.parseInfo?.content}
    <div class="flex flex-col w-full rounded-xl bg-gray-100 dark:bg-gray-800 my-2">
      <div class="flex justify-between items-center h-[55px] p-4">
        <div class="flex flex-row items-center text-sm font-bold">
          <div class="flex items-center justify-center bg-gray-50 dark:bg-gray-600 rounded-full size-[2rem] p-1.5">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
              fill="currentColor"
              class="text-[#D0A870] w-5 h-5"
            >
              <path d={ICONS.twitterX} />
            </svg>
          </div>
          <div class="flex flex-col ml-1">
            <span class="text-sm">{$i18n.t('Twitter Search')}</span>
            <span class="text-xs"> {message?.parseInfo?.content.length} tweets</span>
          </div>
        </div>
        <button on:click={handleWebHidden}>
          <svg
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 20 20"
            fill="currentColor"
            class="h-4 w-4 shrink-0 text-muted-foreground transition-transform duration-200 {webShow
              ? 'rotate-180'
              : 'rotate-0'}"
          >
            <path fill-rule="evenodd" d={ICONS.chevronDown} clip-rule="evenodd" />
          </svg>
        </button>
      </div>

      <div
        class="w-full transition ease-in-out delay-150 overflow-x-auto overflow-y-hidden {webShow ? 'h-0' : 'h-auto'}"
      >
        <div class="flex flex-row px-4 mr-2">
          {#each message?.parseInfo?.content ?? [] as item}
            <div class="mr-3 h-[300px] min-w-[300px]">
              <TwitterEmbed data={item} />
            </div>
          {/each}
        </div>
      </div>
    </div>
  {/if}
{/if}
