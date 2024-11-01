<script lang="ts">
  import Modal from "../common/Modal.svelte";
  export let show = false;
  import { getContext } from "svelte";
  import { showCoinIntruType } from "$lib/stores";
  const i18n = getContext("i18n");

  let coinIntrus = [
    {
      title: "About DGC",
      description: "Prior to launching on the mainnet of any trading platform, DGC tokens are marked as points. These points will be converted at 1:1 ratio when DGC officially launches. DGC team will make sure that this transition goes smoothly and prevent any abuse of this policy."
    },
    {
      title: "About DBC",
      description: "DeepBrainChain is the world's first AI public chain. Its native token, DBC, is used as gas fee in this project. Any DGC transactions requires a certain amount of nominal DBCs."
    }
  ];

</script>

<Modal bind:show size="sm">
  <div class="xs:h-auto flex flex-col w-full">
    <div class="p-6 pt-0 shadow-md mt-0 flex-1">
      <div class="flex flex-col item-center pt-5">
        {#if $showCoinIntruType === 'dgc'}
          <h1 class="text-orange-200 text-center font-bold">{$i18n.t(coinIntrus[0].title)}</h1>
          <p class="text-orange-200 text-xl">{$i18n.t(coinIntrus[0].description)}</p>
        {:else}
          <h1 class="text-orange-200 text-center font-bold">{$i18n.t(coinIntrus[1].title)}</h1>
          <p class="text-orange-200 text-xl">{$i18n.t(coinIntrus[1].description)}</p>
        {/if}
      </div>
      <div class="text-center pt-5">
        <button class="primaryButton px-2 py-1 rounded-lg text-lg"
          on:click={async () => {
            show = false;
          }}>
          {$i18n.t("I konw")}
        </button>
      </div> 
    </div>
  </div>
</Modal>

<style>
  h1 {
    font-size: 24px;
    margin-bottom: 16px;
  }
  p {
    font-size: 16px;
    margin: 8px 0;
  }
</style>
