<!-- top-text.svelte -->
<script lang="ts">
  import Name from '../Name.svelte';
  import Thinking from '../Thinking.svelte';
  import Searching from '../Searching.svelte';
  import WebAnalysis from '../WebAnalysis.svelte';
  import Replying from '../Replying.svelte';
  import { models } from '$lib/stores';
  import dayjs from 'dayjs';
  import { onMount, tick, getContext } from 'svelte';

  // 3. 定义 Props (接收父组件传来的数据)
  export let message;
  export let modelfiles;
  const i18n = getContext('i18n');

  // 校验图片模型
  const checkModelImage = (model) => {
    // console.log("models", $models);
    const checkModel = $models.filter((item: any) => item?.model === model);
    if (checkModel.length > 0 && checkModel[0]?.support === 'image') {
      return true;
    } else {
      return false;
    }
  };
  // 格式化模型名字
  const formatModelName = (model) => {
    // console.log("models", $models);
    const modelName = $models.filter((item) => item.model === model)?.[0]?.name || model;

    return modelName;
  };
</script>

<Name>
  {#if message.model in modelfiles}
    {modelfiles[message.model]?.title}
  {:else}
    {message.model ? ` ${formatModelName(message.model)}` : ''}
  {/if}
  {#if message.content == '' && !message?.done}
    {#if message?.toolflag}
      {#if message?.parseInfo?.web || message?.parseInfo?.videos || message?.parseInfo?.content}
        <Replying />
      {:else if message?.tooltype == 'webread'}
        <WebAnalysis />
      {:else if message?.tooltype == 'twitter'}
        <Searching typeName="Twitter" />
      {:else if message?.tooltype == 'youtube'}
        <Searching typeName="YouTube" />
      {:else if message?.tooltype == 'bing'}
        <Searching typeName="Bing" />
      {:else}
        <Thinking />
      {/if}
    {:else}
      <Thinking />
    {/if}
  {:else if message?.replytime && checkModelImage(message.model)}
    <span class="text-xs"
      >{$i18n.t('Last for {{ time }} seconds', {
        time: (message?.replytime - message?.timestamp) % 60,
      })}</span
    >
  {/if}
  {#if message.timestamp}
    <span class=" self-center text-gray-400 text-xs font-medium uppercase">
      {dayjs(message.timestamp * 1000).format($i18n.t('h:mm a'))}
    </span>
  {/if}
</Name>
