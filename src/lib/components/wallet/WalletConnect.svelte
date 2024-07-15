<script>
  import { getContext, onMount } from "svelte";
  import { writable } from "svelte/store";

  import { createWeb3Modal, defaultWagmiConfig } from "@web3modal/wagmi";
  import { mainnet, bsc } from "@wagmi/core/chains";
  import {
    reconnect,
    http,
    watchConnections,
    sendTransaction,
    signMessage,
    disconnect,
    getAccount,
    watchAccount,
  } from "@wagmi/core";
  import { ethers } from "ethers";
  import { provider } from "$lib/utils/wallet/ether/utils";
  import {
    showPriceModal,
    showRewardsModal,
    showShareModal,
    threesideAccount,
    currentWalletData,
  } from "$lib/stores";
  import DbcThreeSideWalletDetail from "./DbcThreeSideWalletDetail.svelte";
  import { config, projectId } from "$lib/utils/wallet/walletconnect/index";
  const i18n = getContext("i18n");

  // 定义存储
  const walletAddress = writable("");
  const walletBalance = writable(0);
  let modal = null;





  const getBalance = async (address) => {
    try {
      const balance = await provider.getBalance(address);
      console.log("balance", balance);
      // walletBalance.set(ethers.formatEther(balance));
    } catch (error) {
      console.error("Get Balance Error:", error);
    }
  };

  // const calculateGasFee = async () => {
  //   try {
  //     const gasPrice = await provider.getGasPrice();
  //     const gasLimit = 21000;
  //     const gasFee = gasPrice.mul(gasLimit);
  //     console.log('Gas Fee (in wei):', gasFee.toString());
  //     console.log('Gas Fee (in ether):', ethers.formatEther(gasFee));
  //   } catch (error) {
  //     console.error('Calculate Gas Fee Error:', error);
  //   }
  // };

  const initConnection = async () => {
    try {
      console.log("initConnection");
      const res = await reconnect(config);
      console.log("reconnect res", res);
      if (res.length) {
        const address = res[0].accounts[0];
        // threesideAccount.update((prev) => {
        //   return {
        //     // ...prev,
        //     address,
        //   };
        // });
        // // walletAddress.set(address);
        await getBalance(address);
      } else {
        // walletAddress.set('');
        // walletBalance.set(0);
      }
    } catch (error) {
      console.error("Reconnect Error:", error);
    }
  };

  onMount(() => {
    initConnection();
    watchConnections(config, {
      async onChange(data) {
        if (data.length) {
          const address = data[0].accounts[0];
          walletAddress.set(address);
          await getBalance(address);
        } else {
          walletAddress.set("");
          walletBalance.set(0);
        }
      },
    });

    modal = createWeb3Modal({
      wagmiConfig: config,
      projectId,
      enableAnalytics: true,
      enableOnramp: true,
    });
  });

  watchAccount(config, {
    onChange(account) {
      console.log("1", account);
      // if (isConnected) {
      //   signMessage(config, { message: "hello world" }).then((res) => {
      //     console.log(123, res);
      //   });
      // }

      // CreateSignature($currentWalletData.pair,"123", undefined  )

      $threesideAccount = account;
    },
  });

  function connect() {
    console.log("三方钱包数据", threesideAccount);
    // disconnect(config);

    if (getAccount(config).isConnected) {
      disconnect(config);
    } else {
      modal.open();
    }
  }
</script>

<div class="walletConnect flex flex-col gap-4">
  <!-- <button on:click={connect}>connect wallet </button> -->

  {#if !$currentWalletData.walletInfo && !$threesideAccount?.address}
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

  <!-- <w3m-button id="web3button" label="链接钱包"  style="width: 100%;" /> -->

  {#if $threesideAccount?.address}
    <!-- <div class="py-2 px-3"> -->
    <!-- 升级计划 -->
    <button
      on:click={() => {
        $showPriceModal = true;
      }}
      class="w-full px-4 py-2 primaryButton text-gray-100 transition rounded-lg"
    >
      <span class="relative">{$i18n.t("Upgrade Plan")}</span>
    </button>

    <div>
      <!-- 分享按钮 -->
      <div class="flex justify-between items-center flex-row-reverse mb-2">
        <button
          class="flex gap-2 items-center cursor-pointer"
          on:click={() => {
            $showShareModal = true;
          }}
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="1em"
            height="1em"
            viewBox="0 0 24 24"
            ><path
              fill="none"
              stroke="currentColor"
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M10 4H6a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-4m-8-2l8-8m0 0v5m0-5h-5"
            /></svg
          >

          <span> {$i18n.t("Share to Obtain DGC")} </span>
        </button>
      </div>

      <div class="flex items-center">
        <w3m-button id="web3button" label="链接钱包" class="flex-1" />

        <!-- 购买 -->
        <!-- class=" p-1 dark:bg-white dark:text-zinc-950 bg-black text-gray-100 rounded-lg " -->

        <button
          type="submit"
          on:click={async () => {
            $showRewardsModal = true;
          }}
        >
          {$i18n.t("Rewards")}
        </button>
      </div>
    </div>
  {/if}

  <!-- <button on:click={signDemoMessage}>Sign Message</button>
  <button on:click={sendDemoTransaction}>Send Transaction</button> -->
  <!-- <button on:click={calculateGasFee}>Calculate Gas Fee</button> -->
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
  .walletConnect {
  }
</style>
