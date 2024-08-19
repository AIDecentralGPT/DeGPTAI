<script lang="ts">
  import { beforeUpdate, onMount } from "svelte";
  import { fade } from "svelte/transition";
  import dayjs from "dayjs";
  import { getContext } from "svelte";
  import Modal from "../common/Modal.svelte";
  import { currentWalletData, user } from "$lib/stores";
  import { getTransactions } from "$lib/apis/wallet";
  import { ethers } from "ethers";
  const i18n = getContext("i18n");

  export let show = false;

  let modalElement = null;
  let mounted = false;
  let transactionsList = [];

  onMount(() => {
    if (show) {
      fetchData();
    }
  });

  let previousShow = show;

  beforeUpdate(() => {
    if (show !== previousShow) {
      previousShow = show;
      if (show) {
        fetchData();
      }
    }
  });

  async function fetchData() {
    const address = currentWalletData?.walletInfo?.address;
    const res = await getTransactions($user?.id);
    console.log("transactions", res);
    // 合并两个 items 数组
    const mergedItems = [...res[0].items, ...res[1].items];

    // 按时间排序
    mergedItems.sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp));

    console.log(mergedItems);

    transactionsList = mergedItems.filter((item) => !!item.value)?.map((item) => {
      const coinType = item?.tx_types?.[0] === "coin_transfer" ? "DBC" : "DGC";

      console.log("item.value", item.value);
      
      return {
        ...item,
        coinType,
        coinAmount: ethers.formatUnits(item.value, "ether"),
      };
    });
    console.log("transactionsList", transactionsList);
  }
</script>

{#if show}
  <Modal bind:show size="lg">
    <div
      class=" flex justify-between items-center dark:text-gray-300 px-5 pt-4 pb-1"
    >
      <h1 class="text-xl font-semibold">{$i18n.t("Transactions")}</h1>

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

    <div
      class="m-auto rounded-2xl max-w-full mx-2 bg-gray-50 dark:bg-gray-900 shadow-3xl p-4"
    >
      <!-- <h1 class="text-xl font-semibold mb-4">{$i18n.t("Transactions")}</h1> -->
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead>
            <tr>
              <th
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider whitespace-nowrap"
                >Token</th
              >
              <!-- <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider whitespace-nowrap">Token ID</th> -->
              <th
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider whitespace-nowrap"
                >Txn hash</th
              >
              <th
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider whitespace-nowrap"
                >From</th
              >
              <th
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider whitespace-nowrap"
                >To</th
              >
              <th
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider whitespace-nowrap"
                >Value</th
              >
            </tr>
          </thead>
          <tbody
            class="bg-white border-b dark:bg-gray-900 dark:border-gray-700 text-xs"
          >
            {#each transactionsList as historyItem}
              <tr>
                <td class="px-6 py-4 whitespace-nowrap"
                  >{historyItem.coinType}</td
                >
                <!-- <td class="px-6 py-4 whitespace-nowrap">{historyItem.token_transfers ? historyItem.token_transfers.token_id : "N/A"}</td> -->
                <td class="px-6 py-4 whitespace-nowrap">{historyItem.hash}</td>
                <td class="px-6 py-4 whitespace-nowrap"
                  >{historyItem.from.hash}</td
                >
                <td class="px-6 py-4 whitespace-nowrap"
                  >{historyItem.to.hash}</td
                >
                <td class="px-6 py-4 whitespace-nowrap"
                  >{historyItem.coinAmount}</td
                >
              </tr>
            {/each}
          </tbody>
        </table>
      </div>
    </div>
  </Modal>
{/if}

<style>
  .modal-content {
    animation: scaleUp 0.1s ease-out forwards;
  }

  @keyframes scaleUp {
    from {
      transform: scale(0.985);
      opacity: 0;
    }
    to {
      transform: scale(1);
      opacity: 1;
    }
  }

  .icon-wrapper {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 3em;
    height: 3em;
    border-radius: 50%;
    background-color: rgba(184, 142, 86, 1);
    margin: 0 auto 1em;
  }

  .icon-wrapper svg {
    width: 1.5em;
    height: 1.5em;
    fill: white;
  }
</style>
