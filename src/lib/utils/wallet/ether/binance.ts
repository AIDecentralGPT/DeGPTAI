import { ethers } from "ethers";
import ABI from "./abi.json";

const BINANCE_DGC_CONTRACT_ADDRESS = '0x9cfAE8067322394e34E6b734c4a3F72aCC4a7Fe5';
const rpcUrl = "https://bsc-dataseed.binance.org/";

const provider = new ethers.JsonRpcProvider(rpcUrl);


// 创建 DGC 合约实例
export const dgcContract = new ethers.Contract(BINANCE_DGC_CONTRACT_ADDRESS, ABI?.abi, provider);

// 查询 DGC 余额
export async function getBinanceDgcBalance(address) {

  const balanceWei = await dgcContract.balanceOf(address);

  const balanceDGC = ethers.formatUnits(balanceWei, 18);

  console.log("DGC balance:",balanceWei, balanceDGC, ethers.formatEther(balanceWei), "DGC");

  return balanceDGC;

}