<script lang="ts">
  import { getContext, tick } from "svelte";
  import { goto } from "$app/navigation";
  import { channel, user, settings, config, walletKey } from '$lib/stores';
  import { toast } from "svelte-sonner";
  import Modal from "../common/Modal.svelte";
  import { handleWalletSignIn, unlockWalletWithPrivateKey } from "$lib/utils/wallet/ether/utils.js";
  import { importWallet } from "$lib/utils/wallet/ether/utils.js";
  import { updateWalletData } from "$lib/utils/wallet/walletUtils.js";
  import { getLanguages } from "$lib/i18n/index";
  import Checkbox from "$lib/components/common/Checkbox.svelte"
  import { encryptPrivateKey } from "$lib/utils/encrypt"

  const i18n = getContext("i18n");

  export let show = false;

  let showPassword = false;
  let password = "";
  let loading = false;
  let filesInputElement: any = null;
  let inputFiles: any = null;
  let encryptedJson: any = null; //
  let privateKey: string = '';
  let openWalletType = "privateKey";
  let checked = "unchecked";

  const uploadJson = async (file: any) => {
    // const res = await importAccountFromKeystore(file);
    // console.log("uploadJson", res);
    // encryptedJson = res; // 获取json文件中的账户对

    console.log("file", file);
    const reader = new FileReader();
    reader.readAsText(file);
    reader.onload = (e) => {
      try {
        const fileText = e.target?.result;
        if (fileText) {
          encryptedJson = JSON.parse(String(fileText));
        }
      } catch(e) {
        toast.error($i18n.t("Invalid keystore file"));
      }
    };
  }

  const initUserModels = () => {
    if ($user?.models) {
      settings.set({...$settings, models: $user?.models.split(",")});
    } else {
      settings.set({...$settings, models: $config?.default_models.split(",")});
    }
    localStorage.setItem("settings", JSON.stringify($settings));
    goto("/");
    const newChatButton = document.getElementById("new-chat-button");
    setTimeout(() => {
      newChatButton?.click();
    }, 0);
  }

  // 更新用户语言
  async function initLanguage() {
    if ($user?.language) {
      $i18n.changeLanguage($user?.language);
    } else {
      let browserLanguage = navigator.language;
      const languages = await getLanguages();
      let localLanguage = languages.filter(
        (item) => item.code == browserLanguage
      );
      if (localLanguage.length > 0) {
        $i18n.changeLanguage(browserLanguage);
      }
    }
  }

  // 校验是否选中
  function handleChange(event: any) {
    checked = event.detail;
  }

  $: if (!show) {(async () => {
      console.log("show", show);

      password = "";
      privateKey = ""
      checked = "unchecked"
      showPassword = false;
      inputFiles = null;
      encryptedJson = null;
    })();
  }

  $: if (openWalletType) {
    checked = "unchecked";
  }
</script>

<Modal bind:show>
  <!-- min-h-[400px] -->
  <div class="text-gray-700 dark:text-gray-100">
    <div class=" flex justify-between dark:text-gray-300 px-5 pt-4 pb-1">
      <div class=" text-lg font-medium self-center">
        {$i18n.t("Open Wallet")}
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
      <div class="flex w-full">
        <label class="mr-4">
          <input
            type="radio"
            bind:group={openWalletType}
            value="privateKey"
            required
          />
          PrivateKey
        </label>
        <label>
          <input
            type="radio"
            bind:group={openWalletType}
            value="keyStore"
            required
          />
          KeyStore
        </label>
      </div>

      {#if openWalletType === "privateKey"}
        <input
          bind:value={privateKey}
          type="text"
          class="my-4  px-5 py-3 rounded-md w-full text-sm outline-none border dark:border-none dark:bg-gray-850"
          placeholder={$i18n.t("Enter Your privateKey")}
          required
        />
        <!-- 输入密码 -->
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
                  class=" px-5 py-3 rounded-md w-full text-sm outline-none border dark:border-none dark:bg-gray-850"
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
        <div class="flex flex-row items-center my-2">
          <Checkbox bind:state="{checked}" on:change={handleChange}/>
          <span class="ml-1 text-sm">{$i18n.t("Is the password saved locally")}</span>
        </div>
        
        <div class="flex justify-end mt-3">
          <button
            disabled={loading}
            class={" px-4 py-2 primaryButton text-gray-100 transition rounded-lg"}
            style={loading ? "background: rgba(184, 142, 86, 0.6)" : ""}
            type="submit"
            on:click={async () => {
              loading = true;
              await tick();
              console.log("变色了要", loading);

              try {
                const walletImportedRet = await unlockWalletWithPrivateKey(
                  privateKey
                );

                if (!walletImportedRet?.ok) {
                  toast.error($i18n.t(walletImportedRet?.message));
                  loading = false;
                  return;
                }

                // 请求服务端登录钱包账户
                const walletImported = walletImportedRet?.data;
                await handleWalletSignIn({
                  walletImported,
                  password,
                  address_type: "dbc",
                  channel: $channel
                });


                let encryptStr = await encryptPrivateKey(privateKey, password);
                const walletKeyObj = {
                  privateKey: encryptStr,
                  checked: checked == "checked" ? true : false,
                  password: checked == "checked" ? password : ""
                }
                localStorage.walletkey = JSON.stringify(walletKeyObj);
                await walletKey.set(walletKeyObj);

                // 更新用户模型
                initUserModels();
                // 更新用户语言
                await initLanguage();

                updateWalletData(walletImported);

                await tick();
                loading = false;

                show = false;
                password = "";
              } catch (error) {
                console.log("error, ", error, error.message);
                toast.error(error.message);
              }
              loading = false;

          
            }}
          >
            {#if loading}
              <span>{$i18n.t("Unlocking")}</span>
            {:else}
              <span>{$i18n.t("Unlock")}</span>
            {/if}
          </button>
        </div>
      {/if}

      {#if openWalletType === "keyStore"}
        <button
          class="my-4 px-4 py-2 dark:bg-white dark:text-zinc-950 bg-black text-gray-100 transition rounded-lg"
          type="button"
          on:click={() => {
            filesInputElement.click();
          }}
        >
          {$i18n.t("Select Wallet File")}
        </button>

        <input
          bind:this={filesInputElement}
          bind:files={inputFiles}
          type="file"
          hidden
          accept="application/json"
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
        <!-- 输入密码 -->
        {#if encryptedJson}
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
                    class=" px-5 py-3 rounded-md w-full text-sm outline-none border dark:border-none dark:bg-gray-850"
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
          <div class="flex flex-row items-center my-2">
            <Checkbox bind:state="{checked}" on:change={handleChange}/>
            <span class="ml-1 text-sm">{$i18n.t("Is the password saved locally")}</span>
          </div>
        {/if}
        {#if encryptedJson}
          <div class="flex justify-end">
            <button
              disabled={loading}
              class={" px-4 py-2 primaryButton text-gray-100 transition rounded-lg"}
              style={loading ? "background: rgba(184, 142, 86, 0.6)" : ""}
              type="submit"
              on:click={async () => {
                loading = true;
                await tick();
                console.log("变色了要", loading);

                if (password=="") {
                  toast.error($i18n.t("Please input password"));
                  loading = false;
                  return;
                }

                try {
                  const walletImported = await importWallet(
                    encryptedJson,
                    password
                  );

                  // 请求服务端登录钱包账户
                  await handleWalletSignIn({
                    walletImported,
                    password,
                    address_type: "dbc",
                    channel: $channel
                  });

                  // 更新用户模型
                  initUserModels();
                  // 更新用户语言
                  await initLanguage();

                  updateWalletData(walletImported);

                  const encryptStr = await encryptPrivateKey(walletImported?.privateKey, password);
                  const walletKeyObj = {
                    privateKey: encryptStr,
                    checked: checked == "checked" ? true : false,
                    password: checked == "checked" ? password : ""
                  }
                  localStorage.walletkey = JSON.stringify(walletKeyObj);
                  await walletKey.set(walletKeyObj);

                  await tick();
                  loading = false;

                  show = false;
                  password = "";
                } catch (error) {
                  toast.error($i18n.t("Incorrect password"));
                }
                loading = false;

                const lockIndex = 0; // 锁定索引
              }}
            >
              {#if loading}
                <span>{$i18n.t("Unlocking")}</span>
              {:else}
                <span>{$i18n.t("Unlock")}</span>
              {/if}
            </button>
          </div>
        {/if}
      {/if}

    </div>
  </div>
</Modal>

<style>
</style>