import { ethers } from "ethers";
import ABI from "./modelabi.json";
import { modelOne, modelTwo, modelThree, modelFour } from "$lib/stores";
import { toast } from "svelte-sonner";

console.log("ABI", typeof ABI);


// 模型合约地址
const DGC_TOKEN_CONTRACT_ADDRESS = '0x8588fb0Fec459d44a75135EE74E532a34539C749';

// 定义模型合约网址
const modelUrl = "https://rpc-testnet.dbcwallet.io";

// 创建 provider
const provider = new ethers.JsonRpcProvider(modelUrl);
// 创建 DGC 合约实例
export const modelContract = new ethers.Contract(DGC_TOKEN_CONTRACT_ADDRESS, ABI?.abi, provider);


// 授权操作
async function authSigner() {
    if (window.ethereum) {
        let authProvider = new ethers.BrowserProvider(window.ethereum);
        await authProvider.send('eth_requestAccounts', []);
        let signer = await authProvider.getSigner();
        return signer;
    } else {
        toast.warning('Please install Ethereum wallet plugin, such as MetaMask.');
        return "";
    }
}

// 升级vip
export async function payForVip(address) {
    try {
        let signer = await authSigner();
        if (signer) {
            const authContract = new ethers.Contract(DGC_TOKEN_CONTRACT_ADDRESS, ABI?.abi, signer);
            // 授权数量，单位和数值可根据实际情况调整
            const amountToApprove = ethers.parseUnits('1');
            modelContract.approve(address, amountToApprove)
                .then((tx) => tx.wait())
                .then((receipt) => {
                console.log('授权成功，交易收据：', receipt);
                const result = authContract.payForVip();
                console.log("payForVip:", result);
                return result;
            }).catch((error) => {
              console.error('授权失败：', error);
            });
            return null;
        } else {
            return null;
        } 
    } catch(e) {
        console.log("============payForVip-Error==============", e)
        toast.warning("========payForVip-Error======");
        return null;
    }  
}

// 购买vip需要支付的dbc的数量
export async function amountPay() {
    const result = await modelContract.amountPay();
    console.log("amountPay:", result);
    return result;
}

// 某个模型剩余可用数量(0:是405b模型 1:其他)
export async function remainingAmount(address, models) {
    try {
        const result = await modelContract.remainingAmount(address, models);
        console.log("remainingAmount:", result);
        modelOne.set(Number(result[0]));
        modelTwo.set(Number(result[1]));
        modelThree.set(Number(result[2]));
        modelFour.set(Number(result[3]));
    } catch(e) {
        console.log("========remainingAmount-Error======", e);
    }
}

// 用户请求一次模型就调用一次，可用次数减少
export async function requestModel(models) {
    try {
        const result = await modelContract.request(models);
        console.log("remainingAmount:", result);
    } catch(e) {
        console.log("========request-Error======", e);
    }
}