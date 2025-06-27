// dbc.js

import { ethers } from "ethers";
import { provider, signData, getCurrencyPrice, getGas } from "./utils";




// 获取当前区块高度
export async function getCurrentBlockNumber() {
  const blockNumber = await provider.getBlockNumber();
  console.log("Current block number:", blockNumber);
  return blockNumber;
}



// 查询指定账户的 DBC 余额
export async function getDbcBalance(address) {


  const balanceWei = await provider.getBalance(address);
  const balanceDBC = ethers.formatUnits(balanceWei, 18);

  console.log("DBC balance:",balanceWei, balanceDBC, ethers.formatEther(balanceWei), "DBC");


  // const balanceWei = await provider.getBalance("address");
  // const balanceDBC = ethers.formatUnits(balanceWei, 18);

  // console.log("DBC balance:",balanceWei, balanceDBC, ethers.formatEther(balanceWei), "DBC");

  return balanceDBC;
}

// 转账 DBC 到指定账户
export async function transferDbc(toAddress, amountDbc, privateKey) {
  const wallet = new ethers.Wallet(privateKey, provider);
  const amountWei = ethers.parseUnits(amountDbc.toString());
  const { gasLimit, gasPrice  } = await getGas();

  const tx = {
    to: toAddress,
    value: amountWei,
    gasLimit: gasLimit,
    gasPrice: gasPrice,

  };
  
  console.log("tx", tx);

  try {
    const txResponse = await wallet.sendTransaction(tx);
    console.log("Transaction sent:", txResponse);
    console.log("Transaction hash:", txResponse.hash);
    return {
      ok: true,
      data: txResponse
    };
  } catch (error) {
    console.error("Failed to send transaction:", error);
    return {
      ok: false,
      msg: "Failed to send transaction !"
    };
  }
}



