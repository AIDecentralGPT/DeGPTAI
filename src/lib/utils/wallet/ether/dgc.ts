// dgc.js

import { ethers } from "ethers";
import { provider, signData, getCurrencyPrice, getGas } from "./utils";
import ABI from "./abi.json";

console.log("ABI", typeof ABI);


// DGC 合约地址
const DGC_TOKEN_CONTRACT_ADDRESS = '0xE9E985E88232F12F2780955f0c0b99541Aa3cf37'; // 请替换为实际地址

// // ERC-20 ABI
// const ERC20_ABI = [
//   "function balanceOf(address owner) view returns (uint256)",
//   "function transfer(address to, uint256 amount) returns (boolean)",
//   "function symbol() view returns (string)",
//   "function decimals() view returns (uint8)"
//   // 其他你可能需要的 ERC-20 方法
// ];


// 创建 DGC 合约实例
const dgcContract = new ethers.Contract(DGC_TOKEN_CONTRACT_ADDRESS, ABI?.abi, provider);

// 查询 DGC 余额
export async function getDgcBalance(address) {
  const balanceWei = await dgcContract.balanceOf(address);

  const balanceDGC = ethers.formatUnits(balanceWei, 18);

  console.log("DBC balance:",balanceWei, balanceDGC, ethers.formatEther(balanceWei), "DBC");


  return balanceDGC;
}

// 转账 DGC 到指定账户
export async function transferDgc(toAddress, amountDgc, privateKey) {
  const wallet = new ethers.Wallet(privateKey, provider);
  const amountWei = ethers.parseUnits(amountDgc.toString());


  const { gasLimit, gasPrice  } = await getGas();


  const tx = {
    to: DGC_TOKEN_CONTRACT_ADDRESS,
    value: 0,
    data: dgcContract.interface.encodeFunctionData("transfer", [toAddress, amountWei]),
    // gasLimit: gasLimit,
    // gasPrice: gasPrice,

    gasPrice: ethers.parseUnits('50', 'gwei'), // 设置燃气价格
    // gasLimit: ethers.hexlify(21000) // 设置燃气限制

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

// 获取 DGC 的实时价格
export async function getDgcPrice() {
  return getCurrencyPrice("DGC");
}
