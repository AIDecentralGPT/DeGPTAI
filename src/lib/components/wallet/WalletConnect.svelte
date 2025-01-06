<script lang="ts">
  import { getContext, onMount } from "svelte";
  import { goto } from "$app/navigation";
  import { writable } from "svelte/store";
  import { createWeb3Modal } from "@web3modal/wagmi";
  import { watchConnections, getAccount, watchAccount } from "@wagmi/core";
  import { handleWalletSignIn } from "$lib/utils/wallet/ether/utils";
  import { closeWallet } from "$lib/utils/wallet/walletUtils";
  import {
    threesideAccount,
    user,
    theme,
    channel,
    settings,
    config as storeConfig,
  } from "$lib/stores";
  import { config, projectId } from "$lib/utils/wallet/walletconnect/index";
  import { addErrorLog } from "$lib/apis/errorlog";
  import { getLanguages } from "$lib/i18n/index";

  const i18n = getContext("i18n");

  // 定义存储
  const walletAddress = writable("");
  const walletBalance = writable(0);
  let modal: any = { options: { themeMode: "dark" } };

  onMount(() => {
    watchConnections(config, {
      async onChange(data) {
        if (data.length) {
          const address = data[0].accounts[0];
          walletAddress.set(address);
        } else {
          walletAddress.set("");
          walletBalance.set(0);
        }
      },
    });

    modal = createWeb3Modal({
      themeMode: "dark",
      wagmiConfig: config,
      projectId,
      enableAnalytics: true,
      enableOnramp: true,
    });
  });

  const initUserModels = () => {
    if ($user?.models) {
      settings.set({ ...$settings, models: $user?.models.split(",") });
    } else {
      settings.set({
        ...$settings,
        models: $storeConfig?.default_models.split(","),
      });
    }
    localStorage.setItem("settings", JSON.stringify($settings));
    goto("/");
    const newChatButton = document.getElementById("new-chat-button");
    setTimeout(() => {
      newChatButton?.click();
    }, 0);
  };

  // 更新用户语言
  const initLanguage = async () => {
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

  function clearConnector() {
    config.state.connections.forEach((item) => {
      config.state.connections.delete(item.connector.uid);
    });
  }

  function changeModalTheme() {
    if ($theme === "system" || $theme === "light") {
      modal.setThemeMode("light");
    } else {
      modal.setThemeMode("dark");
    }
  }

  watchAccount(config, {
    async onChange() {
      try {
        let account = getAccount(config);
        $threesideAccount = account;
        if (account.status === "connected") {
          if (!$user?.id === undefined || !$user?.id?.startsWith("0x")) {
            await handleWalletSignIn({
              walletImported: {
                address: account?.address,
              },
              address_type: "threeSide",
              channel: $channel,
            });

            // 更新用户模型
            initUserModels();
            // 更新语言模型
            await initLanguage();
          }
        }
        if (account.status === "disconnected") {
          user.set({});
          await closeWallet($channel);
          clearConnector();
          // 更新用户模型
          initUserModels();
          // 更新语言模型
          await initLanguage();
        }
      } catch (error) {
        addErrorLog("第三方登陆", error.toString());
      }
    },
  });

  function connect() {
    if ($user?.id?.startsWith("0x") && getAccount(config).isConnected) {
      closeWallet($channel);
    } else {
      clearConnector();
      changeModalTheme();
      modal.open();
    }
  }
</script>

<div class="walletConnect flex flex-col gap-4">
  {#if !($user?.id && $user?.id?.startsWith("0x"))}
    <button
      id="btn"
      class="flex rounded-md py-2 px-3 w-full hover:bg-gray-50 dark:hover:bg-gray-800 transition"
      on:click={async () => {
        connect();
      }}
    >
      <div class=" self-center mr-3">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="1.4em"
          height="1.4em"
          viewBox="0 0 48 48"
          ><g
            fill="none"
            stroke="currentColor"
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="4"
            ><path
              d="M8 12a4 4 0 1 0 0-8a4 4 0 0 0 0 8m2 30a6 6 0 1 0 0-12a6 6 0 0 0 0 12m28 2a6 6 0 1 0 0-12a6 6 0 0 0 0 12M22 28a8 8 0 1 0 0-16a8 8 0 0 0 0 16m12-16a4 4 0 1 0 0-8a4 4 0 0 0 0 8"
              clip-rule="evenodd"
            /><path d="m11 11l4 4m15-3l-2 2m6 19.5L28 26m-14 5l4-4" /></g
          ></svg
        >
      </div>
      <div class=" self-center font-medium">
        {$i18n.t("Connect Wallet")}
      </div>
    </button>
  {/if}
</div>

<style>
  :root {
    --wui-color-accent-100: linear-gradient(
      90deg,
      #03ffd2 0%,
      #8000ff 100%
    ) !important;
    --wui-gray-glass-010: midnightblue !important;
    --wui-border-radius-m: 12px !important;
  }
</style>
