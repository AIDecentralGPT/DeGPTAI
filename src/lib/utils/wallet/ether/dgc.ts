// dgc.js

import { ethers } from "ethers";
import {
  //  provider,
  
  signData, getCurrencyPrice, getGas } from "./utils";
import ABI from "./abi.json";
import { getDbcBalance } from "./dbc";
import { toast } from "svelte-sonner";

console.log("ABI", typeof ABI);


// DGC 合约地址
const DGC_TOKEN_CONTRACT_ADDRESS = '0x82b1a3d719dDbFDa07AD1312c3063a829e1e66F1'; // 请替换为实际地址

// // ERC-20 ABI
// const ERC20_ABI = [
//   "function balanceOf(address owner) view returns (uint256)",
//   "function transfer(address to, uint256 amount) returns (boolean)",
//   "function symbol() view returns (string)",
//   "function decimals() view returns (uint8)"
//   // 其他你可能需要的 ERC-20 方法
// ];
// 定义 RPC URL 和 Chain ID
const rpcUrl = "https://rpc-testnet.dbcwallet.io"; // 或者 DGC 的 RPC URL
const chainId = 19850818; // 或者 DGC 的 Chain ID

// 创建 provider
const provider = new ethers.JsonRpcProvider(rpcUrl);


// 创建 DGC 合约实例
export const dgcContract = new ethers.Contract(DGC_TOKEN_CONTRACT_ADDRESS, ABI?.abi, provider);

// 查询 DGC 余额
export async function getDgcBalance(address) {

  const balanceWei = await dgcContract.balanceOf(address);

  const balanceDGC = ethers.formatUnits(balanceWei, 18);

  console.log("DBC balance:",balanceWei, balanceDGC, ethers.formatEther(balanceWei), "DBC");

  return balanceDGC;
}

// 转账 DGC 到指定账户
export async function transferDgc(toAddress:string, amountDgc, privateKey) {
  const wallet = new ethers.Wallet(privateKey, provider);
  const amountWei = ethers.parseUnits(amountDgc.toString());


  const { gasLimit, gasPrice  } = await getGas();

  console.log("wallet:", wallet, gasLimit, gasPrice);
  

  // 获取钱包余额
  const dbcBalance = await getDbcBalance(wallet?.address);

  const gasNumber = ethers.formatEther(gasPrice);

  console.log("balance gasCost ", gasPrice, dbcBalance, gasNumber, );

  // 比较余额和gas费用
  if (gasNumber > dbcBalance) {
    toast.error("The DBC balance is not enough to pay gas.");
    return;
  }
  
  const tx = {
    to: DGC_TOKEN_CONTRACT_ADDRESS,
    value: 0,
    data: dgcContract.interface.encodeFunctionData("transfer", [toAddress, amountWei]),
    gasPrice: gasPrice, // 设置燃气价格
  };

  try {
    const txResponse = await wallet.sendTransaction(tx);
    return txResponse;
  } catch (error) {
    console.log("==============transferDgc=============", error) ;
    toast.error("The DGC balance is not enough to pay. You can invite a friend to obtain 6000 DGC");
    return;
  }
}




// 获取 DGC 的实时价格
export async function getDgcPrice() {
  return getCurrencyPrice("DGC");
}
