<script lang="ts">
  import { getContext } from "svelte";
  import { getModels as _getModels, checkUniapp, checkPlatform } from "$lib/utils";

  import {
    user,
    chats,
    showRewardsHistoryModal,
    showRewardDetailModal,
    downLoadUrl,
    showDownLoad,
    mobile,
    settings,
    models,
    showSidebar,
    showWalletView,
    showNewWalletModal,
    showShareModal,
    showUserVerifyModal
  } from "$lib/stores";

  import { getRewardsCount, clockIn } from "$lib/apis/rewards/index.js";

  import DownLoadModal from "$lib/components/download/DownLoadModal.svelte";
  import { RewardProperties } from "$lib/constants"
  import { toast } from "svelte-sonner";

  const i18n = getContext("i18n");

  let clockLoading = false;

  let items = [
    {
      id: "new_wallet",
      text: "Create Wallet",
      reward: RewardProperties?.regist + " DGC",
      icon: '<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 24 24"><path fill="currentColor" d="M6 20q-1.65 0-2.825-1.175T2 16V8q0-1.65 1.175-2.825T6 4h12q1.65 0 2.825 1.175T22 8v8q0 1.65-1.175 2.825T18 20zM6 8h12q.55 0 1.05.125t.95.4V8q0-.825-.587-1.412T18 6H6q-.825 0-1.412.588T4 8v.525q.45-.275.95-.4T6 8m-1.85 3.25l11.125 2.7q.225.05.45 0t.425-.2l3.475-2.9q-.275-.375-.7-.612T18 10H6q-.65 0-1.137.338t-.713.912"/></svg>',
    },
    {
      id: "clock_in",
      text: "Clock In",
      reward: RewardProperties?.clockinall + " DGC",
      icon: '<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 24 24"><path fill="currentColor" d="M4 19q-.825 0-1.412-.587T2 17V5q0-.825.588-1.412T4 3h16q.825 0 1.413.588T22 5v12q0 .825-.587 1.413T20 19h-4v1q0 .425-.288.713T15 21H9q-.425 0-.712-.288T8 20v-1zm0-2h16V5H4zm0 0V5zm4-2h8v-.55q0-1.125-1.1-1.787T12 12t-2.9.663T8 14.45zm4-4q.825 0 1.413-.587T14 9t-.587-1.412T12 7t-1.412.588T10 9t.588 1.413T12 11"/></svg>',
    },
    {
      id: "invite",
      text: "Share",
      reward: RewardProperties?.invite + " DGC",
      icon: '<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 24 24"><path fill="currentColor" d="M18 22q-1.25 0-2.125-.875T15 19q0-.175.025-.363t.075-.337l-7.05-4.1q-.425.375-.95.588T6 15q-1.25 0-2.125-.875T3 12t.875-2.125T6 9q.575 0 1.1.213t.95.587l7.05-4.1q-.05-.15-.075-.337T15 5q0-1.25.875-2.125T18 2t2.125.875T21 5t-.875 2.125T18 8q-.575 0-1.1-.212t-.95-.588L8.9 11.3q.05.15.075.338T9 12t-.025.363t-.075.337l7.05 4.1q.425-.375.95-.587T18 16q1.25 0 2.125.875T21 19t-.875 2.125T18 22"/></svg>',
    },
    // {
    //   id: 4,
    //   text: "Make First Transaction",
    //   reward: "3000DGCs",
    //   icon: ''
    // }
  ];

  let rewardsCount: any = {};

  async function getCount() {
    if ($user) {
      const res = await getRewardsCount(localStorage.token);
      if (res) {
        Object.keys(res).forEach((key) => {
          if (res[key]) {
            rewardsCount[key] = res[key].length;
          } else {
            rewardsCount[key] = 0;
          }          
        });
        console.log("rewardsCount", rewardsCount);
      }
    }
  }

  $: if ($user?.id?.startsWith("0x")) {
    getCount();
  }

  let modObj:any = null;
  $: {
    let selmodels = $settings?.models ?? ['deepseek-chat'];
    if (selmodels.length > 0) {
      modObj = $models.filter(item => selmodels.includes(item?.model));
    }
    if (modObj.length == 0) {
      modObj = [$models.find(item => item?.model === 'deepseek-chat')];
    }
  }
</script>

<div>
  <!-- 模型介绍 -->
  {#if modObj}
    <div class="flex flex-col items-center w-full {$mobile ? 'mb-10':'mb-16'}">
      <img class="size-8" src="{modObj[0]?.modelicon}" alt=""/>
      <span class="text-xl font-bold mt-1">{ modObj[0]?.name }</span>
      <span class="w-full max-w-[600px] text-lg text-center mt-2">{ $i18n.t(modObj[0]?.desc) }</span>
    </div>
  {/if}
  <div class="flex my-2 mt-20
    {$mobile? 'flex-col' : 'flex-wrap items-center flex-wrap justify-between'}">
    <!-- 节点选择 -->
    <!-- <div class="flex flex-col {$mobile ? '' : 'pb-6'}">
      <ModelDeSelector />
      //<span class="text-xl ml-10 mt-1">
      //  {$i18n.t("Unlimited DGC Reward Task")}
      //</span>
    </div> -->
    <!-- app下载 -->
    <div class="flex flex-col self-start">
      {#if !checkUniapp() }
        <div class="flex justify-center items-center my-1">
          <!-- <span class="text-base region-text-color font-bold">
            {$i18n.t("Download DeGPT APP")}
          </span> -->
          {#if checkPlatform() == "ios"}
            <button
              class="flex gap-1 items-center cursor-pointer primaryButton mr-2 mr-10 text-gray-100 rounded-lg px-2 py-1 text-xs"
              on:click={() => {
                window.open(
                  "https://apps.apple.com/us/app/degpt/id6504377109?platform=iphone",
                  "_blank"
                );
              }}
            >
              <svg
                class="icon fill-white"
                viewBox="0 0 1024 1024"
                version="1.1"
                xmlns="http://www.w3.org/2000/svg"
                width="12"
                height="12"
              >
                <path
                  d="M631.125333 128c6.698667 44.074667-11.861333 87.210667-36.266666 117.76-26.154667 32.725333-71.168 58.069333-114.858667 56.746667-8.021333-42.154667 12.416-85.632 37.248-114.858667 27.221333-32.213333 73.941333-56.917333 113.877333-59.648z m131.157334 620.117333c22.528-33.408 30.890667-50.261333 48.384-87.936-127.104-46.805333-147.456-221.696-21.674667-288.853333-38.4-46.506667-92.288-73.557333-143.146667-73.557333-36.693333 0-61.824 9.301333-84.650666 17.706666-19.029333 6.997333-36.437333 13.44-57.685334 13.44-22.954667 0-43.264-7.04-64.512-14.421333-23.338667-8.106667-47.872-16.64-78.293333-16.64-57.130667 0-117.888 33.792-156.416 91.52-54.186667 81.365333-44.970667 234.24 42.922667 364.501333 31.36 46.592 73.301333 98.986667 128.213333 99.413334 22.741333 0.256 37.930667-6.314667 54.314667-13.44 18.773333-8.149333 39.168-17.066667 74.496-17.194667 35.498667-0.213333 55.594667 8.746667 74.069333 17.066667 16 7.082667 30.805333 13.696 53.376 13.44 54.912-0.426667 99.2-58.453333 130.56-105.045334z"
                />
              </svg>
              <span class="truncate">App Store</span>
            </button>
          {:else if checkPlatform() == "android"}
            <button
              class="flex gap-1 items-center cursor-pointer primaryButton mr-2 text-gray-100 rounded-lg px-2 py-1 text-xs"
              on:click={() => {
                window.open("https://play.google.com/store/apps/details?id=uni.UNIEF8864C&hl=en", "_blank");
              }}
            >
              <svg class="icon mr-1 fill-white" 
                viewBox="0 0 1024 1024" 
                version="1.1" 
                xmlns="http://www.w3.org/2000/svg" 
                width="12" 
                height="12">
                <path d="M556.373333 512c0-3.413333-3.413333-10.24-6.826666-13.653333L105.813333 75.093333c-3.413333-3.413333-10.24-3.413333-13.653333-3.413333-6.826667 0-10.24 3.413333-13.653333 10.24-3.413333 10.24-6.826667 20.48-6.826667 30.72v798.72c0 10.24 3.413333 20.48 6.826667 30.72 3.413333 3.413333 6.826667 10.24 13.653333 10.24h3.413333c3.413333 0 10.24 0 10.24-3.413333l447.146667-423.253334c3.413333-3.413333 3.413333-10.24 3.413333-13.653333zM580.266667 477.866667c3.413333 3.413333 6.826667 3.413333 10.24 3.413333s6.826667 0 10.24-3.413333l122.88-116.053334c3.413333-3.413333 6.826667-10.24 6.826666-13.653333 0-6.826667-3.413333-10.24-10.24-13.653333L187.733333 44.373333c-10.24-6.826667-20.48-6.826667-30.72-10.24-6.826667 0-13.653333 3.413333-17.066666 10.24s0 13.653333 3.413333 20.48L580.266667 477.866667zM604.16 546.133333c-6.826667-6.826667-17.066667-6.826667-23.893333 0L143.36 959.146667c-3.413333 6.826667-6.826667 13.653333-3.413333 20.48 3.413333 6.826667 10.24 10.24 17.066666 10.24 10.24 0 20.48-3.413333 30.72-10.24L716.8 686.08c3.413333-3.413333 6.826667-6.826667 10.24-13.653333 0-6.826667 0-10.24-6.826667-13.653334L604.16 546.133333zM914.773333 440.32L785.066667 368.64c-6.826667-3.413333-13.653333-3.413333-20.48 3.413333l-136.533334 129.706667c-3.413333 3.413333-6.826667 6.826667-6.826666 13.653333s3.413333 10.24 6.826666 13.653334l133.12 126.293333c3.413333 3.413333 6.826667 3.413333 10.24 3.413333s6.826667 0 6.826667-3.413333l136.533333-75.093333c23.893333-13.653333 40.96-40.96 40.96-68.266667s-10.24-58.026667-40.96-71.68z" fill="#ffffff"/>
              </svg>
              <span class="truncate">Google Play</span>
            </button>
            <button
              class="flex gap-1 items-center cursor-pointer primaryButton mr-2 text-gray-100 rounded-lg px-2 py-1 text-xs"
              on:click={() => {
                window.open("/static/app/degpt_v2.0_250813.apk", "_blank");
              }}
            >
              <svg
                class="icon mr-1 fill-white"
                viewBox="0 0 1024 1024"
                version="1.1"
                xmlns="http://www.w3.org/2000/svg"
                width="12"
                height="12">
                <path
                  d="M808.398269 218.955161c20.458525 11.691232 27.566623 37.753501 15.876521 58.213157l-65.330296 114.329713c119.461015 74.88989 203.198446 202.202702 217.966199 350.95283 2.492185 25.107214-17.227161 46.882472-42.457572 46.882472H85.333333c-25.230411 0-44.949757-21.775258-42.457571-46.882472 14.120124-142.220715 91.287453-264.84528 202.445704-340.790817l-71.137484-124.491726c-11.691232-20.459656-4.583135-46.521925 15.876521-58.213157 20.459656-11.691232 46.523055-4.583135 58.214287 15.876521l71.589581 125.281766c58.218808-25.812486 122.559011-40.113448 190.028856-40.113448 60.891832 0 119.233837 11.648283 172.825431 32.893457l67.465324-118.061775c11.691232-20.459656 37.754631-27.567753 58.214287-15.876521zM317.895488 554.666667c-23.563302 0-42.666667 19.102234-42.666667 42.666666s19.103364 42.666667 42.666667 42.666667c23.565563 0 42.666667-19.102234 42.666667-42.666667s-19.101104-42.666667-42.666667-42.666666z m384 0c-23.563302 0-42.666667 19.102234-42.666667 42.666666s19.103364 42.666667 42.666667 42.666667c23.565563 0 42.666667-19.102234 42.666667-42.666667s-19.101104-42.666667-42.666667-42.666666z"
                />
              </svg>
              <span class="truncate">Android</span>
            </button>
          {:else}
            <button
              class="flex gap-1 items-center cursor-pointer primaryButton mr-2 text-gray-100 rounded-lg px-2 py-1 text-xs"
              on:click={() => {
                window.open("https://play.google.com/store/apps/details?id=com.degpt.app", "_blank");
              }}
            >
              <svg class="icon mr-1 fill-white" 
                viewBox="0 0 1024 1024" 
                version="1.1" 
                xmlns="http://www.w3.org/2000/svg" 
                width="12" 
                height="12">
                <path d="M556.373333 512c0-3.413333-3.413333-10.24-6.826666-13.653333L105.813333 75.093333c-3.413333-3.413333-10.24-3.413333-13.653333-3.413333-6.826667 0-10.24 3.413333-13.653333 10.24-3.413333 10.24-6.826667 20.48-6.826667 30.72v798.72c0 10.24 3.413333 20.48 6.826667 30.72 3.413333 3.413333 6.826667 10.24 13.653333 10.24h3.413333c3.413333 0 10.24 0 10.24-3.413333l447.146667-423.253334c3.413333-3.413333 3.413333-10.24 3.413333-13.653333zM580.266667 477.866667c3.413333 3.413333 6.826667 3.413333 10.24 3.413333s6.826667 0 10.24-3.413333l122.88-116.053334c3.413333-3.413333 6.826667-10.24 6.826666-13.653333 0-6.826667-3.413333-10.24-10.24-13.653333L187.733333 44.373333c-10.24-6.826667-20.48-6.826667-30.72-10.24-6.826667 0-13.653333 3.413333-17.066666 10.24s0 13.653333 3.413333 20.48L580.266667 477.866667zM604.16 546.133333c-6.826667-6.826667-17.066667-6.826667-23.893333 0L143.36 959.146667c-3.413333 6.826667-6.826667 13.653333-3.413333 20.48 3.413333 6.826667 10.24 10.24 17.066666 10.24 10.24 0 20.48-3.413333 30.72-10.24L716.8 686.08c3.413333-3.413333 6.826667-6.826667 10.24-13.653333 0-6.826667 0-10.24-6.826667-13.653334L604.16 546.133333zM914.773333 440.32L785.066667 368.64c-6.826667-3.413333-13.653333-3.413333-20.48 3.413333l-136.533334 129.706667c-3.413333 3.413333-6.826667 6.826667-6.826666 13.653333s3.413333 10.24 6.826666 13.653334l133.12 126.293333c3.413333 3.413333 6.826667 3.413333 10.24 3.413333s6.826667 0 6.826667-3.413333l136.533333-75.093333c23.893333-13.653333 40.96-40.96 40.96-68.266667s-10.24-58.026667-40.96-71.68z" fill="#ffffff"/>
              </svg>
              <span class="truncate">Google Play</span>
            </button>
            <button
              class="flex gap-1 items-center cursor-pointer primaryButton mr-2 text-gray-100 rounded-lg px-2 py-1 text-xs"
              on:click={() => {
                window.open("/static/app/degpt_v2.0_250813.apk", "_blank");
              }}
            >
              <svg
                class="icon mr-1 fill-white"
                viewBox="0 0 1024 1024"
                version="1.1"
                xmlns="http://www.w3.org/2000/svg"
                width="12"
                height="12">
                <path
                  d="M808.398269 218.955161c20.458525 11.691232 27.566623 37.753501 15.876521 58.213157l-65.330296 114.329713c119.461015 74.88989 203.198446 202.202702 217.966199 350.95283 2.492185 25.107214-17.227161 46.882472-42.457572 46.882472H85.333333c-25.230411 0-44.949757-21.775258-42.457571-46.882472 14.120124-142.220715 91.287453-264.84528 202.445704-340.790817l-71.137484-124.491726c-11.691232-20.459656-4.583135-46.521925 15.876521-58.213157 20.459656-11.691232 46.523055-4.583135 58.214287 15.876521l71.589581 125.281766c58.218808-25.812486 122.559011-40.113448 190.028856-40.113448 60.891832 0 119.233837 11.648283 172.825431 32.893457l67.465324-118.061775c11.691232-20.459656 37.754631-27.567753 58.214287-15.876521zM317.895488 554.666667c-23.563302 0-42.666667 19.102234-42.666667 42.666666s19.103364 42.666667 42.666667 42.666667c23.565563 0 42.666667-19.102234 42.666667-42.666667s-19.101104-42.666667-42.666667-42.666666z m384 0c-23.563302 0-42.666667 19.102234-42.666667 42.666666s19.103364 42.666667 42.666667 42.666667c23.565563 0 42.666667-19.102234 42.666667-42.666667s-19.101104-42.666667-42.666667-42.666666z"
                />
              </svg>
              <span class="truncate">Android</span>
            </button>
            <button
              class="flex gap-1 items-center cursor-pointer primaryButton mr-2 mr-10 text-gray-100 rounded-lg px-2 py-1 text-xs"
              on:click={() => {
                window.open(
                  "https://apps.apple.com/us/app/degpt/id6504377109?platform=iphone",
                  "_blank"
                );
              }}
            >
              <svg
                class="icon fill-white"
                viewBox="0 0 1024 1024"
                version="1.1"
                xmlns="http://www.w3.org/2000/svg"
                width="12"
                height="12"
              >
                <path
                  d="M631.125333 128c6.698667 44.074667-11.861333 87.210667-36.266666 117.76-26.154667 32.725333-71.168 58.069333-114.858667 56.746667-8.021333-42.154667 12.416-85.632 37.248-114.858667 27.221333-32.213333 73.941333-56.917333 113.877333-59.648z m131.157334 620.117333c22.528-33.408 30.890667-50.261333 48.384-87.936-127.104-46.805333-147.456-221.696-21.674667-288.853333-38.4-46.506667-92.288-73.557333-143.146667-73.557333-36.693333 0-61.824 9.301333-84.650666 17.706666-19.029333 6.997333-36.437333 13.44-57.685334 13.44-22.954667 0-43.264-7.04-64.512-14.421333-23.338667-8.106667-47.872-16.64-78.293333-16.64-57.130667 0-117.888 33.792-156.416 91.52-54.186667 81.365333-44.970667 234.24 42.922667 364.501333 31.36 46.592 73.301333 98.986667 128.213333 99.413334 22.741333 0.256 37.930667-6.314667 54.314667-13.44 18.773333-8.149333 39.168-17.066667 74.496-17.194667 35.498667-0.213333 55.594667 8.746667 74.069333 17.066667 16 7.082667 30.805333 13.696 53.376 13.44 54.912-0.426667 99.2-58.453333 130.56-105.045334z"
                />
              </svg>
              <span class="truncate">App Store</span>
            </button>
          {/if}
          <!-- <button
            class="primaryButton text-xs text-gray-100 rounded-md ml-2 px-2 py-1 whitespace-nowrap"
            on:click={() => {
              $showDownLoad = true;
            }}
          >
            {$i18n.t("Download")}
          </button> -->
        </div>
        <!-- <div class="flex flex-wrap mt-1">
          <a class="text-sm" href="https://www.decentralgpt.org" target="_blank">
            <span>
              {$i18n.t("More info")},
            </span>
            <span class="text-blue-600">
              {$i18n.t("Visit")}
            </span>
            <span>
              {$i18n.t("official website")}
            </span>
          </a>
        </div>  -->
      {/if}
    </div>
    <div class="flex text-xs gap-1 {$mobile ? 'flex-wrap self-stat' : 'self-end'}">
      <button
          class="flex gap-1 items-center cursor-pointer primaryButton text-gray-100 rounded-lg my-1 px-2 py-1"
          on:click={() => {
            if (checkUniapp()) {
              $downLoadUrl = "https://www.decentralgpt.org";
              $showDownLoad = true;
            } else {
              window.open("https://www.decentralgpt.org", "_blank");
            }
          }}
        >
          <span> {$i18n.t("Visit")}{$i18n.t("official website")}</span>
      </button>
      {#if $user?.id?.startsWith("0x")}
        <button
          class="flex gap-1 items-center cursor-pointer primaryButton text-gray-100 rounded-lg my-1 px-2 py-1"
          on:click={() => {
            $showRewardsHistoryModal = true;
          }}
        >
          <svg
            class="primaryText cursor-pointer"
            xmlns="http://www.w3.org/2000/svg"
            width="1em"
            height="1em"
            viewBox="0 0 24 24"
            ><path
              fill="#ffffff"
              d="M13.26 3C8.17 2.86 4 6.95 4 12H2.21c-.45 0-.67.54-.35.85l2.79 2.8c.2.2.51.2.71 0l2.79-2.8a.5.5 0 0 0-.36-.85H6c0-3.9 3.18-7.05 7.1-7c3.72.05 6.85 3.18 6.9 6.9c.05 3.91-3.1 7.1-7 7.1c-1.61 0-3.1-.55-4.28-1.48a.994.994 0 0 0-1.32.08c-.42.42-.39 1.13.08 1.49A8.858 8.858 0 0 0 13 21c5.05 0 9.14-4.17 9-9.26c-.13-4.69-4.05-8.61-8.74-8.74m-.51 5c-.41 0-.75.34-.75.75v3.68c0 .35.19.68.49.86l3.12 1.85c.36.21.82.09 1.03-.26c.21-.36.09-.82-.26-1.03l-2.88-1.71v-3.4c0-.4-.34-.74-.75-.74"
            /></svg
          >
          <span> {$i18n.t("Rewards History")} </span>
        </button>
      {/if}
      <button
        class="flex gap-1 items-center cursor-pointer primaryButton text-gray-100 rounded-lg my-1 px-2 py-1"
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
            fill="#ffffff"
            d="M128 24a104 104 0 1 0 104 104A104.11 104.11 0 0 0 128 24m0 192a88 88 0 1 1 88-88a88.1 88.1 0 0 1-88 88m-32-88a32 32 0 0 0 57.6 19.2a8 8 0 0 1 12.8 9.61a48 48 0 1 1 0-57.62a8 8 0 0 1-12.8 9.61A32 32 0 0 0 96 128"
          /></svg
        >
        <span> {$i18n.t("Rewards Details")} </span>
      </button>
      <button
        class="flex gap-1 items-center cursor-pointer primaryButton text-gray-100 rounded-lg my-1 px-2 py-1"
        on:click={() => {
          $showSidebar = true;
          $showWalletView = true;
        }}
      >
        <span> {$i18n.t("Enter wallet")} </span>
      </button>
    </div>
  </div>

  <div class="flex flex-wrap lg:justify-between">
    {#each items as item, index}
      {#if (item.id !== "new_wallet" && $user?.id?.startsWith("0x")) || (item.id === "new_wallet" && !$user?.id?.startsWith("0x"))}
        <div
          class="flex direction-column justify-center gap-2 w-full lg:w-2/5 lg:px-2 mb-2 text-xs lg:text-sm break-normal"
        >
          <div
            class="flex justify-start items-center gap-2 w-[180px] lg:w-auto"
          >
            {@html item.icon}
            <span>{$i18n.t(item.text)}</span>
          </div>
          <div
            class="px-4 py-2 primaryButton text-gray-100 transition rounded-lg flex justify-between items-center"
          >
            <span class="relative">{item.reward}</span>
            <button
              disabled={clockLoading}
              class={"px-2 lg:px-3.5 py-1 dark:bg-white dark:text-zinc-950 bg-white text-zinc-950 transition rounded-lg break-words"}
              style={clockLoading && item.id === "clock_in"
                ? "background: rgba(251, 251, 251, 0.8)"
                : ""}
              on:click={async () => {
                if (item.id === "new_wallet") {
                  $showNewWalletModal = true;
                } else if (item.id === "invite") {
                  $showShareModal = true;
                } else if (item.id === "clock_in") {
                  if (!$user?.verified) {
                    toast.warning($i18n.t("To claim the reward, you must first complete user verification !"));
                    $showUserVerifyModal = true;
                  }else if ($chats.length > 0) {
                    clockLoading = true;
                    await clockIn(localStorage.token)
                      .then((res) => {
                        console.log("Clock In  res", res);
                        getCount();
                        if (res?.ok) {
                          toast.success($i18n.t(res?.message, RewardProperties));
                        }
                        if (res?.detail) {
                          toast.warning($i18n.t(res?.detail, RewardProperties));
                        }
                      })
                      .catch((res) => {
                        console.log("Clock In  error", res);
                      });
                    clockLoading = false;
                  } else {
                    toast.warning(
                      $i18n.t(
                        "You need to complete a conversation to receive a reward ！"
                      )
                    );
                  }
                }
                return;
              }}
            >
              {(($user?.id?.startsWith("0x") && rewardsCount[item.id]) || 0) > 0
                ? clockLoading && item.id === "clock_in"
                  ? $i18n.t("Done...")
                  : $i18n.t("Done")
                : clockLoading && item.id === "clock_in"
                ? $i18n.t("Get Now...")
                : $i18n.t("Get Now!")}
            </button>
          </div>
        </div>
      {/if}
    {/each}
  </div>
</div>

<DownLoadModal bind:show={$showDownLoad} />

<style>
  .mt-20 {
    margin-top: 20px;
  }
  .mr-10 {
    margin-right: 10px;
  }
  .direction-column {
    flex-direction: column;
  }
  .region-text-color {
    color: rgba(184, 142, 86, 1);
  }
</style>
