<script lang="ts">
  import { afterUpdate, getContext } from "svelte";
  import { toast } from "svelte-sonner";
  import { currentWalletData } from "$lib/stores";
  import { transferDBC, transferDLC } from "$lib/utils/wallet/dbc"; // 导入 transferDLC 方法

  import Modal from "../common/Modal.svelte";
  import { transferDbc } from "$lib/utils/wallet/ether/dbc";
  import { transferDgc } from "$lib/utils/wallet/ether/dgc";
  import { provider } from "$lib/utils/wallet/ether/utils";
  import { ethers } from "ethers";
  import { updateWalletData } from "$lib/utils/wallet/walletUtils";

  const i18n = getContext("i18n");

  export let show = false;

  let loading = false;
  let amount = "";
  let address = "";
  let password = "";
  let transferType = "dbc";
  let gas = {
    gasPrice: 0,
    maxFeePerGas: 0,
    maxPriorityFeePerGas: 0,
  };
  let showError = {
    amount: false,
    address: false,
    // password: false,
    transferType: false,
  };

  $: buttonStyle = loading ? "background: rgba(184, 142, 86, 0.6)" : "";

  // 监听show变量的变化，当show变为false时清空输入框
  $: if (!show) {
    amount = "";
    address = "";
    password = "";
    transferType = "DBC";
    showError = {
      amount: false,
      address: false,
      // password: false,
      transferType: false,
    };
  }

  function handleAmountChange(data) {
    console.log("data1", data);

    if (amount) {
      // 在这里调用 provider.getFeeData()
      provider.getFeeData().then((data) => {
        console.log("data", data);
        gas = data; // 更新 gas 变量
      });
    }
  }

  async function handleTransfer() {
    showError = {
      amount: !amount,
      address: !address,
      // password: !password,
      transferType: !transferType,
    };

    if (!amount || !address || !transferType) {
      toast.error($i18n.t("All fields are required!"));
      return;
    }

    try {
      if ($currentWalletData?.walletInfo) {
        loading = true;

        const transferMethod =
          transferType === "DBC" ? transferDbc : transferDgc; // 根据 transferType 选择方法

        console.log(
          "currentWalletData?.walletInfo?.privateKey",
          $currentWalletData?.walletInfo?.privateKey
        );


        try {
          await transferMethod(
            // $currentWalletData?.pair?.address,
            address,
            amount,
            $currentWalletData?.walletInfo?.privateKey
            // (res) => {
            //   loading = false;
            //   if (res?.msg) {
            //     toast.error(res?.msg);
            //     // throw new Error("111");
            //   } else {
            //     show = false;
            //     toast.success($i18n.t("Transfer successful!"));
            //     console.log(res);
            //   }
            // }
          );
          toast.success($i18n.t("Transfer successful,please be patient!"));

        } catch (error) {
          loading = false;
          toast.error(error?.message);
        }
        loading = false;

        show = false;
        updateWalletData($currentWalletData?.walletInfo)

        // try {
        //   await transferDBC(
        //     $currentWalletData?.pair?.address,
        //     amount,
        //     password,
        //     (res) => {
        //       loading = false;
        //       if (res?.msg) {
        //         toast.error(res?.msg);
        //         throw new Error("111");
        //       } else {
        //       show = false;

        //         toast.success($i18n.t("Transfer successful!"));
        //         console.log(res);
        //       }
        //     }
        //   );
        // } catch (error) {
        //   // toast.success($i18n.t("Transfer successful!"));
        // }
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
        <label class="flex items-center gap-1 mb-2">
          <span class="text-red-500 flex items-center">*</span>
          {$i18n.t("Transfer Type")}
        </label>
        <div class="flex w-full">
          <label class="mr-4">
            <input
              type="radio"
              bind:group={transferType}
              value="DBC"
              required
            />
            DBC
          </label>
          <!-- <label>
            <input
              type="radio"
              bind:group={transferType}
              value="DGC"
              required
            />
            DGC
          </label> -->
        </div>
        {#if showError.transferType}
          <div class="text-red-500 text-sm">
            {$i18n.t("Transfer type is required!")}
          </div>
        {/if}
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
        {#if showError.address}
          <div class="text-red-500 text-sm">
            {$i18n.t("Address is required!")}
          </div>
        {/if}
      </div>

      <div class="mb-6 pt-0.5 max-w-[300px]">
        <label class="flex items-center gap-1 mb-2">
          <span class="text-red-500 flex items-center">*</span>
          {$i18n.t("Enter Amount")}
        </label>
        <div class="flex flex-col w-full">
          <input
            type="number"
            bind:value={amount}
            class="px-5 py-3 rounded-md w-full text-sm outline-none border dark:border-none dark:bg-gray-850"
            placeholder={$i18n.t("Enter Amount")}
            required
            on:input={handleAmountChange}
            min="0.001"
            step="0.001"
          />
        </div>
        {#if showError.amount}
          <div class="text-red-500 text-sm">
            {$i18n.t("Amount is required!")}
          </div>
        {/if}


      </div>

      <!-- <div class="mb-6 pt-0.5 max-w-[300px]">
        <label class="flex items-center gap-1 mb-2">
          <span class="text-red-500 flex items-center">*</span>
          {$i18n.t("Enter Password")}
        </label>
        <div class="flex flex-col w-full">
          <input
            bind:value={password}
            type="password"
            class="px-5 py-3 rounded-md w-full text-sm outline-none border dark:border-none dark:bg-gray-850"
            placeholder={$i18n.t("Enter Password")}
            required
          />
        </div>
        {#if showError.password}
          <div class="text-red-500 text-sm">
            {$i18n.t("Password is required!")}
          </div>
        {/if}
      </div> -->

      {#if amount && gas}
      <div class="-mt-2">
        {$i18n.t("Estimated fuel costs:")}

        {`${ethers.formatUnits(gas?.gasPrice)} < ${ethers.formatUnits(
          gas?.maxFeePerGas
        )} DBC `}

        <div>
          {`Maximum cost: < ${ethers.formatUnits(gas?.maxFeePerGas)} DBC`}
        </div>
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
