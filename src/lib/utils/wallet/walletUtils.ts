import { printSignIn } from "$lib/apis/auths";
import { user, pageUpdateNumber, chats, currentWalletData, binanceFlag } from "$lib/stores";
import { get } from "svelte/store";
import { goto } from "$app/navigation";
import { getDbcBalance } from "./ether/dbc";
import { getDgcBalance } from "./ether/dgc";
import { DefaultCurrentWalletData } from "$lib/constants";
import { getBinanceBnbBalance, getBinanceDgcBalance } from "./ether/binance";

// 处理登录逻辑（不管有没有token，触发 用初始化状态登录，即删掉token，然后指纹登录）
export async function handleSigninAsIntialStatus() {
  // 处理没有token的情况
  if (!localStorage.token) {
    console.log("handleSignin");

    // 没token统一走指纹登录的逻辑（这是最初始的状态）
    await printSignIn("").then((res) => {
      if (res.token) {
        localStorage.token = res.token;
        user.set(res); 
        forceUpdate();
      }
    });

    // const pair = await getCurrentPair();
    // if (pair) {
    //  //  // 打开钱包登录弹窗
    //   // $showOpenWalletModal = true;

    //   console.log("pair", pair);
    // } else {
    //   // 没token
    //   await printSignIn().then((res) => {
    //     if (res.token) {
    //       localStorage.token = res.token;
    //       user.set(res);
    //     }
    //   });
    // }
  } else {
    // 如果有token
    localStorage.token = "";
    await printSignIn().then((res) => {
      if (res.token) {
        localStorage.token = res.token;
        user.set(res);
        forceUpdate();
      }
    });
  }
}

// // 用钱包登录
// export async function handleWalletSignIn(pair: string, password: string, inviterId?:string) {
//   const { nonce, signature } = await signData(pair, password, undefined);

//   console.log("pair, password", pair, password);

//   const walletSignInResult = await walletSignIn({
//     address: pair?.address,
//     nonce,
//     device_id: localStorage.visitor_id ,
//     // data: pair,
//     signature,
//     id: localStorage.visitor_id,
//     inviter_id: inviterId
//   });

//   if (walletSignInResult?.token) {
//     localStorage.removeItem("token");

//     localStorage.token = walletSignInResult.token;

//     console.log("钱包登录后获得的用户信息", walletSignInResult);
//     user.set(walletSignInResult);

//     if (walletSignInResult.token) {
//       await chats.set(await getChatList(localStorage.token));
//     }

//     console.log("walletSignInResult", walletSignInResult);

//     if (walletSignInResult.id) {
//       // ----------------
//       await chats.set([]) 
//       // 获取钱包面板数据
//       updateWalletData(pair);
//     }
//   }
// }

export async function closeWallet(channel:string) {
  currentWalletData.update(() => DefaultCurrentWalletData)

  localStorage.removeItem("token");
  localStorage.removeItem("user");
  localStorage.removeItem("walletImported");
  localStorage.removeItem("walletKey");

  console.log("==================", "token 被清除");

  await printSignIn(channel);
  forceUpdate();
  

  goto("/");
}

function forceUpdate() {
  // 触发重新渲染新会话组件
  const currentCount = get(pageUpdateNumber);
  pageUpdateNumber.set(currentCount + 1);
}

export async function updateWalletData(walletInfo: any) {
  const walletAdress = walletInfo?.address;

  await showWallet(walletInfo)

  // const dbcBalance = await getDbcBalance(walletAdress);
  let dbcBalance = "0";
  let dgcBalance = "0";
  if (get(binanceFlag)) {
    dbcBalance = await getBinanceBnbBalance(walletAdress);
    dgcBalance = await getBinanceDgcBalance(walletAdress);
  } else {
    dbcBalance = await getDbcBalance(walletAdress);
    dgcBalance = await getDgcBalance(walletAdress);
  }
  
  currentWalletData.update((data) => {
    return {
      ...data,
      walletInfo,
      dbcBalance,
      dgcBalance
    };
  });
}

export async function showWallet(walletInfo: any) {
  // 先更新pair，让钱包板块的页面先渲染出来
  currentWalletData.update((data) => {
    return {
      ...data,
      walletInfo,
    };
  });
}
