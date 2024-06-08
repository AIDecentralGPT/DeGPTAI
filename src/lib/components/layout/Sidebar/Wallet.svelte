<script lang="ts">
  import { DropdownMenu } from "bits-ui";
  import { createEventDispatcher, getContext } from "svelte";

  import { flyAndScale } from "$lib/utils/transitions";
  import { goto } from "$app/navigation";
  import ArchiveBox from "$lib/components/icons/ArchiveBox.svelte";
  import {
    showSettings,
    showNewWalletModal,
    showOpenWalletModal,
    currentWalletData,
    chatId,
    pageUpdateNumber,
  } from "$lib/stores";
  import { fade, slide } from "svelte/transition";
  import {
    GetApi,
    createAccountFromSeed,
    dbcPriceOcw,
  } from "$lib/utils/wallet/dbc";
  import DbcAccountDetail from "$lib/components/wallet/DbcAccountDetail.svelte";
  import WalletConnect from "$lib/components/wallet/WalletConnect.svelte";
  // import connectThreeSide from "$lib/utils/wallet/walletconnect";

  const i18n = getContext("i18n");

  export let show = false;
  export let role = "";
  export let className = "max-w-[240px]";

  const dispatch = createEventDispatcher();

  // ---------------------
  // 连接三方钱包
  import { createWeb3Modal, defaultWagmiConfig } from "@web3modal/wagmi";

  import { mainnet, arbitrum } from "viem/chains";
  import { reconnect } from "@wagmi/core";
  import {
    watchAccount,
    disconnect,
    getAccount,
    signMessage,
  } from "@wagmi/core";

  // 1. Your WalletConnect Cloud project ID
  const projectId = "a365ccf6c502136ee70fd89768611fc2";

  // 2. Create a metadata object
  const metadata = {
    name: "degpt-demo",
    description: "Web3Modal Example",
    url: "https://web3modal.com", // origin must match your domain & subdomain
    icons: ["https://avatars.githubusercontent.com/u/37784886"],
  };

  // 3. Create wagmiConfig
  const chains = [mainnet, arbitrum];
  const config = defaultWagmiConfig({
    chains,
    projectId,
    metadata,
  });

  reconnect(config);
  // 3. Create modal

  const modal = createWeb3Modal({
    wagmiConfig: config,
    projectId,
    enableAnalytics: true, // Optional - defaults to your Cloud configuration
    enableOnramp: true, // Optional - false as default
    themeVariables: {
      // '--w3m-color-mix': '#00BB7F',
      // '--w3m-color-mix-strength': 40,
      // --wui-color-accent-base-100
      "--w3m-accent": "transport",
    },
    themeMode: "dark",
  });

  let threesideAccount = getAccount(config);
  console.log("三方钱包数据threesideAccount", threesideAccount);

  function connect() {
    console.log("三方钱包数据", threesideAccount);
    // disconnect(config);

    if (getAccount(config).isConnected) {
      disconnect(config);
    } else {
      modal.open();
    }
  }

  // ---------------------

  const btnEl = document.getElementById("btn");
  const userEl = document.getElementById("user");

  watchAccount(config, {
    onChange(account) {
      console.log("1", account);
      // if (isConnected) {
      //   signMessage(config, { message: "hello world" }).then((res) => {
      //     console.log(123, res);
      //   });
      // }

      // CreateSignature($currentWalletData.pair,"123", undefined  )

      threesideAccount = account;
    },
  });

  // signMessage只在threesideAccount改变时执行一次。（reactive）
  // let signedMessage;
  // $: if (threesideAccount && !signedMessage) {
  //   signMessage(config, { message: 'hello world' }).then((res) => {
  //     console.log(123, res);
  //     signedMessage = res;
  //   });
  // }

  // watchAccount(config, {
  //   onChange(account) {
  //     userEl.innerText = account?.address ?? "";
  //     if (account.isConnected) {
  //       btnEl.innerText = "Disconnect";
  //     } else {
  //       btnEl.innerText = "Connect";
  //     }
  //   },
  // });
</script>

<div name="content">
  <!-- <w3m-connect-button class="bg-red-500 text-black" /> -->
  <!-- <button id="btn">Connect</button> -->
  <span id="user" />

  <!-- <span
  on:click={ () => {
    console.log("测试", threesideAccount);
    
  }}
  
  >测试</span> -->

  <hr class=" dark:border-gray-800 my-2 p-0" />


  <!-- 三方钱包账号展示 -->
  {#if threesideAccount?.address}
    <w3m-button />
  {/if}

  <!-- 创建，连接，打开钱包，三个按钮 -->
  {#if !$currentWalletData.pair && !threesideAccount?.address}
    <div>
      <button
        id="btn"
        class="flex rounded-md py-2 px-3 w-full hover:bg-gray-50 dark:hover:bg-gray-800 transition"
        on:click={async () => {
          connect();
          // connectThreeSide()
          // localStorage.removeItem('token');
          // location.href = '/auth';
          // show = false;
          // GetApi()
          // console.log("createAccount在这里");
          // const res = await createAccountFromSeed()
          // // const res = await dbcPriceOcw()
          // console.log("res", res);
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
          {$i18n.t("Connect WALLET")}
          <!-- <WalletConnect /> -->
        </div>
      </button>

      <button
        class="flex rounded-md py-2 px-3 w-full hover:bg-gray-50 dark:hover:bg-gray-800 transition"
        on:click={async () => {
          // // localStorage.removeItem('token');
          // // location.href = '/auth';
          // // show = false;
          // // GetApi()
          // console.log("createAccount在这里");

          // const res = await createAccountFromSeed()

          // // const res = await dbcPriceOcw()
          // console.log("res", res);
          $showNewWalletModal = true;


        }}
      >
        <div class=" self-center mr-3">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="1.4em"
            height="1.4em"
            viewBox="0 0 24 24"
            ><path
              fill="currentColor"
              d="M20 6h-8l-2-2H4c-1.11 0-1.99.89-1.99 2L2 18c0 1.11.89 2 2 2h16c1.11 0 2-.89 2-2V8c0-1.11-.89-2-2-2m0 12H4V6h5.17l2 2H20zm-8-4h2v2h2v-2h2v-2h-2v-2h-2v2h-2z"
            /></svg
          >
        </div>
        <div class=" self-center font-medium">{$i18n.t("Create WALLET")}</div>
      </button>

      <button
        class="flex rounded-md py-2 px-3 w-full hover:bg-gray-50 dark:hover:bg-gray-800 transition"
        on:click={async () => {
          // localStorage.removeItem('token');
          // location.href = '/auth';
          // show = false;
          // GetApi()
          // console.log("createAccount在这里");

          // const res = await createAccountFromSeed()

          // // const res = await dbcPriceOcw()
          // console.log("res", res);

          $showOpenWalletModal = true;
        }}
      >
        <div class=" self-center mr-3">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="1.4em"
            height="1.4em"
            viewBox="0 0 512 512"
            ><rect
              width="416"
              height="288"
              x="48"
              y="144"
              fill="none"
              stroke="currentColor"
              stroke-linejoin="round"
              stroke-width="32"
              rx="48"
              ry="48"
            /><path
              fill="none"
              stroke="currentColor"
              stroke-linejoin="round"
              stroke-width="32"
              d="M411.36 144v-30A50 50 0 0 0 352 64.9L88.64 109.85A50 50 0 0 0 48 159v49"
            /><path
              fill="currentColor"
              d="M368 320a32 32 0 1 1 32-32a32 32 0 0 1-32 32"
            /></svg
          >
        </div>
        <div class=" self-center font-medium">{$i18n.t("Open Wallet")}</div>
      </button>
    </div>
  {/if}

  <!-- 钱包数据面板 -->
  {#if $currentWalletData.pair}
    <DbcAccountDetail />
  {/if}
</div>

<style>
  .w3m-button {
  }
</style>
