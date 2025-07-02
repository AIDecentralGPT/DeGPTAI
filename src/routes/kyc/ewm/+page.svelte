<script lang="ts">
  import { onMount, getContext } from 'svelte';
  import { getliveness } from "$lib/apis/auths";
  import { page } from '$app/stores';

  const i18n = getContext("i18n");

  onMount(() => {
    const queryParams = new URLSearchParams($page.url.search);
    let token: any = queryParams.get("token");
    toAliFace(token)
  });

  let error: string = "";
  let loading = true;
  function toAliFace(token: string) {
    loading = true;
    getliveness(token).then((res) => {
      if (res.passed) {
        window.location.href = res.data;
      } else {
        error = res.message;
      }
      loading = false;
    })
  }

</script>

<div class="flex flex-col justify-center items-center w-full h-screen">
  <img src="/static/logo.png" alt=""/>
  {#if !loading}
    <div class="mt-2">{$i18n.t(error)}</div>
  {/if}
</div>

