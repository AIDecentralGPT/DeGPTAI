<script lang="ts">
  import { getContext } from "svelte";
  import { toast } from "svelte-sonner";
  import { goto } from "$app/navigation";

  import {
    getModels as _getModels,
    copyToClipboard,
    checkUniapp,
  } from "$lib/utils";

  import Modal from "../common/Modal.svelte";
  import {
    currentWalletData,
    user,
    inviterId,
    channel,
    settings,
    config,
    showDownLoad
  } from "$lib/stores";
  import { updateWalletData } from "$lib/utils/wallet/walletUtils.js";
  import {
    createAccount,
    downloadKeyStore,
    handleWalletSignIn,
  } from "$lib/utils/wallet/ether/utils.js";

  import DownLoadModal from '$lib/components/download/DownLoadModal.svelte'

  const i18n = getContext("i18n");

  export let show = false;
  let loading = false;

  let showPassword = false;
  let password = "";
  let passwordError = "";
  let walletCreatedData: any = null; // 创建钱包返回的数据
  let keystoreJson: string | null = null;

  const validatePassword = () => {
    if (password.length < 8) {
      passwordError = $i18n.t("Password must be at least 8 characters long.");
    } else {
      passwordError = "";
    }
  };

  const initUserModels = () => {
    if ($user?.models) {
      settings.set({ ...$settings, models: $user?.models.split(",") });
    } else {
      settings.set({
        ...$settings,
        models: $config?.default_models.split(","),
      });
    }
    localStorage.setItem("settings", JSON.stringify($settings));
    goto("/");
    const newChatButton = document.getElementById("new-chat-button");
    setTimeout(() => {
      newChatButton?.click();
    }, 0);
  };

  let isMobile = false;
  $: if (!show) {
    walletCreatedData = null;
    const userAgent = navigator.userAgent || navigator.vendor || window.opera;
    // 检测常见的移动设备标识
    isMobile =
      /android|iphone|ipad|iPod|blackberry|opera mini|iemobile|wpdesktop/i.test(
        userAgent
      );
  }
</script>

<Modal bind:show>
  <!-- min-h-[400px] -->
  <div class="text-gray-700 dark:text-gray-100">
    <div class=" flex justify-between dark:text-gray-300 px-5 pt-4 pb-1">
      <div class=" text-lg font-medium self-center">
        <!-- {$i18n.t("NEW DBC WALLET")} -->
        {$i18n.t("NEW DGC WALLET")}
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
    <div class="flex flex-col md:flex-row w-full md:space-x-4 px-5 py-2">
      <!-- 输入密码，进行创建 -->
      {#if !walletCreatedData}
        <div class="w-full">
          <p class="text-md mb-4 px-2">
            {$i18n.t(
              "You must remember your password, do not lose it, You need this password and your private key file to unlock the wallet"
            )}
          </p>
          <div class="pt-0.5 max-w-[300px] px-2">
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
            <!-- <input
              bind:value={$inviterId}
              type="text"
              class="mt-4 px-5 py-3 rounded-md w-full text-sm outline-none border dark:border-none dark:bg-gray-850"
              placeholder={$i18n.t("Enter the inviter id here")}
              autocomplete="current-password"
              on:input={validatePassword}
              required
            /> -->
          </div>

          <div class="flex justify-between my-4">
            <!-- 下载按钮 -->
            <div class="flex p-2 items-center">
              {#if !checkUniapp()}
                <button class="text-sm font-medium text-center cursor-pointer"
                  on:click={() => {
                    $showDownLoad = true;
                  }}>
                  {$i18n.t("Download DeGPT to obtain rewards")}
                </button>
              {/if}
            </div>
            <!-- 提交按钮 -->
            <div class="grid place-content-end p-2">
              <button
                disabled={loading}
                class=" px-4 py-2 primaryButton text-gray-100 transition rounded-lg max-h-[40px]"
                style={loading ? "background: rgba(184, 142, 86, 0.6)" : ""}
                type="submit"
                on:click={async () => {
                  if (!password) {
                    toast.error("Please enter your password");
                  }
                  loading = true;

                  // 1. 创建钱包
                  const { wallet, keystore, accountPrivateKey } =
                    await createAccount(password);
                  console.log("wallet", wallet);
                  keystoreJson = keystore;
                  // 2. 请求服务端登录钱包账户
                  await handleWalletSignIn({
                    walletImported: wallet,
                    password,
                    address_type: "dbc",
                    inviterId: $inviterId,
                    channel: $channel,
                  });

                  loading = false;

                  // 更新用户模型
                  initUserModels();

                  // 3. 展示钱包面板数据
                  walletCreatedData = wallet;
                  updateWalletData(wallet);

                  // 4. 自动下载json文件
                  if (keystore) {
                    downloadKeyStore(keystore);
                    toast.success(
                      $i18n.t(
                        "The KeyStore has been downloaded automatically. If necessary, you can download JSON manually or copy the private key"
                      )
                    );
                  }
                }}
              >
                {#if loading}
                  <span class="truncate">{$i18n.t("Creating")}</span>
                {:else}
                  <span class="truncate">{$i18n.t("Create")}</span>
                {/if}
              </button>
            </div>
          </div>
        </div>
      {/if}

      <!-- 下载密钥文件 -->
      {#if walletCreatedData}
        <div>
          {#if $user.user_no}
            <p class="mb-2">
              <span> {$i18n.t("Congratulations on becoming")}</span>
              <!-- <strong> the {$user.user_no}</strong> -->
              <span>
                {$i18n.t("wallet registered user!")}
              </span>
            </p>
          {/if}

          <p>
            {$i18n.t(
              "Save your private key file in a safe place, such as writing it down and putting it in a safe"
            )}
          </p>

          <button
            class="my-4 px-4 py-2 primaryButton text-gray-100 transition rounded-lg"
            type="submit"
            on:click={async () => {
              // 进行下载动作
              // const json = await exportAccountForKeystore(
              //   walletCreatedData?.pair,
              //   password
              // );
              if (keystoreJson) {
                console.log("keystoreJson", keystoreJson);

                // 下载keystore文件
                downloadKeyStore(keystoreJson);
              }

              // 保存账户对

              // console.log("exportAccountForKeystore", json);
            }}
          >
            {$i18n.t("Key DOWNLOAD ENCRYPTED KEY")}
          </button>

          <div class="mb-4">
            <div class="mb-2">
              {$i18n.t("You can copy the private key below:")}
            </div>

            <div class="flex-1 relative primaryButton rounded-md">
              <p
                class="
                    text-ellipsis overflow-hidden whitespace-nowrap
                    pr-[35px]
                    px-5 py-3 rounded-md w-full text-sm outline-none border dark:border-none"
              >
                {$currentWalletData?.walletInfo?.privateKey}
              </p>
              <button
                on:click={async () => {
                  const res = await copyToClipboard(
                    $currentWalletData?.walletInfo?.privateKey
                  );
                  if (res) {
                    toast.success(
                      $i18n.t("Copying to clipboard was successful!")
                    );
                  }
                }}
                type="button"
                class="absolute inset-y-0 right-0 px-3 py-2 text-sm primaryButton rounded-md"
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

          <p>
            <b>
              {$i18n.t("Do not lose it!")}
            </b>
            {$i18n.t("If lost it can not be retrieved")}
            <br />
            {$i18n.t("Do not lose it!")}
            {$i18n.t(
              "Do not share it. Do not send it to anyone on WeChat, QQ, Facebook, Line, KakaoTalk, WhatsApp or any other communication software. If you use this document on a malicious phishing website your asset will be stolen!"
            )}
            <br />
            {$i18n.t(
              "You must have a back-up! Treat it as if one day if could be worth millions of USD"
            )}
          </p>

          <div class="flex justify-between mt-4 border-t border-dotted">
            <!-- 下载按钮 -->
            <div class="flex items-center py-2">
              {#if !checkUniapp()}
                <button class="text-sm font-medium text-center cursor-pointer"
                  on:click={() => {
                    $showDownLoad = true;
                  }}>
                  {$i18n.t("Download DeGPT to obtain rewards")}
                </button>
              {/if}
            </div>
            <!-- 完成按钮 -->
            <div class="grid place-content-end p-2">
              <button
                class=" px-4 py-2 primaryButton text-gray-100 transition rounded-lg"
                type="submit"
                on:click={async () => {
                  show = false;
                }}
              >
                <span class="truncate">{$i18n.t("FINISHED")}</span>
              </button>
            </div>
          </div>
        </div>
      {/if}
    </div>
  </div>
</Modal>

<!-- 赋值模型 -->
<DownLoadModal bind:show={ $showDownLoad }/>

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
