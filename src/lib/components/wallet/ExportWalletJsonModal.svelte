<script lang="ts">
  import { getContext } from "svelte";
  import { toast } from "svelte-sonner";
  import { currentWalletData, walletKey } from "$lib/stores";

  import { copyToClipboard } from "$lib/utils";

  import { decryptPrivateKey } from "$lib/utils/encrypt"

  import Modal from "../common/Modal.svelte";
  import {
    downloadKeyStore,
    storeWallet,
    loadWallet
  } from "$lib/utils/wallet/ether/utils.js";

  const i18n = getContext("i18n");

  export let show = false;

  let showPassword = false;
  let password = "";
  let loading = false;

  $: buttonStyle = loading ? "background: rgba(184, 142, 86, 0.6)" : "";

  async function checkPassword() {
    try {
      loading = true;
      await decryptPrivateKey($walletKey?.privateKey, password);
      showPrivate = true;
      loading = false;
    } catch (error) {
      loading = false;
      toast.error($i18n.t("Incorrect password"));
    }
  }

  let showPrivate = false;
  $: if (show) {
    showPrivate = false;
    if($walletKey?.checked) {
      password = $walletKey?.password;
      checkPassword();
    }
  }
  

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
      <div class="flex flex-row items-center mb-6">
        <div class="pt-0.5 max-w-[270px]">
          <div class="flex flex-col w-full">
            <div class="flex-1 relative">
              {#if showPassword}
                <input
                  bind:value={password}
                  type="text"
                  class="pl-5 pr-10 py-3 rounded-md w-full text-sm outline-none border dark:border-none dark:bg-gray-850"
                  placeholder={$i18n.t("Enter Your Password")}
                  autocomplete="current-password"
                  required
                />
                <!-- 开眼图标 -->
                <button class="absolute right-3 top-1/2 -translate-y-1/2"
                  on:click={() => {
                    showPassword = false
                  }}>
                  <svg xmlns="http://www.w3.org/2000/svg" 
                    class="h-5 w-5" 
                    viewBox="0 0 20 20" 
                    fill="currentColor">
                    <path d="M10 12a2 2 0 100-4 2 2 0 000 4z" />
                    <path fill-rule="evenodd" d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z" clip-rule="evenodd" />
                  </svg>
                </button>
              {:else}
                <input
                  bind:value={password}
                  type="password"
                  class="pl-5 pr-10 py-3 rounded-md w-full text-sm outline-none border dark:border-none dark:bg-gray-850"
                  placeholder={$i18n.t("Enter Your Password")}
                  autocomplete="current-password"
                  required
                />
                <!-- 闭眼图标 -->
                <button class="absolute right-3 top-1/2 -translate-y-1/2"
                  on:click={() => {
                    showPassword = true
                  }}>
                  <svg xmlns="http://www.w3.org/2000/svg" 
                    class="h-5 w-5" 
                    viewBox="0 0 20 20" 
                    fill="currentColor">
                    <path fill-rule="evenodd" d="M3.707 2.293a1 1 0 00-1.414 1.414l14 14a1 1 0 001.414-1.414l-1.473-1.473A10.014 10.014 0 0019.542 10C18.268 5.943 14.478 3 10 3a9.958 9.958 0 00-4.512 1.074l-1.78-1.781zm4.261 4.26l1.514 1.515a2.003 2.003 0 012.45 2.45l1.514 1.514a4 4 0 00-5.478-5.478z" clip-rule="evenodd" />
                    <path d="M12.454 16.697L9.75 13.992a4 4 0 01-3.742-3.741L2.335 6.578A9.98 9.98 0 00.458 10c1.274 4.057 5.065 7 9.542 7 .847 0 1.669-.105 2.454-.303z" />
                  </svg>
                </button>
              {/if}
            </div>
          </div>
        </div>
        {#if !$walletKey?.checked}
          <div class="ml-2">
            <button
              disabled={loading}
              class={" px-4 py-2.5 primaryButton text-gray-100 transition rounded-lg"}
              style={buttonStyle}
              on:click={async () => {
                if (!password) {
                  toast.error($i18n.t(`Please enter the password!`));
                  return;
                }
                await checkPassword();
              }}
            >
              <span class="relative leading-none">{$i18n.t("Unlock")}</span>
            </button>
          </div>
        {/if}
      </div>

      <!-- 私钥 -->
      {#if showPrivate}
        <div class="mb-4">
          <div class="mb-2">
            {$i18n.t("You can copy the private key below:")}
          </div>
          
          <div class="flex-1 relative">
            <p
              class="
              text-ellipsis overflow-hidden whitespace-nowrap
              pr-[35px]
              px-5 py-3 rounded-md w-full text-sm outline-none border dark:border-none dark:bg-gray-850"
            >
              {$currentWalletData?.walletInfo?.privateKey}

            </p>
            <button
              on:click={async () => {
                const res = await copyToClipboard(
                  // $currentWalletData?.walletInfo?.address
                  $currentWalletData?.walletInfo?.privateKey

                );
                if (res) {
                  toast.success($i18n.t("Copying to clipboard was successful!"));
                }
              }}
              type="button"
              class="absolute inset-y-0 right-0 px-3 py-2 text-sm dark:text-gray-300 dark:bg-gray-850 rounded-md"
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
      {/if}

      <!--  -->
      <!-- style={loading ? "background: rgba(184, 142, 86, 0.6)" : ""} -->

      <div class="flex justify-end">
        {#if showPrivate}
          <button
            disabled={loading}
            class={" px-4 py-2 primaryButton text-gray-100 transition rounded-lg"}
            style={buttonStyle}
            on:click={async () => {
              if (!password) {
                toast.error($i18n.t(`Please enter the password!`));
                return;
              }
              // loading= true
              try {
                if ($currentWalletData?.walletInfo && password) {
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
        {/if}
      </div>
    </div>
  </div>
</Modal>

<style>
</style>
