<script>
	import '../polyfills'; // 必须在其他代码之前引入

  import { onMount, tick, setContext } from "svelte";
  import {
    config,
    user,
    theme,
    WEBUI_NAME,
    mobile,
    currentWalletData,
    showOpenWalletModal,
    chats,
  } from "$lib/stores";
  import { goto } from "$app/navigation";
  import { Toaster, toast } from "svelte-sonner";

  import { getBackendConfig } from "$lib/apis";
  import { getSessionUser, printSignIn, walletSignIn } from "$lib/apis/auths";
  import { onGetBalance, onGetDLCBalance, removePair } from "$lib/utils/wallet/dbc";

  import "../tailwind.css";
  import "../app.css";
  import VConsole from 'vconsole';
  const vConsole = new VConsole();

  import "tippy.js/dist/tippy.css";

  import { WEBUI_BASE_URL } from "$lib/constants";
  import i18n, { initI18n } from "$lib/i18n";
  import FingerprintJS from "@fingerprintjs/fingerprintjs";
  import { getCurrentPair, signData } from "$lib/utils/wallet/dbc";
  import { updateUserById } from "$lib/apis/users";
  import { handleSigninAsIntialStatus } from "$lib/utils/wallet/walletUtils";

  setContext("i18n", i18n);

  let loaded = false;
  const BREAKPOINT = 768;

  onMount(async () => {
    // 加载 FingerprintJS 库，获取指纹
    const fp = await FingerprintJS.load();
    const result = await fp.get();
    const visitorId = result.visitorId;
    localStorage.setItem("visitor_id", visitorId);



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

    console.log("backendConfig", backendConfig);

    if (backendConfig) {
      // 如果backendConfig存在，则执行以下操作

      // 将Backend的状态保存到Store中
      await config.set(backendConfig);

      // 设置WEBUI_NAME为backendConfig中的name
      await WEBUI_NAME.set(backendConfig.name);

      if ($config) {
        // 如果$config存在，则执行以下操作



        console.log("localStorage.token", localStorage.token);
        if (localStorage.token) {
          // 如果localStorage中存在token，则获取会话用户信息

          const sessionUser = await getSessionUser(localStorage.token).catch(
            (error) => {
              // 如果获取会话用户信息失败，则显示错误信息
              // toast.error(error + "35");
              return null;
            }
          );

          console.log("sessionUser", sessionUser);

          // 如果当前用户id和钱包不匹配，那么清空本地的pair
          const pair = await getCurrentPair();
          if(sessionUser?.id !== pair?.address) {
            localStorage.removeItem('pair')
          }

          if (sessionUser) {
            // 如果sessionUser存在，将其保存到Store中
            await user.set(sessionUser);
          } else {
            handleSigninAsIntialStatus()

            // // 如果sessionUser不存在，则进行浏览器指纹登录
            // await printSignIn().then((res) => {
            //   console.log("printSignIn res", res);

            //   $chats = []
            //   if (res.token) {
            //     localStorage.token = res.token;
            //     if($currentWalletData?.pair?.address) {
            //       removePair($currentWalletData?.pair?.address);
            //     }
            //     user.set(res);
            //   }
            // });
            // 如果sessionUser不存在，则重定向无效会话用户到/auth页面
            // localStorage.removeItem('token');
            // await goto('/auth');
          }
        } else {
            handleSigninAsIntialStatus()
          // 如果localStorage中不存在token，则重定向到/auth页面
          // await goto('/auth');


        }
      }
    } else {
      // 如果没有检测到Backend，则重定向到/error页面
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

<Toaster richColors position="top-center" class="flex"  />
