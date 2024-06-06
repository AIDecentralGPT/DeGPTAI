<script>
  import "../polyfills"; // 必须在其他代码之前引入

  import { onMount, tick, setContext } from "svelte";
  import { config, user, theme, WEBUI_NAME, mobile, currentWalletData, showOpenWalletModal } from "$lib/stores";
  import { goto } from "$app/navigation";
  import { Toaster, toast } from "svelte-sonner";

  import { getBackendConfig } from "$lib/apis";
  import { getSessionUser, printSignIn, walletSignIn } from "$lib/apis/auths";
  import { onGetBalance, onGetDLCBalance } from "$lib/utils/wallet/dbc";

  import "../tailwind.css";
  import "../app.css";
  // import VConsole from 'vconsole';
  // const vConsole = new VConsole();

  import "tippy.js/dist/tippy.css";

  import { WEBUI_BASE_URL } from "$lib/constants";
  import i18n, { initI18n } from "$lib/i18n";
  import FingerprintJS from "@fingerprintjs/fingerprintjs";
  import { getCurrentPair, signData } from "$lib/utils/wallet/dbc";
  import { updateUserById } from "$lib/apis/users";

  setContext("i18n", i18n);

  let loaded = false;
  const BREAKPOINT = 768;

  onMount(async () => {
    // localStorage.setItem("token", "public_token")

    // // 加载 FingerprintJS 库
    // await FingerprintJS.load().then(fp => {
    // 		// 获取设备指纹
    // 		fp.get().then(result => {
    // 				// `result.visitorId` 是设备指纹 ID
    // 				const visitorId = result.visitorId;
    // 				console.log("visitorId", visitorId); // 27841987f3d61173059f66f530b63f15
    // 				// fingerprintSignIn(visitorId)
    // 				localStorage.setItem('visitor_id', visitorId)

    // 				printSignIn().then((res ) => {
    // 					console.log(res);
    // 					user.set(res)
    // 				})

    // 		});

    // });


            // 加载 FingerprintJS 库
            const fp = await FingerprintJS.load();
        // 获取设备指纹
        const result = await fp.get();
        // `result.visitorId` 是设备指纹 ID
        const visitorId = result.visitorId;
        console.log("visitorId", visitorId); // 27841987f3d61173059f66f530b63f15
        localStorage.setItem("visitor_id", visitorId);

    // /-------------------------自动登录，如果没钱包，就用指纹登录
    if (!localStorage.token) {
      const pair = await getCurrentPair();
      if (pair) {
        // walletSignIn(pair?.address).then((res) => {
        //   console.log(res);
        // });

        console.log("pair", pair);
        // 展示打开钱包modal
        // $showOpenWalletModal = true;


        // // 获取钱包面板数据

        // const balance = await onGetBalance(pair?.address);
        // const dlcBalance = await onGetDLCBalance(pair?.address);
        // console.log("balance", balance, pair);
        // console.log("dlcBalance", dlcBalance);

        // currentWalletData.update((data) => {
        //   return {
        //     ...data,
        //     pair,
        //     balance,
        //     dlcBalance,
        //   };
        // });

        //                 const { nonce, signature } = await signData(
        //                   pair,
        //                   password,
        //                   undefined
        //                 );


        // --------------------------------

        //     walletSignIn({
        //       address: pair?.address,
        // nonce: string,
        // data?: any,
        // signature: string,
        // id: string
        //     }).then((res) => {
        //       console.log(res);
        //       localStorage.token = res.token;
        //       user.set(res);
        //     });

        // const a = await signData(pair, "123", undefined)
        // console.log("签名", a);

        // 更新用户id,行不通，要改好多表
        // 	const res = await updateUserById(localStorage.token, pair?.address, {
        // 		name: pair?.address,
        // 		// password:
        // 	}).catch((error) => {
        // 	toast.error(error);
        // });
      } else {


        await printSignIn().then((res) => {
          console.log("printSignIn res", res);

          if(res.token) {
            localStorage.token = res.token;
          user.set(res);
          }

        });
      }
    }

    // -----------------

    theme.set(localStorage.theme);

    mobile.set(window.innerWidth < BREAKPOINT);
    const onResize = () => {
      if (window.innerWidth < BREAKPOINT) {
        mobile.set(true);
      } else {
        mobile.set(false);
      }
    };

    window.addEventListener("resize", onResize);

    let backendConfig = null;
    try {
      backendConfig = await getBackendConfig();
    } catch (error) {
      console.error("Error loading backend config:", error);
    }
    // Initialize i18n even if we didn't get a backend config,
    // so `/error` can show something that's not `undefined`.
    initI18n(backendConfig?.default_locale);

    if (backendConfig) {
      // Save Backend Status to Store
      await config.set(backendConfig);

      await WEBUI_NAME.set(backendConfig.name);

      if ($config) {
        if (localStorage.token) {
          // Get Session User Info
          const sessionUser = await getSessionUser(localStorage.token).catch(
            (error) => {
              toast.error(error);
              return null;
            }
          );

          if (sessionUser) {
            // Save Session User to Store
            await user.set(sessionUser);
          } else {
            // Redirect Invalid Session User to /auth Page
            // localStorage.removeItem('token');
            // await goto('/auth');
          }
        } else {
          // await goto('/auth');
        }
      }
    } else {
      // Redirect to /error when Backend Not Detected
      await goto(`/error`);
    }

    await tick();

    document.getElementById("splash-screen")?.remove();
    loaded = true;

    return () => {
      window.removeEventListener("resize", onResize);
    };
  });
</script>

<svelte:head>
  <title>{$WEBUI_NAME}</title>
  <link
    crossorigin="anonymous"
    rel="icon"
    href="{WEBUI_BASE_URL}/static/favicon.png"
  />

  <!-- rosepine themes have been disabled as it's not up to date with our latest version. -->
  <!-- feel free to make a PR to fix if anyone wants to see it return -->
  <!-- <link rel="stylesheet" type="text/css" href="/themes/rosepine.css" />
	<link rel="stylesheet" type="text/css" href="/themes/rosepine-dawn.css" /> -->
</svelte:head>

{#if loaded}
  <slot />
{/if}

<Toaster richColors position="top-center" />
