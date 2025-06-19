<script lang="ts">
  import Modal from "../common/Modal.svelte";
  export let show = false;
  import { getContext } from "svelte";
  import {
    user,
    showConfirmUpgradeModal,
    vipupgrade
  } from "$lib/stores";
  import ConfirmUpgradeModal from "./ConfirmUpgradeModal.svelte";
  import { isPro } from "$lib/apis/users/index.js";
    import Switch from "../common/Switch.svelte";
  const i18n = getContext("i18n");

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
    }
  }

  // 显示初始化Socket
  $: if (show) {
    checkProLoading = true;
    checkPlus(); 
  }

  let viptype = "basic";
  let viptime = "month";
  let money = 3;
  let basicstat = false;
  let standardstat = false;
  let prostat = false;
</script>

<Modal bind:show size="lg">
  <div class="max-h-[80vh] xs:h-auto flex flex-col">
    <div class="flex justify-between dark:text-gray-300 px-5 pt-4 pb-2">
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

    <div class="mx-auto max-w-7xl px-6 lg:px-8 flex-1 overflow-auto">
      <div class="mx-auto max-w-4xl text-center">
        <h2 class="font-semibold leading-7 primaryText text-2xl">
          {$i18n.t("Pricing")}
        </h2>
      </div>

      <div
        class="isolate mx-auto grid max-w-md grid-cols-1 gap-8 lg:mx-0 lg:max-w-none lg:grid-cols-2 h-8/10 md:h-108 overflow-y-auto pb-4"
      >
        <div class="rounded-3xl p-8 ring-1 xl:p-10 ring-gray-200 m-4">
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
              {$i18n.t("Current Status")}
            </button>
          </div>
          
          <ul
            role="list"
            class="mt-8 space-y-3 text-sm leading-6 xl:mt-10 font-bold text-gray-600 dark:text-gray-300"
          >
            <li class="flex gap-x-3">
              <svg
                class="h-6 w-5 flex-none"
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
                class="h-6 w-5 flex-none"
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
                    <img class="size-5" src="./icon/deepseek.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">DeepSeek V3</span>
                  </div>
                  <div class="flex flex-row items-center mt-2">
                    <img class="size-5" src="./icon/doubao.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">DouBao-1.5-pro</span>
                  </div>
                  <div class="flex flex-row items-center mt-2">
                    <img class="size-5" src="./icon/qwen.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">Qwen3 235B</span>
                  </div>
                  <div class="flex flex-row items-center mt-2">
                    <img class="size-5" src="./icon/qwen.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">Qwen3 235B Thinking</span>
                  </div>
                </div>
              </div>
            </li>
            <li class="flex gap-x-3">
              <svg
                class="h-6 w-5 flex-none"
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
            <li class="flex gap-x-3">
              <svg
                class="h-6 w-5 flex-none"
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
                <div>{$i18n.t("For users who have not created a wallet, the foundation model: {{ num }} times/day", {num: 3})}</div>
                <div>{$i18n.t("For users who have created a wallet, the foundation model: {{ num }} times/day", {num: 5})}</div>
                <div>{$i18n.t("For users who have completed KYC, the foundation model: {{ num }} times/day", {num: 10})}</div>
              </div>
            </li>
          </ul>
        </div>
        <div class="rounded-3xl p-8 ring-1 xl:p-10 ring-gray-200 m-4">
          <h3 id="tier-plus" class="text-lg font-semibold leading-8 text-center">
            {$i18n.t("Basic Vip")}
          </h3>
          <div class="mt-2 flex flex-col justify-center items-center gap-x-1">
            <div>
              <span class="text-4xl font-bold tracking-tight">$3</span>
              <span class="text-xl tracking-tight"> / {$i18n.t("Month")}</span>
              <span class="text-sm">(={3/0.00006}DGC)</span>
            </div>
          </div>
          {#if basicInfo}
            <div
              class="flex flex-col mt-6 px-1 py-1.5 primaryButton text-gray-100 text-sm transition rounded-lg w-full"
            >
              <div class="text-white text-center text-base leading-5">{$i18n.t("Basic Vip")}</div>       
              <div class="flex-1 flex flex-row justify-center items-center leading-4">
                {$i18n.t("Valid until")} { basicInfo.end_date}
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
              <div class="flex flex-row items-center mb-2 ml-1">
                <span class="text-sm tracking-tight primaryText font-bold mr-2">$33 / {$i18n.t("Year")} ({$i18n.t("Instant Savings")} 8%)</span>
                <Switch bind:state={basicstat}/>
              </div>
              <button
                on:click={() => {
                  viptype = "basic";
                  viptime = basicstat ? "year" : "month";
                  money = basicstat ? 33 : 3;
                  $showConfirmUpgradeModal = true;
                }}
                aria-describedby="tier-plus"
                class="px-4 py-2 primaryButton text-gray-100 text-sm transition rounded-lg w-full flex flex-row justify-center items-center"
                disabled = { checkProLoading }
              >
                {$i18n.t("Upgrade to Vip")}
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
                    <img class="size-5" src="./icon/deepseek.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">DeepSeek V3</span>
                  </div>
                  <div class="flex flex-row items-center mt-2">
                    <img class="size-5" src="./icon/doubao.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">DouBao-1.5-pro</span>
                  </div>
                  <div class="flex flex-row items-center mt-2">
                    <img class="size-5" src="./icon/qwen.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">Qwen3 235B</span>
                  </div>
                  <div class="flex flex-row items-center mt-2">
                    <img class="size-5" src="./icon/qwen.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">Qwen3 235B Thinking</span>
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
                    <img class="size-5" src="./icon/grok.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">Grok 3</span>
                  </div>
                  <div class="flex flex-row items-center mt-2">
                    <img class="size-5" src="./icon/gemini.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">Gemini 2.5 Flash</span>
                  </div>
                  <div class="flex flex-row items-center mt-2">
                    <img class="size-5" src="./icon/gpt_round.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">GPT-4.1</span>
                  </div>
                  <div class="flex flex-row items-center mt-2">
                    <img class="size-5" src="./icon/gemini.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">Gemini 2.5 Pro</span>
                  </div>
                  <div class="flex flex-row items-center mt-2">
                    <img class="size-5" src="./icon/claude.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">Claude 3.7 Sonnet</span>
                  </div>
                  <div class="flex flex-row items-center mt-2">
                    <img class="size-5" src="./icon/deepseek.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">DeepSeek R1</span>
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
                    <img class="size-5" src="./icon/claude.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">Claude 4 Sonnet</span>
                  </div>
                  <div class="flex flex-row items-center mt-2">
                    <img class="size-5" src="./icon/claude.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">Claude 4 Opus</span>
                  </div>
                  <div class="flex flex-row items-center mt-2">
                    <img class="size-5" src="./icon/claude.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">Claude 4 Opus Thinking</span>
                  </div>
                  <div class="flex flex-row items-center mt-2">
                    <img class="size-5" src="./icon/claude.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">Claude 4 Sonnet Thinking</span>
                  </div>
                  <div class="flex flex-row items-center mt-2">
                    <img class="size-6" src="./icon/gpt3.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">GPT o3</span>
                  </div>
                  <div class="flex flex-row items-center mt-2">
                    <img class="size-5" src="./icon/gpt_round.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">GPT o4-mini</span>
                  </div>
                  <div class="flex flex-row items-center mt-2">
                    <img class="size-5" src="./icon/gpt_round.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">GPT o4-mini high</span>
                  </div>
                  <div class="flex flex-row items-center mt-2">
                    <img class="size-5" src="./icon/gpt_round.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">GPT 4.5</span>
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
            </li>
          </ul>
        </div>
        <div class="rounded-3xl p-8 ring-1 xl:p-10 ring-gray-200 m-4">
          <h3 id="tier-plus" class="text-lg font-semibold leading-8 text-center">
            {$i18n.t("Standard Vip")}
          </h3>
          <div class="mt-2 flex flex-col justify-center items-center gap-x-1">
            <div>
              <span class="text-4xl font-bold tracking-tight">$8</span>
              <span class="text-xl tracking-tight"> / {$i18n.t("Month")}</span>
              <span class="text-sm">(={Math.round(8/0.00006)}DGC)</span>
            </div>
          </div>
          {#if standardInfo}
            <div
              class="flex flex-col mt-6 px-1 py-1.5 primaryButton text-gray-100 text-sm transition rounded-lg w-full"
            >
              <div class="text-white text-center text-base leading-5">{$i18n.t("Standard Vip")}</div>       
              <div class="flex-1 flex flex-row justify-center items-center leading-4">
                {$i18n.t("Valid until")} {standardInfo.end_date}
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
              <div class="flex flex-row items-center mb-2 ml-1">
                <span class="text-sm tracking-tight primaryText font-bold mr-2">$88 / {$i18n.t("Year")} ({$i18n.t("Instant Savings")} 8%)</span>
                <Switch bind:state={standardstat}/>
              </div>
              <button
                on:click={() => {
                  viptype = "standard";
                  viptime = standardstat ? "year" : "month";
                  money = standardstat ? 88 : 8;
                  $showConfirmUpgradeModal = true;
                }}
                aria-describedby="tier-plus"
                class="px-4 py-2 primaryButton text-gray-100 text-sm transition rounded-lg w-full flex flex-row justify-center items-center"
                disabled = { checkProLoading }
              >
                {$i18n.t("Upgrade to Vip")}
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
                    <img class="size-5" src="./icon/deepseek.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">DeepSeek V3</span>
                  </div>
                  <div class="flex flex-row items-center mt-2">
                    <img class="size-5" src="./icon/doubao.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">DouBao-1.5-pro</span>
                  </div>
                  <div class="flex flex-row items-center mt-2">
                    <img class="size-5" src="./icon/qwen.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">Qwen3 235B</span>
                  </div>
                  <div class="flex flex-row items-center mt-2">
                    <img class="size-5" src="./icon/qwen.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">Qwen3 235B Thinking</span>
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
                    <img class="size-5" src="./icon/grok.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">Grok 3</span>
                  </div>
                  <div class="flex flex-row items-center mt-2">
                    <img class="size-5" src="./icon/gemini.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">Gemini 2.5 Flash</span>
                  </div>
                  <div class="flex flex-row items-center mt-2">
                    <img class="size-5" src="./icon/gpt_round.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">GPT-4.1</span>
                  </div>
                  <div class="flex flex-row items-center mt-2">
                    <img class="size-5" src="./icon/gemini.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">Gemini 2.5 Pro</span>
                  </div>
                  <div class="flex flex-row items-center mt-2">
                    <img class="size-5" src="./icon/claude.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">Claude 3.7 Sonnet</span>
                  </div>
                  <div class="flex flex-row items-center mt-2">
                    <img class="size-5" src="./icon/deepseek.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">DeepSeek R1</span>
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
                    <img class="size-5" src="./icon/claude.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">Claude 4 Sonnet</span>
                  </div>
                  <div class="flex flex-row items-center mt-2">
                    <img class="size-5" src="./icon/claude.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">Claude 4 Opus</span>
                  </div>
                  <div class="flex flex-row items-center mt-2">
                    <img class="size-5" src="./icon/claude.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">Claude 4 Opus Thinking</span>
                  </div>
                  <div class="flex flex-row items-center mt-2">
                    <img class="size-5" src="./icon/claude.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">Claude 4 Sonnet Thinking</span>
                  </div>
                  <div class="flex flex-row items-center mt-2">
                    <img class="size-6" src="./icon/gpt3.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">GPT o3</span>
                  </div>
                  <div class="flex flex-row items-center mt-2">
                    <img class="size-5" src="./icon/gpt_round.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">GPT o4-mini</span>
                  </div>
                  <div class="flex flex-row items-center mt-2">
                    <img class="size-5" src="./icon/gpt_round.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">GPT o4-mini high</span>
                  </div>
                  <div class="flex flex-row items-center mt-2">
                    <img class="size-5" src="./icon/gpt_round.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">GPT 4.5</span>
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
            </li>
          </ul>
        </div>
        <div class="rounded-3xl p-8 ring-1 xl:p-10 ring-gray-200 m-4">
          <h3 id="tier-plus" class="text-lg font-semibold leading-8 text-center">
            {$i18n.t("Pro Vip")}
          </h3>
          <div class="mt-2 flex flex-col justify-center items-center gap-x-1">
            <div>
              <span class="text-4xl font-bold tracking-tight">$15</span>
              <span class="text-xl tracking-tight"> / {$i18n.t("Month")}</span>
              <span class="text-sm">(={15/0.00006}DGC)</span>
            </div>
          </div>
          {#if proInfo}
            <div
              class="flex flex-col mt-6 px-1 py-1.5 primaryButton text-gray-100 text-sm transition rounded-lg w-full"
            >
              <div class="text-white text-center text-base leading-5">{$i18n.t("Pro Vip")}</div>       
              <div class="flex-1 flex flex-row justify-center items-center leading-4">
                {$i18n.t("Valid until")} {proInfo.end_date}
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
              <div class="flex flex-row items-center mb-2 ml-1">
                <span class="text-sm tracking-tight primaryText font-bold mr-2">$165 / {$i18n.t("Year")} ({$i18n.t("Instant Savings")} 9%)</span>
                <Switch bind:state={prostat}/>
              </div>
              <button
                on:click={() => {
                  viptype = "pro";
                  viptime = prostat ? "year" : "month";
                  money = prostat ? 165 : 15;
                  $showConfirmUpgradeModal = true;
                }}
                aria-describedby="tier-plus"
                class="px-4 py-2 primaryButton text-gray-100 text-sm transition rounded-lg w-full flex flex-row justify-center items-center"
                disabled = { checkProLoading }
              >
                {$i18n.t("Upgrade to Vip")}
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
                    <img class="size-5" src="./icon/deepseek.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">DeepSeek V3</span>
                  </div>
                  <div class="flex flex-row items-center mt-2">
                    <img class="size-5" src="./icon/doubao.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">DouBao-1.5-pro</span>
                  </div>
                  <div class="flex flex-row items-center mt-2">
                    <img class="size-5" src="./icon/qwen.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">Qwen3 235B</span>
                  </div>
                  <div class="flex flex-row items-center mt-2">
                    <img class="size-5" src="./icon/qwen.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">Qwen3 235B Thinking</span>
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
                    <img class="size-5" src="./icon/grok.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">Grok 3</span>
                  </div>
                  <div class="flex flex-row items-center mt-2">
                    <img class="size-5" src="./icon/gemini.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">Gemini 2.5 Flash</span>
                  </div>
                  <div class="flex flex-row items-center mt-2">
                    <img class="size-5" src="./icon/gpt_round.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">GPT-4.1</span>
                  </div>
                  <div class="flex flex-row items-center mt-2">
                    <img class="size-5" src="./icon/gemini.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">Gemini 2.5 Pro</span>
                  </div>
                  <div class="flex flex-row items-center mt-2">
                    <img class="size-5" src="./icon/claude.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">Claude 3.7 Sonnet</span>
                  </div>
                  <div class="flex flex-row items-center mt-2">
                    <img class="size-5" src="./icon/deepseek.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">DeepSeek R1</span>
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
                    <img class="size-5" src="./icon/claude.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">Claude 4 Sonnet</span>
                  </div>
                  <div class="flex flex-row items-center mt-2">
                    <img class="size-5" src="./icon/claude.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">Claude 4 Opus</span>
                  </div>
                  <div class="flex flex-row items-center mt-2">
                    <img class="size-5" src="./icon/claude.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">Claude 4 Opus Thinking</span>
                  </div>
                  <div class="flex flex-row items-center mt-2">
                    <img class="size-5" src="./icon/claude.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">Claude 4 Sonnet Thinking</span>
                  </div>
                  <div class="flex flex-row items-center mt-2">
                    <img class="size-6" src="./icon/gpt3.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">GPT o3</span>
                  </div>
                  <div class="flex flex-row items-center mt-2">
                    <img class="size-5" src="./icon/gpt_round.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">GPT o4-mini</span>
                  </div>
                  <div class="flex flex-row items-center mt-2">
                    <img class="size-5" src="./icon/gpt_round.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">GPT o4-mini high</span>
                  </div>
                  <div class="flex flex-row items-center mt-2">
                    <img class="size-5" src="./icon/gpt_round.png" alt="icon"/>
                    <span class="text-base font-bold ml-2">GPT 4.5</span>
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
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</Modal>

<ConfirmUpgradeModal bind:viptype={viptype} bind:viptime={viptime} bind:money={money} bind:show={$showConfirmUpgradeModal} />

<style>
</style>
