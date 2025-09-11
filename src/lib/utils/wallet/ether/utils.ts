// utils.js
import { ethers } from "ethers";
import { printSignIn, walletSignIn } from "$lib/apis/auths";
import { isPro } from "$lib/apis/users";
import { chats, user } from "$lib/stores";
import { getChatList } from "$lib/apis/chats";
import { updateWalletData } from "../walletUtils";
import dayjs from 'dayjs';
import { Base64 } from 'js-base64';

// 定义 RPC URL 和 Chain ID
// const rpcUrl = "https://rpc-testnet.dbcwallet.io"; // 旧 的 RPC URL
const rpcUrl = "https://rpc1.dbcwallet.io"; // 新 的 RPC URL
// const chainId = 19850818; // 旧 的 Chain ID
const chainId = 19880818; //新 的 Chain ID

// 创建 provider
const provider = new ethers.JsonRpcProvider(rpcUrl);

// 签名数据
export async function signData(data, privateKey) {
  const wallet = new ethers.Wallet(privateKey, provider);
  const dataBytes = ethers.toUtf8Bytes(data);
  const signature = await wallet.signMessage(dataBytes);
  console.log("Data:", data);
  console.log("Signature:", signature);
  return signature;
}

// 查询实时价格
export async function getCurrencyPrice(currency) {
  // 这里是一个虚拟的价格查询示例，实际使用时需要调用真实的价格 API
  const price = 2.5; // 假设价格为 2.5
  console.log(`Current ${currency} price:`, price, "USD");
  return price;
}

// 加密钱包并保存到 localStorage
export async function storeWallet(wallet, password) {
  console.log("wallet", wallet, password);

  const keystore = await wallet.encrypt(password);
  console.log("加密后的Keystore文件:", keystore);
  return keystore;

  // // 将加密后的Keystore文件存储到LocalStorage（一般不这么干，黑客入侵容易被盗）
  // localStorage.setItem('keystore', keystore);
}

// 从 localStorage 中加载并解密钱包
export async function loadWallet(password) {
  const json = localStorage.getItem("ethereum_wallet");
  const wallet = await ethers.Wallet.fromEncryptedJson(json, password);
  return wallet;
}

// loadWallet('your_password').then(wallet => {
//   console.log('Address:', wallet.address);
// });

// 创建一个新的 钱包 账户
export async function createAccount(password: string) {
  const wallet = ethers.Wallet.createRandom();
  console.log("New DBC account created:");
  console.log("Address:", wallet.address);
  console.log("Private Key:", wallet.privateKey);
  console.log("Mnemonic 助记词:", wallet.mnemonic.phrase); // 提示用户备份这个助记词

  // const ethAddress = '0x82b1a3d719dDbFDa07AD1312c3063a829e1e66F1';
  // const balance = await provider.getBalance(ethAddress);
  // const ethValue = ethers.formatEther(balance);

  //       // const ethValue = ethers.formatEther(balance);
  //       console.log("链上余额", balance);

  // 设置密码以加密Keystore文件
  const keystore = await storeWallet(wallet, password);

  return {
    wallet, // 钱包对象
    keystore, // 加密后的Keystore文件
    accountPrivateKey: wallet.privateKey,
  };
}

// 下载钱包Json
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

// ----------导出和导入JSON文件-------------
// // 导出为加密 JSON keystore 文件
// async function exportEncryptedJson(wallet, password) {
//   // 以太坊使用 ethers.js 加密钱包，并将其存储为 JSON keystore 文件。

//   const json = await wallet.encrypt(password);
//   const blob = new Blob([json], { type: 'application/json' });
//   const url = URL.createObjectURL(blob);

//   const link = document.createElement('a');
//   link.href = url;
//   link.download = 'wallet.json';
//   document.body.appendChild(link);
//   link.click();
//   document.body.removeChild(link);

//   console.log('Encrypted JSON Keystore:', json);
//   return json;
// }

// 从加密 JSON keystore 文件导入
async function importFromEncryptedJson(json, password) {
  const wallet = await ethers.Wallet.fromEncryptedJson(json, password);
  console.log("Imported Wallet Address:", wallet.address);
  return wallet;
}

// 签名消息
async function signMessage(wallet, message) {
  const signature = await wallet.signMessage(message);
  console.log("Signature:", signature);
  return signature;
}

// 验证签名
function verifyMessage(message, signature) {
  const recoveredAddress = ethers.utils.verifyMessage(message, signature);
  console.log("Recovered Address:", recoveredAddress);
  return recoveredAddress;
}

// --------钱包登录------------

// 用户签名挑战
export async function signChallenge(wallet, challenge) {
  const walletWithProvider = new ethers.Wallet(
    wallet.privateKey,
    new ethers.JsonRpcProvider()
  );
  const signature = await walletWithProvider.signMessage(challenge);
  return signature;
}

// 示例验证签名的函数
export async function verifySignature(wallet, challenge, signature) {
  const recoveredAddress = ethers.verifyMessage(challenge, signature);
  return recoveredAddress === wallet.address;
}

// 使用助记词恢复钱包
function restoreWallet(mnemonic) {
  const wallet = ethers.Wallet.fromMnemonic(mnemonic);
  console.log("Restored Wallet:");
  console.log("Address:", wallet.address);
  return wallet;
}

// 使用示例
async function demo(params) {
  const wallet = await createAccount();
  console.log("Generated Wallet:");
  console.log("Address:", wallet.address);
  console.log("Private Key:", wallet.privateKey);
  console.log("Mnemonic:", wallet.mnemonic.phrase); // 提示用户备份这个助记词

  // const signature = await signChallenge(wallet, message);
  // console.log("Signature:", signature);

  // const isValid = await verifySignature(wallet, message, signature);
  // console.log("Signature Valid:", isValid);

  // 用户备份助记词后，可以用以下代码恢复钱包
  const restoredWallet = restoreWallet(wallet.mnemonic.phrase);

  // 签名挑战
  const signature = await signChallenge(restoredWallet, message);
  console.log("Signature:", signature);

  // 验证签名
  const isValid = await verifySignature(
    restoredWallet.address,
    message,
    signature
  );
  console.log("Signature Valid:", isValid);
}

// 通过keystore和password 导入钱包
async function importWallet(encryptedJson, password) {
  // 从加密 JSON keystore 文件导入钱包
  const importedWallet = await importFromEncryptedJson(encryptedJson, password);
  console.log("importedWallet", importedWallet);
  return importedWallet;
}

/**
 * 使用私钥解锁钱包
 * @param {string} privateKey - 用户的钱包私钥
 * @returns {object} wallet - 解锁后的钱包对象
 */
export async function unlockWalletWithPrivateKey(privateKey:string) {
  try {
    // 使用私钥和 provider 创建钱包对象
    const wallet = new ethers.Wallet(privateKey, provider);
    console.log("钱包地址:", wallet.address);
    return {ok: true, data: wallet};
  } catch (error) {
    console.error("解锁钱包失败:", error);
    return {ok: false, message: "Invalid private key"};
  }
}

async function unLockWithJsonAndPwdDemo() {
  const wallet = ethers.Wallet.createRandom();

  const password = "your_password";

  // 导出加密 JSON keystore 文件
  const encryptedJson = await exportEncryptedJson(wallet, password);

  // 从加密 JSON keystore 文件导入钱包
  const importedWallet = await importFromEncryptedJson(encryptedJson, password);

  // 签名和验证消息
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

// 登录钱包
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
    // Example: Generate a random message of 32 bytes (256 bits)
    // const signature = threeSideSignature;
    // const signature = await walletconnectSignMessage(randomMessage);
    // // 将消息转换为十六进制字符串
    // const messageHex = ethers.hexlify(ethers.toUtf8Bytes(randomMessage));
    // console.log(
    //   "第三方登录请求数据",
    //   {
    //     wallet: walletImported?.address,
    //     signature: signature,
    //     hash: messageHex,
    //   }
    // );
    
    // 采用base64加密传输
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
    // 模拟的随机挑战或数据
    const message = randomMessage;
    const prefixedMessage =
      "\x19Ethereum Signed Message:\n" + message.length + message;

    const signature = await signChallenge(walletImported, prefixedMessage);

    // 将消息转换为十六进制字符串
    // const messageHex = ethers.hexlify(ethers.toUtf8Bytes(message));
    // console.log("Message Hex:", messageHex);
    // console.log(
    //   "因吹斯汀要的数据",
    //   {
    //     wallet: walletImported?.address,
    //     signature: signature,
    //     hash: messageHex,
    //   }
    // );

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

    console.log("==================", "token 被清除");

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

    // 获取用户是否是VIP
    const proInfo = await isPro(localStorage.token);
    user.set({
      ...walletSignInResult,
      vipInfo: proInfo
    });

  }
}

async function signOut(channel: string) {
  localStorage.removeItem("token");
  localStorage.removeItem("user");
  localStorage.removeItem("walletImported");
  localStorage.removeItem("walletKey");
  const res = await printSignIn(channel);
  localStorage.token = res.token;
  user.set(res);

  console.log("==================", "token 被清除");
  console.log("token 被清除");
}

export { provider, demo, importWallet, handleWalletSignIn, getGas, signOut };

async function getGas() {
  // 获取当前推荐的 gas price
  const gasPrice = (await provider.getFeeData()).gasPrice;

  // 设置 gasLimit，可以根据具体情况设定一个合理的值
  const gasLimit = 210000; // 这里假设转账交易的 gasLimit

  return {
    gasPrice: gasPrice,
    gasLimit: gasLimit,
  };
}
