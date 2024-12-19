<script lang="ts">
  import { beforeUpdate, onMount } from "svelte";
  import dayjs from "dayjs";
  import { getContext } from "svelte";
  import Modal from "../common/Modal.svelte";
  import { toast } from "svelte-sonner";
  import { copyToClipboard } from "$lib/utils";
  import { user } from "$lib/stores";
  import {
    getRewardsHistory,
    creatWalletCheck,
    inviteCheck,
    clockInCheck,
  } from "$lib/apis/rewards";
  import { getUserInfo } from "$lib/apis/users";

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
  let rewardsHistory = { row: [], total: 1 };

  $: pageTotal =
    Math.ceil(rewardsHistory?.total / pageSize) == 0
      ? "1"
      : Math.ceil(rewardsHistory?.total / pageSize);
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
      rewardsHistory = { row: [], total: 1 };
    }
    prePage = currentPage;
    getRewardsHistory(localStorage.token, {
      pageSize: pageSize,
      pageNum: currentPage,
    })
      .then((result) => {
        loading = false;
        if (result) {
          rewardsHistory = result;
        }
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
    } else if (type === "clock_in") {
      rewardApiMethod = clockInCheck;
    } else if (type === "invite" || type === "invitee") {
      rewardApiMethod = inviteCheck;
    }
    if (rewardApiMethod === null) {
      return;
    }
    await rewardApiMethod(localStorage.token, id)
      .then((res) => {
        console.log("Clock In Check res", res);
        if (res?.ok) {
          const checkReward = res.data;
          const index = rewardsHistory?.row.findIndex(
            (item) => item.id === checkReward.id
          );
          if (index !== -1) {
            let rowinfo = rewardsHistory?.row[index];
            rewardsHistory.row[index] = {
              ...rowinfo,
              transfer_hash: checkReward.transfer_hash,
              status: checkReward.status,
            };
          }
        }
        if (res?.detail) {
          toast.warning($i18n.t(res?.detail));
        }
      })
      .catch((res) => {
        console.log("Clock In Check  error", res);
      });
    console.log("Clock In Check res update", rewardsHistory);
    obtainLoad = false;
  }

  let selItem = "";

  function formateAddress(val) {
    return val.substring(0, 6) + "*****" + val.substring(val.length - 2);
  }
</script>

{#if show}
  <!-- svelte-ignore a11y-click-events-have-key-events -->
  <!-- svelte-ignore a11y-no-static-element-interactions -->
  <Modal bind:show size="lg">
    <div
      class=" flex justify-between items-center dark:text-gray-300 px-5 pt-4 pb-1"
    >
      <h1 class="text-xl font-semibold">{$i18n.t("View Reward")}</h1>
      <div class="flex flex-row gap-2 text-xs">
        <!-- <button
          class="flex gap-1 items-center cursor-pointer primaryButton text-gray-100 rounded-lg px-2 py-1"
          on:click={() => {
            window.open("https://twitter.com/DecentralGPT", "_blank");
            showFollowTwitterModal.set(true);
          }}
        >
          <svg
            viewBox="0 0 1024 1024"
            xmlns="http://www.w3.org/2000/svg"
            width="1.3em"
            height="1.3em"
            ><path
              d="M789.4 378.8c0-6.8-0.1-13.5-0.4-20.1 28.9-21.6 54.1-48.5 73.9-79.4-26.6 11.9-55.1 19.9-85.1 23.3 30.6-18.8 54.1-48.9 65.1-85-28.6 17.4-60.3 29.8-94 36.2-27-30.7-65.5-50.2-108.1-51-81.8-1.3-148.1 67.7-148.1 154.3 0 12.3 1.3 24.2 3.8 35.8-123.2-7.9-232.3-72-305.3-168.6-12.7 23.1-20.1 50.2-20.1 79.2 0 54.8 26.1 103.5 65.9 132.3-24.3-1.1-47.1-8.5-67.1-20.5v2c0 76.6 51.1 140.8 118.8 155.8-12.4 3.5-25.5 5.4-39 5.3-9.6-0.1-18.8-1.1-27.9-3 18.8 62.8 73.6 108.7 138.3 110.2-50.7 42-114.6 67.1-183.9 66.9-11.9 0-23.8-0.8-35.3-2.3 65.6 45 143.4 71.1 227.1 71.1 272.5 0 421.4-236.9 421.4-442.5z"
              fill="#ffffff"
            />
          </svg>
          <span> {$i18n.t("Follow Twitter")} </span>
        </button> -->
        <!-- <button
          class="flex gap-1 items-center cursor-pointer primaryButton text-gray-100 rounded-lg px-2 py-1 mr-2"
          on:click={() => {
            showFollowTGGroupModal.set(true);
          }}
        >
          <svg
            viewBox="0 0 1024 1024"
            xmlns="http://www.w3.org/2000/svg"
            width="1em"
            height="1em"
            ><path
              d="M984.239354 114.550695c-22.6438-20.202081-54.362985-26.026805-82.834818-15.320298L74.058856 411.843205C43.284265 423.495961 23.082184 451.152233 21.59664 484.093932c-1.493816 32.948317 15.859593 62.356472 45.548976 76.862863l129.189428 63.181958c2.583987 1.217551 4.880129 2.976052 6.918203 4.873512 13.424491 34.569512 66.427658 169.998889 90.014398 218.93914 11.927367 24.941596 33.892911 42.427347 54.220717 50.027115-1.349893-0.140614-2.840401-0.410262-4.473176-0.679909 3.928918 1.48389 8.003412 2.708058 12.20694 3.523618 26.837402 5.422733 54.354714-2.843709 73.607237-22.230229l48.128-48.129654c8.537745-8.541053 21.955619-10.438514 32.531438-4.473176l207.283076 117.669014c12.466662 7.043929 26.293144 10.713124 40.12128 10.713125a80.695832 80.695832 0 0 0 32.136064-6.65021c23.58674-10.167212 40.667192-30.228679 46.902178-55.170275l173.110591-697.886604c7.460808-29.279121-2.168763-60.052058-24.802636-80.113525zM254.769215 612.347037l443.564045-253.779955-250.391987 256.484705c-4.064569 4.201874-7.043929 8.944698-9.082003 14.504736-0.133997 0.272956-0.133997 0.410262-0.269648 0.683219-0.54095 1.619541-50.017189 147.624737-79.302927 213.647095-5.965338-3.930572-13.146572-10.304517-17.356718-19.118527-21.687625-45.544013-72.249073-174.467102-87.160762-212.421273z m0 0"
              fill="#ffffff"
            />
          </svg>
          <span> {$i18n.t("Follow TG Group")} </span>
        </button> -->
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
        <tbody class="bg-white dark:bg-gray-900 text-xs">
          {#each rewardsHistory?.row as historyItem}
            <tr>
              <td class="px-6 py-4 whitespace-nowrap">
                {formateAddress(historyItem.transfer_hash)}
                <button
                  on:click={async () => {
                    const res = await copyToClipboard(
                      historyItem.transfer_hash
                    );
                    if (res) {
                      toast.success(
                        $i18n.t("Copying to clipboard was successful!")
                      );
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
                    /></svg
                  >
                </button>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                {#if historyItem.status}
                  {historyItem.reward_amount} {historyItem.amount_type}
                {:else}
                  <div
                    class="flex direction-column {historyItem.expird
                      ? 'amount-expird-styl'
                      : 'amount-styl'}"
                  >
                    <div class="obtain-amount">
                      {historyItem.reward_amount}
                      {historyItem.amount_type}
                    </div>
                    {#if historyItem.expird}
                      <button class="obtain-styl cursor-pointer">
                        <span>{$i18n.t("Reward expird")}</span>
                      </button>
                    {:else}
                      <button
                        class="obtain-styl cursor-pointer"
                        style={obtainLoad && selItem == historyItem?.id
                          ? "background: rgba(251, 251, 251, 0.8)"
                          : ""}
                        disabled={obtainLoad && selItem == historyItem?.id}
                        on:click={async () => {
                          if (!$user?.verified) {
                            const userInfo = await getUserInfo(localStorage.token);
                            await user.set({
                              ...$user,
                              verified: userInfo?.verified,
                            });
                          }
                          selItem = historyItem?.id;
                          if ($user?.verified) {
                            await updateReward(historyItem.id,historyItem.reward_type);
                          } else {
                            toast.warning(
                              $i18n.t("Please complete the KYC verification !")
                            );
                          }
                        }}
                      >
                        {#if obtainLoad && selItem == historyItem?.id}
                          <span>{$i18n.t("Obtain in...")}</span>
                        {:else}
                          <span>{$i18n.t("Obtain now")}</span>
                        {/if}
                      </button>
                    {/if}
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
        <div
          class="flex items-center justify-center inset-0 z-10 bg-opacity-50 w-full absolute"
        >
          <div
            class="flex items-center justify-center bg-gray-300 w-[100px] h-[100px] rounded-xl opacity-60"
          >
            <svg
              class="animate-spin"
              xmlns="http://www.w3.org/2000/svg"
              width="30"
              height="30"
              viewBox="0 0 24 24"
            >
              <path
                fill="white"
                d="M12 20q-3.35 0-5.675-2.325T4 12t2.325-5.675T12 4q1.725 0 3.3.712T18 6.75V4h2v7h-7V9h4.2q-.8-1.4-2.187-2.2T12 6Q9.5 6 7.75 7.75T6 12t1.75 4.25T12 18q1.925 0 3.475-1.1T17.65 14h2.1q-.7 2.65-2.85 4.325T12 20"
              />
            </svg>
          </div>
        </div>
      {/if}
    </div>

    <div class="flex justify-center items-center h-[50px] pt-5 pb-10">
      <button
        class="px-1.5 py-1.5 mr-4 dark:bg-white dark:text-zinc-950 text-gray-100 rounded-full"
        on:click={previousPage}
      >
        <svg
          class="icon"
          viewBox="0 0 1024 1024"
          version="1.1"
          xmlns="http://www.w3.org/2000/svg"
          width="12"
          height="12"
        >
          <path
            d="M510.0475173 510.0475173l3.9049654 3.9049654-3.9049654-3.9049654zM514.38636775 509.61363225l-4.7727355 4.7727355c1.73554016-1.51859766 3.25413782-3.03719531 4.7727355-4.7727355z"
            fill="#515151"
          />
          <path
            d="M216.74122852 512.21694254c0 18.00622928 6.72521815 34.27691837 18.00622926 46.64264205l4.77273549 4.77273547 46.64264205 46.64264208L689.0250974 1013.13722421c26.90087265 26.90087265 71.157147 26.90087265 98.27496213 0 26.90087265-26.90087265 26.90087265-71.157147 0-98.27496216L384.22085499 512l402.86226199-403.07920455c26.90087265-26.90087265 26.90087265-71.157147 0-98.27496217-26.90087265-26.90087265-71.157147-26.90087265-98.05801958 0.21694251L286.16283532 413.72503786l-47.29346962 47.29346962-3.90496539 3.90496538c-11.49795361 12.3657237-18.44011431 29.07029783-18.22317179 47.29346968z"
            fill="#515151"
          />
        </svg>
      </button>
      <div class="fs-16">{currentPage} / {pageTotal}</div>
      <button
        class="px-1.5 py-1.5 ml-4 dark:bg-white dark:text-zinc-950 text-gray-100 rounded-full"
        on:click={nextPage}
      >
        <svg
          class="icon"
          viewBox="0 0 1024 1024"
          version="1.1"
          xmlns="http://www.w3.org/2000/svg"
          width="12"
          height="12"
        >
          <path
            d="M784.246262 454.443749L360.714443 30.88935a85.577949 85.577949 0 0 0-120.983285 121.005865l363.062756 363.040176-363.085336 362.995017a85.577949 85.577949 0 0 0 120.983285 120.983285l423.554399-423.464079a85.510209 85.510209 0 0 0 0-121.005865z"
            fill="#515151"
          />
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
    background-color: #b88e56;
    border-radius: 5px;
    padding: 8px;
  }

  .amount-expird-styl {
    background-color: #b6b6b6;
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
