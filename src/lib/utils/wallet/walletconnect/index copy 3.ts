import { ethers } from "ethers";
import {
  reconnect,
  http,
  watchConnections,
  sendTransaction,
  signMessage,
  disconnect,getConnections,
  getAccount,
  watchAccount,
  getChainId,
  switchChain,
  createConfig
} from "@wagmi/core";
import { parseEther } from 'viem'

import { writeContract } from "@wagmi/core";


import { mainnet, bsc, sepolia } from "@wagmi/core/chains";
import { openProServices } from "$lib/apis/users";
import { user, showSidebar } from "$lib/stores";
import { get } from "svelte/store";

import { toast } from "svelte-sonner";

// import { provider, signData, getCurrencyPrice, getGas } from "../ether/utils";
const rpcUrl = "https://rpc-testnet.dbcwallet.io"; // 或者 DGC 的 RPC URL
const provider = new ethers.JsonRpcProvider(rpcUrl);

import ABI from "../ether/abi.json";
import { transferDLC } from "../dbc";
import { defaultWagmiConfig } from "@web3modal/wagmi";
const DGC_TOKEN_CONTRACT_ADDRESS = "0x82b1a3d719dDbFDa07AD1312c3063a829e1e66F1"; // 请替换为实际地址
// 创建 DGC 合约实例
const dgcContract = new ethers.Contract(
  DGC_TOKEN_CONTRACT_ADDRESS,
  ABI?.abi,
  provider
);
// const signer = new ethers.JsonRpcSigner(provider, DGC_TOKEN_CONTRACT_ADDRESS);
// const dgcSignerContract = new ethers.Contract(
//   DGC_TOKEN_CONTRACT_ADDRESS,
//   ABI?.abi,
//   signer
// );

// const signer1 = provider.getSigner();
// console.log("signer", signer, signer1);

// const erc20_rw = new ethers.Contract(
//   DGC_TOKEN_CONTRACT_ADDRESS,
//   ABI?.abi,
//   signer
// );

export const walletconnectSignMessage = async (message: string) => {
  try {
    // const message = "This is a demo message.";
    const signature = await signMessage(config, { message });
    console.log("Signature:", signature);
    return signature;
  } catch (error) {
    console.error("Sign Message Error:", error);
  }
};

// 自动连接到测试网
const connectToTestnet = async () => {
  try {
    const chainId = await getChainId(config);
    console.log("getChainId", chainId);

    if (chainId !== dbcTestnet.id) {
      console.log("Switching to the testnet...");
      await switchChain(config, { chainId: dbcTestnet.id });
    }
    console.log("Connected to the testnet.");
  } catch (error) {
    console.error("Failed to switch to the testnet:", error);
  }
};

// 定义发送 DGC 的函数
export const walletconnectSendDGCTransaction = async (value: number) => {
  // 在应用启动时调用
  await connectToTestnet();

  // const tx = await dgcContract.transfer(transactionParameters.to, ethers.parseUnits(String(value), 18));
  const transactionParameters = {
    to: "0xf3851DE68b2Ac824B1D4c85878df76e7cE2bD808", // 替换为实际接收方地址
    value: BigInt(ethers.parseUnits(String(value), "ether").toString()), // 发送的金额，单位是ether
  };
  const userInfo = get(user);

  // console.log(
  //   "dgcSignerContract",
  //   dgcSignerContract,
  //   value,
  //   userInfo.id,
  //   transactionParameters.to
  // );
  const connections = getConnections(config)

  console.log("connections[0]?.connector",connections,  connections[connections.length-1]?.connector);
  

  const result = await sendTransaction(config, {
    connector: connections[connections.length-1]?.connector, 
    to: '0xf3851DE68b2Ac824B1D4c85878df76e7cE2bD808',
    value: parseEther('0.01'),
  })

  console.log("result", result);
  
  


  

};

// 1. Define constants
export const projectId = "59443aa943b8865491317c04a19a8be3";
// 2. Create wagmiConfig
const metadata = {
  name: "degpt",
  description: "Web3Modal Example",
  url: "https://web3modal.com",
  icons: ["https://avatars.githubusercontent.com/u/37784886"],
};

const dbcTestnet = {
  id: 19850818,
  name: "dbcTestnet",
  nativeCurrency: {
    name: "DBC",
    symbol: "DBC",
    decimals: 18,
  },
  // network: "dbcTestnet",
  rpcUrls: {
    default: { http: ["https://rpc-testnet.dbcwallet.io"] },
  },

  blockExplorers: {
    default: {
      name: "Blockscout",
      url: "https://blockscout-testnet.dbcscan.io",
    },
  },
  // testnet: true,
};

// const chains = [
//   mainnet, bsc,
//   // dbcTestnet,
// ];

// export const config = defaultWagmiConfig({
//   chains,
//   projectId,
//   metadata,
//   transports: {
//     //     [mainnet.id]: http(),
//     // [sepolia.id]: http(),

//     [mainnet.id]: http(),
//     [bsc.id]: http(),
//     // [dbcTestnet.id]: http("https://rpc-testnet.dbcwallet.io"),
    
//   },
// });



export const config = createConfig({
  chains: [dbcTestnet],
  transports: {
    [dbcTestnet.id]: http("https://rpc-testnet.dbcwallet.io"),
  },
})

