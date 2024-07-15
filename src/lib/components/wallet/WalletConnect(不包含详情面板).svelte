<script>
  import { onMount } from 'svelte';
  import { writable } from 'svelte/store';
  import { createWeb3Modal, defaultWagmiConfig } from '@web3modal/wagmi';
  import { mainnet, bsc } from '@wagmi/core/chains';
  import { reconnect, http, watchConnections, sendTransaction, signMessage } from '@wagmi/core';
  import { ethers } from 'ethers';
  import { provider } from '$lib/utils/wallet/ether/utils';
  import { threesideAccount } from '$lib/stores';
  import DbcThreeSideWalletDetail from './DbcThreeSideWalletDetail.svelte';

  // 定义存储
  const walletAddress = writable('');
  const walletBalance = writable(0);

  // 定义常量
  const projectId = "a365ccf6c502136ee70fd89768611fc2";

  const metadata = {
    name: "degpt-demo",
    description: "Web3Modal Example",
    url: "https://web3modal.com",
    icons: ["https://avatars.githubusercontent.com/u/37784886"],
  };

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
    dbcTestnet,
    mainnet,
    bsc,
  ];

  const config = defaultWagmiConfig({
    chains,
    projectId,
    metadata,
    transports: {
      [mainnet.id]: http(),
      [bsc.id]: http(),
      [dbcTestnet.id]: http(),
    }
  });

  const signDemoMessage = async () => {
    try {
      const message = "This is a demo message.";
      const signature = await signMessage(config, { message });
      console.log('Signature:', signature);
    } catch (error) {
      console.error('Sign Message Error:', error);
    }
  };

  const sendDemoTransaction = async () => {
    try {
      // const transactionParameters = {
      //   to: '0xde184A6809898D81186DeF5C0823d2107c001Da2',
      //   value: ethers.parseEther("0.01"),
      //   // gasLimit: ethers.hexlify(21000),
      //   // gasPrice: ethers.hexlify(ethers.parseUnits('10', 'gwei'))
      // };
      // const tx = await sendTransaction(config, transactionParameters);



      const transactionParameters = {
        to: '0xde184A6809898D81186DeF5C0823d2107c001Da2', // 替换为实际接收方地址
        value: BigInt(ethers.parseUnits("0.01", "ether").toString()), // 发送的金额，单位是ether
      };
      const tx = await sendTransaction(config, {
        to: transactionParameters.to,
        value: transactionParameters.value, // 发送的金额，转换为bigint
      // gasLimit: BigInt(ethers.hexlify(21000)), // 设置gas limit，转换为bigint
      // gasPrice: BigInt(ethers.parseUnits('10', 'gwei').toString()) // 设置gas price，转换为bigint

      });



      console.log('Transaction:', tx);
    } catch (error) {
      console.error('Send Transaction Error:', error);
    }
  };

  const getBalance = async (address) => {
    try {
      const balance = await provider.getBalance(address);
      console.log("balance", balance);
      // walletBalance.set(ethers.formatEther(balance));
    } catch (error) {
      console.error('Get Balance Error:', error);
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
        threesideAccount.update((prev) => {
          return {
            // ...prev,
            address,
          };
        });
        // // walletAddress.set(address);
        await getBalance(address);
      } else {
        // walletAddress.set('');
        // walletBalance.set(0);
      }
    } catch (error) {
      console.error('Reconnect Error:', error);
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
          walletAddress.set('');
          walletBalance.set(0);
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

<DbcThreeSideWalletDetail></DbcThreeSideWalletDetail>

  <w3m-button id="web3button" label="链接钱包"  style="width: 100%;" />

  

  <!-- <button on:click={signDemoMessage}>Sign Message</button>
  <button on:click={sendDemoTransaction}>Send Transaction</button> -->
  <!-- <button on:click={calculateGasFee}>Calculate Gas Fee</button> -->
</div>

<style>
  :root {
    --wui-color-accent-100: linear-gradient(90deg, #03FFD2 0%, #8000FF 100%) !important;
    --wui-gray-glass-010: midnightblue !important;
    --wui-border-radius-m: 12px !important;
  }
  .walletConnect {
  }
  button {
    margin: 10px 16px;
    width: 100%;

  }
</style>
