import { ethers } from "ethers";
import ABI from "./abi.json";
import { createConfig, http, sendTransaction } from '@wagmi/core';
import { mainnet, bsc } from '@wagmi/core/chains';
import { injected } from '@wagmi/connectors';

const BINANCE_DGC_CONTRACT_ADDRESS = '0x9cfAE8067322394e34E6b734c4a3F72aCC4a7Fe5';
const rpcUrl = "https://bsc-dataseed.binance.org/";

const provider = new ethers.JsonRpcProvider(rpcUrl);

// 创建配置
export const bnbconfig = createConfig({
  chains: [mainnet, bsc],
  transports: {
    [mainnet.id]: http(),
    [bsc.id]: http(),
  },
  connectors: [
    injected({
      target: 'metaMask', // 明确声明目标钱包，增强兼容性
    }),
  ],
});

// 创建 DGC 合约实例
export const dgcContract = new ethers.Contract(BINANCE_DGC_CONTRACT_ADDRESS, ABI?.abi, provider);


// 查询 BNB 余额
export async function getBinanceBnbBalance(address: string) {

  const balanceWei = await provider.getBalance(address);

  const balanceBNB = ethers.formatUnits(balanceWei, 18);

  console.log("BNB balance:", balanceWei, balanceBNB, ethers.formatEther(balanceWei), "BNB");

  return balanceBNB;

}


// 查询 DGC 余额
export async function getBinanceDgcBalance(address: string) {

  const balanceWei = await dgcContract.balanceOf(address);

  const balanceDGC = ethers.formatUnits(balanceWei, 18);

  console.log("DGC balance:", balanceWei, balanceDGC, ethers.formatEther(balanceWei), "DGC");

  return balanceDGC;

}

// binance转账
export async function binanceTransferDgc(address: string, toAddress: string, amountDgc) {
  try {
    // 校验余额是否充足
    const dgcBalance = await getBinanceDgcBalance(address);
    if (parseFloat(dgcBalance) < amountDgc) {
      return { ok: false, msg: "The DGC balance is not enough to pay. You can invite a friend to obtain 3000 DGC." };
    }

    // 格式化转账金额
    const amountWei = ethers.parseUnits(amountDgc.toString());
    const data = new ethers.Interface(ABI?.abi).encodeFunctionData('transfer', [toAddress, amountWei]);
    const txResponse = await sendTransaction(bnbconfig, {
      to: BINANCE_DGC_CONTRACT_ADDRESS,
      data: data,
      gas: 50000
    });
    return {
      ok: true,
      data: { hash: txResponse }
    };
  } catch (e) {
    console.log("===========================", e);
    return { ok: false, msg: "Failed to send transaction !" };
  }
}