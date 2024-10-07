<script lang="ts">
  import { beforeUpdate, onMount } from "svelte";
  import { fade } from "svelte/transition";
  import dayjs from "dayjs";
  import { getContext } from "svelte";
  import { getCurrentPair } from "$lib/utils/wallet/dbc";
  import Modal from "../common/Modal.svelte";
  import { toast } from "svelte-sonner";
  import { copyToClipboard } from "$lib/utils";
  import { currentWalletData, user} from "$lib/stores";
  import { getRewardsHistory, clockInCheck } from "$lib/apis/rewards";

  const i18n = getContext("i18n");

  export let show = true;

  let modalElement = null;
  let mounted = false;

  let rewardsHistory = [];

  // onMount(async () => {
  //   mounted = true;

  //   const address = $currentWalletData?.walletInfo?.address;
  //   const rewardsHistory = await getRewardsHistory(localStorage.token,);
  //   console.log("rewardsHistory", rewardsHistory);
  // });

  // $: if (show) {
  //   (async () => {
  //     const address = $currentWalletData?.walletInfo?.address;
  //     rewardsHistory = await getRewardsHistory(localStorage.token);
  //     console.log("rewardsHistory", rewardsHistory);
  //   })();
  // }


  // 当组件挂载时运行一次
  onMount(() => {
    if (show) {
      fetchData();
    }
  });

  // 使用变量来跟踪 show 状态的变化
  let previousShow = show;


  // 当 show 状态变化时运行
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
    rewardsHistory = await getRewardsHistory(localStorage.token);
    console.log("rewardsHistory", rewardsHistory);
  }

  async function updateReward(id) {
    await clockInCheck(localStorage.token, id)
      .then((res) => {
        console.log("Clock In Check res", res);
        if (res?.ok) {
          const checkReward = res.data;
          const index = rewardsHistory.findIndex(item => item.id === checkReward.id);
          if (index !== -1) {
            rewardsHistory[index] = { 
              ...rewardsHistory[index], 
              transfer_hash: checkReward.transfer_hash, 
              status: checkReward.status 
            };
          }
        }
        if (res?.detail) {
          toast.warning(res?.detail);
        }
      }).catch((res) => {
        console.log("Clock In Check  error", res);
      }); 
    console.log("Clock In Check res update", rewardsHistory);
  }

</script>

{#if show}
  <!-- svelte-ignore a11y-click-events-have-key-events -->
  <!-- svelte-ignore a11y-no-static-element-interactions -->
  <Modal bind:show size="lg">


    <div class=" flex justify-between items-center dark:text-gray-300 px-5 pt-4 pb-1">
      <h1 class="text-xl font-semibold ">{$i18n.t("View Reward")}</h1>

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
      class=" m-auto rounded-2xl max-w-full mx-2 bg-gray-50 dark:bg-gray-900 shadow-3xl p-4"
      on:mousedown={(e) => {
        e.stopPropagation();
      }}
    >


      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead>
            <tr>
              <!-- <th
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider whitespace-nowrap"
              >
                {$i18n.t("user ID")}
              </th> -->
              <th
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider whitespace-nowrap"
              >
                {$i18n.t("transfer hash")}
              </th>
              <th
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider whitespace-nowrap"
              >
                {$i18n.t("reward amount")}
              </th>
              <th
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider whitespace-nowrap"
              >
                {$i18n.t("reward date")}
              </th>
              <th
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider whitespace-nowrap"
              >
                {$i18n.t("reward type")}
              </th>
            </tr>
          </thead>
          <tbody
            class="bg-white border-b dark:bg-gray-900 dark:border-gray-700 text-xs"
          >
            {#each rewardsHistory as historyItem}
              <tr>
                <!-- <td class="px-6 py-4 whitespace-nowrap flex items-center">
                  {historyItem.user_id}
                </td> -->
                <td class="px-6 py-4 whitespace-nowrap"
                  >{historyItem.transfer_hash}</td
                >
                <td class="px-6 py-4 whitespace-nowrap">   
                  {#if historyItem.status}
                    {historyItem.reward_amount} DGC
                  {:else}
                    <div class="flex direction-column amount-styl">
                      <div class="obtain-amount">{historyItem.reward_amount} DGC</div>
                      <div class="obtain-styl cursor-pointer" 
                        on:click={() => {
                          if ($user.verified) {
                            updateReward(historyItem.id)
                          } else {
                            toast.warning("Please complete the KYC verification to convert your points into cash");
                          }
                        }}
                      >Obtain now</div>
                    </div>
                  {/if}
                  
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  {dayjs(historyItem.reward_date).format("YYYY-MM-DD")}
                </td>
                <td class="px-6 py-4 whitespace-nowrap"
                  >{historyItem.reward_type}</td
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

  .direction-column {
    flex-direction: column;
  }
  
  .amount-styl {
    background-color: #B88E56;
    border-radius: 5px;
    padding: 8px;
  }

  .obtain-amount {
    padding: 6px;
  }

  .obtain-styl {
    background-color: #ffffff;
    border-radius: 5px;
    padding: 6px;
    text-align: center;
    color: #000000;
  }
</style>
