<script lang="ts">
  import { getContext } from "svelte";
  import { toast } from "svelte-sonner";
  import {
    currentWalletData,
    walletKey,
    checkPasswordShow2,
    binanceFlag,
  } from "$lib/stores";

  import Modal from "../common/Modal.svelte";
  import { transferDbc } from "$lib/utils/wallet/ether/dbc";
  import { transferDgc, tranGasLimit } from "$lib/utils/wallet/ether/dgc";
  import { provider } from "$lib/utils/wallet/ether/utils";
  import { ethers } from "ethers";
  import { updateWalletData } from "$lib/utils/wallet/walletUtils";
  import CheckPasswordModal2 from "$lib/components/wallet/CheckPasswordModal2.svelte";
  import { binanceTransferDgc } from "$lib/utils/wallet/ether/binance";

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
    transferType = $binanceFlag ? "DGC" : "DBC";
    showError = {
      amount: false,
      address: false,
      // password: false,
      transferType: false,
    };
    loading = false;
    checkPassword = false;
  }

  $: if (transferType) {
    handleAmountChange();
  }

  async function handleAmountChange() {
    if (amount) {
      if (transferType === "DBC") {
        // 获取gasLimit
        const transaction = {
          to: "0xEc9011d12CCBE93C7213C176dEFEa998bfbBA21b",
          value: ethers.parseUnits("1"),
        };
        const gasLimit = await provider.estimateGas(transaction);
        // 在这里调用 provider.getFeeData()
        await provider.getFeeData().then((data) => {
          const gasPrice = BigInt(data?.gasPrice) * gasLimit;
          const maxFeePerGas = BigInt(data?.maxFeePerGas) * gasLimit;
          const maxPriorityFeePerGas = data?.maxPriorityFeePerGas;
          // 更新 gas 变量
          gas = {
            gasPrice,
            maxFeePerGas,
            maxPriorityFeePerGas,
          };
        });
      } else {
        // 获取预估gasLimit
        const gasLimit = await tranGasLimit($currentWalletData?.walletInfo);
        // 在这里调用 provider.getFeeData()
        await provider.getFeeData().then((data) => {
          const gasPrice = BigInt(data?.gasPrice) * gasLimit;
          const maxFeePerGas = BigInt(data?.maxFeePerGas) * gasLimit;
          const maxPriorityFeePerGas = data?.maxPriorityFeePerGas;
          // 更新 gas 变量
          gas = {
            gasPrice,
            maxFeePerGas,
            maxPriorityFeePerGas,
          };
        });
      }
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

        try {
          let response = null;
          if ($binanceFlag) {
            response = await binanceTransferDgc($currentWalletData?.walletInfo?.address, address, amount);
          } else {
            response = await transferMethod(
              address,
              amount,
              $currentWalletData?.walletInfo?.privateKey
            );
          }

          if (response?.ok) {
            toast.success($i18n.t("Transfer successful,please be patient!"));
          } else {
            toast.error($i18n.t(response?.msg));
          }
        } catch (error) {
          loading = false;
          toast.error(error?.message);
        }
        loading = false;

        show = false;
        updateWalletData($currentWalletData?.walletInfo);
      }
    } catch (error) {
      loading = false;
      toast.error(error?.message);
    }
  }

  let checkPassword = false;
  async function checkTransfer() {
    if (!$walletKey?.checked && !$binanceFlag) {
      $checkPasswordShow2 = true;
    } else {
      await handleTransfer();
    }
  }

  function checkPasswordResult(event: any) {
    if (event?.detail) {
      handleTransfer();
    }
  }
</script>

{#if $checkPasswordShow2}
  <CheckPasswordModal2
    bind:show={$checkPasswordShow2}
    bind:checked={checkPassword}
    on:change={checkPasswordResult}
  />
{:else}
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
            {#if !$binanceFlag}
              <label class="mr-4">
                <input
                  type="radio"
                  bind:group={transferType}
                  value="DBC"
                  required
                />
                DBC
              </label>
            {/if}
            <label>
              <input
                type="radio"
                bind:group={transferType}
                value="DGC"
                required
              />
              DGC
            </label>
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

        {#if amount && gas && !$binanceFlag}
          <div class="flex flex-row mt-2">
            <div>{$i18n.t("Estimated fuel costs:")}</div>
            <div>
              {`${ethers.formatUnits(gas?.gasPrice)} - ${ethers.formatUnits(
                gas?.maxFeePerGas
              )} DBC `}
            </div>
            <div class="ml-2">
              {$i18n.t("Maximum cost:")}{` ${ethers.formatUnits(
                gas?.maxFeePerGas
              )} DBC`}
            </div>
          </div>
        {/if}

        <div class="flex justify-end mt-1">
          <button
            disabled={loading}
            class="px-4 py-2 primaryButton text-gray-100 transition rounded-lg"
            style={buttonStyle}
            on:click={checkTransfer}
          >
            <span class="relative">{$i18n.t("Transfer")}</span>
          </button>
        </div>
      </div>
    </div>
  </Modal>
{/if}

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
