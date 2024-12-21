import { ethers } from "ethers";
import {
  http,
  signMessage,
  getChainId,
  switchChain
} from "@wagmi/core";

import { defaultWagmiConfig } from "@web3modal/wagmi";

// import { provider, signData, getCurrencyPrice, getGas } from "../ether/utils";
// const rpcUrl = "https://rpc-testnet.dbcwallet.io"; // 旧 的 RPC URL
const rpcUrl = "https://rpc.dbcwallet.io"; // 新得 的 RPC URL
const provider = new ethers.JsonRpcProvider(rpcUrl);

import ABI from "../ether/abi.json";
// const DGC_TOKEN_CONTRACT_ADDRESS = "0x82b1a3d719dDbFDa07AD1312c3063a829e1e66F1"; // 旧合约地址
const DGC_TOKEN_CONTRACT_ADDRESS = '0x04024865D3ba51e9c2F4adDd7A20AA0dA496309A'; // 新合约地址

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

// 1. Define constants
export const projectId = "59443aa943b8865491317c04a19a8be3";

// 2. Create wagmiConfig
const metadata = {
  name: "degpt",
  description: "Web3Modal Example",
  url: "https://web3modal.com",
  icons: ["https://avatars.githubusercontent.com/u/37784886"],
};

// id: 19850818,
const dbcTestnet = {
  id: 19880818,
  name: "dbcTestnet",
  nativeCurrency: {
    name: "DBC",
    symbol: "DBC",
    decimals: 18,
  },
  // network: "dbcTestnet",
  rpcUrls: {
    default: { http: ["https://rpc.dbcwallet.io"] },
  },

  blockExplorers: {
    default: {
      name: "Blockscout",
      url: "https://testnet.dbcscan.io", //https://blockscout-testnet.dbcscan.io
    },
  },
};

const chains: any = [ dbcTestnet ];

export const config = defaultWagmiConfig({
  projectId,
  chains,
  metadata,
  transports: {
    [dbcTestnet.id]: http("https://rpc.dbcwallet.io"),
  },
});
