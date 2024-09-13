<script lang="ts">
  import {
    exportAccountForKeystore,
    createAccountFromMnemonic,
    createAccountFromSeed,
    getCurrentPair,
    savePair,
  } from "./../../utils/wallet/dbc.js";
  import { getContext, onMount } from "svelte";
  import { toast } from "svelte-sonner";

  import { getModels as _getModels } from "$lib/utils";

  import Modal from "../common/Modal.svelte";
  import { onGetBalance } from "$lib/utils/wallet/dbc.js";
  import { onGetDLCBalance } from "$lib/utils/wallet/dbc.js";
  import {
    currentWalletData,
    models,
    settings,
    user,
    inviterId,
    showRewardsModal,
    threesideAccount,
    showShareModal,
    showRewardsHistoryModal,
    showNewWalletModal,
    showRewardDetailModal,
    showUserVerifyModal,
  } from "$lib/stores";

  import {
    createAccount,
    downloadKeyStore,
  } from "$lib/utils/wallet/ether/utils.js";
  import { clockIn, getRewardsCount } from "$lib/apis/rewards/index.js";

  const i18n = getContext("i18n");

  let clockLoading = false;

  const items = [
    {
      id: "new_wallet",
      text: "Create Wallet",
      reward: "2000DGCs",
      icon: '<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 24 24"><path fill="currentColor" d="M6 20q-1.65 0-2.825-1.175T2 16V8q0-1.65 1.175-2.825T6 4h12q1.65 0 2.825 1.175T22 8v8q0 1.65-1.175 2.825T18 20zM6 8h12q.55 0 1.05.125t.95.4V8q0-.825-.587-1.412T18 6H6q-.825 0-1.412.588T4 8v.525q.45-.275.95-.4T6 8m-1.85 3.25l11.125 2.7q.225.05.45 0t.425-.2l3.475-2.9q-.275-.375-.7-.612T18 10H6q-.65 0-1.137.338t-.713.912"/></svg>',
    },
    {
      id: "clock_in",
      text: "Clock In",
      reward: "15000DGCs",
      icon: '<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 24 24"><path fill="currentColor" d="M4 19q-.825 0-1.412-.587T2 17V5q0-.825.588-1.412T4 3h16q.825 0 1.413.588T22 5v12q0 .825-.587 1.413T20 19h-4v1q0 .425-.288.713T15 21H9q-.425 0-.712-.288T8 20v-1zm0-2h16V5H4zm0 0V5zm4-2h8v-.55q0-1.125-1.1-1.787T12 12t-2.9.663T8 14.45zm4-4q.825 0 1.413-.587T14 9t-.587-1.412T12 7t-1.412.588T10 9t.588 1.413T12 11"/></svg>',
    },
    {
      id: "invite",
      text: "Share",
      reward: "10000DGCs",
      icon: '<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 24 24"><path fill="currentColor" d="M18 22q-1.25 0-2.125-.875T15 19q0-.175.025-.363t.075-.337l-7.05-4.1q-.425.375-.95.588T6 15q-1.25 0-2.125-.875T3 12t.875-2.125T6 9q.575 0 1.1.213t.95.587l7.05-4.1q-.05-.15-.075-.337T15 5q0-1.25.875-2.125T18 2t2.125.875T21 5t-.875 2.125T18 8q-.575 0-1.1-.212t-.95-.588L8.9 11.3q.05.15.075.338T9 12t-.025.363t-.075.337l7.05 4.1q.425-.375.95-.587T18 16q1.25 0 2.125.875T21 19t-.875 2.125T18 22"/></svg>',
    },
    // {
    //   id: 4,
    //   text: "Make First Transaction",
    //   reward: "3000DGCs",
    //   icon: ''
    // }
  ];

  let rewardsCount = {};

  async function getCount() {
    if ($user) {
      const res = await getRewardsCount(localStorage.token);
      if (res) {
        Object.keys(res).forEach((key) => {
          rewardsCount[key] = res[key].length;
        });
        console.log("rewardsCount", rewardsCount);
      }
    }
  }

  $: if ($user?.id?.startsWith("0x")) {
    getCount();
  }
</script>

<div>
  <div class="flex gap-3 items-center my-4 flex-wrap justify-between mt-20">
    <span class="text-xl ml-10"> 40000+ DGC Tokens Reward Task </span>
  
    <div class="flex fs-12">
      {#if $user?.id?.startsWith("0x")}
        <div
          class="flex gap-1 items-center cursor-pointer"
          on:click={() => {
            if ($user?.verified) {
              $showRewardsHistoryModal = true;
            } else {
              $showUserVerifyModal = true;
            }
          }}
        >
          <svg
            class="primaryText cursor-pointer"
            xmlns="http://www.w3.org/2000/svg"
            width="1em"
            height="1em"
            viewBox="0 0 24 24"
            ><path
              fill="currentColor"
              d="M13.26 3C8.17 2.86 4 6.95 4 12H2.21c-.45 0-.67.54-.35.85l2.79 2.8c.2.2.51.2.71 0l2.79-2.8a.5.5 0 0 0-.36-.85H6c0-3.9 3.18-7.05 7.1-7c3.72.05 6.85 3.18 6.9 6.9c.05 3.91-3.1 7.1-7 7.1c-1.61 0-3.1-.55-4.28-1.48a.994.994 0 0 0-1.32.08c-.42.42-.39 1.13.08 1.49A8.858 8.858 0 0 0 13 21c5.05 0 9.14-4.17 9-9.26c-.13-4.69-4.05-8.61-8.74-8.74m-.51 5c-.41 0-.75.34-.75.75v3.68c0 .35.19.68.49.86l3.12 1.85c.36.21.82.09 1.03-.26c.21-.36.09-.82-.26-1.03l-2.88-1.71v-3.4c0-.4-.34-.74-.75-.74"
            /></svg>
          <span> Rewards History </span>
        </div>
      {/if}
  
      <div
        class="flex gap-1 items-center cursor-pointer ml-10 mr-10"
        on:click={() => {
          $showRewardDetailModal = true;
        }}
      >
        <svg
          class="primaryText cursor-pointer"
          xmlns="http://www.w3.org/2000/svg"
          width="1em"
          height="1em"
          viewBox="0 0 256 256"
          ><path
            fill="currentColor"
            d="M128 24a104 104 0 1 0 104 104A104.11 104.11 0 0 0 128 24m0 192a88 88 0 1 1 88-88a88.1 88.1 0 0 1-88 88m-32-88a32 32 0 0 0 57.6 19.2a8 8 0 0 1 12.8 9.61a48 48 0 1 1 0-57.62a8 8 0 0 1-12.8 9.61A32 32 0 0 0 96 128"
          /></svg>
        <span> Rewards Details </span>
      </div>
    </div>
  </div>
  
  <div class="flex flex-wrap lg:justify-between">
    {#each items as item, index}
      {#if (item.text !== "Create Wallet" && $user?.id?.startsWith("0x")) || (item.text === "Create Wallet" && !$user?.id.startsWith("0x"))}
        <div
          class="flex direction-column justify-center gap-2 w-full lg:w-1/2 lg:px-2 mb-2 text-xs lg:text-sm break-normal"
        >
          <div class="flex justify-start items-center gap-2 w-[180px] lg:w-auto">
            {@html item.icon}
            <span>{item.text}</span>
          </div>
          <div
            class="px-4 py-2 primaryButton text-gray-100 transition rounded-lg flex justify-between items-center"
          >
            <span class="relative">{item.reward}</span>
            <button
              disabled={clockLoading}
              class={"px-2 lg:px-3.5 py-1 dark:bg-white dark:text-zinc-950 bg-black text-gray-100 transition rounded-lg break-words" +
                `${clockLoading ? "" : ""}`}
              on:click={async () => {
                console.log("user info ", $user);
  
                if (item.text === "Create Wallet") {
                  $showNewWalletModal = true;
                  return
                }
  
                if (!$user.verified) {
                  toast.warning("Please do identification first!");
                  $showUserVerifyModal = true;
                  return 
                }
  
                if (item.text === "Share") {
                  $showShareModal = true;
                }
  
                if (item.text === "Clock In") {
                  clockLoading = true;
                  await clockIn(localStorage.token)
                    .then((res) => {
                      console.log("Clock In  res", res);
  
                      getCount();
                      if (res?.ok) {
                        toast.success(
                          "Congratulations on your successful clocking in!"
                        );
                      }
                      if (res?.detail) {
                        toast.warning(res?.detail);
                      }
                    })
                    .catch((res) => {
                      console.log("Clock In  error", res);
                    });
  
                  clockLoading = false;
                }
  
  
              }}
            >
              {(($user?.id?.startsWith("0x") && rewardsCount[item.id]) || 0) > 0
                ? "Done"
                : "Get Now!"}
            </button>
          </div>
        </div>
      {/if}
    {/each}
  </div>
</div>


<style>
.fs-12 {
  font-size: 12px;
}
.mt-20 {
  margin-top: 20px;
}
.ml-10 {
  margin-left: 10px;
}
.mr-10 {
  margin-right: 10px;
}
.direction-column {
  flex-direction: column;
}
</style>
