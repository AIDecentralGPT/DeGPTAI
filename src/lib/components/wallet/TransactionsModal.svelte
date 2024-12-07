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

  onMount(async () => {
    if (show) {
      fetchData();
    }
  });

  let previousShow = show;

  beforeUpdate(async () => {
    if (show !== previousShow) {
      previousShow = show;
      if (show) {
        await fetchData();
      }
    }
  });

  async function fetchData() {
    loading = true;
    pagedItems = [];
    
    try {
      const res = await getTransactions($user?.id);
      // 合并两个 items 数组
      const mergedItems = [...res[0].items, ...res[1].items];
      // 按时间排序
      mergedItems.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));

      transactionsList = mergedItems.filter((item) => !!item.value)?.map((item) => {
        const coinType = (item?.tx_types?.[0] === "coin_transfer") ? "DBC" : "DGC";
        if (coinType === "DGC") {
          let toHash = item?.to?.hash;
          if (item.decoded_input) {
            toHash = item?.decoded_input?.parameters[0].value;
          }
          let coinAmount = '0.00000';
          if (item.decoded_input?.parameters[1]?.value) {
            coinAmount = Number(ethers.formatUnits(item.decoded_input.parameters[1].value, "ether")).toFixed(5);
          }
          return {
            ...item,
            coinType,
            toHash,
            coinAmount: coinAmount,
          };
        } else {
          const toHash = item.to.hash;
          return {
            ...item,
            coinType,
            toHash,
            coinAmount: Number(ethers.formatUnits(item.value, "ether")).toFixed(5),
          };    
        } 
      });
      loading = false;
    } catch (error) {
      loading = false;
      console.log("transactionsList-error", error);
    }
    
  }

  function formateAddress(val: String) {
    try {
      return val.substring(0, 6) + '*****' + val.substring(val.length - 2);
    } catch(error) {
      return "*************";
    }
    
  }

  // 分页功能
  let currentPage = 0;
  let pageSize = 10;
  let loading = false;

  $: pageTotal = Math.ceil(transactionsList.length / pageSize) == 0 ? 1 : Math.ceil(transactionsList.length / pageSize);
  $: pagedItems = transactionsList.slice(currentPage * pageSize, (currentPage + 1) * pageSize);
 
  function previousPage() {
    if (currentPage > 0) {
      currentPage--;
    }
  }
 
  function nextPage() {
    if (currentPage < (Math.ceil(transactionsList.length / pageSize) - 1)) {
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
      class="m-auto rounded-2xl max-w-full min-h-[50vh] max-h-[68vh] overflow-auto mx-2 bg-gray-50 dark:bg-gray-900 shadow-3xl p-4"
    >
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="dark:border-gray-200 border-b">
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
          class="bg-white dark:bg-gray-900 text-xs"
        >
          {#each pagedItems as historyItem}
            <tr>
              <td class="px-6 py-4 whitespace-nowrap">{historyItem.coinType}</td>
              <!-- <td class="px-6 py-4 whitespace-nowrap">{historyItem.token_transfers ? historyItem.token_transfers.token_id : "N/A"}</td> -->
              <td class="px-6 py-4 whitespace-nowrap">
                {formateAddress(historyItem?.hash)}
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
      {#if loading}
        <div class="flex items-center justify-center inset-0 z-10 bg-opacity-50 w-full absolute">
          <div class="flex items-center justify-center bg-gray-300 w-[100px] h-[100px] rounded-xl opacity-60">
            <svg class="animate-spin"
              xmlns="http://www.w3.org/2000/svg"
              width="30"
              height="30"
              viewBox="0 0 24 24">
                <path fill="white" d="M12 20q-3.35 0-5.675-2.325T4 12t2.325-5.675T12 4q1.725 0 3.3.712T18 6.75V4h2v7h-7V9h4.2q-.8-1.4-2.187-2.2T12 6Q9.5 6 7.75 7.75T6 12t1.75 4.25T12 18q1.925 0 3.475-1.1T17.65 14h2.1q-.7 2.65-2.85 4.325T12 20"/>
            </svg>
          </div> 
        </div>
      {/if}
    </div>
    <div class="flex justify-center items-center h-[50px] pt-5 pb-10">
      <button class="px-1.5 py-1.5 mr-4 dark:bg-white dark:text-zinc-950 text-gray-100 rounded-full" on:click={previousPage}> 
        <svg class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" width="12" height="12">
          <path d="M510.0475173 510.0475173l3.9049654 3.9049654-3.9049654-3.9049654zM514.38636775 509.61363225l-4.7727355 4.7727355c1.73554016-1.51859766 3.25413782-3.03719531 4.7727355-4.7727355z" fill="#515151"></path>
          <path d="M216.74122852 512.21694254c0 18.00622928 6.72521815 34.27691837 18.00622926 46.64264205l4.77273549 4.77273547 46.64264205 46.64264208L689.0250974 1013.13722421c26.90087265 26.90087265 71.157147 26.90087265 98.27496213 0 26.90087265-26.90087265 26.90087265-71.157147 0-98.27496216L384.22085499 512l402.86226199-403.07920455c26.90087265-26.90087265 26.90087265-71.157147 0-98.27496217-26.90087265-26.90087265-71.157147-26.90087265-98.05801958 0.21694251L286.16283532 413.72503786l-47.29346962 47.29346962-3.90496539 3.90496538c-11.49795361 12.3657237-18.44011431 29.07029783-18.22317179 47.29346968z" fill="#515151"></path>
        </svg>  
      </button>
      <div class="fs-16">{ currentPage + 1 } / { pageTotal }</div>
      <button class="px-1.5 py-1.5 ml-4 dark:bg-white dark:text-zinc-950 text-gray-100 rounded-full" on:click={nextPage}>
        <svg class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" width="12" height="12">
          <path d="M784.246262 454.443749L360.714443 30.88935a85.577949 85.577949 0 0 0-120.983285 121.005865l363.062756 363.040176-363.085336 362.995017a85.577949 85.577949 0 0 0 120.983285 120.983285l423.554399-423.464079a85.510209 85.510209 0 0 0 0-121.005865z" fill="#515151"></path>
        </svg>
      </button>
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
