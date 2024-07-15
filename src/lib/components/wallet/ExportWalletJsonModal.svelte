<script lang="ts">
  import { importAccountFromKeystore } from "./../../utils/wallet/dbc.js";

  import { getContext } from "svelte";
  import { toast } from "svelte-sonner";
  import { currentWalletData, models, settings, user } from "$lib/stores";

  import { getModels as _getModels } from "$lib/utils";
  import {
    SUPPORTED_FILE_TYPE,
    SUPPORTED_FILE_EXTENSIONS,
    WEBUI_BASE_URL,
  } from "$lib/constants";

  import Modal from "../common/Modal.svelte";
  import {
    onGetBalance,
    createAccountFromSeed,
    onGetDLCBalance,
    exportAccountForKeystore,
    createAccountFromMnemonic,
  } from "$lib/utils/wallet/dbc";
  import {
    downloadKeyStore,
    storeWallet,
  } from "$lib/utils/wallet/ether/utils.js";

  const i18n = getContext("i18n");

  export let show = false;

  let showPassword = false;
  let password = "";
  let loading = false;

  $: buttonStyle = loading ? "background: rgba(184, 142, 86, 0.6)" : "";
</script>

<Modal bind:show>
  <!-- min-h-[400px] -->
  <div
    class="text-gray-700 dark:text-gray-100
	"
  >
    <div class=" flex justify-between dark:text-gray-300 px-5 pt-4 pb-1">
      <div class=" text-lg font-medium self-center">
        {$i18n.t("Export Wallet")}
      </div>

      <!-- X 关闭键 -->
      <button
        class="self-center"
        on:click={() => {
          show = false;
          loading = false;
          password = "";
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

    <!-- 主体 -->
    <!-- flex flex-col md:space-x-4 -->
    <div class=" w-full p-4 px-8">
      <!-- 输入密码 -->
      <div class="mb-6 pt-0.5 max-w-[300px]">
        <div class="flex flex-col w-full">
          <div class="flex-1 relative">
            {#if showPassword}
              <input
                bind:value={password}
                type="text"
                class=" px-5 py-3 rounded-md w-full text-sm outline-none border dark:border-none dark:bg-gray-850"
                placeholder={$i18n.t("Enter Your Password")}
                autocomplete="current-password"
                required
              />
            {:else}
              <input
                bind:value={password}
                type="password"
                class=" px-5 py-3 rounded-md w-full text-sm outline-none border dark:border-none dark:bg-gray-850"
                placeholder={$i18n.t("Enter Your Password")}
                autocomplete="current-password"
                required
              />
            {/if}
          </div>
        </div>
      </div>

      <!-- style={loading ? "background: rgba(184, 142, 86, 0.6)" : ""} -->

      <div class="flex justify-end">
        <button
          disabled={loading}
          class={" px-4 py-2 primaryButton text-gray-100 transition rounded-lg"}
          style={buttonStyle}
          on:click={async () => {
            if (!password) {
              toast.error(`Please enter the password!`);

              return;
            }
            // loading= true

            try {
              if ($currentWalletData?.walletInfo && password) {
                // console.log("loading", loading);

                // 设置密码以加密Keystore文件
                const keystore = await storeWallet(
                  $currentWalletData?.walletInfo,
                  password
                );
                downloadKeyStore(keystore);

                // loading= false
                show = false;
                // console.log("loading", loading);
              }
            } catch (error) {
              loading = false;
              toast.error(error?.message);
            }
          }}
        >
          <span class="relative">{$i18n.t("Export")}</span>
        </button>
      </div>

      <div />
    </div>
  </div>
</Modal>

<style>
</style>
