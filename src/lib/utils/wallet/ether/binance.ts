import { ethers } from "ethers";
import { getProvider } from "@binance/w3w-ethereum-provider";

const ERC20_ABI = ["function transfer(address to, uint256 amount) returns (bool)"];
const BINANCE_DGC_CONTRACT_ADDRESS = '0x9cfAE8067322394e34E6b734c4a3F72aCC4a7Fe5';
const rpcUrl = "https://bsc-dataseed.binance.org/";

const provider = new ethers.JsonRpcProvider(rpcUrl);

export const binanceprovider = getProvider({ chainId: 56 });

// 创建 DGC 合约实例
export const dgcContract = new ethers.Contract(BINANCE_DGC_CONTRACT_ADDRESS, ERC20_ABI, provider);


// 查询 BNB 余额
export async function getBinanceBnbBalance(address: string) {

  const balanceWei = await provider.getBalance(address);

  const balanceBNB = ethers.formatUnits(balanceWei, 18);

  console.log("BNB balance:",balanceWei, balanceBNB, ethers.formatEther(balanceWei), "BNB");

  return balanceBNB;

}


// 查询 DGC 余额
export async function getBinanceDgcBalance(address: string) {

  const balanceWei = await dgcContract.balanceOf(address);

  const balanceDGC = ethers.formatUnits(balanceWei, 18);

  console.log("DGC balance:", balanceWei, balanceDGC, ethers.formatEther(balanceWei), "DGC");

  return balanceDGC;

}

// 转账
export async function binanceTransferDgc(address: string, toAddress: string, amountDgc) {
  const dgcBalance = await getBinanceDgcBalance(address);
  if (parseFloat(dgcBalance) < amountDgc) {
    return { ok: false, msg: "The DGC balance is not enough to pay. You can invite a friend to obtain 3000 DGC." };
  }
  try {
    await binanceprovider.request({
      method: 'wallet_switchEthereumChain',
      params: [{ chainId: '0x38' }] // BSC主网
    });
    await binanceprovider.request({ method: 'eth_requestAccounts' });
    // 构造 transfer 方法的 data
    const data = "0xa9059cbb" + // transfer 方法签名
      toAddress.replace('0x', '').padStart(64, '0') + // 接收地址
      BigInt(amountDgc).toString(16).padStart(64, '0'); // 转账金额
    
    // 发起转账
    const txResponse = await binanceprovider.request({
      method: "eth_sendTransaction",
      params: [
        {
          from: address,
          to: BINANCE_DGC_CONTRACT_ADDRESS, // BEP-20 代币合约地址
          data: data,
          gas: "0x19023",
          value: "0x0", // 代币转账 value 必须为 0
        },
      ],
    });
    console.log("==============================", txResponse);
    return {
      ok: true,
      data: txResponse
    };
  } catch (e) {
    console.log("===========================", e);
    return { ok: false, msg: "The DGC balance is not enough to pay. You can invite a friend to obtain 3000 DGC." };
  }
}