import { ethers } from "ethers";
import ABI from "./abi.json";
import { getProvider } from "@binance/w3w-ethereum-provider";

const BINANCE_DGC_CONTRACT_ADDRESS = '0x9cfAE8067322394e34E6b734c4a3F72aCC4a7Fe5';
const rpcUrl = "https://bsc-dataseed.binance.org/";

const provider = new ethers.JsonRpcProvider(rpcUrl);

export const binanceprovider = getProvider({ chainId: 56 });

// 创建 DGC 合约实例
export const dgcContract = new ethers.Contract(BINANCE_DGC_CONTRACT_ADDRESS, ABI?.abi, provider);


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
    // 校验是否已连接钱包
    const accounts = await binanceprovider.request({ method: 'eth_accounts' });
    console.log("=========Accounts==========", accounts);
    // 格式化转账金额
    const amountWei = ethers.parseUnits(amountDgc.toString());
    const ethersProvider = new ethers.BrowserProvider(binanceprovider);
    const signer = await ethersProvider.getSigner();
    const signerContract = new ethers.Contract(BINANCE_DGC_CONTRACT_ADDRESS, ABI?.abi, signer);
    const tx = await signerContract.transfer(toAddress, amountWei);
    const txResponse = await tx.wait();
    return {
      ok: true,
      data: txResponse
    };
  } catch (e) {
    console.log("===========================", e);
    return { ok: false, msg: "Failed to send transaction !" };
  }
}

// binanceAPP转账
export async function binanceAppTransferDgc(toAddress: string, amountDgc) {
  try {
    console.log("===========binancew3w==========", window.binancew3w)
    // 校验是否连接
    const accounts = await binanceprovider.request({ method: "eth_accounts" });
    if (!accounts?.length) {
      await binanceprovider.request({ method: "eth_requestAccounts" });
    }

    // 校验余额是否充足
    const dgcBalance = await getBinanceDgcBalance(accounts[0]);
    if (parseFloat(dgcBalance) < amountDgc) {
      return { ok: false, msg: "The DGC balance is not enough to pay. You can invite a friend to obtain 3000 DGC." };
    }

    // 格式化转账金额
    const amountWei = ethers.parseUnits(amountDgc.toString());
    const data = new ethers.Interface(ABI?.abi).encodeFunctionData('transfer', [toAddress, amountWei]);
    const txResponse = await binanceprovider.request({
      method: "eth_sendTransaction",
      params: [{
        from: accounts[0],
        to: BINANCE_DGC_CONTRACT_ADDRESS,
        data,
        value: "0x0"
      }]
    });
    console.log("==============txResponse=============", txResponse);
    return {
      ok: true,
      data: txResponse
    };
  } catch (e) {
    console.log("===========================", e);
    return { ok: false, msg: "Failed to send transaction !" };
  }
}