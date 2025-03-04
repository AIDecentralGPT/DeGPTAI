import { printSignIn } from "$lib/apis/auths";
import { user, pageUpdateNumber, chats, currentWalletData } from "$lib/stores";
import { get } from "svelte/store";
import { goto } from "$app/navigation";
import { getDbcBalance } from "./ether/dbc";
import { getDgcBalance } from "./ether/dgc";
import { DefaultCurrentWalletData } from "$lib/constants";

// Process login logic (regardless of whether there is a token or not, trigger login with initialization status, that is, delete the token, and then fingerprint login)
export async function handleSigninAsIntialStatus() {
  // Dealing with situations without tokens
  if (!localStorage.token) {
    console.log("handleSignin");

    // Unified fingerprint login logic without token (this is the initial state)
    await printSignIn("").then((res) => {
      if (res.token) {
        localStorage.token = res.token;
        user.set(res); 
        forceUpdate();
      }
    });
  } else {
    // If there is a token
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

export async function closeWallet(channel:string) {
  currentWalletData.update(() => DefaultCurrentWalletData)

  localStorage.removeItem("token");
  localStorage.removeItem("user");
  localStorage.removeItem("walletImported");

  await printSignIn(channel);
  forceUpdate();
  

  goto("/");
}

function forceUpdate() {
  // Trigger re rendering of new session components
  const currentCount = get(pageUpdateNumber);
  pageUpdateNumber.set(currentCount + 1);
}

export async function updateWalletData(walletInfo: any) {
  const walletAdress = walletInfo?.address;

  await showWallet(walletInfo)

  // const dbcBalance = await getDbcBalance(walletAdress);
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
  // Update the pair first, so that the wallet section page is rendered first
  currentWalletData.update((data) => {
    return {
      ...data,
      walletInfo,
    };
  });
}
