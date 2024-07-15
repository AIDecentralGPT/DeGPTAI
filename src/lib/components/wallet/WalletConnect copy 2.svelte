<script>
  import { onMount } from 'svelte';
  import { createWeb3Modal, defaultWagmiConfig } from '@web3modal/wagmi';
  import { mainnet, bsc } from '@wagmi/core/chains';
  import { reconnect, http, watchConnections } from '@wagmi/core';
  // import { getKycInfo, getInviteCode } from '@/api';
  // import logo from "@/assets/media/youtube_channels.jpg";
  import { writable } from 'svelte/store';

  // Define stores
  const connectWallet = writable('');
  const userInfo = writable({});
  const inviteCode = writable({});

  // Define constants




    // 1. Your WalletConnect Cloud project ID
  const projectId = "a365ccf6c502136ee70fd89768611fc2";

  // 2. Create a metadata object
  const metadata = {
    name: "degpt-demo",
    description: "Web3Modal Example",
    url: "https://web3modal.com", // origin must match your domain & subdomain
    icons: ["https://avatars.githubusercontent.com/u/37784886"],
  };

    // Define your custom chain
    const dbcTestnet = {
    id: 19850818,
    name: "dbcTestnet",
    network: "dbcTestnet",
    rpcUrls: {
      default: "https://rpc-testnet.dbcwallet.io",
    },
    nativeCurrency: {
      name: "DBC",
      symbol: "DBC",
      decimals: 18,
    },
    blockExplorers: {
      default: { name: "Blockscout", url: "https://blockscout-testnet.dbcscan.io" },
    },
    testnet: true,
  };


  const chains = [
    mainnet,
    bsc,
    dbcTestnet

  ];


  // // 3. Create wagmiConfig
  // const config = defaultWagmiConfig({
  //   chains,
  //   projectId,
  //   metadata,
  // });


  const config = defaultWagmiConfig({
    chains,
    projectId,
    metadata,
    transports: {
      [mainnet.id]: http(),
      [bsc.id]: http(),
    }
  });

  const initConnection = async () => {
    try {
      const res = await reconnect(config);
      if (res.length) {
        connectWallet.set(res[0].accounts[0]);
        try {
          // const userinfo = await getKycInfo({ wallet: res[0].accounts[0] });
          // if (userinfo.success) {
          //   userInfo.set(userinfo.data);
          // }

          // const getcode = await getInviteCode({ wallet: res[0].accounts[0] });
          // if (getcode.success) {
          //   inviteCode.set(getcode.data);
          // }
        } catch (error) {
          console.error('getKycInfo', error);
        }
      } else {
        connectWallet.set('');
        userInfo.set({});
        inviteCode.set({});
      }
    } catch (error) {
      console.error('reconnect error', error);
    }
  };

  onMount(() => {
    initConnection();
    watchConnections(config, {
      async onChange(data) {
        if (data.length) {
          connectWallet.set(data[0].accounts[0]);
          try {
            // const userinfo = await getKycInfo({ wallet: data[0].accounts[0] });
            // if (userinfo.success) {
            //   userInfo.set(userinfo.data);
            // }

            // const getcode = await getInviteCode({ wallet: data[0].accounts[0] });
            // if (getcode.success) {
            //   inviteCode.set(getcode.data);
            // }
          } catch (error) {
            console.error('getKycInfo', error);
          }
        } else {
          connectWallet.set('');
          userInfo.set({});
          inviteCode.set({});
        }
      }
    });

    createWeb3Modal({
      wagmiConfig: config,
      projectId,
      enableAnalytics: true,
      enableOnramp: true
    });
  });
</script>



<div class="walletConnect">
  <w3m-button id="web3button" label="链接钱包"/>
</div>



<!-- <style>
  :root {
    --wui-color-accent-100: linear-gradient(90deg, #03FFD2 0%, #8000FF 100%) !important;
    --wui-gray-glass-010: midnightblue !important;
    --wui-border-radius-m: 12px !important;
  }
  .walletConnect {
    // 添加你的样式
  }
</style> -->