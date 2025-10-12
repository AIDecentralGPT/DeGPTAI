import { ethers } from "ethers";
import ABI from "./abi.json";
import { getProvider } from "@binance/w3w-ethereum-provider";
import { utf8ToHex } from "@binance/w3w-utils";

const BINANCE_DGC_CONTRACT_ADDRESS = '0x9cfAE8067322394e34E6b734c4a3F72aCC4a7Fe5';
const rpcUrl = "https://bsc-dataseed.binance.org/";

const provider = new ethers.JsonRpcProvider(rpcUrl);

export const binanceprovider = getProvider({ chainId: 56 });

// 创建 DGC 合约实例
export const dgcContract = new ethers.Contract(BINANCE_DGC_CONTRACT_ADDRESS, ABI?.abi, provider);


// 查询 BNB 余额
export async function getBinanceBnbBalance(address: string) {

  const balanceWei = await provider.getBalance(address);

  const balanceBNB = ethers.formatUnits(balanceWei, 18);

  console.log("BNB balance:",balanceWei, balanceBNB, ethers.formatEther(balanceWei), "BNB");

  return balanceBNB;

}


// 查询 DGC 余额
export async function getBinanceDgcBalance(address: string) {

  const balanceWei = await dgcContract.balanceOf(address);

  const balanceDGC = ethers.formatUnits(balanceWei, 18);

  console.log("DGC balance:", balanceWei, balanceDGC, ethers.formatEther(balanceWei), "DGC");

  return balanceDGC;

}

// 转账
export async function binanceTransferDgc(address: string, toAddress: string, amountDgc) {
  const dgcBalance = await getBinanceDgcBalance(address);
  if (parseFloat(dgcBalance) < amountDgc) {
    return { ok: false, msg: "The DGC balance is not enough to pay. You can invite a friend to obtain 3000 DGC." };
  }
  try {
    await signMessage(address);
    // 请求账户授权
    await binanceprovider.request({ method: 'eth_requestAccounts' });
    // 格式化转账金额
    const amountWei = ethers.parseUnits(amountDgc.toString());  
    // 发起转账
    const txResponse = await binanceprovider.request({
      method: "eth_sendTransaction",
      params: [
        {
          from: address,
          to: BINANCE_DGC_CONTRACT_ADDRESS,
          data: dgcContract.interface.encodeFunctionData("transfer", [toAddress, amountWei]),
          gas: "0x19023",
          value: 0
        },
      ],
    });
    console.log("==============================", txResponse)
    return {
      ok: true,
      data: txResponse
    };
  } catch (e) {
    console.log("===========================", e);
    return { ok: false, msg: "The DGC balance is not enough to pay. You can invite a friend to obtain 3000 DGC." };
  }
}

const signMessage = async (address: string) => {
    const message = "hello world";
    try {
      const res = await binanceprovider.request({
        method: "personal_sign",
        params: [utf8ToHex(message), address],
      });
      console.log("🚀 ~ signMessage ~ res:", res);
    } catch (error) {
      throw error;
    }
  };