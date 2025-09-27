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