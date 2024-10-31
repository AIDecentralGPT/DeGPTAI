<script lang="ts">
  import { beforeUpdate, onMount } from "svelte";
  import { copyToClipboard } from "$lib/utils";
  import { toast } from "svelte-sonner";
  import dayjs from "dayjs";
  import { getContext } from "svelte";
  import Modal from "../common/Modal.svelte";
  import { user } from "$lib/stores";
  import { getTransactions } from "$lib/apis/wallet";
  import { ethers } from "ethers";
  const i18n = getContext("i18n");

  export let show = false;

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
    const res = await getTransactions($user?.id);
    // 合并两个 items 数组
    const mergedItems = [...res[0].items, ...res[1].items];

    // 按时间排序
    mergedItems.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));

    transactionsList = mergedItems.filter((item) => !!item.value)?.map((item) => {
      const coinType = (item?.tx_types?.[0] === "coin_transfer" || item?.tx_types?.[0] === "contract_call") ? "DBC" : "DGC";
      if (coinType === "DGC") {
        const toHash = item.decoded_input.parameters[0].value;
        return {
          ...item,
          coinType,
          toHash,
          coinAmount: ethers.formatUnits(item.decoded_input.parameters[1].value, "ether"),
        };
      } else {
        const toHash = item.to.hash;
        return {
          ...item,
          coinType,
          toHash,
          coinAmount: ethers.formatUnits(item.value, "ether"),
        };
      } 
    });
    console.log("transactionsList", transactionsList);
  }

  function formateAddress(val) {
    return val.substring(0, 6) + '*****' + val.substring(val.length - 2);
  }

  // 分页功能
  let currentPage = 0;
  let pageSize = 10;

  $: pageTotal = Math.ceil(transactionsList.length / pageSize);
  $: pagedItems = transactionsList.slice(currentPage * pageSize, (currentPage + 1) * pageSize);
 
  function previousPage() {
    if (currentPage > 0) {
      currentPage--;
    }
  }
 
  function nextPage() {
    if (currentPage < (transactionsList.length / pageSize) - 1) {
      currentPage++;
    }
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
      class="m-auto rounded-2xl max-w-full h-v-60 overflow-auto mx-2 bg-gray-50 dark:bg-gray-900 shadow-3xl p-4"
    >
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
            <th
              class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider whitespace-nowrap"
              >Date</th
            >
          </tr>
        </thead>
        <tbody
          class="bg-white border-b dark:bg-gray-900 dark:border-gray-700 text-xs"
        >
          {#each pagedItems as historyItem}
            <tr>
              <td class="px-6 py-4 whitespace-nowrap">{historyItem.coinType}</td>
              <!-- <td class="px-6 py-4 whitespace-nowrap">{historyItem.token_transfers ? historyItem.token_transfers.token_id : "N/A"}</td> -->
              <td class="px-6 py-4 whitespace-nowrap">
                {formateAddress(historyItem.hash)}
                <button
                  on:click={async () => {
                    const res = await copyToClipboard(historyItem.hash);
                    if (res) {
                      toast.success($i18n.t("Copying to clipboard was successful!"));
                    }
                  }}
                  type="button"
                  class="inset-y-0 right-0 px-3 py-2 text-sm-12 dark:text-gray-300 dark:bg-gray-650 rounded-md fs12"
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="1em"
                    height="1em"
                    viewBox="0 0 512 512"
                    ><rect
                      width="336"
                      height="336"
                      x="128"
                      y="128"
                      fill="none"
                      stroke="currentColor"
                      stroke-linejoin="round"
                      stroke-width="32"
                      rx="57"
                      ry="57"
                    /><path
                      fill="none"
                      stroke="currentColor"
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="32"
                      d="m383.5 128l.5-24a56.16 56.16 0 0 0-56-56H112a64.19 64.19 0 0 0-64 64v216a56.16 56.16 0 0 0 56 56h24"
                    /></svg>
                </button>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                {formateAddress(historyItem.from.hash)}
                <button
                  on:click={async () => {
                    const res = await copyToClipboard(historyItem.from.hash);
                    if (res) {
                      toast.success($i18n.t("Copying to clipboard was successful!"));
                    }
                  }}
                  type="button"
                  class="inset-y-0 right-0 px-3 py-2 text-sm-12 dark:text-gray-300 dark:bg-gray-650 rounded-md fs12"
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="1em"
                    height="1em"
                    viewBox="0 0 512 512"
                    ><rect
                      width="336"
                      height="336"
                      x="128"
                      y="128"
                      fill="none"
                      stroke="currentColor"
                      stroke-linejoin="round"
                      stroke-width="32"
                      rx="57"
                      ry="57"
                    /><path
                      fill="none"
                      stroke="currentColor"
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="32"
                      d="m383.5 128l.5-24a56.16 56.16 0 0 0-56-56H112a64.19 64.19 0 0 0-64 64v216a56.16 56.16 0 0 0 56 56h24"
                    /></svg>
                </button>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                {formateAddress(historyItem.toHash)}
                <button
                  on:click={async () => {
                    const res = await copyToClipboard(historyItem.toHash);
                    if (res) {
                      toast.success($i18n.t("Copying to clipboard was successful!"));
                    }
                  }}
                  type="button"
                  class="inset-y-0 right-0 px-3 py-2 text-sm-12 dark:text-gray-300 dark:bg-gray-650 rounded-md fs12"
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="1em"
                    height="1em"
                    viewBox="0 0 512 512"
                    ><rect
                      width="336"
                      height="336"
                      x="128"
                      y="128"
                      fill="none"
                      stroke="currentColor"
                      stroke-linejoin="round"
                      stroke-width="32"
                      rx="57"
                      ry="57"
                    /><path
                      fill="none"
                      stroke="currentColor"
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="32"
                      d="m383.5 128l.5-24a56.16 56.16 0 0 0-56-56H112a64.19 64.19 0 0 0-64 64v216a56.16 56.16 0 0 0 56 56h24"
                    /></svg>
                </button>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">{historyItem.coinAmount}</td>
              <td class="px-6 py-4 whitespace-nowrap">{dayjs(new Date(historyItem.timestamp)).format('YYYY-MM-DD HH:mm:ss')}</td>
            </tr>
          {/each}
        </tbody>
      </table>
    </div>
    <div class="flex justify-center items-center h-[50px]">
      <button class="px-2 py-1 fs-12 mr-4 dark:bg-white dark:text-zinc-950 text-gray-100 rounded-md" on:click={previousPage}> Pre </button>
      <div class="fs-16">{ currentPage + 1 } / { pageTotal }</div>
      <button class="px-2 py-1 fs-12 ml-4 dark:bg-white dark:text-zinc-950 text-gray-100 rounded-md" on:click={nextPage}> Next </button>
    </div>  
  </Modal>
{/if}

<style>

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

  .fs-12 {
    font-size: 12px;
  }
  .fs-16 {
    font-size: 20px;
  }
  .h-v-60 {
    height: 60vh;
  }
</style>
