<script lang="ts">
  import { onMount, getContext } from "svelte";

  const i18n = getContext("i18n");

  let iframeUrl:string = 'https://www.baidu.com';

  onMount(() => {
    // 获取URL中的参数
    const params = new URLSearchParams(window.location.search);
    // iframeUrl = params.get("url") || '';
  });

</script>
<div>
  test
</div>

<!-- <iframe title="degpt" src={iframeUrl} width="100%" height="100vh"></iframe> -->