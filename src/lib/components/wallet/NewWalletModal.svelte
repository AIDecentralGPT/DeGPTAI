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
    currentWalletData as walletDataStore,
    models,
    settings,
    user,
  } from "$lib/stores";

  const i18n = getContext("i18n");

  export let show = false;

  let showPassword = false;
  let password = "";
  let passwordError = "";
  let walletCreatedData = null; // 创建钱包返回的数据

  function validatePassword() {
    if (password.length < 8) {
      passwordError = "Password must be at least 8 characters long.";
    } else {
      passwordError = "";
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
        {$i18n.t("NEW DBC WALLET")}
      </div>

      <!-- X 关闭键 -->
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

    <!-- 主体 -->
    <div class="flex flex-col md:flex-row w-full p-4 px-8 md:space-x-4">
      <!-- 输入密码，进行创建 -->
      {#if !walletCreatedData}
        <div>
          <p class="text-md mb-4">
            You must remember your password, do not lose it, You need this
            password and your private key file to unlock the wallet
          </p>
          <div class="pt-0.5 max-w-[300px]">
            <div class="flex flex-col w-full">
              <div class="flex-1 relative">
                {#if showPassword}
                  <input
                    bind:value={password}
                    type="text"
                    class=" px-5 py-3 rounded-md w-full text-sm outline-none border dark:border-none dark:bg-gray-850"
                    placeholder={$i18n.t("Enter Your Password")}
                    autocomplete="current-password"
                    on:input={validatePassword}
                    required
                  />
                {:else}
                  <input
                    bind:value={password}
                    type="password"
                    class=" px-5 py-3 rounded-md w-full text-sm outline-none border dark:border-none dark:bg-gray-850"
                    placeholder={$i18n.t("Enter Your Password")}
                    autocomplete="current-password"
                    on:input={validatePassword}
                    required
                  />
                {/if}

                <button
                  type="button"
                  class="absolute inset-y-0 right-0 px-3 py-2 text-sm dark:text-gray-300 dark:bg-gray-850 rounded-md"
                  on:click={() => (showPassword = !showPassword)}
                >
                  {#if showPassword}
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width="1em"
                      height="1em"
                      viewBox="0 0 512 512"
                      ><path
                        fill="none"
                        stroke="currentColor"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="32"
                        d="M255.66 112c-77.94 0-157.89 45.11-220.83 135.33a16 16 0 0 0-.27 17.77C82.92 340.8 161.8 400 255.66 400c92.84 0 173.34-59.38 221.79-135.25a16.14 16.14 0 0 0 0-17.47C428.89 172.28 347.8 112 255.66 112"
                      /><circle
                        cx="256"
                        cy="256"
                        r="80"
                        fill="none"
                        stroke="currentColor"
                        stroke-miterlimit="10"
                        stroke-width="32"
                      /></svg
                    >
                  {:else}
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width="1em"
                      height="1em"
                      viewBox="0 0 24 24"
                      ><g
                        fill="none"
                        stroke="currentColor"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        ><path
                          d="M9.88 9.88a3 3 0 1 0 4.24 4.24m-3.39-9.04A10 10 0 0 1 12 5c7 0 10 7 10 7a13.2 13.2 0 0 1-1.67 2.68"
                        /><path
                          d="M6.61 6.61A13.5 13.5 0 0 0 2 12s3 7 10 7a9.74 9.74 0 0 0 5.39-1.61M2 2l20 20"
                        /></g
                      ></svg
                    >
                  {/if}
                </button>
              </div>
              {#if passwordError}
                <p class="text-red-500 text-sm mt-1">{passwordError}</p>
              {/if}
            </div>
          </div>

          <!-- 提交按钮 -->
          <div class="flex justify-end my-4">
            <button
              class=" px-4 py-2 primaryButton text-gray-100 transition rounded-lg"
              type="submit"
              on:click={async () => {
                const res = await createAccountFromSeed(); // 创建新账户
                console.log("createAccountFromSeed", res);
                walletCreatedData = res;

                // const pair = await getCurrentPair(); // 这里没必要
                const pair = walletCreatedData?.pair;
                console.log("pair", pair);

                // 存储本地密码
                savePair(pair, password);

                // const res1 = await createAccountFromMnemonic(); // 创建新账户
                // console.log("createAccountFromMnemonic", res1);

                // 登录账号
                const balance = await onGetBalance(pair?.address);
                const dlcBalance = await onGetDLCBalance(pair?.address);
                console.log("balance", balance, pair);
                console.log("dlcBalance", dlcBalance);
                // $currentWalletData.pair = pair
                // $currentWalletData.balance = balance
                // $currentWalletData.dlcBalance = dlcBalance







// ----------------
// 更新钱包面板
                walletDataStore.update((data) => {
                  return {
                    ...data,
                    pair,
                    balance,
                    dlcBalance,
                  };
                });
              }}
            >
              {$i18n.t("Create")}
            </button>
          </div>
        </div>
      {/if}

      <!-- 下载密钥文件 -->
      {#if walletCreatedData}
        <div>
          <p>
            Save your private key file in a safe place, such as writing it down
            and putting it in a safe.
          </p>

          <button
            class="my-4 px-4 py-2 dark:bg-white dark:text-zinc-950 bg-black text-gray-100 transition rounded-lg"
            type="submit"
            on:click={async () => {
              // 进行下载动作
              const json = await exportAccountForKeystore(
                walletCreatedData?.pair,
                password
              );

              // 保存账户对

              // console.log("exportAccountForKeystore", json);
            }}
          >
            {$i18n.t(" Key DOWNLOAD ENCRYPTED KEY ")}
          </button>

          <p>
            <b>Do not lose it!</b>If lost it can not be retrieved<br />
            Do not share it. Do not send it to anyone on WeChat, QQ, Facebook, Line,
            KakaoTalk, WhatsApp or any other communication softwareIf you use this
            document on a malicious phishing website your asset will be stolen!<br
            />You must have a back-up!Treat it as if one day if could be worth
            millions of USD
          </p>

          <div class="flex justify-end mt-4">
            <button
              class=" px-4 py-2 primaryButton text-gray-100 transition rounded-lg"
              type="submit"
              on:click={async () => {
                show = false;
              }}
            >
              {$i18n.t("  FINISHED  ")}
            </button>
          </div>
        </div>
      {/if}
    </div>
  </div>
</Modal>

<style>
  input::-webkit-outer-spin-button,
  input::-webkit-inner-spin-button {
    /* display: none; <- Crashes Chrome on hover */
    -webkit-appearance: none;
    margin: 0; /* <-- Apparently some margin are still there even though it's hidden */
  }

  .tabs::-webkit-scrollbar {
    display: none; /* for Chrome, Safari and Opera */
  }

  .tabs {
    -ms-overflow-style: none; /* IE and Edge */
    scrollbar-width: none; /* Firefox */
  }

  input[type="number"] {
    -moz-appearance: textfield; /* Firefox */
  }

  .text-red-500 {
    color: #f56565; /* 使用常见的错误红色 */
  }
</style>
