<script lang="ts">
  import { getContext } from "svelte";
  import { toast } from "svelte-sonner";
  import { goto } from "$app/navigation";

  import {
    getModels as _getModels,
    copyToClipboard,
    isWebView,
  } from "$lib/utils";

  import Modal from "../common/Modal.svelte";
  import {
    currentWalletData,
    user,
    inviterId,
    channel,
    settings,
    config,
  } from "$lib/stores";
  import { updateWalletData } from "$lib/utils/wallet/walletUtils.js";
  import {
    createAccount,
    downloadKeyStore,
    handleWalletSignIn,
  } from "$lib/utils/wallet/ether/utils.js";
  import { i } from "vitest/dist/reporters-yx5ZTtEV";

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
            <div class="flex flex-col p-2">
              <div class="text-sm font-medium text-center">
                {$i18n.t("Download DeGPT to obtain rewards")}
              </div>
              <div class="flex flex-row mt-1 px-2">
                {#if isWebView()}
                  <div></div>
                {:else}
                  <button
                    class="flex flex-row items-center rounded-full px-4 py-2 mr-3 primaryButton text-gray-900"
                    on:click={() => {
                      window.open("/static/app/degptv1.0_0712.apk", "_blank");
                    }}
                  >
                    <svg
                      class="icon mr-1 fill-white dark:fill-gray-900"
                      viewBox="0 0 1024 1024"
                      version="1.1"
                      xmlns="http://www.w3.org/2000/svg"
                      width="20"
                      height="20"
                    >
                      <path
                        d="M808.398269 218.955161c20.458525 11.691232 27.566623 37.753501 15.876521 58.213157l-65.330296 114.329713c119.461015 74.88989 203.198446 202.202702 217.966199 350.95283 2.492185 25.107214-17.227161 46.882472-42.457572 46.882472H85.333333c-25.230411 0-44.949757-21.775258-42.457571-46.882472 14.120124-142.220715 91.287453-264.84528 202.445704-340.790817l-71.137484-124.491726c-11.691232-20.459656-4.583135-46.521925 15.876521-58.213157 20.459656-11.691232 46.523055-4.583135 58.214287 15.876521l71.589581 125.281766c58.218808-25.812486 122.559011-40.113448 190.028856-40.113448 60.891832 0 119.233837 11.648283 172.825431 32.893457l67.465324-118.061775c11.691232-20.459656 37.754631-27.567753 58.214287-15.876521zM317.895488 554.666667c-23.563302 0-42.666667 19.102234-42.666667 42.666666s19.103364 42.666667 42.666667 42.666667c23.565563 0 42.666667-19.102234 42.666667-42.666667s-19.101104-42.666667-42.666667-42.666666z m384 0c-23.563302 0-42.666667 19.102234-42.666667 42.666666s19.103364 42.666667 42.666667 42.666667c23.565563 0 42.666667-19.102234 42.666667-42.666667s-19.101104-42.666667-42.666667-42.666666z"
                      />
                    </svg>
                    <span class="{isMobile ? 'w-full' : ''} truncate"
                      >Android</span
                    >
                  </button>
                  <!-- <button class="flex flex-row items-center rounded-full px-4 py-2 mr-3 bg-gray-700 dark:bg-white text-white dark:text-gray-900">
                  <svg class="icon mr-1 fill-white dark:fill-gray-900" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" width="18" height="18">
                    <path d="M131.015111 937.301333c-10.24-16.952889-17.237333-44.373333-17.237333-83.854222V170.552889c0-39.480889 7.054222-66.901333 17.237333-83.854222l413.809778 425.699555-413.809778 424.903111z m588.572445-245.134222l-422.456889 235.406222c-47.786667 26.624-77.539556 39.537778-112.071111 39.537778h-3.868445l402.773333-415.232 135.623112 140.288z m50.915555-332.117333l89.315556 49.948444c32.995556 18.545778 83.057778 52.394667 83.057777 102.4 0 49.152-50.062222 83.057778-83.057777 101.603556l-89.315556 49.948444-147.342222-151.552 147.342222-152.348444zM181.134222 56.888889h3.982222c34.474667 0 64.284444 12.913778 112.071112 39.480889l422.4 235.463111-135.566223 140.231111L181.191111 56.888889z"></path>
                  </svg>
                  <span>Google Play</span>
                </button> -->
                  <button
                    class="flex flex-row items-center rounded-full px-4 py-2 primaryButton text-gray-900"
                    on:click={() => {
                      window.open(
                        "https://apps.apple.com/us/app/degpt/id6504377109?platform=iphone",
                        "_blank"
                      );
                    }}
                  >
                    <svg
                      class="icon fill-white dark:fill-gray-900"
                      viewBox="0 0 1024 1024"
                      version="1.1"
                      xmlns="http://www.w3.org/2000/svg"
                      width="24"
                      height="24"
                    >
                      <path
                        d="M631.125333 128c6.698667 44.074667-11.861333 87.210667-36.266666 117.76-26.154667 32.725333-71.168 58.069333-114.858667 56.746667-8.021333-42.154667 12.416-85.632 37.248-114.858667 27.221333-32.213333 73.941333-56.917333 113.877333-59.648z m131.157334 620.117333c22.528-33.408 30.890667-50.261333 48.384-87.936-127.104-46.805333-147.456-221.696-21.674667-288.853333-38.4-46.506667-92.288-73.557333-143.146667-73.557333-36.693333 0-61.824 9.301333-84.650666 17.706666-19.029333 6.997333-36.437333 13.44-57.685334 13.44-22.954667 0-43.264-7.04-64.512-14.421333-23.338667-8.106667-47.872-16.64-78.293333-16.64-57.130667 0-117.888 33.792-156.416 91.52-54.186667 81.365333-44.970667 234.24 42.922667 364.501333 31.36 46.592 73.301333 98.986667 128.213333 99.413334 22.741333 0.256 37.930667-6.314667 54.314667-13.44 18.773333-8.149333 39.168-17.066667 74.496-17.194667 35.498667-0.213333 55.594667 8.746667 74.069333 17.066667 16 7.082667 30.805333 13.696 53.376 13.44 54.912-0.426667 99.2-58.453333 130.56-105.045334z"
                      />
                    </svg>
                    <span class="{isMobile ? 'w-[50px]' : ''} truncate"
                      >App Store</span
                    >
                  </button>
                {/if}
              </div>
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
            <div class="flex flex-col py-2">
              <div class="text-sm font-medium text-center">
                {$i18n.t(" obtain rewards")}
              </div>
              <div class="flex flex-row mt-1 px-2">
                <button
                  class="flex flex-row items-center rounded-full px-4 py-2 mr-3 primaryButton text-gray-900"
                  on:click={() => {
                    window.open("/static/app/degptv1.0_0712.apk", "_blank");
                  }}
                >
                  <svg
                    class="icon mr-1 fill-white dark:fill-gray-900"
                    viewBox="0 0 1024 1024"
                    version="1.1"
                    xmlns="http://www.w3.org/2000/svg"
                    width="20"
                    height="20"
                  >
                    <path
                      d="M808.398269 218.955161c20.458525 11.691232 27.566623 37.753501 15.876521 58.213157l-65.330296 114.329713c119.461015 74.88989 203.198446 202.202702 217.966199 350.95283 2.492185 25.107214-17.227161 46.882472-42.457572 46.882472H85.333333c-25.230411 0-44.949757-21.775258-42.457571-46.882472 14.120124-142.220715 91.287453-264.84528 202.445704-340.790817l-71.137484-124.491726c-11.691232-20.459656-4.583135-46.521925 15.876521-58.213157 20.459656-11.691232 46.523055-4.583135 58.214287 15.876521l71.589581 125.281766c58.218808-25.812486 122.559011-40.113448 190.028856-40.113448 60.891832 0 119.233837 11.648283 172.825431 32.893457l67.465324-118.061775c11.691232-20.459656 37.754631-27.567753 58.214287-15.876521zM317.895488 554.666667c-23.563302 0-42.666667 19.102234-42.666667 42.666666s19.103364 42.666667 42.666667 42.666667c23.565563 0 42.666667-19.102234 42.666667-42.666667s-19.101104-42.666667-42.666667-42.666666z m384 0c-23.563302 0-42.666667 19.102234-42.666667 42.666666s19.103364 42.666667 42.666667 42.666667c23.565563 0 42.666667-19.102234 42.666667-42.666667s-19.101104-42.666667-42.666667-42.666666z"
                    />
                  </svg>
                  <span class="{isMobile ? 'w-full' : ''} truncate"
                    >Android</span
                  >
                </button>
                <!-- <button class="flex flex-row items-center rounded-full px-4 py-2 mr-3 bg-gray-700 dark:bg-white text-white dark:text-gray-900">
                  <svg class="icon mr-1 fill-white dark:fill-gray-900" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" width="18" height="18">
                    <path d="M131.015111 937.301333c-10.24-16.952889-17.237333-44.373333-17.237333-83.854222V170.552889c0-39.480889 7.054222-66.901333 17.237333-83.854222l413.809778 425.699555-413.809778 424.903111z m588.572445-245.134222l-422.456889 235.406222c-47.786667 26.624-77.539556 39.537778-112.071111 39.537778h-3.868445l402.773333-415.232 135.623112 140.288z m50.915555-332.117333l89.315556 49.948444c32.995556 18.545778 83.057778 52.394667 83.057777 102.4 0 49.152-50.062222 83.057778-83.057777 101.603556l-89.315556 49.948444-147.342222-151.552 147.342222-152.348444zM181.134222 56.888889h3.982222c34.474667 0 64.284444 12.913778 112.071112 39.480889l422.4 235.463111-135.566223 140.231111L181.191111 56.888889z"></path>
                  </svg>
                  <span>Google Play</span>
                </button> -->
                <button
                  class="flex flex-row items-center rounded-full px-4 py-2 primaryButton text-gray-900"
                  on:click={() => {
                    window.open(
                      "https://apps.apple.com/us/app/degpt/id6504377109?platform=iphone",
                      "_blank"
                    );
                  }}
                >
                  <svg
                    class="icon fill-white dark:fill-gray-900"
                    viewBox="0 0 1024 1024"
                    version="1.1"
                    xmlns="http://www.w3.org/2000/svg"
                    width="24"
                    height="24"
                  >
                    <path
                      d="M631.125333 128c6.698667 44.074667-11.861333 87.210667-36.266666 117.76-26.154667 32.725333-71.168 58.069333-114.858667 56.746667-8.021333-42.154667 12.416-85.632 37.248-114.858667 27.221333-32.213333 73.941333-56.917333 113.877333-59.648z m131.157334 620.117333c22.528-33.408 30.890667-50.261333 48.384-87.936-127.104-46.805333-147.456-221.696-21.674667-288.853333-38.4-46.506667-92.288-73.557333-143.146667-73.557333-36.693333 0-61.824 9.301333-84.650666 17.706666-19.029333 6.997333-36.437333 13.44-57.685334 13.44-22.954667 0-43.264-7.04-64.512-14.421333-23.338667-8.106667-47.872-16.64-78.293333-16.64-57.130667 0-117.888 33.792-156.416 91.52-54.186667 81.365333-44.970667 234.24 42.922667 364.501333 31.36 46.592 73.301333 98.986667 128.213333 99.413334 22.741333 0.256 37.930667-6.314667 54.314667-13.44 18.773333-8.149333 39.168-17.066667 74.496-17.194667 35.498667-0.213333 55.594667 8.746667 74.069333 17.066667 16 7.082667 30.805333 13.696 53.376 13.44 54.912-0.426667 99.2-58.453333 130.56-105.045334z"
                    />
                  </svg>
                  <span class="{isMobile ? 'w-[50px]' : ''} truncate"
                    >App Store</span
                  >
                </button>
              </div>
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
