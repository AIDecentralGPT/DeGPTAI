<script lang="ts">
  import { onMount, getContext } from 'svelte';
  import { page } from '$app/stores';

  const i18n = getContext("i18n");

  let message: any = "";
  let loading = true;
  onMount(() => {
    const queryParams = new URLSearchParams($page.url.search);
    message = queryParams.get("message");
    let lang: any = queryParams.get("lang");
    $i18n.changeLanguage(lang);
    loading = false;
  });

</script>

<div class="flex flex-col justify-center items-center w-full h-screen">
  <img src="/static/logo.png" alt=""/>
  {#if !loading}
    <div class="mt-2">{$i18n.t(message)}</div>
  {/if}
</div>

