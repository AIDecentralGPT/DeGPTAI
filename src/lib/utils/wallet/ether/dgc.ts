// dgc.js

import { ethers } from "ethers";
import { getCurrencyPrice, getGas } from "./utils";
import ABI from "./abi.json";
import { getDbcBalance } from "./dbc";
import { getAccount } from "@wagmi/core";
import { config } from "$lib/utils/wallet/walletconnect/index";

// DGC 合约地址
//const DGC_TOKEN_CONTRACT_ADDRESS = '0xC260ed583545d036ed99AA5C76583a99B7E85D26'; // 旧地址
//const DGC_TOKEN_CONTRACT_ADDRESS = '0x18386F368e7C211E84324337fA8f62d5093272E1'; // 新地址
const DGC_TOKEN_CONTRACT_ADDRESS = '0x8E5e4a4d8aE3741DA073303e492B73cb913fb72D'; // 最新新地址


// XAA 合约地址
// const DGC_TOKEN_CONTRACT_ADDRESS = '0x16d83F6B17914a4e88436251589194CA5AC0f452'; // XAA地址
// DLC 合约地址
// const DGC_TOKEN_CONTRACT_ADDRESS = '0x6f8F70C74FE7d7a61C8EAC0f35A4Ba39a51E1BEe'; // DLC地址
// SIC 合约地址
// const DGC_TOKEN_CONTRACT_ADDRESS = '0x07D325030dA1A8c1f96C414BFFbe4fBD539CED45'; // SIC地址
// STID 合约地址
// const DGC_TOKEN_CONTRACT_ADDRESS = '0x2282D5DA5f39Bb7B90cef532341FBB998A1d0965'; // STID地址
// LOGO 合约地址
// const DGC_TOKEN_CONTRACT_ADDRESS = '0xD78F268291f3fe244CB965C768EDb515b529eD02'; // STID地址



// // ERC-20 ABI
// const ERC20_ABI = [
//   "function balanceOf(address owner) view returns (uint256)",
//   "function transfer(address to, uint256 amount) returns (boolean)",
//   "function symbol() view returns (string)",
//   "function decimals() view returns (uint8)"
//   // 其他你可能需要的 ERC-20 方法
// ];
// 定义 RPC URL 和 Chain ID
// const rpcUrl = "https://rpc-testnet.dbcwallet.io"; // 旧 的 RPC URL
const rpcUrl = "https://rpc1.dbcwallet.io";  // 新 的 RPC URL

// const chainId = 19850818; // 旧 的 Chain ID
const chainId = 19880818; // 新 的 Chain ID

// 创建 provider
const provider = new ethers.JsonRpcProvider(rpcUrl);


// 创建 DGC 合约实例
export const dgcContract = new ethers.Contract(DGC_TOKEN_CONTRACT_ADDRESS, ABI?.abi, provider);

// 查询 DGC 余额
export async function getDgcBalance(address) {

  const balanceWei = await dgcContract.balanceOf(address);

  const balanceDGC = ethers.formatUnits(balanceWei, 18);

  console.log("DGC balance:",balanceWei, balanceDGC, ethers.formatEther(balanceWei), "DGC");

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
    return {
      ok: false,
      msg: "DBC balance is insufficient. You need to have at least 0.01 DBC in your wallet balance."
    };
  }
  const tx = {
    to: DGC_TOKEN_CONTRACT_ADDRESS,
    value: 0,
    data: dgcContract.interface.encodeFunctionData("transfer", [toAddress, amountWei]),
    gasPrice: gasPrice, // 设置燃气价格
    // gasLimit: gasLimit
  };

  try {
    const txResponse = await wallet.sendTransaction(tx);
    return {
      ok: true,
      data: txResponse
    };
  } catch (error) {
    return {
      ok: false,
      msg: "The DGC balance is not enough to pay. You can invite a friend to obtain 3000 DGC."
    };
  }
}

// 第三方登陆转账
export async function thirdTransferDgc(address:string, toAddress:string, amountDgc) {
  const dbcBalance = await getDbcBalance(address);
  let dgcBalance = await getDgcBalance(address);
  if (parseFloat(dbcBalance) < 0.01) {
    return {ok: false, msg: "DBC balance is insufficient. You need to have at least 0.01 DBC in your wallet balance."};
  }
  if (parseFloat(dgcBalance) < amountDgc) {
    return {ok: false, msg: "The DGC balance is not enough to pay. You can invite a friend to obtain 3000 DGC."};
  }
  try {
    const account = getAccount(config);
    const provider = await account?.connector?.getProvider();
    let eprovider = new ethers.BrowserProvider(provider);
    await eprovider.send('eth_requestAccounts', []);
    let signer = await eprovider.getSigner();
    // 创建 DGC 合约实例
    const dgcContract = new ethers.Contract(DGC_TOKEN_CONTRACT_ADDRESS, ABI?.abi, signer);
    const amountWei = ethers.parseUnits(amountDgc.toString());
    const tx = await dgcContract.transfer(toAddress, amountWei);
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

// 转账 DGC 所需gasLimit
export async function tranGasLimit(walletInfo: any) {
  const wallet = new ethers.Wallet(walletInfo?.privateKey, provider);
  // 获取签名者
  const signer = wallet.connect(provider);
  const contractWithSigner = dgcContract.connect(signer);
  const amountWei = ethers.parseUnits("1");
  // 估算gas费
  const gasEstimate = await contractWithSigner.transfer.estimateGas(walletInfo?.address, amountWei);
  return gasEstimate;
}

// 获取 DGC 的实时价格
export async function getDgcPrice() {
  return getCurrencyPrice("DGC");
}
