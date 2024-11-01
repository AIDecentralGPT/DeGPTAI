<script lang="ts">
  import { getContext } from "svelte";

  import Modal from "../common/Modal.svelte";

  const i18n = getContext("i18n");

  export let show = false;

  let coinType = "DBC";
</script>

<Modal bind:show>
  <div class="text-gray-700 dark:text-gray-100 px-5 pt-4 pb-4">
    <!-- <h2 class="text-2xl font-bold mb-4">Buy Coins</h2> -->

    <div class="flex justify-between dark:text-gray-300">
      <div class="text-lg font-medium self-center">
        {$i18n.t("Purchase Digital Coins")}
      </div>
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

    <p class="mt-4 mb-1" style="color: rgba(184, 142, 86, 1);">
      <strong>{$i18n.t("Note:")}</strong> {$i18n.t("DBC is a type of digital asset. The price is always fluctuating. Please be aware of the risks!")}
    </p>
    

    <!-- --------------- -->
    <!-- 选择购买类型 -->
    <div class="mb-6 pt-0.5 flex justify-start items-center">
      <label class="flex items-center gap-1 mr-4">
        {$i18n.t("Select purchase type")}:
      </label>
      <div class="flex">
        <label class="mr-4 flex items-center cursor-pointer">
          <input
            type="radio"
            bind:group={coinType}
            value="DBC"
            required
            class="mr-1.5 cursor-pointer"
          />
          DBC
        </label>
        <label class="mr-4 flex items-center cursor-pointer">
          <input
            type="radio"
            bind:group={coinType}
            value="DGC"
            required
            class="mr-1.5 cursor-pointer"
            disabled
          />
          DGC
        </label>
      </div>
    </div>

    <!-- 购买BDC -->
    {#if coinType === "DBC"}
      <div class="flex flex-col sm:flex-row sm:justify-between">
        <div
          class="bg-gray-200 dark:bg-gray-700 rounded-md px-4 py-2 text-center mb-4 sm:mb-0 sm:mx-2 flex-1"
        >
          <h3 class="text-xl mb-2">01</h3>
          <p class="mb-4"> {$i18n.t("From Huobi Exchange")}</p>
          <button
            class="my-4 px-4 py-2 dark:bg-white dark:text-zinc-950 bg-black text-gray-100 transition rounded-lg"
            type="submit"
            on:click={() => {
              window.open(
                "https://www.htx.com/trade/dbc_usdt?type=spot",
                "_blank"
              );
            }}
          >
            {$i18n.t("Buy Now")}
          </button>
        </div>
        <div
          class="bg-gray-200 dark:bg-gray-700 rounded-md px-4 py-2 text-center mb-4 sm:mb-0 sm:mx-2 flex-1"
        >
          <h3 class="text-xl mb-2">02</h3>
          <p class="mb-4"> {$i18n.t("From Gate Exchange")}</p>
          <button
            class="my-4 px-4 py-2 dark:bg-white dark:text-zinc-950 bg-black text-gray-100 transition rounded-lg"
            type="submit"
            on:click={() => {
              window.open("https://www.gate.tv/zh/trade/DBC_USDT", "_blank");
            }}
          >
            {$i18n.t("Buy Now")}
          </button>
        </div>
        <div
          class="bg-gray-200 dark:bg-gray-700 rounded-md px-4 py-2 text-center sm:mx-2 flex-1"
        >
          <h3 class="text-xl mb-2">03</h3>
          <p class="mb-4"> {$i18n.t("From Bitmart Exchange")}</p>
          <button
            class="my-4 px-4 py-2 dark:bg-white dark:text-zinc-950 bg-black text-gray-100 transition rounded-lg"
            type="submit"
            on:click={() => {
              window.open(
                "https://www.bitmart.com/trade/en-US?layout=pro&theme=dark&symbol=DBC_USDT",
                "_blank"
              );
            }}
          >
            {$i18n.t("Buy Now")}
          </button>
        </div>
      </div>
    {/if}
    {#if coinType === "DGC"}
      <div class="flex justify-center">
        <button
          class="my-4 px-4 py-2 dark:bg-white dark:text-zinc-950 bg-black text-gray-100 transition rounded-lg"
          type="submit"
          on:click={() => {
            window.open(
              "https://deeplink.cloud/public-sale/",
              "_blank"
            );
          }}
        >
          {$i18n.t("Buy Now")}
        </button>
      </div>
    {/if}
  </div>
</Modal>
