// utils.js
import { ethers } from "ethers";
import { printSignIn, walletSignIn } from "$lib/apis/auths";
import { isPro } from "$lib/apis/users";
import { chats, user } from "$lib/stores";
import { getChatList } from "$lib/apis/chats";
import { updateWalletData } from "../walletUtils";
import dayjs from 'dayjs';
import { Base64 } from 'js-base64';

// Define RPC URL and Chain ID
// const rpcUrl = "https://rpc-testnet.dbcwallet.io"; // Old RPC URL
const rpcUrl = "https://rpc.dbcwallet.io"; // New RPC URL
// const chainId = 19850818; // Old Chain ID
const chainId = 19880818; // New Chain ID

// Create provider
const provider = new ethers.JsonRpcProvider(rpcUrl);

// Signature data
export async function signData(data, privateKey) {
  const wallet = new ethers.Wallet(privateKey, provider);
  const dataBytes = ethers.toUtf8Bytes(data);
  const signature = await wallet.signMessage(dataBytes);
  console.log("Data:", data);
  console.log("Signature:", signature);
  return signature;
}

// Real time price inquiry
export async function getCurrencyPrice(currency) {
  // This is a virtual price query example, which requires calling the real price API for actual use
  const price = 2.5; // Assuming the price is 2.5
  console.log(`Current ${currency} price:`, price, "USD");
  return price;
}

// Encrypt the wallet and save it to localStorage
export async function storeWallet(wallet, password) {
  console.log("wallet", wallet, password);

  const keystore = await wallet.encrypt(password);
  console.log("Encrypted Keystore file:", keystore);
  return keystore;
}

// From localStorage Load and decrypt the wallet in the middle
export async function loadWallet(password) {
  const json = localStorage.getItem("ethereum_wallet");
  const wallet = await ethers.Wallet.fromEncryptedJson(json, password);
  return wallet;
}

// loadWallet('your_password').then(wallet => {
//   console.log('Address:', wallet.address);
// });

// Create a new wallet account
export async function createAccount(password: string) {
  const wallet = ethers.Wallet.createRandom();
  console.log("New DBC account created:");
  console.log("Address:", wallet.address);
  console.log("Private Key:", wallet.privateKey);
  console.log("Mnemonic Mnemonic words:", wallet.mnemonic.phrase); // Prompt users to backup this mnemonic word

  // const ethAddress = '0x82b1a3d719dDbFDa07AD1312c3063a829e1e66F1';
  // const balance = await provider.getBalance(ethAddress);
  // const ethValue = ethers.formatEther(balance);

  //       // const ethValue = ethers.formatEther(balance);
  //       console.log("On chain balance", balance);

  // Set password to encrypt Keystore files
  const keystore = await storeWallet(wallet, password);

  return {
    wallet, // Wallet Object
    keystore, // Encrypted Keystore file
    accountPrivateKey: wallet.privateKey,
  };
}

// Download Wallet Json
export function downloadKeyStore(keyStoreStr: string) {
  console.log("keyStoreStr", keyStoreStr);

  const blob = new Blob([JSON.stringify(keyStoreStr)], {
    type: "application/json",
  });
  const url = URL.createObjectURL(blob);

  const link = document.createElement("a");
  link.href = url;
  const currentDate = dayjs();
  const dateTime = currentDate.format('YYYYMMDDHHmm');
  link.download = "keystore_degpt_" + dateTime + ".json";
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);

  // console.log("Generated Wallet:", json);
}

// Import from encrypted JSON Keystore file
async function importFromEncryptedJson(json, password) {
  const wallet = await ethers.Wallet.fromEncryptedJson(json, password);
  console.log("Imported Wallet Address:", wallet.address);
  return wallet;
}

// Signature message
async function signMessage(wallet, message) {
  const signature = await wallet.signMessage(message);
  console.log("Signature:", signature);
  return signature;
}

// verify signature
function verifyMessage(message, signature) {
  const recoveredAddress = ethers.utils.verifyMessage(message, signature);
  console.log("Recovered Address:", recoveredAddress);
  return recoveredAddress;
}

// --------Wallet login------------
// User Signature Challenge
export async function signChallenge(wallet, challenge) {
  const walletWithProvider = new ethers.Wallet(
    wallet.privateKey,
    new ethers.JsonRpcProvider()
  );
  const signature = await walletWithProvider.signMessage(challenge);
  return signature;
}

// Example Verification Signature Function
export async function verifySignature(wallet, challenge, signature) {
  const recoveredAddress = ethers.verifyMessage(challenge, signature);
  return recoveredAddress === wallet.address;
}

// Use mnemonic words to restore wallet
function restoreWallet(mnemonic) {
  const wallet = ethers.Wallet.fromMnemonic(mnemonic);
  console.log("Restored Wallet:");
  console.log("Address:", wallet.address);
  return wallet;
}

// Example usage
async function demo(params) {
  const wallet = await createAccount();
  console.log("Generated Wallet:");
  console.log("Address:", wallet.address);
  console.log("Private Key:", wallet.privateKey);
  console.log("Mnemonic:", wallet.mnemonic.phrase); // Prompt users to backup this mnemonic word

  // const signature = await signChallenge(wallet, message);
  // console.log("Signature:", signature);

  // const isValid = await verifySignature(wallet, message, signature);
  // console.log("Signature Valid:", isValid);

  // After backing up the mnemonic words, users can use the following code to restore their wallet
  const restoredWallet = restoreWallet(wallet.mnemonic.phrase);

  // Signature Challenge
  const signature = await signChallenge(restoredWallet, message);
  console.log("Signature:", signature);

  // Verify signature
  const isValid = await verifySignature(
    restoredWallet.address,
    message,
    signature
  );
  console.log("Signature Valid:", isValid);
}

// Import wallet through Keystore and Password
async function importWallet(encryptedJson, password) {
  // Import wallet from encrypted JSON Keystore file
  const importedWallet = await importFromEncryptedJson(encryptedJson, password);
  console.log("importedWallet", importedWallet);
  return importedWallet;
}

/**
 * Unlock wallet with private key
 * @param {string} privateKey - User's wallet private key
 * @returns {object} wallet - Unlocked wallet object
 */
export async function unlockWalletWithPrivateKey(privateKey:string) {
  try {
    // Create wallet object using private key and provider
    const wallet = new ethers.Wallet(privateKey, provider);
    console.log("Wallet address:", wallet.address);
    return {ok: true, data: wallet};
  } catch (error) {
    console.error("Unlocking wallet failed:", error);
    return {ok: false, message: "Invalid private key"};
  }
}

async function unLockWithJsonAndPwdDemo() {
  const wallet = ethers.Wallet.createRandom();

  const password = "your_password";

  // Export encrypted JSON Keystore file
  const encryptedJson = await exportEncryptedJson(wallet, password);

  // Import wallet from encrypted JSON Keystore file
  const importedWallet = await importFromEncryptedJson(encryptedJson, password);

  // Sign and verify messages
  const message = "Hello, Ethereum!";
  const signature = await signMessage(importedWallet, message);
  const isValid = verifyMessage(message, signature) === importedWallet.address;

  console.log("Signature Valid:", isValid);
}

// Generate a random message
function generateRandomMessage(length) {
  const randomBytes = new Uint8Array(length);
  crypto.getRandomValues(randomBytes);
  return ethers.hexlify(randomBytes);
}

// Login Wallet
async function handleWalletSignIn({
  walletImported,
  address_type,
  inviterId,
  channel,
}: {
  walletImported: any;
  address_type: string;
  inviterId?: string;
  signature?: string;
  channel?: string
}) {
  
  let walletSignInResult = {};
  const randomMessage = generateRandomMessage(32);

  if (address_type === "threeSide") {  
    // Using base64 encryption for transmission
    let combinedText = '';
    for (let i = 0; i < randomMessage.length; i++) {
      let charCode = randomMessage.charCodeAt(i);
      let vectorCharCode = walletImported?.address.charCodeAt(i % walletImported?.address.length);
      combinedText += String.fromCharCode((charCode + vectorCharCode) % 256);
    }
    const signature = Base64.encode(combinedText);
    if (signature) {
      walletSignInResult = await walletSignIn({
        address: walletImported?.address,
        nonce: randomMessage,
        device_id: localStorage.visitor_id || "",
        address_type: address_type || "dbc",
        signature,
        id: localStorage.visitor_id || "",
        inviter_id: inviterId,
        channel: channel
      });
    }
  }

  if (address_type === "dbc") {
    // const { nonce, signature } = await signData(pair, password, undefined);

    // console.log("pair, password", pair, password);
    // Simulated random challenges or data
    const message = randomMessage;
    const prefixedMessage =
      "\x19Ethereum Signed Message:\n" + message.length + message;

    const signature = await signChallenge(walletImported, prefixedMessage);

    walletSignInResult = await walletSignIn({
      address: walletImported?.address,
      nonce: prefixedMessage,
      device_id: localStorage.visitor_id,
      address_type: address_type || "dbc",
      // data: pair,
      signature,
      id: localStorage.visitor_id,
      inviter_id: inviterId,
      channel: channel
    });
  }

  if (walletSignInResult?.token) {
    localStorage.removeItem("token");

    localStorage.token = walletSignInResult.token;

    user.set(walletSignInResult);
    localStorage.user = JSON.stringify(walletSignInResult);

    if (walletSignInResult.token) {
      await chats.set([]); 
      await chats.set(await getChatList(localStorage.token));
    }

    console.log("walletSignInResult", walletSignInResult);

    if (walletSignInResult.id) {
      updateWalletData(walletImported);
      let localWalletImported = {
        'address': walletImported?.address,
        'chainCode':walletImported?.chainCode,
        'depth':walletImported?.depth,
        'fingerprint':walletImported?.fingerprint,
        'index':walletImported?.index,
        'mnemonic':walletImported?.mnemonic,
        'parentFingerprint':walletImported?.parentFingerprint,
        'path':walletImported?.path,
        'provider':walletImported?.provider,
        'publicKey':walletImported?.publicKey,
        'extendedKey':walletImported?.extendedKey,
        'privateKey':walletImported?.privateKey,
        'signingKey':walletImported?.signingKey
      }
      localStorage.walletImported = JSON.stringify(localWalletImported);
    }  

    // Determine whether the user is a VIP
    const proInfo = await isPro(localStorage.token);
    user.set({
      ...walletSignInResult,
      isPro: proInfo ? proInfo.is_pro : false,
      proEndDate: proInfo ? proInfo.end_date : null
    });

  }
}

async function signOut(channel: string) {
  localStorage.removeItem("token");
  localStorage.removeItem("user");
  localStorage.removeItem("walletImported");
  const res = await printSignIn(channel);
  localStorage.token = res.token;
  user.set(res);
  console.log("Fingerprint login:", res);
}

export { provider, demo, importWallet, handleWalletSignIn, getGas, signOut };

async function getGas() {
  // Get the current recommended gas price
  const gasPrice = (await provider.getFeeData()).gasPrice;

  // Set gasLimit to a reasonable value based on specific circumstances
  const gasLimit = 210000; // Assuming the gasLimit of the transfer transaction here

  return {
    gasPrice: gasPrice,
    gasLimit: gasLimit,
  };
}
