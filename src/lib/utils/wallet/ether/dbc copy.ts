// dbc.js

import { ethers } from "ethers";
import { provider, signData, getCurrencyPrice } from "./utils";
import ABI from "./abi.json";

console.log("ABI", ABI);


// DBC 合约地址
const DBC_TOKEN_CONTRACT_ADDRESS = '0xE9E985E88232F12F2780955f0c0b99541Aa3cf37'; // 请替换为实际地址

// // ERC-20 ABI
// const ERC20_ABI = [
//   "function balanceOf(address owner) view returns (uint256)",
//   "function transfer(address to, uint256 amount) returns (boolean)",
//   "function symbol() view returns (string)",
//   "function decimals() view returns (uint8)"
//   // 其他你可能需要的 ERC-20 方法
// ];



// 创建 DBC 合约实例
const dbcContract = new ethers.Contract(DBC_TOKEN_CONTRACT_ADDRESS, ABI, provider);

// 查询 DBC 余额
export async function getDbcBalance(address) {
  const balance = await dbcContract.balanceOf(address);
  provider.getBalance(address)
  console.log(`DBC Balance of ${address}:`, ethers.formatUnits(balance));
  return balance;
}

// 转账 DBC 到指定账户
export async function transferDbc(toAddress, amountDbc, privateKey) {
  const wallet = new ethers.Wallet(privateKey, provider);
  const amountWei = ethers.parseUnits(amountDbc.toString());

  const tx = {
    to: DBC_TOKEN_CONTRACT_ADDRESS,
    value: 0,
    data: dbcContract.interface.encodeFunctionData("transfer", [toAddress, amountWei]),
  };

  try {
    const txResponse = await wallet.sendTransaction(tx);
    console.log("Transaction sent:", txResponse);
    console.log("Transaction hash:", txResponse.hash);
    return txResponse;
  } catch (error) {
    console.error("Failed to send transaction:", error);
    throw error;
  }
}

// 获取 DBC 的实时价格
export async function getDbcPrice() {
  return getCurrencyPrice("DBC");
}
