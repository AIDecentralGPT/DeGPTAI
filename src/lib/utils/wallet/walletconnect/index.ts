import { ethers } from "ethers";
import {
  reconnect,
  http,
  watchConnections,
  sendTransaction,
  signMessage,
  disconnect,
  getAccount,
  watchAccount,
  getChainId,
  switchChain,
} from "@wagmi/core";
import { defaultWagmiConfig } from "@web3modal/wagmi";
import { mainnet, bsc } from "@wagmi/core/chains";
import { openProServices } from "$lib/apis/users";
import { toast } from "svelte-sonner";


// import { provider, signData, getCurrencyPrice, getGas } from "../ether/utils";
const rpcUrl = "https://rpc-testnet.dbcwallet.io"; // 或者 DGC 的 RPC URL
const provider = new ethers.JsonRpcProvider(rpcUrl);

import ABI from "../ether/abi.json";
const DGC_TOKEN_CONTRACT_ADDRESS = '0xE9E985E88232F12F2780955f0c0b99541Aa3cf37'; // 请替换为实际地址
// 创建 DGC 合约实例
 const dgcContract = new ethers.Contract(DGC_TOKEN_CONTRACT_ADDRESS, ABI?.abi, provider);

// export const signDemoMessage = async () => {
//   try {
//     const message = "This is a demo message.";
//     const signature = await signMessage(config, { message });
//     console.log("Signature:", signature);
//   } catch (error) {
//     console.error("Sign Message Error:", error);
//   }
// };

// export const sendDemoTransaction = async () => {
//   try {
//     // const transactionParameters = {
//     //   to: '0xde184A6809898D81186DeF5C0823d2107c001Da2',
//     //   value: ethers.parseEther("0.01"),
//     //   // gasLimit: ethers.hexlify(21000),
//     //   // gasPrice: ethers.hexlify(ethers.parseUnits('10', 'gwei'))
//     // };
//     // const tx = await sendTransaction(config, transactionParameters);

//     const transactionParameters = {
//       to: "0xde184A6809898D81186DeF5C0823d2107c001Da2", // 替换为实际接收方地址
//       value: BigInt(ethers.parseUnits("0.01", "ether").toString()), // 发送的金额，单位是ether
//     };
//     const tx = await sendTransaction(config, {
//       to: transactionParameters.to,
//       value: transactionParameters.value, // 发送的金额，转换为bigint
//       // gasLimit: BigInt(ethers.hexlify(21000)), // 设置gas limit，转换为bigint
//       // gasPrice: BigInt(ethers.parseUnits('10', 'gwei').toString()) // 设置gas price，转换为bigint
//     });

//     console.log("Transaction:", tx);
//   } catch (error) {
//     console.error("Send Transaction Error:", error);
//   }
// };



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


export const   walletconnectSendTransaction = async ({
  value
}: any) => {



// 在应用启动时调用
connectToTestnet();

  try {
    const transactionParameters = {
      to: "0xf3851DE68b2Ac824B1D4c85878df76e7cE2bD808", // 替换为实际接收方地址
      value: BigInt(ethers.parseUnits(String(value), "ether").toString()), // 发送的金额，单位是ether
    };
    const tx = await sendTransaction(config, {
      to: transactionParameters.to,
      value: transactionParameters.value, // 发送的金额，转换为bigint
      // gasLimit: BigInt(ethers.hexlify(21000)), // 设置gas limit，转换为bigint
      // gasPrice: BigInt(ethers.parseUnits('10', 'gwei').toString()) // 设置gas price，转换为bigint
    });

    console.log("Transaction:", tx);
    // Transaction: 0x203634242ee3f126b90dcf8bae455eeadf2c2ca37e30fffa17e192efddc9539a

   const res = await  openProServices(
      localStorage.token,
      tx,
   value,
    );



    console.log("openProServices res", res);
    return res



  } catch (error) {
    console.error("Send Transaction Error:", error);
  }
};



// 定义发送 DGC 的函数
export const walletconnectSendDGCTransaction = async (value:number) => {
  // 在应用启动时调用
  await connectToTestnet();

  try {
    const transactionParameters = {
      to: "0xf3851DE68b2Ac824B1D4c85878df76e7cE2bD808", // 替换为实际接收方地址
      value: BigInt(ethers.parseUnits(String(value), "ether").toString()), // 发送的金额，单位是ether
    };
    

    const tx = await dgcContract.transfer(transactionParameters.to, ethers.parseUnits(String(value), 18));
    console.log("Transaction:", tx);

    const receipt = await tx.wait();
    console.log("Transaction receipt:", receipt);

    // const res = await openProServices(localStorage.token, tx, value);
    // console.log("openProServices res", res);
    // return res;
  } catch (error) {
    console.error("Send DGC Transaction Error:", error);
  }
};




  // 定义常量
 export  const projectId = "a365ccf6c502136ee70fd89768611fc2";

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
      default: {
        name: "Blockscout",
        url: "https://blockscout-testnet.dbcscan.io",
      },
    },
    testnet: true,
  };

  const chains = [dbcTestnet, mainnet, bsc];

  export const config = defaultWagmiConfig({
    chains,
    projectId,
    metadata,
    transports: {
      [mainnet.id]: http(),
      [bsc.id]: http(),
      [dbcTestnet.id]: http(),
    },
  });