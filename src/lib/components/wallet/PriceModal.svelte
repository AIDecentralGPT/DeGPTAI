<script lang="ts">
  import Modal from "../common/Modal.svelte";
  export let show = false;
  import { getContext } from "svelte";
  import {
    user,
    showConfirmUpgradeModal,
    vipupgrade,
    currentWalletData,
    dgcRate
  } from "$lib/stores";
  import { getDgcRate } from "$lib/apis/wallet/index";
  import ConfirmUpgradeModal from "./ConfirmUpgradeModal.svelte";
  import { isPro } from "$lib/apis/users/index.js";
  import Switch from "../common/Switch.svelte";
  import { toast } from "svelte-sonner";
  import { conversationUseTotal } from "$lib/apis/chats/index.js";
  const i18n = getContext("i18n");

  import { updateWalletData } from "$lib/utils/wallet/walletUtils";

  let checkProLoading = true;
  function checkPlus() {
    isPro(localStorage.token).then(result => {
      if (result) {
        user.set({
          ...$user,
          vipInfo: result,
        });
        assiganVip(result);
      } else{
        user.set({
          ...$user,
          vipInfo: []
        });
      }
      checkProLoading = false;
    }).catch(() => {
      checkProLoading = false;
    });    
  }

  async function refreshDgcRate() {
    getDgcRate(localStorage.token).then((result) => {
      if (result) {
        dgcRate.set({ rate: result });
      }
    });
  }

  // 封装成函数
function divideAndRound(num1, num2) {
  // 处理除数为0的情况
  if (num2 === 0) {
    throw new Error("除数不能为0");
  }
  return Math.round(num1 / num2);
}

  let basicInfo = null;
  let standardInfo = null;
  let proInfo = null;
  function assiganVip(vipInfo) {
    basicInfo = null;
    standardInfo = null;
    proInfo = null;
    vipInfo.forEach(item => {
      if (item.vip == "basic") {
        basicInfo = item;
      } else if (item.vip == "standard") {
        standardInfo = item;
      } else if (item.vip == "pro") {
        proInfo = item;
      }
    });
  }

  $: if (vipupgrade || !vipupgrade) {
    if ($user?.vipInfo) {
      assiganVip($user?.vipInfo);
      getUserUserTotal();
    }
  }

  // 显示初始化Socket
  $: if (show) {
    checkProLoading = true;
    checkPlus();
    isLoaded = false;
    getUserUserTotal();
    refreshDgcRate();
  }

  let viptype = "basic";
  let viptime = "month";
  let money = 3;
  let basicstat = false;
  let standardstat = false;
  let prostat = false;

  // 获取用户使用汇总
  let userTotal:any = {}
  let isLoaded = false;
  function getUserUserTotal() {
    conversationUseTotal().then(res => {
      console.log("=====================", res);
      userTotal = res;
      isLoaded = true;
    })
  }
  function checkUse(type, vip) {
    let html = "";
    userTotal?.month_total?.forEach(item => {
      if (item?.type==type && item?.vip == vip) {
        if (item?.show) {
          if (item?.time == "month") {
            if (item?.use / item?.total > 0.9) {
              html = "<div><span class='text-red-900 font-bold'>" + item?.use + "</span>" + 
                "<span class='mx-0.5 text-red-900'>/</span>" + 
                "<span class='primaryText'>" + item?.total + "</span></div>";
            } else {
              html = "<div><span class='text-green-900'>" + item?.use + "</span>" + 
                "<span class='mx-0.5 text-green-900'>/</span>" + 
                "<span class='primaryText'>" + item?.total + "</span></div>";
            }
          } else {
            if (item?.use / (item?.total * 12) > 0.9) {
              html = "<div><span class='text-red-900 font-bold'>" + item?.use + "</span>" + 
                "<span class='mx-0.5 text-red-900'>/</span>" + 
                "<span class='primaryText'>" + item?.total + ' x 12' + "</span></div>";
            } else {
              html = "<div><span class='text-green-900'>" + item?.use + "</span>" + 
                "<span class='mx-0.5 text-green-900'>/</span>" + 
                "<span class='primaryText'>" + item?.total + ' x 12' + "</span></div>";
            }
          }
        }    
      }
    })
    return html;
  }

  function openUpgradeModel() {
    updateWalletData($currentWalletData?.walletInfo);
    $showConfirmUpgradeModal = true;
  }
</script>

<Modal bind:show size="big">
  <div class="max-h-[80vh] xs:h-auto flex flex-col">
    <div class="flex justify-between dark:text-gray-300 px-8 pt-4 pb-2">
      <div class="text-lg font-medium self-center">{$i18n.t("Upgrade")}</div>
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

    <div class="mx-4 px-2 flex-1 overflow-auto">
      <div class="mx-4 text-center">
        <h2 class="font-semibold leading-7 primaryText text-2xl">
          {$i18n.t("Pricing")}
        </h2>
      </div>

      <div
        class="flex flex-gird flex-wrap justify-center h-8/10 md:h-108 overflow-y-auto pb-4 mt-4"
      >
        <div class="rounded-3xl p-4 ring-1 min-w-[337px] max-w-[376px] ring-gray-200 m-4">
          <h3 id="tier-free" class="text-lg font-semibold leading-8 text-center">
            {$i18n.t("Free")}
          </h3>
          <div class="mt-2 flex justify-center items-baseline gap-x-1">
            <span class="text-4xl font-bold tracking-tight">$0</span>
          </div>
          <div class="flex justify-center mt-8">
            <button
              disabled
              class="w-full block rounded-md py-2 px-3 text-center text-sm font-semibold leading-6 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 dark:bg-white dark:text-zinc-950 bg-black text-gray-100"
            >
              {#if $user?.vipInfo?.length > 0}
                {$i18n.t("Free")}
              {:else}
                {$i18n.t("Current Status")}
              {/if}
            </button>
          </div>
          <div class="flex justify-center mt-2">
            {#if userTotal?.free_total?.show}
              <span class="{userTotal?.free_total?.use/userTotal?.free_total?.total > 0.9 ? 'text-red-900 font-bold' : 'text-green-900'}">{userTotal?.free_total?.use}</span>
              <span class="mx-0.5 {userTotal?.free_total?.use/userTotal?.free_total?.total > 0.9 ? 'text-red-900' : 'text-green-900'}">/</span>
              <span class="primaryText">{userTotal?.free_total?.total}</span>
            {/if}
          </div>
          <ul
            role="list"
            class="mt-8 space-y-3 text-sm leading-6 xl:mt-10 font-bold text-gray-600 dark:text-gray-300"
          >
            <li class="flex gap-x-3">
              <svg
                class="h-6 w-5 flex-none primaryText"
                viewBox="0 0 20 20"
                fill="currentColor"
                aria-hidden="true"
              >
                <path
                  fill-rule="evenodd"
                  d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z"
                  clip-rule="evenodd"
                />
              </svg>
              <div>
                <div>{$i18n.t("Basic Model")}:</div>
                <div>{$i18n.t("Non-wallet users: {{ num }} times/day", {num: 3})}</div>
                <div>{$i18n.t("Wallet users: {{ num }} times/day", {num: 5})}</div>
                <div>{$i18n.t("KYC-verified users: {{ num }} times/day", {num: 10})}</div>
              </div>
            </li>

            <li class="flex gap-x-3">
              <svg
                class="h-6 w-5 flex-none primaryText"
                viewBox="0 0 20 20"
                fill="currentColor"
                aria-hidden="true"
              >
                <path
                  fill-rule="evenodd"
                  d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z"
                  clip-rule="evenodd"
                />
              </svg>
              {$i18n.t("All models share memory with each other.")}
            </li>
            <li class="flex gap-x-3">
              <svg
                class="h-6 w-5 flex-none primaryText"
                viewBox="0 0 20 20"
                fill="currentColor"
                aria-hidden="true"
              >
                <path
                  fill-rule="evenodd"
                  d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z"
                  clip-rule="evenodd"
                />
              </svg>
              {$i18n.t("Extended access rights for message, image understanding, advanced data analysis, and web browsing")}
            </li>
            <li class="flex gap-x-3">
              <svg
                class="h-6 w-5 flex-none primaryText"
                viewBox="0 0 20 20"
                fill="currentColor"
                aria-hidden="true"
              >
                <path
                  fill-rule="evenodd"
                  d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z"
                  clip-rule="evenodd"
                />
              </svg>
              <div>
                {$i18n.t("Accessible Foundation Model")}
                <div>
                  <div class="flex flex-row items-center mt-2">
                    <img class="w-[22px]" src="/static/icon/deepseek.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">DeepSeek V3.2</span>
                  </div>
                  <div class="flex flex-row items-center mt-2">
                    <img class="w-[22px]" src="/static/icon/doubao.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">DouBao 1.6 (TikTok)</span>
                  </div>
                  <div class="flex flex-row items-center mt-2">
                    <img class="w-[22px]" src="/static/icon/qwen.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">Qwen3 Max (Ali Cloud)</span>
                  </div>
                  <div class="flex flex-row items-center mt-2">
                    <img class="w-[22px]" src="/static/icon/qwen.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">Qwen3 Thinking (Ali Cloud)</span>
                  </div>
                  <div class="flex flex-row items-center mt-2">
                    <img class="w-[24px]" src="/static/icon/gpt3.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">GPT-5 mini (OpenAI)</span>
                  </div>
                </div>
              </div>
            </li>
            <li class="flex gap-x-3">
              <svg
                class="h-6 w-5 flex-none primaryText"
                viewBox="0 0 20 20"
                fill="currentColor"
                aria-hidden="true"
              >
                <path
                  fill-rule="evenodd"
                  d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z"
                  clip-rule="evenodd"
                />
              </svg>
              {$i18n.t("Access on web, iOS, Android")}
            </li> 
          </ul>
        </div>
        <div class="rounded-3xl p-4 ring-1 min-w-[337px] max-w-[376px] ring-gray-200 m-4">
          <h3 id="tier-plus" class="text-lg font-semibold leading-8 text-center">
            {$i18n.t("Basic VIP")}
          </h3>
          <div class="mt-2 flex flex-col justify-center items-center gap-x-1">
            <div>
              <span class="text-4xl font-bold tracking-tight">$3</span>
              <span class="text-xl tracking-tight"> / {$i18n.t("Month")}</span>
              <span class="text-sm">(={divideAndRound(3, $dgcRate.rate)}DGC)</span>
            </div>
          </div>
          {#if basicInfo}
            <div
              class="flex flex-col mt-6 px-1 py-1.5 primaryButton text-gray-100 text-sm transition rounded-lg w-full"
            >
              <div class="text-white text-center text-xs font-bold leading-5">{$i18n.t("Basic VIP")}</div>       
              <div class="flex-1 flex flex-row justify-center items-center leading-4 text-xs">
                <span>{$i18n.t("Valid until")} { basicInfo.end_date}</span>
                {#if checkProLoading}
                  <svg class="animate-spin ml-2"
                    xmlns="http://www.w3.org/2000/svg"
                    width="1em"
                    height="1em"
                    viewBox="0 0 24 24">
                    <path fill="#ffffff"
                      d="M12 20q-3.35 0-5.675-2.325T4 12t2.325-5.675T12 4q1.725 0 3.3.712T18 6.75V4h2v7h-7V9h4.2q-.8-1.4-2.187-2.2T12 6Q9.5 6 7.75 7.75T6 12t1.75 4.25T12 18q1.925 0 3.475-1.1T17.65 14h2.1q-.7 2.65-2.85 4.325T12 20"/>
                  </svg>
                {/if}
              </div>
            </div>
          {:else}
            <div class="flex flex-col mt-4">
              <div class="flex flex-row justify-start mb-2 ml-1">
                <div class="flex flex-row flex-wrap">
                  <span class="text-sm tracking-tight primaryText font-bold mr-1">$33 / {$i18n.t("Year")} ({$i18n.t("Instant Savings")} 8%)</span>
                  <span class="text-sm tracking-tight font-bold primaryText mr-2">(={divideAndRound(33, $dgcRate.rate)}DGC)</span>
                </div>
                <div class="flex-1 flex justify-start pt-1">
                  <Switch bind:state={basicstat}/>
                </div>
              </div>
              <button
                on:click={() => {
                  if ($user?.id?.startsWith("0x")) {
                    viptype = "basic";
                    viptime = basicstat ? "year" : "month";
                    money = basicstat ? 33 : 3;
                    openUpgradeModel();
                  } else {
                    toast.warning($i18n.t("Please create or log in to your wallet first."))
                  }
                }}
                aria-describedby="tier-plus"
                class="px-4 py-2 primaryButton text-gray-100 text-sm transition rounded-lg w-full flex flex-row justify-center items-center"
                disabled = { checkProLoading }
              >
                {$i18n.t("Upgrade to VIP")}
                {#if checkProLoading}
                  <svg class="animate-spin ml-2"
                    xmlns="http://www.w3.org/2000/svg"
                    width="1em"
                    height="1em"
                    viewBox="0 0 24 24">
                      <path fill="#ffffff"
                        d="M12 20q-3.35 0-5.675-2.325T4 12t2.325-5.675T12 4q1.725 0 3.3.712T18 6.75V4h2v7h-7V9h4.2q-.8-1.4-2.187-2.2T12 6Q9.5 6 7.75 7.75T6 12t1.75 4.25T12 18q1.925 0 3.475-1.1T17.65 14h2.1q-.7 2.65-2.85 4.325T12 20"/>
                  </svg>
                {/if}
              </button>
            </div>
          {/if}

          <ul
            role="list"
            class="mt-8 space-y-3 text-sm leading-6 xl:mt-10 font-bold text-gray-600 dark:text-gray-300"
          >
            <li class="flex gap-x-3">
              <svg
                class="h-6 w-5 flex-none primaryText"
                viewBox="0 0 20 20"
                fill="currentColor"
                aria-hidden="true"
              >
                <path
                  fill-rule="evenodd"
                  d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z"
                  clip-rule="evenodd"
                />
              </svg>
              {$i18n.t("Basic Model: {{ num }} Times/Month", {num: "1,000"})}
              {#if isLoaded}
                {@html checkUse("base", "basic")}
              {/if}
            </li>
            <li class="flex gap-x-3">
              <svg
                class="h-6 w-5 flex-none primaryText"
                viewBox="0 0 20 20"
                fill="currentColor"
                aria-hidden="true"
              >
                <path
                  fill-rule="evenodd"
                  d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z"
                  clip-rule="evenodd"
                />
              </svg>
              {$i18n.t("Premium Model: {{ num }} Times/Month", {num: 100})}
              {#if isLoaded}
                {@html checkUse("adv", "basic")}
              {/if}
            </li>
            <li class="flex gap-x-3">
              <svg
                class="h-6 w-5 flex-none primaryText"
                viewBox="0 0 20 20"
                fill="currentColor"
                aria-hidden="true"
              >
                <path
                  fill-rule="evenodd"
                  d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z"
                  clip-rule="evenodd"
                />
              </svg>
              {$i18n.t("Top-tier Model: {{ num }} Times/Month", {num: 10})}
              {#if isLoaded}
                {@html checkUse("top", "basic")}
              {/if}
            </li>

            <li class="flex gap-x-3">
              <svg
                class="h-6 w-5 flex-none primaryText"
                viewBox="0 0 20 20"
                fill="currentColor"
                aria-hidden="true"
              >
                <path
                  fill-rule="evenodd"
                  d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z"
                  clip-rule="evenodd"
                />
              </svg>
              {$i18n.t("All models share memory with each other.")}
            </li>
            <li class="flex gap-x-3">
              <svg
                class="h-6 w-5 flex-none primaryText"
                viewBox="0 0 20 20"
                fill="currentColor"
                aria-hidden="true"
              >
                <path
                  fill-rule="evenodd"
                  d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z"
                  clip-rule="evenodd"
                />
              </svg>
              {$i18n.t("Extended access rights for message, image understanding, advanced data analysis, and web browsing")}
            </li>
            <li class="flex gap-x-3">
              <svg
                class="h-6 w-5 flex-none primaryText"
                viewBox="0 0 20 20"
                fill="currentColor"
                aria-hidden="true"
              >
                <path
                  fill-rule="evenodd"
                  d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z"
                  clip-rule="evenodd"
                />
              </svg>
              <div>
                {$i18n.t("Accessible Foundation Model")}
                <div>
                  <div class="flex flex-row items-center mt-2">
                    <img class="w-[22px]" src="/static/icon/deepseek.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">DeepSeek V3.2</span>
                  </div>
                  <div class="flex flex-row items-center mt-2">
                    <img class="w-[22px]" src="/static/icon/doubao.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">DouBao 1.6 (TikTok)</span>
                  </div>
                  <div class="flex flex-row items-center mt-2">
                    <img class="w-[22px]" src="/static/icon/qwen.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">Qwen3 Max (Ali Cloud)</span>
                  </div>
                  <div class="flex flex-row items-center mt-2">
                    <img class="w-[22px]" src="/static/icon/qwen.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">Qwen3 Thinking (Ali Cloud)</span>
                  </div>
                  <div class="flex flex-row items-center mt-2">
                    <img class="w-[24px]" src="/static/icon/gpt3.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">GPT-5 mini (OpenAI)</span>
                  </div>
                </div>
              </div>
            </li>
            <li class="flex gap-x-3">
              <svg
                class="h-6 w-5 flex-none primaryText"
                viewBox="0 0 20 20"
                fill="currentColor"
                aria-hidden="true"
              >
                <path
                  fill-rule="evenodd"
                  d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z"
                  clip-rule="evenodd"
                />
              </svg>
              <div>
                {$i18n.t("Accessible Advanced Model")}
                <div>
                  <div class="flex flex-row items-center mt-2">
                    <img class="w-[22px]" src="/static/icon/gpt_round.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">GPT-4o audio (OpenAI)</span>
                  </div>
                  <div class="flex flex-row items-center mt-2">
                    <img class="w-[22px]" src="/static/icon/deepseek.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">DeepSeek R1</span>
                  </div>
                  <div class="flex flex-row items-center mt-2">
                    <img class="w-[22px]" src="/static/icon/gemini.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">Gemini 2.5 Flash (Google)</span>
                  </div>
                  <div class="flex flex-row items-center mt-2">
                    <img class="w-[22px]" src="/static/icon/grok.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">Grok 3 (Elon Musk)</span>
                  </div>
                  <div class="flex flex-row items-center mt-2">
                    <img class="w-[22px]" src="/static/icon/doubao.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">DouBao 1.6 Thinking (TikTok)</span>
                  </div>
              </div>
            </li>
            <li class="flex gap-x-3">
              <svg
                class="h-6 w-5 flex-none primaryText"
                viewBox="0 0 20 20"
                fill="currentColor"
                aria-hidden="true"
              >
                <path
                  fill-rule="evenodd"
                  d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z"
                  clip-rule="evenodd"
                />
              </svg>
              <div>
                {$i18n.t("Accessible Top-Level Model")}
                <div>
                  <div class="flex flex-row items-center mt-2">
                    <img class="w-[22px]" src="/static/icon/gpt_round.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">GPT-5 (OpenAI)</span>
                  </div>
                  <div class="flex flex-row items-center mt-2">
                    <img class="w-[22px]" src="/static/icon/claude.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">Claude 4.5 Sonnet (Anthropic)</span>
                  </div>
                  <div class="flex flex-row items-center mt-2">
                    <img class="w-[22px]" src="/static/icon/claude.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">Claude 4.5 Sonnet Thinking (Anthropic)</span>
                  </div>
                  <div class="flex flex-row items-center mt-2">
                    <img class="w-[22px]" src="/static/icon/grok.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">Grok 3 Thinking (Elon Musk)</span>
                  </div>
                  <div class="flex flex-row items-center mt-2">
                    <img class="w-[22px]" src="/static/icon/gemini.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">Gemini 2.5 Pro (Google)</span>
                  </div>
              </div>
            </li>
            <li class="flex gap-x-3">
              <svg
                class="h-6 w-5 flex-none primaryText"
                viewBox="0 0 20 20"
                fill="currentColor"
                aria-hidden="true"
              >
                <path
                  fill-rule="evenodd"
                  d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z"
                  clip-rule="evenodd"
                />
              </svg>
              {$i18n.t("Access on web, iOS, Android")}
            </li>
          </ul>
        </div>
        <div class="rounded-3xl p-4 ring-1 min-w-[337px] max-w-[376px] ring-gray-200 m-4">
          <h3 id="tier-plus" class="text-lg font-semibold leading-8 text-center">
            {$i18n.t("Standard VIP")}
          </h3>
          <div class="mt-2 flex flex-col justify-center items-center gap-x-1">
            <div>
              <span class="text-4xl font-bold tracking-tight">$8</span>
              <span class="text-xl tracking-tight"> / {$i18n.t("Month")}</span>
              <span class="text-sm">(={divideAndRound(8, $dgcRate.rate)}DGC)</span>
            </div>
          </div>
          {#if standardInfo}
            <div
              class="flex flex-col mt-6 px-1 py-1.5 primaryButton text-gray-100 text-sm transition rounded-lg w-full"
            >
              <div class="text-white text-center text-xs font-bold leading-5">{$i18n.t("Standard VIP")}</div>       
              <div class="flex-1 flex flex-row justify-center items-center leading-4">
                <span class="text-xs">{$i18n.t("Valid until")} {standardInfo.end_date}</span>
                {#if checkProLoading}
                  <svg class="animate-spin ml-2"
                    xmlns="http://www.w3.org/2000/svg"
                    width="1em"
                    height="1em"
                    viewBox="0 0 24 24">
                    <path fill="#ffffff"
                      d="M12 20q-3.35 0-5.675-2.325T4 12t2.325-5.675T12 4q1.725 0 3.3.712T18 6.75V4h2v7h-7V9h4.2q-.8-1.4-2.187-2.2T12 6Q9.5 6 7.75 7.75T6 12t1.75 4.25T12 18q1.925 0 3.475-1.1T17.65 14h2.1q-.7 2.65-2.85 4.325T12 20"/>
                  </svg>
                {/if}
              </div>
            </div>
          {:else}
            <div class="flex flex-col mt-4">
              <div class="flex flex-row justify-start mb-2 ml-1">
                <div class="flex flex-row flex-wrap">
                  <span class="text-sm tracking-tight primaryText font-bold mr-1">$88 / {$i18n.t("Year")} ({$i18n.t("Instant Savings")} 8%)</span>
                  <span class="text-sm tracking-tight font-bold primaryText mr-2">(={divideAndRound(88, $dgcRate.rate)}DGC)</span>
                </div>
                <div class="flex-1 flex justify-start pt-1">
                  <Switch bind:state={standardstat}/>
                </div>
              </div>
              <button
                on:click={() => {
                  if ($user?.id?.startsWith("0x")) {
                    viptype = "standard";
                    viptime = standardstat ? "year" : "month";
                    money = standardstat ? 88 : 8;
                    openUpgradeModel();
                  } else {
                    toast.warning($i18n.t("Please create or log in to your wallet first."))
                  }
                }}
                aria-describedby="tier-plus"
                class="px-4 py-2 primaryButton text-gray-100 text-sm transition rounded-lg w-full flex flex-row justify-center items-center"
                disabled = { checkProLoading }
              >
                {$i18n.t("Upgrade to VIP")}
                {#if checkProLoading}
                  <svg class="animate-spin ml-2"
                    xmlns="http://www.w3.org/2000/svg"
                    width="1em"
                    height="1em"
                    viewBox="0 0 24 24">
                      <path fill="#ffffff"
                        d="M12 20q-3.35 0-5.675-2.325T4 12t2.325-5.675T12 4q1.725 0 3.3.712T18 6.75V4h2v7h-7V9h4.2q-.8-1.4-2.187-2.2T12 6Q9.5 6 7.75 7.75T6 12t1.75 4.25T12 18q1.925 0 3.475-1.1T17.65 14h2.1q-.7 2.65-2.85 4.325T12 20"/>
                  </svg>
                {/if}
              </button>
            </div>
          {/if}

          <ul
            role="list"
            class="mt-8 space-y-3 text-sm leading-6 xl:mt-10 font-bold text-gray-600 dark:text-gray-300"
          >
            <li class="flex gap-x-3">
              <svg
                class="h-6 w-5 flex-none primaryText"
                viewBox="0 0 20 20"
                fill="currentColor"
                aria-hidden="true"
              >
                <path
                  fill-rule="evenodd"
                  d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z"
                  clip-rule="evenodd"
                />
              </svg>
              {$i18n.t("Basic Model: {{ num }} Times/Month", {num: "5,000"})}
              {#if isLoaded}
                {@html checkUse("base", "standard")}
              {/if}
            </li>
            <li class="flex gap-x-3">
              <svg
                class="h-6 w-5 flex-none primaryText"
                viewBox="0 0 20 20"
                fill="currentColor"
                aria-hidden="true"
              >
                <path
                  fill-rule="evenodd"
                  d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z"
                  clip-rule="evenodd"
                />
              </svg>
              {$i18n.t("Premium Model: {{ num }} Times/Month", {num: 300})}
              {#if isLoaded}
                {@html checkUse("adv", "standard")}
              {/if}
            </li>
            <li class="flex gap-x-3">
              <svg
                class="h-6 w-5 flex-none primaryText"
                viewBox="0 0 20 20"
                fill="currentColor"
                aria-hidden="true"
              >
                <path
                  fill-rule="evenodd"
                  d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z"
                  clip-rule="evenodd"
                />
              </svg>
              {$i18n.t("Top-tier Model: {{ num }} Times/Month", {num: 100})}
              {#if isLoaded}
                {@html checkUse("top", "standard")}
              {/if}
            </li>

            <li class="flex gap-x-3">
              <svg
                class="h-6 w-5 flex-none primaryText"
                viewBox="0 0 20 20"
                fill="currentColor"
                aria-hidden="true"
              >
                <path
                  fill-rule="evenodd"
                  d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z"
                  clip-rule="evenodd"
                />
              </svg>
              {$i18n.t("All models share memory with each other.")}
            </li>
            <li class="flex gap-x-3">
              <svg
                class="h-6 w-5 flex-none primaryText"
                viewBox="0 0 20 20"
                fill="currentColor"
                aria-hidden="true"
              >
                <path
                  fill-rule="evenodd"
                  d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z"
                  clip-rule="evenodd"
                />
              </svg>
              {$i18n.t("Extended access rights for message, image understanding, advanced data analysis, and web browsing")}
            </li>
            <li class="flex gap-x-3">
              <svg
                class="h-6 w-5 flex-none primaryText"
                viewBox="0 0 20 20"
                fill="currentColor"
                aria-hidden="true"
              >
                <path
                  fill-rule="evenodd"
                  d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z"
                  clip-rule="evenodd"
                />
              </svg>
              <div>
                {$i18n.t("Accessible Foundation Model")}
                <div>
                  <div class="flex flex-row items-center mt-2">
                    <img class="w-[22px]" src="/static/icon/deepseek.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">DeepSeek V3.2</span>
                  </div>
                  <div class="flex flex-row items-center mt-2">
                    <img class="w-[22px]" src="/static/icon/doubao.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">DouBao 1.6 (TikTok)</span>
                  </div>
                  <div class="flex flex-row items-center mt-2">
                    <img class="w-[22px]" src="/static/icon/qwen.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">Qwen3 Max (Ali Cloud)</span>
                  </div>
                  <div class="flex flex-row items-center mt-2">
                    <img class="w-[22px]" src="/static/icon/qwen.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">Qwen3 Thinking (Ali Cloud)</span>
                  </div>
                  <div class="flex flex-row items-center mt-2">
                    <img class="w-[24px]" src="/static/icon/gpt3.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">GPT-5 mini (OpenAI)</span>
                  </div>
              </div>
            </li>
            <li class="flex gap-x-3">
              <svg
                class="h-6 w-5 flex-none primaryText"
                viewBox="0 0 20 20"
                fill="currentColor"
                aria-hidden="true"
              >
                <path
                  fill-rule="evenodd"
                  d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z"
                  clip-rule="evenodd"
                />
              </svg>
              <div>
                {$i18n.t("Accessible Advanced Model")}
                <div>
                  <div class="flex flex-row items-center mt-2">
                    <img class="w-[22px]" src="/static/icon/gpt_round.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">GPT-4o audio (OpenAI)</span>
                  </div>
                  <div class="flex flex-row items-center mt-2">
                    <img class="w-[22px]" src="/static/icon/deepseek.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">DeepSeek R1</span>
                  </div>
                  <div class="flex flex-row items-center mt-2">
                    <img class="w-[22px]" src="/static/icon/gemini.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">Gemini 2.5 Flash (Google)</span>
                  </div>
                  <div class="flex flex-row items-center mt-2">
                    <img class="w-[22px]" src="/static/icon/grok.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">Grok 3 (Elon Musk)</span>
                  </div>
                  <div class="flex flex-row items-center mt-2">
                    <img class="w-[22px]" src="/static/icon/doubao.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">DouBao 1.6 Thinking (TikTok)</span>
                  </div>
              </div>
            </li>
            <li class="flex gap-x-3">
              <svg
                class="h-6 w-5 flex-none primaryText"
                viewBox="0 0 20 20"
                fill="currentColor"
                aria-hidden="true"
              >
                <path
                  fill-rule="evenodd"
                  d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z"
                  clip-rule="evenodd"
                />
              </svg>
              <div>
                {$i18n.t("Accessible Top-Level Model")}
                <div>
                  <div class="flex flex-row items-center mt-2">
                    <img class="w-[22px]" src="/static/icon/gpt_round.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">GPT-5 (OpenAI)</span>
                  </div>
                  <div class="flex flex-row items-center mt-2">
                    <img class="w-[22px]" src="/static/icon/claude.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">Claude 4.5 Sonnet (Anthropic)</span>
                  </div>
                  <div class="flex flex-row items-center mt-2">
                    <img class="w-[22px]" src="/static/icon/claude.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">Claude 4.5 Sonnet Thinking (Anthropic)</span>
                  </div>
                  <div class="flex flex-row items-center mt-2">
                    <img class="w-[22px]" src="/static/icon/grok.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">Grok 3 Thinking (Elon Musk)</span>
                  </div>
                  <div class="flex flex-row items-center mt-2">
                    <img class="w-[22px]" src="/static/icon/gemini.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">Gemini 2.5 Pro (Google)</span>
                  </div>
              </div>
            </li>
            <li class="flex gap-x-3">
              <svg
                class="h-6 w-5 flex-none primaryText"
                viewBox="0 0 20 20"
                fill="currentColor"
                aria-hidden="true"
              >
                <path
                  fill-rule="evenodd"
                  d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z"
                  clip-rule="evenodd"
                />
              </svg>
              {$i18n.t("Access on web, iOS, Android")}
            </li>
          </ul>
        </div>
        <div class="rounded-3xl p-4 ring-1 min-w-[337px] max-w-[376px] ring-gray-200 m-4">
          <h3 id="tier-plus" class="text-lg font-semibold leading-8 text-center">
            {$i18n.t("Pro VIP")}
          </h3>
          <div class="mt-2 flex flex-col justify-center items-center gap-x-1">
            <div>
              <span class="text-4xl font-bold tracking-tight">$15</span>
              <span class="text-xl tracking-tight"> / {$i18n.t("Month")}</span>
              <span class="text-sm">(={divideAndRound(15, $dgcRate.rate)}DGC)</span>
            </div>
          </div>
          {#if proInfo}
            <div
              class="flex flex-col mt-6 px-1 py-1.5 primaryButton text-gray-100 text-sm transition rounded-lg w-full"
            >
              <div class="text-white text-center text-xs font-bold leading-5">{$i18n.t("Pro VIP")}</div>       
              <div class="flex-1 flex flex-row justify-center items-center leading-4">
                <span class="text-xs">{$i18n.t("Valid until")} {proInfo.end_date}</span>
                {#if checkProLoading}
                  <svg class="animate-spin ml-2"
                    xmlns="http://www.w3.org/2000/svg"
                    width="1em"
                    height="1em"
                    viewBox="0 0 24 24">
                    <path fill="#ffffff"
                      d="M12 20q-3.35 0-5.675-2.325T4 12t2.325-5.675T12 4q1.725 0 3.3.712T18 6.75V4h2v7h-7V9h4.2q-.8-1.4-2.187-2.2T12 6Q9.5 6 7.75 7.75T6 12t1.75 4.25T12 18q1.925 0 3.475-1.1T17.65 14h2.1q-.7 2.65-2.85 4.325T12 20"/>
                  </svg>
                {/if}
              </div>
            </div>
          {:else}
            <div class="flex flex-col mt-4">
              <div class="flex flex-row justify-start mb-2 ml-1">
                <div class="flex flex-row flex-wrap">
                  <span class="text-sm tracking-tight primaryText font-bold mr-1">$165 / {$i18n.t("Year")} ({$i18n.t("Instant Savings")} 9%)</span>
                  <span class="text-sm tracking-tight font-bold primaryText mr-2">(={divideAndRound(165, $dgcRate.rate)}DGC)</span>
                </div>
                <div class="flex-1 flex justify-start pt-1">
                  <Switch bind:state={prostat}/>
                </div>
              </div>
              <button
                on:click={() => {
                  if ($user?.id?.startsWith("0x")) {
                    viptype = "pro";
                    viptime = prostat ? "year" : "month";
                    money = prostat ? 165 : 15;
                    openUpgradeModel();
                  } else {
                    toast.warning($i18n.t("Please create or log in to your wallet first."))
                  }
                }}
                aria-describedby="tier-plus"
                class="px-4 py-2 primaryButton text-gray-100 text-sm transition rounded-lg w-full flex flex-row justify-center items-center"
                disabled = { checkProLoading }
              >
                {$i18n.t("Upgrade to VIP")}
                {#if checkProLoading}
                  <svg class="animate-spin ml-2"
                    xmlns="http://www.w3.org/2000/svg"
                    width="1em"
                    height="1em"
                    viewBox="0 0 24 24">
                      <path fill="#ffffff"
                        d="M12 20q-3.35 0-5.675-2.325T4 12t2.325-5.675T12 4q1.725 0 3.3.712T18 6.75V4h2v7h-7V9h4.2q-.8-1.4-2.187-2.2T12 6Q9.5 6 7.75 7.75T6 12t1.75 4.25T12 18q1.925 0 3.475-1.1T17.65 14h2.1q-.7 2.65-2.85 4.325T12 20"/>
                  </svg>
                {/if}
              </button>
            </div>
          {/if}

          <ul
            role="list"
            class="mt-8 space-y-3 text-sm leading-6 xl:mt-10 font-bold text-gray-600 dark:text-gray-300"
          >
            <li class="flex gap-x-3">
              <svg
                class="h-6 w-5 flex-none primaryText"
                viewBox="0 0 20 20"
                fill="currentColor"
                aria-hidden="true"
              >
                <path
                  fill-rule="evenodd"
                  d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z"
                  clip-rule="evenodd"
                />
              </svg>
              {$i18n.t("Basic Model: {{ num }} Times/Month", {num: "10,000"})}
              {#if isLoaded}
                {@html checkUse("base", "pro")}
              {/if}
            </li>
            <li class="flex gap-x-3">
              <svg
                class="h-6 w-5 flex-none primaryText"
                viewBox="0 0 20 20"
                fill="currentColor"
                aria-hidden="true"
              >
                <path
                  fill-rule="evenodd"
                  d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z"
                  clip-rule="evenodd"
                />
              </svg>
              {$i18n.t("Premium Model: {{ num }} Times/Month", {num: "5,000"})}
              {#if isLoaded}
                {@html checkUse("adv", "pro")}
              {/if}
            </li>
            <li class="flex gap-x-3">
              <svg
                class="h-6 w-5 flex-none primaryText"
                viewBox="0 0 20 20"
                fill="currentColor"
                aria-hidden="true"
              >
                <path
                  fill-rule="evenodd"
                  d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z"
                  clip-rule="evenodd"
                />
              </svg>
              {$i18n.t("Top-tier Model: {{ num }} Times/Month", {num: 250})}
              {#if isLoaded}
                {@html checkUse("top", "pro")}
              {/if}
            </li>

            <li class="flex gap-x-3">
              <svg
                class="h-6 w-5 flex-none primaryText"
                viewBox="0 0 20 20"
                fill="currentColor"
                aria-hidden="true"
              >
                <path
                  fill-rule="evenodd"
                  d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z"
                  clip-rule="evenodd"
                />
              </svg>
              {$i18n.t("All models share memory with each other.")}
            </li>
            <li class="flex gap-x-3">
              <svg
                class="h-6 w-5 flex-none primaryText"
                viewBox="0 0 20 20"
                fill="currentColor"
                aria-hidden="true"
              >
                <path
                  fill-rule="evenodd"
                  d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z"
                  clip-rule="evenodd"
                />
              </svg>
              {$i18n.t("Extended access rights for message, image understanding, advanced data analysis, and web browsing")}
            </li>
            <li class="flex gap-x-3">
              <svg
                class="h-6 w-5 flex-none primaryText"
                viewBox="0 0 20 20"
                fill="currentColor"
                aria-hidden="true"
              >
                <path
                  fill-rule="evenodd"
                  d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z"
                  clip-rule="evenodd"
                />
              </svg>
              <div>
                {$i18n.t("Accessible Foundation Model")}
                <div>
                  <div class="flex flex-row items-center mt-2">
                    <img class="w-[22px]" src="/static/icon/deepseek.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">DeepSeek V3.2</span>
                  </div>
                  <div class="flex flex-row items-center mt-2">
                    <img class="w-[22px]" src="/static/icon/doubao.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">DouBao 1.6 (TikTok)</span>
                  </div>
                  <div class="flex flex-row items-center mt-2">
                    <img class="w-[22px]" src="/static/icon/qwen.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">Qwen3 Max (Ali Cloud)</span>
                  </div>
                  <div class="flex flex-row items-center mt-2">
                    <img class="w-[22px]" src="/static/icon/qwen.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">Qwen3 Thinking (Ali Cloud)</span>
                  </div>
                  <div class="flex flex-row items-center mt-2">
                    <img class="w-[24px]" src="/static/icon/gpt3.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">GPT-5 mini (OpenAI)</span>
                  </div>
              </div>
            </li>
            <li class="flex gap-x-3">
              <svg
                class="h-6 w-5 flex-none primaryText"
                viewBox="0 0 20 20"
                fill="currentColor"
                aria-hidden="true"
              >
                <path
                  fill-rule="evenodd"
                  d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z"
                  clip-rule="evenodd"
                />
              </svg>
              <div>
                {$i18n.t("Accessible Advanced Model")}
                <div>
                  <div class="flex flex-row items-center mt-2">
                    <img class="w-[22px]" src="/static/icon/gpt_round.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">GPT-4o audio (OpenAI)</span>
                  </div>
                  <div class="flex flex-row items-center mt-2">
                    <img class="w-[22px]" src="/static/icon/deepseek.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">DeepSeek R1</span>
                  </div>
                  <div class="flex flex-row items-center mt-2">
                    <img class="w-[22px]" src="/static/icon/gemini.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">Gemini 2.5 Flash (Google)</span>
                  </div>
                  <div class="flex flex-row items-center mt-2">
                    <img class="w-[22px]" src="/static/icon/grok.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">Grok 3 (Elon Musk)</span>
                  </div>
                  <div class="flex flex-row items-center mt-2">
                    <img class="w-[22px]" src="/static/icon/doubao.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">DouBao 1.6 Thinking (TikTok)</span>
                  </div>
              </div>
            </li>
            <li class="flex gap-x-3">
              <svg
                class="h-6 w-5 flex-none primaryText"
                viewBox="0 0 20 20"
                fill="currentColor"
                aria-hidden="true"
              >
                <path
                  fill-rule="evenodd"
                  d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z"
                  clip-rule="evenodd"
                />
              </svg>
              <div>
                {$i18n.t("Accessible Top-Level Model")}
                <div>
                  <div class="flex flex-row items-center mt-2">
                    <img class="w-[22px]" src="/static/icon/gpt_round.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">GPT-5 (OpenAI)</span>
                  </div>
                  <div class="flex flex-row items-center mt-2">
                    <img class="w-[22px]" src="/static/icon/claude.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">Claude 4.5 Sonnet (Anthropic)</span>
                  </div>
                  <div class="flex flex-row items-center mt-2">
                    <img class="w-[22px]" src="/static/icon/claude.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">Claude 4.5 Sonnet Thinking (Anthropic)</span>
                  </div>
                  <div class="flex flex-row items-center mt-2">
                    <img class="w-[22px]" src="/static/icon/grok.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">Grok 3 Thinking (Elon Musk)</span>
                  </div>
                  <div class="flex flex-row items-center mt-2">
                    <img class="w-[22px]" src="/static/icon/gemini.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">Gemini 2.5 Pro (Google)</span>
                  </div>
              </div>
            </li>
            <li class="flex gap-x-3">
              <svg
                class="h-6 w-5 flex-none primaryText"
                viewBox="0 0 20 20"
                fill="currentColor"
                aria-hidden="true"
              >
                <path
                  fill-rule="evenodd"
                  d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z"
                  clip-rule="evenodd"
                />
              </svg>
              {$i18n.t("Access on web, iOS, Android")}
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</Modal>

<ConfirmUpgradeModal bind:viptype={viptype} bind:viptime={viptime} bind:money={money} bind:rate={$dgcRate.rate} bind:show={$showConfirmUpgradeModal} />

<style>
</style>