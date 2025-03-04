// dgc.js

import { ethers } from "ethers";
import {
  //  provider,
  
  signData, getCurrencyPrice, getGas } from "./utils";
import ABI from "./abi.json";
import { getDbcBalance } from "./dbc";
import { toast } from "svelte-sonner";

// DGC contract address
//const DGC_TOKEN_CONTRACT_ADDRESS = '0xC260ed583545d036ed99AA5C76583a99B7E85D26'; // Old address
const DGC_TOKEN_CONTRACT_ADDRESS = '0x18386F368e7C211E84324337fA8f62d5093272E1'; // new address

// XAA contract address
// const DGC_TOKEN_CONTRACT_ADDRESS = '0x16d83F6B17914a4e88436251589194CA5AC0f452'; // XAA address
// DLC contract address
// const DGC_TOKEN_CONTRACT_ADDRESS = '0x6f8F70C74FE7d7a61C8EAC0f35A4Ba39a51E1BEe'; // DLC address
// SIC contract address
// const DGC_TOKEN_CONTRACT_ADDRESS = '0x07D325030dA1A8c1f96C414BFFbe4fBD539CED45'; // SIC address

// // ERC-20 ABI
// const ERC20_ABI = [
//   "function balanceOf(address owner) view returns (uint256)",
//   "function transfer(address to, uint256 amount) returns (boolean)",
//   "function symbol() view returns (string)",
//   "function decimals() view returns (uint8)"
//   // Other ERC-20 methods you may need
// ];
// Define RPC URL and Chain ID
// const rpcUrl = "https://rpc-testnet.dbcwallet.io"; // Old RPC URL
const rpcUrl = "https://rpc.dbcwallet.io";  // New RPC URL

// const chainId = 19850818; // Old Chain ID
const chainId = 19880818; // New Chain ID

// Create provider
const provider = new ethers.JsonRpcProvider(rpcUrl);


// Create DGC contract instance
export const dgcContract = new ethers.Contract(DGC_TOKEN_CONTRACT_ADDRESS, ABI?.abi, provider);

// Query DGC balance
export async function getDgcBalance(address) {

  const balanceWei = await dgcContract.balanceOf(address);

  const balanceDGC = ethers.formatUnits(balanceWei, 18);

  console.log("DGC balance:",balanceWei, balanceDGC, ethers.formatEther(balanceWei), "DGC");

  return balanceDGC;
}

// Transfer DGC to the designated account
export async function transferDgc(toAddress:string, amountDgc, privateKey) {
  const wallet = new ethers.Wallet(privateKey, provider);
  const amountWei = ethers.parseUnits(amountDgc.toString());


  const { gasLimit, gasPrice  } = await getGas();

  console.log("wallet:", wallet, gasLimit, gasPrice);
  

  // Get wallet balance
  const dbcBalance = await getDbcBalance(wallet?.address);

  const gasNumber = ethers.formatEther(gasPrice);

  console.log("balance gasCost ", gasPrice, dbcBalance, gasNumber, );

  // Compare balance and gas cost
  if (gasNumber > dbcBalance) {
    toast.error("The DBC balance is not enough to pay gas.");
    return;
  }
  const tx = {
    to: DGC_TOKEN_CONTRACT_ADDRESS,
    value: 0,
    data: dgcContract.interface.encodeFunctionData("transfer", [toAddress, amountWei]),
    gasPrice: gasPrice, // Set gas prices
    // gasLimit: gasLimit
  };

  try {
    const txResponse = await wallet.sendTransaction(tx);
    console.log("========================", txResponse);
    return txResponse;
  } catch (error) {
    console.log("==============transferDgc=============", error) ;
    toast.error("The DGC balance is not enough to pay. You can invite a friend to obtain 6000 DGC");
    return;
  }
}

// Gas Limit Required for DGC Transfer
export async function tranGasLimit(walletInfo: any) {
  const wallet = new ethers.Wallet(walletInfo?.privateKey, provider);
  // Obtain signer
  const signer = wallet.connect(provider);
  const contractWithSigner = dgcContract.connect(signer);
  const amountWei = ethers.parseUnits("1");
  // Estimate gas cost
  const gasEstimate = await contractWithSigner.transfer.estimateGas(walletInfo?.address, amountWei);
  return gasEstimate;
}

// Get real-time prices for DGC
export async function getDgcPrice() {
  return getCurrencyPrice("DGC");
}
