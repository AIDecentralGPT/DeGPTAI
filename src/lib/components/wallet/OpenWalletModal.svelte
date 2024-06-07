<script lang="ts">
  import { getChatList } from "$lib/apis/chats";
  import {
    importAccountFromKeystore,
    savePair,
    signData,
  } from "./../../utils/wallet/dbc.js";
  import {
    exportAccountForKeystore,
    createAccountFromMnemonic,
  } from "../../utils/wallet/dbc.js";
  import { createAccountFromSeed } from "$lib/utils/wallet/dbc.js";
  import { getContext, tick } from "svelte";
  import { toast } from "svelte-sonner";
  import {
    chats,
    currentWalletData,
    models,
    settings,
    user,
  } from "$lib/stores";

  import { getModels as _getModels } from "$lib/utils";
  import {
    SUPPORTED_FILE_TYPE,
    SUPPORTED_FILE_EXTENSIONS,
    WEBUI_BASE_URL,
  } from "$lib/constants";

  import Modal from "../common/Modal.svelte";
  import { unlockDLC } from "$lib/utils/wallet/dbc.js";
  import { onGetBalance } from "$lib/utils/wallet/dbc.js";
  import { onGetDLCBalance } from "$lib/utils/wallet/dbc.js";
  import { walletSignIn } from "$lib/apis/auths/index.js";
  import { handleWalletSignIn } from "$lib/utils/wallet/walletUtils.js";

  const i18n = getContext("i18n");

  export let show = false;

  let showPassword = false;
  let password = "";
  let loading = false;
  let passwordError = "";
  let walletCreatedData = null; // 创建钱包返回的数据
  let filesInputElement;
  let inputFiles;
  let pair = null; //

  $: if (!show) {
    (async () => {
      console.log("show", show);

      password = "";
      showPassword = false;
      inputFiles = null;
      pair = null;
    })();
  }

  async function uploadJson(file) {
    const res = await importAccountFromKeystore(file);
    console.log("uploadJson", res);
    pair = res; // 获取json文件中的账户对

    // unlockDLC(password, lockIndex, callback)

    // try {
    //   const reader = new FileReader();
    //   reader.onload = (event) => {
    //     const jsonContent = event.target.result;
    //     // 在这里处理 JSON 文件内容，例如上传到服务器
    //     console.log("JSON content:", jsonContent);
    //   };
    //   reader.readAsText(file);
    // } catch (error) {
    //   toast.error($i18n.t(`Error uploading JSON file: ${error.message}`));
    // }
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
        {$i18n.t("Open Wallet ")}
      </div>

      <!-- X 关闭键 -->
      <button
        class="self-center"
        on:click={() => {
          show = false;
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
      <!-- <button
        class=" px-4 py-2 dark:bg-white dark:text-zinc-950 bg-black text-gray-100 transition rounded-lg"
        on:click={async () => {
          show = false;
        }}
      >
        {$i18n.t("  FINISHED  ")}
      </button>
      <button> Select Wallet File </button> -->

      <button
        class="my-4 px-4 py-2 dark:bg-white dark:text-zinc-950 bg-black text-gray-100 transition rounded-lg"
        type="button"
        on:click={() => {
          filesInputElement.click();
        }}
      >
        {$i18n.t(" Select Wallet File ")}
      </button>

      <input
        bind:this={filesInputElement}
        bind:files={inputFiles}
        type="file"
        hidden
        accept=".json"
        on:change={async () => {
          if (inputFiles && inputFiles.length > 0) {
            const file = inputFiles[0]; // 假设只上传一个文件
            if (
              file.type === "application/json" ||
              file.name.split(".").pop().toLowerCase() === "json"
            ) {
              uploadJson(file);
              inputFiles = null;
              filesInputElement.value = "";
            } else {
              toast.error(
                $i18n.t(`Unsupported file type, please upload a JSON file.`)
              );
            }
          } else {
            toast.error($i18n.t(`File not found.`));
          }
        }}
      />

      <!-- ------ -->

      <!-- 输入密码 -->
      {#if pair}
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
      {/if}
      {#if pair}
        <div class="flex justify-end">
          <button
            disabled={loading}
            class={" px-4 py-2 primaryButton text-gray-100 transition rounded-lg"}
            style={loading ? "background: rgba(184, 142, 86, 0.6)" : ""}
            type="submit"
            on:click={async () => {
              
              loading = true;
              await tick()
              console.log("变色了要", loading);

              const lockIndex = 0; // 锁定索引
              unlockDLC(password, lockIndex, async (result) => {
                console.log("Unlock DGC result:", result);

                // 解锁失败
                if (result && !result?.success) {
                  toast.error(result?.msg);
                  loading = false;
                  await tick(); // 确保状态更新立即生效

                  return;
                }

                // 解锁成功
                if (result && result?.success) {
                  // 存储本地密码
                  savePair(pair, password);

                  // ----------------
                  // 请求服务端登录钱包账户
                  await handleWalletSignIn(pair, password);

                  loading = false;
              await tick()

                  show = false;
                  password = "";
                }
              });
            }}
          >
            {$i18n.t("  Unlock  ")}
          </button>
        </div>
      {/if}

      <div />
    </div>
  </div>
</Modal>

<style>
</style>
