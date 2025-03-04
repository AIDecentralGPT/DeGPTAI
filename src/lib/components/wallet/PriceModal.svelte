<script lang="ts">
  import Modal from "../common/Modal.svelte";
  export let show = false;
  import { getContext } from "svelte";
  import {
    user,
    showConfirmUpgradeModal,
  } from "$lib/stores";
  import ConfirmUpgradeModal from "./ConfirmUpgradeModal.svelte";
  import { isPro } from "$lib/apis/users/index.js";
  const i18n = getContext("i18n");

  const upgradePrice = 3;

  let checkProLoading = true;
  function checkPlus() {
    isPro(localStorage.token).then(result => {
      if (result) {
        user.set({
          ...$user,
          isPro: result.is_pro,
          proEndDate: result.end_date
        });
      } else{
        user.set({
          ...$user,
          isPro: false,
          proEndDate: ""
        });
      }
      checkProLoading = false;
    }).catch(() => {
      checkProLoading = false;
    });    
  }

  // Initialize Socket
  $: if (show) {
    checkProLoading = true;
    checkPlus(); 
  }
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
        class="isolate mx-auto grid max-w-md grid-cols-1 gap-8 lg:mx-0 lg:max-w-none lg:grid-cols-2 h-8/10 md:h-108 overflow-y-auto"
      >
        <div class="rounded-3xl p-8 ring-1 xl:p-10 ring-gray-200 m-4">
          <h3 id="tier-free" class="text-lg font-semibold leading-8">
            {$i18n.t("Free")}
          </h3>
          <p class="mt-6 flex items-baseline gap-x-1">
            <span class="text-4xl font-bold tracking-tight">$0</span>
            <span class="text-sm font-semibold leading-6 text-gray-400"
              >(0DGC)</span
            >
          </p>
          <p class="text-sm leading-6 text-gray-400">
            {$i18n.t("per user, billed monthly")}
          </p>
          <button
            disabled
            class="w-full mt-6 block rounded-md py-2 px-3 text-center text-sm font-semibold leading-6 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 dark:bg-white dark:text-zinc-950 bg-black text-gray-100"
          >
            {$i18n.t("Your Basic Plan")}
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
              {$i18n.t("Extended access rights for message, image understanding, advanced data analysis, and web browsing")}
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
                  >Llmma 3.3, Pixtral Large 1.0, DeepSeek 3.0, Qwen o1</span
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
              {$i18n.t("For users who have created a wallet, the daily limit is 50 times. For users who have not created a wallet, the daily limit is 5 times.")}
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
              >(6000DGC)</span
            >
          </p>
          <p class="text-sm leading-6 text-gray-400">
            {$i18n.t("per user, billed monthly")}
          </p>
          {#if $user.isPro}
            <div
              class="flex flex-col mt-6 px-1 py-1.5 primaryButton text-gray-100 text-sm transition rounded-lg w-full"
            >
              <div class="text-white text-center text-base leading-5">VIP</div>       
              <div class="flex-1 flex flex-row justify-center items-center leading-4">
                {$i18n.t("Valid until")} {$user.proEndDate}
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
            <button
              on:click={() => {
                $showConfirmUpgradeModal = true;
              }}
              aria-describedby="tier-plus"
              class="mt-6 px-4 py-2 primaryButton text-gray-100 text-sm transition rounded-lg w-full flex flex-row justify-center items-center"
              disabled = { checkProLoading }
            >
              {$i18n.t("Upgrade to Plus")}
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
                {$i18n.t("Access to ")}
                <span class=" dark:text-gray-100 text-zinc-950"
                  >Llmma 3.3, Pixtral Large 1.0, DeepSeek 3.0, Qwen o1</span
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
              {$i18n.t("For o1 and other models, the daily limit is 1000 times.")}
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
