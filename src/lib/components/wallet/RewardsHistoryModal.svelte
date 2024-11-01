<script lang="ts">
  import { beforeUpdate, onMount } from "svelte";
  import dayjs from "dayjs";
  import { getContext } from "svelte";
  import Modal from "../common/Modal.svelte";
  import { toast } from "svelte-sonner";
  import { copyToClipboard } from "$lib/utils";
  import { user} from "$lib/stores";
  import { getRewardsHistory, creatWalletCheck, inviteCheck, clockInCheck } from "$lib/apis/rewards";

  const i18n = getContext("i18n");

  export let show = true;

  // 当组件挂载时运行一次
  onMount(async () => {
    if (show) {
      firstCtrl = true;
      await fetchData();
    }
  });

  // 使用变量来跟踪 show 状态的变化
  let previousShow = show;


  // 当 show 状态变化时运行
  beforeUpdate(async () => {
    if (show !== previousShow) {
      previousShow = show;
      if (show) {
        currentPage = 1;
        firstCtrl = true;
        await fetchData();
      }
    }
  });

  // 分页功能
  let currentPage = 1;
  let prePage = 1;
  let pageSize = 10;
  let loading = false;
  let firstCtrl = true;
  let rewardsHistory = {row: [], total: 1};

  $: pageTotal = Math.ceil(rewardsHistory?.total / pageSize);
  $: if (currentPage != prePage) {
    (async () => {
      await fetchData();
    })();
    
  }
 
  function previousPage() {
    if (currentPage > 1) {
      currentPage--;
    }
  }
 
  function nextPage() {
    if (currentPage < Math.ceil(rewardsHistory?.total / pageSize)) {
      currentPage++;
    }
  }

  function fetchData() {
    loading = true;
    if (firstCtrl) {
      firstCtrl = false;
      rewardsHistory = {row: [], total: 1};
    }
    prePage = currentPage;
    getRewardsHistory(localStorage.token, {pageSize: pageSize, pageNum: currentPage})
      .then(result => {
          loading = false;
          rewardsHistory = result;
          console.log("rewardsHistory", rewardsHistory);
      })
      .catch((error) => {
        loading = false;
      });
      
  }

  let obtainLoad = false;
  async function updateReward(id, type) {
    obtainLoad = true;
    let rewardApiMethod = null;
    if (type === "new_wallet") {
      rewardApiMethod = creatWalletCheck;
    } else if (type === "clock_in"){
      rewardApiMethod = clockInCheck;
    } else if (type === "invite" || type === "invitee") {
      rewardApiMethod = inviteCheck;
    }
    if (rewardApiMethod === null) {
      console.log("===============方法未找到===============")
      return;
    }
    await rewardApiMethod(localStorage.token, id)
      .then((res) => {
        console.log("Clock In Check res", res);
        if (res?.ok) {
          const checkReward = res.data;
          const index = rewardsHistory?.row.findIndex(item => item.id === checkReward.id);
          if (index !== -1) {
            let rowinfo = rewardsHistory?.row[index];
            rowinfo = { 
              ...rowinfo, 
              transfer_hash: checkReward.transfer_hash, 
              status: checkReward.status 
            };
          }
        }
        if (res?.detail) {
          toast.warning($i18n.t(res?.detail));
        }
      }).catch((res) => {
        console.log("Clock In Check  error", res);
      }); 
    console.log("Clock In Check res update", rewardsHistory);
    obtainLoad = false;
  }

  let selItem = '';

  function formateAddress(val) {
    return val.substring(0, 6) + '*****' + val.substring(val.length - 2);
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
      class=" m-auto rounded-2xl max-w-full min-h-[50vh] max-h-[68vh] mx-2 bg-gray-50 dark:bg-gray-900 shadow-3xl p-4 overflow-auto relative"
      on:mousedown={(e) => {
        e.stopPropagation();
      }}
    >
      <table class="min-w-full divide-y divide-gray-200 overflow-auto">
        <thead class="dark:border-gray-200 border-b">
          <tr>
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
          class="bg-white dark:bg-gray-900 text-xs"
        >
          {#each rewardsHistory?.row as historyItem}
            <tr>
              <td class="px-6 py-4 whitespace-nowrap">
                {formateAddress(historyItem.transfer_hash)}
                <button
                  on:click={async () => {
                    const res = await copyToClipboard(historyItem.transfer_hash);
                    if (res) {
                      toast.success($i18n.t("Copying to clipboard was successful!"));
                    }
                  }}
                  type="button"
                  class="px-3 py-2 text-sm-12 dark:text-gray-300 dark:bg-gray-650 rounded-md fs12"
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
                {#if historyItem.status}
                  {historyItem.reward_amount} DGC
                {:else}
                  <div class="flex direction-column amount-styl">
                    <div class="obtain-amount">{historyItem.reward_amount} DGC</div>
                    <button class="obtain-styl cursor-pointer" style={(obtainLoad && selItem == historyItem?.id) ? "background: rgba(251, 251, 251, 0.8)" : ""} disabled={(obtainLoad && selItem == historyItem?.id)}
                      on:click={() => {
                        selItem = historyItem?.id;
                        if ($user?.verified) {
                          updateReward(historyItem.id, historyItem.reward_type)
                        } else {
                          toast.warning($i18n.t("Please complete the KYC verification to convert your points into cash")); 
                        } 
                      }}
                    >
                    {#if (obtainLoad && selItem == historyItem?.id) }
                      <span>Obtain in...</span>
                    {:else}
                      <span>Obtain now</span>
                    {/if}
                    
                  </button>
                  </div>
                {/if}
                
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                {dayjs(historyItem.reward_date).format("YYYY-MM-DD HH:mm:ss")}
              </td>
              <td class="px-6 py-4 whitespace-nowrap"
                >{historyItem.reward_type}</td
              >
            </tr>
          {/each}
        </tbody>
      </table>
      {#if loading}
        <div class="flex items-center justify-center inset-0 z-10 bg-opacity-50 w-full absolute">
          <div class="flex items-center justify-center bg-gray-300 w-[150px] h-[150px] rounded-xl opacity-90">
            <svg class="animate-spin"
              xmlns="http://www.w3.org/2000/svg"
              width="80"
              height="80"
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
      <div class="fs-16">{ currentPage } / { pageTotal }</div>
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
  .h-v-80 {
    height: 80vh;
  }
</style>
