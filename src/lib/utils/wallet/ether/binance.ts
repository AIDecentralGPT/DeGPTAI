import { ethers } from "ethers";
import ABI from "./abi.json";
import { getProvider } from "@binance/w3w-ethereum-provider";

const BINANCE_DGC_CONTRACT_ADDRESS = '0x9cfAE8067322394e34E6b734c4a3F72aCC4a7Fe5';
const rpcUrl = "https://bsc-dataseed.binance.org/";

const provider = new ethers.JsonRpcProvider(rpcUrl);

export const binanceprovider = getProvider({ chainId: 56 });

// 创建 DGC 合约实例
export const dgcContract = new ethers.Contract(BINANCE_DGC_CONTRACT_ADDRESS, ABI?.abi, provider);

// 查询 DGC 余额
export async function getBinanceDgcBalance(address: string) {

  const balanceWei = await dgcContract.balanceOf(address);

  const balanceDGC = ethers.formatUnits(balanceWei, 18);

  console.log("DGC balance:",balanceWei, balanceDGC, ethers.formatEther(balanceWei), "DGC");

  return balanceDGC;

}

// 转账
export async function binanceTransferDgc(address:string, toAddress:string, amountDgc) {
  const dgcBalance = await getBinanceDgcBalance(address);
  if (parseFloat(dgcBalance) < amountDgc) {
    return {ok: false, msg: "The DGC balance is not enough to pay. You can invite a friend to obtain 3000 DGC."};
  }
  try {
    // 使用币安的专用provider
    await binanceprovider.request({
      method: 'wallet_switchEthereumChain',
      params: [{ chainId: '0x38' }] // BSC主网
    });
    await binanceprovider.request({ method: 'eth_requestAccounts' });
    let eprovider = new ethers.BrowserProvider(binanceprovider);
    await eprovider.send('eth_requestAccounts', []);
    let signer = await eprovider.getSigner();
    // 创建 DGC 合约实例
    const binanceContract = new ethers.Contract(BINANCE_DGC_CONTRACT_ADDRESS, ABI?.abi, signer);
    const amountWei = ethers.parseUnits(amountDgc.toString());
    const tx = await binanceContract.transfer(toAddress, amountWei);
    const txResponse = await tx.wait();
    return {
      ok: true,
      data: txResponse
    };
  } catch(e) {
    console.log("===========================", e);
    return {ok: false, msg: "The DGC balance is not enough to pay. You can invite a friend to obtain 3000 DGC."};
  }
}