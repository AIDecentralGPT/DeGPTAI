<script lang="ts">
  import Modal from "../common/Modal.svelte";
  export let show = false;
  import { getContext } from "svelte";
  import { showCoinIntruType } from "$lib/stores";
  import { copyToClipboard } from "$lib/utils";
  import { toast } from "svelte-sonner";
  const i18n = getContext("i18n");

  let coinIntrus = [
    {
      title: "About DGC",
      wallet_tip: "Instructions for importing private keys into wallets",
      wallet_inst:"The private keys of wallets created on the website can be imported into the following wallets, such as Metamask, imToken...",
      imp_tip: "Steps for importing wallets",
      imp_step: {
        step1: {
          tip: "Click on [Add Custom Network]",
        },
        step2: {
          tip: "Enter the following information",
          list: [
            { tip: "Network Name", info: "DeepBrain Chain Mainnet" },
            { tip: "Chain RPC Address", info: "https://rpc1.dbcwallet.io" },
            { tip: "Chain ID", info: "19880818" },
            { tip: "Coin Symbol", info: "DBC" },
          ],
        },
        step3: {
          tip: "The contract address of DGC",
          info: "0x8E5e4a4d8aE3741DA073303e492B73cb913fb72D",
        },
      },
      inst: "Instructions",
      desc: "Before the mainnet launch on any trading platform, DGC tokens are designated as points. When DGC is officially launched, these points will be converted at a predetermined ratio. The DGC team will ensure a smooth conversion process and prevent any misuse of this policy.",
      help: "If the problem remains unresolved, please join the Telegram group and follow us on X",
    },
    {
      title: "About DBC",
      description: "DeepBrainChain is the world's first AI public chain. Its native token, DBC, is used as gas fee in this project. Any DGC transactions requires a certain amount of nominal DBCs.",
    },
  ];
</script>

<Modal bind:show size={$showCoinIntruType === "dgc" ? "md" : "sm"}>
  <div class="flex flex-col overflow-y-auto w-full max-h-[80vh]">
    <div class="p-6 pt-0 shadow-md mt-0 flex-1">
      <div class="flex flex-col item-center pt-5">
        {#if $showCoinIntruType === "dgc"}
          <h1 class="text-color text-center font-bold">{$i18n.t(coinIntrus[0].title)}</h1>
          <p class="text-color text-base font-bold">
            1. {$i18n.t(coinIntrus[0].wallet_tip)}：
          </p>
          <div class="text-color text-base">
            {$i18n.t(coinIntrus[0].wallet_inst)}
          </div>
          <p class="text-color text-base font-bold mt-2">
            2. {$i18n.t(coinIntrus[0].imp_tip)}：
          </p>
          <div>
            <div class="text-color text-base">
              ① {$i18n.t(coinIntrus[0].imp_step.step1.tip)}
            </div>
            <div class="text-color text-base">
              ② {$i18n.t(coinIntrus[0].imp_step.step2.tip)}：
            </div>
            <div class="ml-4">
              {#each coinIntrus[0].imp_step.step2.list as item, index}
                <div class="flex">
                  <div class="size-4 min-w-4 mt-1.5 mr-2 bg-color rounded-full text-gray-50 text-xs font-bold text-center">{index + 1}</div>
                  <div>
                    <span class="text-color text-base break-all">{$i18n.t(item.tip)}：{ item.info }</span>
                    <button
                      on:click={async () => {
                        const res = await copyToClipboard(item.info, false);
                        if (res) {
                          toast.success(
                            $i18n.t("Copying to clipboard was successful!")
                          );
                        }
                      }}
                      type="button"
                      class="px-3 py-2 leading-3 text-color rounded-md text-xs"
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
                  </div>
                </div>
              {/each}
            </div>
            <div class="text-color text-base">
              ③ {$i18n.t(coinIntrus[0].imp_step.step3.tip)}
            </div>
            <div class="text-color text-base">
              {$i18n.t(coinIntrus[0].imp_step.step3.info)}
              <button
                on:click={async () => {
                  const res = await copyToClipboard(coinIntrus[0].imp_step.step3.info, false);
                  if (res) {
                    toast.success(
                      $i18n.t("Copying to clipboard was successful!")
                    );
                  }
                }}
                type="button"
                class="px-3 py-2 leading-3 text-color rounded-md text-xs"
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
            </div>
          </div>
          <p class="text-color text-base font-bold mt-2">
            3. {$i18n.t(coinIntrus[0].inst)}
          </p>
          <div class="text-color text-base">
            {$i18n.t(coinIntrus[0].desc)}
          </div>
          <p class="text-color text-base font-bold mt-2">
            4. {$i18n.t(coinIntrus[0].help)}
          </p>
        {:else}
          <h1 class="text-color text-center font-bold">
            {$i18n.t(coinIntrus[1].title)}
          </h1>
          <p class="text-color text-base">
            {$i18n.t(coinIntrus[1].description)}
          </p>
        {/if}
      </div>
      <div class="text-center pt-5">
        <button
          class="primaryButton px-2 py-1 rounded-lg text-lg text-gray-50"
          on:click={async () => {
            show = false;
          }}
        >
          {$i18n.t("I know")}
        </button>
      </div>
    </div>
  </div>
</Modal>

<style>
  h1 {
    font-size: 20px;
    margin-bottom: 16px;
  }
  .text-color {
    color: rgba(184, 142, 86, 1);
  }
  .bg-color{
    background-color: rgba(184, 142, 86, 1);
  }
</style>
