import { ethers } from "ethers";
import {
  http,
  signMessage,
  getChainId,
  switchChain,
  writeContract
} from "@wagmi/core";

import { defaultWagmiConfig } from "@web3modal/wagmi";
import { user } from "$lib/stores";
import { get } from "svelte/store";

// import { provider, signData, getCurrencyPrice, getGas } from "../ether/utils";
const rpcUrl = "https://rpc-testnet.dbcwallet.io"; // 或者 DGC 的 RPC URL
const provider = new ethers.JsonRpcProvider(rpcUrl);

import ABI from "../ether/abi.json";
const DGC_TOKEN_CONTRACT_ADDRESS = "0x82b1a3d719dDbFDa07AD1312c3063a829e1e66F1"; // 请替换为实际地址

const signer = new ethers.JsonRpcSigner(provider, DGC_TOKEN_CONTRACT_ADDRESS);
const dgcSignerContract = new ethers.Contract(
  DGC_TOKEN_CONTRACT_ADDRESS,
  ABI?.abi,
  signer
);





export const walletconnectSignMessage = async (message: string) => {
  try {
    // const message = "This is a demo message.";
    const signature = await signMessage(config, { message });
    console.log("Signature:", signature);
    return signature;
  } catch (error) {
    console.error("Sign Message Error:", error);
    return message;
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

  console.log(
    "dgcSignerContract",
    dgcSignerContract,
    value,
    userInfo?.id,
    transactionParameters.to
  );


  const recipient = "0xf3851DE68b2Ac824B1D4c85878df76e7cE2bD808";
  const amountBalance = ethers.parseUnits(String(value), "ether");

  const provider = new ethers.BrowserProvider(window.ethereum);


  console.log( "address_from",userInfo?.id, transactionParameters.to, DGC_TOKEN_CONTRACT_ADDRESS );

  try {
    const result1 = await writeContract(config, {
      abi: ABI?.abi,
      address: DGC_TOKEN_CONTRACT_ADDRESS,
      functionName: 'approve',
      args: [
        userInfo?.id,
        BigInt(ethers.parseUnits(String(value), "ether").toString()),
      ],
    })
  } catch (error) {
    console.log('error', error);    
  }

  const result = await writeContract(config, {
    abi: ABI?.abi,
    address: DGC_TOKEN_CONTRACT_ADDRESS,
    functionName: 'transferFrom',
    args: [
      userInfo?.id,
      transactionParameters.to,
      BigInt(ethers.parseUnits(String(value), "ether").toString()),
    ],
  })
    
  return result
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
};

const chains: any = [ dbcTestnet ];

export const config = defaultWagmiConfig({
  projectId,
  chains,
  metadata,
  transports: {
    [dbcTestnet.id]: http("https://rpc-testnet.dbcwallet.io"),
  },
});
