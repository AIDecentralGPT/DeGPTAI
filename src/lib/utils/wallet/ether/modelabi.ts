import { ethers } from "ethers";
import DGCABI from "./abi.json";
import MODELABI from "./modelabi.json";
import { modelLimits, user, currentWalletData } from "$lib/stores";
import { toast } from "svelte-sonner";

// DGC 合约地址
const DGC_TOKEN_CONTRACT_ADDRESS = '0x82b1a3d719dDbFDa07AD1312c3063a829e1e66F1';
// 模型合约地址
const MODEL_TOKEN_CONTRACT_ADDRESS = '0x8588fb0Fec459d44a75135EE74E532a34539C749';

// 定义合约RPC网址
const modelUrl = "https://rpc-testnet.dbcwallet.io";

// 创建 provider
const provider = new ethers.JsonRpcProvider(modelUrl);

// 创建 DGC 合约实例
export const modelContract = new ethers.Contract(MODEL_TOKEN_CONTRACT_ADDRESS, MODELABI?.abi, provider);


// 授权操作
async function authSigner(data:any, type: string) {
    if (type == 'dbc') {
        // 通过私钥创建signer
        return new ethers.Wallet(data?.walletInfo.privateKey, provider);
    } else {
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
    
}

// 升级vip
export async function payForVip(data:any, type: string) {
    try {
        let signer = await authSigner(data, type);
        console.log("===================================", signer)
        if (false) {
            // 创建 DGC 合约实例
            const dgcContract = new ethers.Contract(DGC_TOKEN_CONTRACT_ADDRESS, DGCABI?.abi, signer);

            // 授权数量，单位和数值可根据实际情况调整
            const amountToApprove = ethers.parseUnits('5');
            console.log("====================授权额度===================", amountToApprove);
            let approveFlag = await dgcContract.approve(MODEL_TOKEN_CONTRACT_ADDRESS, amountToApprove)
                .then((tx) => tx.wait())
                .then((receipt) => {
                console.log('授权成功，交易收据：', receipt);
                return true;
            }).catch((error) => {
              console.error('授权失败：', error);
              return false;
            });

            // 升级VIP方法
            if (approveFlag) {
                // 查询 授权额度
                const amount = await dgcContract.allowance(signer?.address, MODEL_TOKEN_CONTRACT_ADDRESS);
                console.log("============allowance=============", amount);

                // 模型VIP合约
                const vipContract = new ethers.Contract(MODEL_TOKEN_CONTRACT_ADDRESS, MODELABI?.abi, signer);
                const result = await vipContract.payForVip();
                console.log("payForVip:", result);
                return result;
            }
            return null;
        } else {
            return null;
        } 
    } catch(e) {
        console.log("============payForVip-Error==============", e)
        toast.warning("Upgrade to Plus failed!");
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
        modelLimits.set([
            {name: 'Llama-3.1-405B', num: Number(result[0])},
            {name: 'Qwen2-72B', num: Number(result[1])},
            {name: 'Gemma-2-27B', num: Number(result[2])},
            {name: 'Codestral-22B-v0.1', num: Number(result[3])}
        ])
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