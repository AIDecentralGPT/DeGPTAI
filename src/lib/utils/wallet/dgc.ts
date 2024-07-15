import { ethers } from "ethers";


// 获取当前区块高度
export async function getCurrentBlockNumber() {
  const blockNumber = await provider.getBlockNumber();
  console.log("Current block number:", blockNumber);
  return blockNumber;
}



// 查询指定账户的 DBC 余额
export async function getDbcBalance(address) {
  const balance = await provider.getBalance(address);
  console.log("DBC balance:", ethers.formatEther(balance), "DBC");
  return balance;
}

// 转账 DBC 到指定账户
export async function transferDbc(toAddress, amountDbc, privateKey) {
  const wallet = new ethers.Wallet(privateKey, provider);
  const amountWei = ethers.parseEther(amountDbc.toString());
  
  const tx = {
    to: toAddress,
    value: amountWei,
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

// 签名数据
export async function signData(data, privateKey) {
  const wallet = new ethers.Wallet(privateKey, provider);
  const dataBytes = ethers.toUtf8Bytes(data);
  const signature = await wallet.signMessage(dataBytes);
  console.log("Data:", data);
  console.log("Signature:", signature);
  return signature;
}

// 查询 DBC 的实时价格
export async function getDbcPrice() {
  // 这里是一个虚拟的价格查询示例，实际使用时需要调用真实的价格 API
  const price = 2.5; // 假设 DBC 的价格为 2.5 美元
  console.log("Current DBC price:", price, "USD");
  return price;
}




