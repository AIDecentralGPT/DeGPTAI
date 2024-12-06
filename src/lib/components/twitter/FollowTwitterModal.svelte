<script lang="ts">
  import Modal from "../common/Modal.svelte";
  export let show = false;
  import { getContext } from "svelte";
  const i18n = getContext("i18n");

  let account = "";
  let loading = false;

  // 显示初始化Socket
  $: if (show) {
  }
</script>

<Modal bind:show size="sm">
  <div class="max-h-[80dvh] xs:h-auto flex flex-col py-4">
    <div class="flex justify-between dark:text-gray-300 px-5 pb-2">
      <div class="text-lg font-medium self-center">
        {$i18n.t("Follow Twitter")}
      </div>
      <button
        class="self-center"
        on:click={() => {
          show = false;
        }}
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 20 20"
          fill="currentColor"
          class="w-5 h-5"
        >
          <path
            d="M6.28 5.22a.75.75 0 00-1.06 1.06L8.94 10l-3.72 3.72a.75.75 0 101.06 1.06L10 11.06l3.72 3.72a.75.75 0 101.06-1.06L11.06 10l3.72-3.72a.75.75 0 00-1.06-1.06L10 8.94 6.28 5.22z"
          />
        </svg>
      </button>
    </div>

    <div class="w-full px-5">
      <input
        bind:value={account}
        type="text"
        class="my-4 px-5 py-3 rounded-md w-full text-sm outline-none border dark:border-none dark:bg-gray-850"
        placeholder={$i18n.t("Enter Your Twitter Account")}
        required
      />
    </div>
    <div class="flex justify-end w-full px-5">
      <button
        disabled={loading}
        class={" px-4 py-2 primaryButton text-gray-100 transition rounded-lg"}
        style={loading ? "background: rgba(184, 142, 86, 0.6)" : ""}
        type="submit"
        on:click={async () => {}}
      >
        {#if loading}
          <span>{$i18n.t("Checking")}</span>
        {:else}
          <span>{$i18n.t("Check")}</span>
        {/if}
      </button>
    </div>
  </div>
</Modal>

<style>
</style>
