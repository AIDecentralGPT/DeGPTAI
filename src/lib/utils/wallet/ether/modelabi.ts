import { ethers } from "ethers";
import DGCABI from "./abi.json";
import MODELABI from "./modelabi.json";
import { modelLimits } from "$lib/stores";
import { getDbcBalance } from "$lib/utils/wallet/ether/dbc";
import { getDgcBalance } from "$lib/utils/wallet/ether/dgc";
import { currentWalletData } from "$lib/stores";
import { getAccount } from "@wagmi/core";
import { config } from "$lib/utils/wallet/walletconnect/index";

// DGC Contract Information
// const DGC_TOKEN_CONTRACT_ADDRESS = '0xC260ed583545d036ed99AA5C76583a99B7E85D26'; // Old contract address
const DGC_TOKEN_CONTRACT_ADDRESS = '0x18386F368e7C211E84324337fA8f62d5093272E1'; // New contract address

// const modelUrl = "https://rpc-testnet.dbcwallet.io"; // Old Contract RPC URL
const modelUrl = "https://rpc.dbcwallet.io"; // New Contract RPC URL

// Model old contract address
// const MODEL_TOKEN_CONTRACT_ADDRESS = '0x8588fb0Fec459d44a75135EE74E532a34539C749';
// Model new contract address
const MODEL_TOKEN_CONTRACT_ADDRESS = '0x2e0a85CB5352d7C542D632EdB4949DF879f8e981';


// Create provider
const provider = new ethers.JsonRpcProvider(modelUrl);

// Create DGC contract instance
export const modelContract = new ethers.Contract(MODEL_TOKEN_CONTRACT_ADDRESS, MODELABI?.abi, provider);

export async function checkMoney(address: string) {
    const dbcBalance = await getDbcBalance(address);
    const dgcBalance = await getDgcBalance(address);
    await currentWalletData.update((data) => {
        return {
        ...data,
        dbcBalance,
        dgcBalance
        };
    });
    if (parseFloat(dbcBalance) < 0.01) {
        return {ok: false, message: "The DBC gas fee is not enough.Please recharge at least 1 DBC."};
    }
    if (parseFloat(dgcBalance) < 6000) {
        return {ok: false, message: "The DGC balance is not enough to pay."};
    }
    return {ok: true, message: "success."};;
}

// Failed to obtain authorization information
export async function authSigner(data:any, type: string) {
    try {
        if (type == 'dbc') {
            // Create a signer using a private key
            let signer = new ethers.Wallet(data?.walletInfo?.privateKey, provider);
            return {ok: true, data: signer};
        } else { 
            const account = getAccount(config);
            const provider = await account?.connector?.getProvider();
            let eprovider = new ethers.BrowserProvider(provider);
            await eprovider.send('eth_requestAccounts', []);
            let signer = await eprovider.getSigner();
            return {ok: true, data: signer};
        }
    } catch(error) {
        console.log("===============authSigner===============", error);
        return {ok: false, message: "Failed to obtain authorization information."};
    }  
}

// Upgrade VIP
export async function payForVip(signer:any) {
    try {
        // Create DGC contract instance
        const dgcContract = new ethers.Contract(DGC_TOKEN_CONTRACT_ADDRESS, DGCABI?.abi, signer);

        // The authorized quantity, unit, and value can be adjusted according to the actual situation
        const amountToApprove = ethers.parseUnits('6000');
        let approveFlag = await dgcContract.approve(MODEL_TOKEN_CONTRACT_ADDRESS, amountToApprove)
            .then((tx) => tx.wait())
            .then((receipt) => {
            console.log('Authorization successful, transaction receipt：', receipt);
            return true;
        }).catch((error) => {
            console.error('privilege grant failed：', error);
            return false;
        });

        // Upgrade VIP method
        if (approveFlag) {
            // Query authorization limit
            const amount = await dgcContract.allowance(signer?.address, MODEL_TOKEN_CONTRACT_ADDRESS);
            console.log("============allowance=============", amount);
            // Model VIP Contract
            const vipContract = new ethers.Contract(MODEL_TOKEN_CONTRACT_ADDRESS, MODELABI?.abi, signer);
            const result = await vipContract.payForVip();
            console.log("payForVip:", result);
            return {ok: true, data: result};
        } else {
            return {ok: false, message: "privilege grant failed!"};
        }

    } catch(e) {
        console.log("============payForVip-Error==============", e)
        return {ok: false, message: "Upgrade to Plus failed!"};
    }  
}

// The quantity of DBC required to purchase VIP
export async function amountPay() {
    const result = await modelContract.amountPay();
    console.log("amountPay:", result);
    return result;
}

// Remaining available quantity of a certain model (0: 405b model 1: other)
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

// The model is called once per user request, reducing the number of available times
export async function requestModel(models) {
    try {
        const result = await modelContract.request(models);
        console.log("remainingAmount:", result);
    } catch(e) {
        console.log("========request-Error======", e);
    }
}