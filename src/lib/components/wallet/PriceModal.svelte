<script lang="ts">
  import { toast } from "svelte-sonner";
  import Modal from "../common/Modal.svelte";
  export let show = false;
  import { onMount, getContext } from "svelte";
  import { transferDgc } from "$lib/utils/wallet/ether/dgc";
  import {
    currentWalletData,
    user,
    showConfirmUpgradeModal,
  } from "$lib/stores";
  import { walletconnectSendDGCTransaction } from "$lib/utils/wallet/walletconnect/index";
  import ConfirmUpgradeModal from "./ConfirmUpgradeModal.svelte";
  import { isPro, openProServices } from "$lib/apis/users/index.js";
  const i18n = getContext("i18n");

  const upgradePrice = 3;

  async function checkPlus() {
    const userPro = await isPro(localStorage.token); // 发送请求到你的 API
    if (userPro) {
      user.set({
        ...$user,
        isPro: userPro.is_pro,
        proEndDate: userPro.end_date
      });
    }
  }

  // 显示初始化Socket
  $: if (show) {
    checkPlus();
  }
</script>

<Modal bind:show size="lg">
  <div class="max-h-[80dvh] xs:h-auto flex flex-col">
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
        class="isolate mx-auto grid max-w-md grid-cols-1 gap-8 lg:mx-0 lg:max-w-none lg:grid-cols-2 h-8/10 md:h-108 overflow-y-auto"
      >
        <div class="rounded-3xl p-8 ring-1 xl:p-10 ring-gray-200 m-4">
          <h3 id="tier-free" class="text-lg font-semibold leading-8">
            {$i18n.t("Free")}
          </h3>
          <p class="mt-6 flex items-baseline gap-x-1">
            <span class="text-4xl font-bold tracking-tight">$0</span>
            <span class="text-sm font-semibold leading-6 text-gray-400"
              >DGC</span
            >
          </p>
          <p class="text-sm leading-6 text-gray-400">
            {$i18n.t("per user, billed monthly")}
          </p>
          <button
            disabled
            class="w-full mt-6 block rounded-md py-2 px-3 text-center text-sm font-semibold leading-6 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 dark:bg-white dark:text-zinc-950 bg-black text-gray-100"
          >
            {$i18n.t("Your Current Plan")}
          </button>
          <ul
            role="list"
            class="mt-8 space-y-3 text-sm leading-6 xl:mt-10 text-gray-400"
          >
            <li class="flex gap-x-3">
              <svg
                class="h-6 w-5 flex-none text-gray-500"
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
              {$i18n.t("Unlimited messages, interactions and history")}
            </li>
            <li class="flex gap-x-3">
              <svg
                class="h-6 w-5 flex-none text-gray-500"
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
                {$i18n.t("Access to ")}
                <span class=" dark:text-gray-100 text-zinc-950"
                  >Llama3.1-405B、Mistral Large2-123B、Qwen2-72B、Gemma2</span
                >
              </div>
            </li>
            <li class="flex gap-x-3">
              <svg
                class="h-6 w-5 flex-none text-gray-500"
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
              {$i18n.t("Regular model updates")}
            </li>
            <li class="flex gap-x-3">
              <svg
                class="h-6 w-5 flex-none text-gray-500"
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
                class="h-6 w-5 flex-none text-gray-500"
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
              {$i18n.t(
                "The usage limit for the model Llama-3.1-405B is 10 times per day, other models is 100 times per day."
              )}
            </li>
          </ul>
        </div>
        <div class="rounded-3xl p-8 ring-1 xl:p-10 ring-gray-200 m-4">
          <h3 id="tier-plus" class="text-lg font-semibold leading-8">
            {$i18n.t("Plus")}
          </h3>
          <p class="mt-6 flex items-baseline gap-x-1">
            <span class="text-4xl font-bold tracking-tight"
              >${upgradePrice}</span
            >
            <span class="text-sm font-semibold leading-6 text-gray-400"
              >DGC</span
            >
          </p>
          <p class="text-sm leading-6 text-gray-400">
            {$i18n.t("per user, billed monthly")}
          </p>
          {#if $user.isPro}
            <div
              class="flex mt-6 px-1 primaryButton text-gray-100 text-sm transition rounded-lg w-full h-[40px]"
            >
              <svg xmlns="http://www.w3.org/2000/svg" 
                t="1728631736809" 
                class="icon" 
                viewBox="0 0 1024 1024" 
                version="1.1" 
                width="20" 
                height="20">
                  <path d="M938.666667 896H85.333333c-46.933333 0-85.333333-38.4-85.333333-85.333333V213.333333c0-46.933333 38.4-85.333333 85.333333-85.333333h853.333334c46.933333 0 85.333333 38.4 85.333333 85.333333v597.333334c0 46.933333-38.4 85.333333-85.333333 85.333333zM106.666667 213.333333c-12.8 0-21.333333 8.533333-21.333334 21.333334v554.666666c0 12.8 8.533333 21.333333 21.333334 21.333334h810.666666c12.8 0 21.333333-8.533333 21.333334-21.333334v-554.666666c0-12.8-8.533333-21.333333-21.333334-21.333334h-810.666666z m554.666666 426.666667V384H810.666667c34.133333 0 64 29.866667 64 64V512c0 34.133333-29.866667 64-64 64h-85.333334V640h-64z m64-119.466667h51.2c17.066667 0 34.133333-12.8 34.133334-34.133333V469.333333c0-17.066667-12.8-34.133333-34.133334-34.133333H725.333333v85.333333zM448 640v-64h34.133333v-128h-34.133333V384h128v64h-34.133333v128h34.133333V640h-128zM213.333333 640L149.333333 384H213.333333l42.666667 192L298.666667 384h64L298.666667 640H213.333333z" fill="#ffffff"></path>
                </svg>
                <div class="flex-1 flex justify-center items-center">
                  Valid until {$user.proEndDate}
                </div>
            </div>
          {:else}
            <button
              on:click={() => {
                // handleUpgrade();
                // toast.warning("Coming soon...");
                $showConfirmUpgradeModal = true;
              }}
              href="#"
              aria-describedby="tier-plus"
              class="mt-6 px-4 py-2 primaryButton text-gray-100 text-sm transition rounded-lg w-full"
            >
              {$i18n.t("Upgrade to Plus")}
            </button>
          {/if}

          <ul
            role="list"
            class="mt-8 space-y-3 text-sm leading-6 xl:mt-10 text-gray-400"
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
              {$i18n.t("Everything in Free")}
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
                {$i18n.t("Access to ")}
                <span class=" dark:text-gray-100 text-zinc-950"
                  >LIama3.1-405B、Mistral Large2-123B、Qwen2-72B、Gemma2</span
                >
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
              {$i18n.t("Regular model updates")}
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
              {$i18n.t(
                "The usage limit for the model Llama-3.1-405B is 1000 times per day, other model is 10000 times per day."
              )}
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</Modal>

<ConfirmUpgradeModal bind:show={$showConfirmUpgradeModal} />

<style>
</style>
