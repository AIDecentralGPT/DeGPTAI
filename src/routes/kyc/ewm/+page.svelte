<script lang="ts">
  import { onMount } from 'svelte';
  import { faceliveness } from "$lib/apis/auths";
  import { goto } from "$app/navigation";
  import { page } from '$app/stores';

  let metadata:any = {};
  let token:any = "";
  onMount(() => {
    const queryParams = new URLSearchParams($page.url.search);
    metadata = queryParams.get('metainfo');
    token = queryParams.get("token");
    toAliFace()
  });

  function toAliFace() {
    faceliveness(token, metadata).then(async (res) => {
      goto(res.transaction_url);
    })
  }

</script>

