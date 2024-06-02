<script lang="ts">
  import { getContext } from "svelte";
  import { toast } from "svelte-sonner";
  import { currentWalletData } from "$lib/stores";
  import { transferDBC } from "$lib/utils/wallet/dbc";
  import Modal from "../common/Modal.svelte";

  const i18n = getContext("i18n");

  export let show = false;

  let loading = false;
  let amount = "";
  let address = "";
  let password = "";
  let transferType = "dbc";
  let showError = false;

  $: buttonStyle = loading ? "background: rgba(184, 142, 86, 0.6)" : "";

  async function handleTransfer() {
    showError = false;
    if (!amount || !address || !password || !transferType) {
      showError = true;
      toast.error($i18n.t("All fields are required!"));
      return;
    }

    try {
      if ($currentWalletData?.pair) {
        loading = true;
        await transferDBC(
          $currentWalletData?.pair?.address,
          amount,
          password,
          (a, b, c) => {
            console.log(a, b, c);
          }
        );
        loading = false;
        show = false;
        toast.success($i18n.t("Transfer successful!"));
      }
    } catch (error) {
      loading = false;
      toast.error(error?.message);
    }
  }
</script>

<Modal bind:show>
  <div class="text-gray-700 dark:text-gray-100">
    <div class="flex justify-between dark:text-gray-300 px-5 pt-4 pb-1">
      <div class="text-lg font-medium self-center">
        {$i18n.t("Transfer")}
      </div>
      <button
        class="self-center"
        on:click={() => {
          show = false;
          loading = false;
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

    <div class="w-full p-6 px-8">
      <div class="mb-6 pt-0.5 max-w-[300px]">
           <label class="flex items-center gap-1 mb-2"
          >
          <span class="text-red-500 flex items-center">*</span>
          {$i18n.t("Transfer Type")}
        </label>
        <div class="flex w-full">
             <label  class="mr-4">
            <input
              type="radio"
              bind:group={transferType}
              value="dbc"
              required
            />
            DBC
          </label>
             <label >
            <input
              type="radio"
              bind:group={transferType}
              value="dlc"
              required
            />
            DLC
          </label>
        </div>
      </div>

      <div class="mb-6 pt-0.5 max-w-[300px]">
           <label class="flex items-center gap-1 mb-2">
        <span class="text-red-500 flex items-center">*</span>
        {$i18n.t("Enter Address")}

        </label>
        <div class="flex flex-col w-full">
          <input
            bind:value={address}
            type="text"
            class="px-5 py-3 rounded-md w-full text-sm outline-none border dark:border-none dark:bg-gray-850"
            placeholder={$i18n.t("Enter Address")}
            required
          />
        </div>
      </div>

      <div class="mb-6 pt-0.5 max-w-[300px]">
           <label class="flex items-center gap-1 mb-2"
        >
        
        <span class="text-red-500 flex items-center">*</span>
        {$i18n.t("Enter Amount")}
          
          </label >
        <div class="flex flex-col w-full">
          <input
            bind:value={amount}
            type="text"
            class="px-5 py-3 rounded-md w-full text-sm outline-none border dark:border-none dark:bg-gray-850"
            placeholder={$i18n.t("Enter Amount")}
            required
          />
        </div>
      </div>

      <div class="mb-6 pt-0.5 max-w-[300px]">
           <label class="flex items-center gap-1 mb-2" 
          >
          
          <span class="text-red-500 flex items-center">*</span>
          {$i18n.t("Enter Password")}
          </label
        >
        <div class="flex flex-col w-full">
          <input
            bind:value={password}
            type="password"
            class="px-5 py-3 rounded-md w-full text-sm outline-none border dark:border-none dark:bg-gray-850"
            placeholder={$i18n.t("Enter Password")}
            required
          />
        </div>
      </div>

      {#if showError}
        <div class="text-red-500 text-sm mb-4">
          {$i18n.t("All fields are required!")}
        </div>
      {/if}

      <div class="flex justify-end">
        <button
          disabled={loading}
          class="px-4 py-2 primaryButton text-gray-100 transition rounded-lg"
          style={buttonStyle}
          on:click={handleTransfer}
        >
          <span class="relative">{$i18n.t("Transfer")}</span>
        </button>
      </div>
    </div>
  </div>
</Modal>

<style>
  .px-8 {
    padding-left: 2rem;
    padding-right: 2rem;
  }
  .p-6 {
    padding: 1.5rem;
  }
  .mb-6 {
    margin-bottom: 1.5rem;
  }
</style>
