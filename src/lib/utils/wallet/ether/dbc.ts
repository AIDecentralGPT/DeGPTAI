// dbc.js

import { ethers } from "ethers";
import { provider, signData, getCurrencyPrice, getGas } from "./utils";




// Get the current block height
export async function getCurrentBlockNumber() {
  const blockNumber = await provider.getBlockNumber();
  console.log("Current block number:", blockNumber);
  return blockNumber;
}



// Query the DBC balance of the specified account
export async function getDbcBalance(address) {


  const balanceWei = await provider.getBalance(address);
  const balanceDBC = ethers.formatUnits(balanceWei, 18);

  console.log("DBC balance:",balanceWei, balanceDBC, ethers.formatEther(balanceWei), "DBC");


  // const balanceWei = await provider.getBalance("address");
  // const balanceDBC = ethers.formatUnits(balanceWei, 18);

  // console.log("DBC balance:",balanceWei, balanceDBC, ethers.formatEther(balanceWei), "DBC");

  return balanceDBC;
}

// Transfer DBC to the designated account
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
    return txResponse;
  } catch (error) {
    console.error("Failed to send transaction:", error);
    throw error;
  }
}



