import { printSignIn } from "$lib/apis/auths";
import { user, pageUpdateNumber, chats, currentWalletData } from "$lib/stores";
import { get } from "svelte/store";
import {
  getCurrentPair,
  onGetBalance,
  onGetDLCBalance,
  signData,
  removePair,
} from "./dbc";
import { getChatList } from "$lib/apis/chats";
import { goto } from "$app/navigation";
import { getDbcBalance } from "./ether/dbc";
import { getDgcBalance } from "./ether/dgc";
import { DefaultCurrentWalletData } from "$lib/constants";

import { config } from "$lib/utils/wallet/walletconnect/index";

// 处理登录逻辑（不管有没有token，触发 用初始化状态登录，即删掉token，然后指纹登录）
export async function handleSigninAsIntialStatus() {
  // 处理没有token的情况
  if (!localStorage.token) {
    console.log("handleSignin");

    // 没token统一走指纹登录的逻辑（这是最初始的状态）
    await printSignIn().then((res) => {
      if (res.token) {
        localStorage.token = res.token;
        user.set(res);
        forceUpdate();

        console.log("111", get(pageUpdateNumber));

        console.log(222, get(chats));

        // 触发页面组件更新，回到初始化状态
        // pageUpdateNumber.subscribe(value => {
        //     pageUpdateNumber.set(value + 1);
        //     console.log(
        //       "value", value
        //     );
        // });
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

        console.log("111", get(pageUpdateNumber));

        console.log(222, get(chats));

        // 触发页面组件更新，回到初始化状态
        // pageUpdateNumber.subscribe(value => {
        //     pageUpdateNumber.set(value + 1);
        //     console.log(
        //       "value", value
        //     );
        // });
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

export async function closeWallet() {
  const walletData = get(currentWalletData);
  currentWalletData.update(() => DefaultCurrentWalletData)

  localStorage.removeItem("token");
  localStorage.removeItem("user");
  localStorage.removeItem("walletImported");

  await printSignIn().then((res) => {
    console.log("printSignIn的res", res);
    forceUpdate();
  });
  // $chats = [];

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

  // 获取钱包面板数据

  // const balance = await onGetBalance(pair?.address);
  // const dlcBalance = await onGetDLCBalance(pair?.address);

  const dbcBalance = await getDbcBalance(walletAdress);
  const dgcBalance = await getDgcBalance(walletAdress);
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

// export async function  handleSignin () {
//   // /-------------------------自动登录，如果没钱包，就用指纹登录
//   if (!localStorage.token) {
//     const pair = await getCurrentPair();
//     if (pair) {
//       // walletSignIn(pair?.address).then((res) => {
//       //   console.log(res);
//       // });

//       console.log("pair", pair);
//       // 展示打开钱包modal
//       // $showOpenWalletModal = true;

//       // // 获取钱包面板数据

//       // const balance = await onGetBalance(pair?.address);
//       // const dlcBalance = await onGetDLCBalance(pair?.address);
//       // console.log("balance", balance, pair);
//       // console.log("dlcBalance", dlcBalance);

//       // currentWalletData.update((data) => {
//       //   return {
//       //     ...data,
//       //     pair,
//       //     balance,
//       //     dlcBalance,
//       //   };
//       // });

//       //                 const { nonce, signature } = await signData(
//       //                   pair,
//       //                   password,
//       //                   undefined
//       //                 );

//       // --------------------------------

//       //     walletSignIn({
//       //       address: pair?.address,
//       // nonce: string,
//       // data?: any,
//       // signature: string,
//       // id: string
//       //     }).then((res) => {
//       //       console.log(res);
//       //       localStorage.token = res.token;
//       //       user.set(res);
//       //     });

//       // const a = await signData(pair, "123", undefined)
//       // console.log("签名", a);

//       // 更新用户id,行不通，要改好多表
//       // 	const res = await updateUserById(localStorage.token, pair?.address, {
//       // 		name: pair?.address,
//       // 		// password:
//       // 	}).catch((error) => {
//       // 	toast.error(error);
//       // });
//     } else {
//       await printSignIn().then((res) => {
//         console.log("printSignIn res", res);

//         if (res.token) {
//           localStorage.token = res.token;
//           user.set(res);
//         }
//       });
//     }
//   }

// }
