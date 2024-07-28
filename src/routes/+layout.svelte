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
  import {  printSignIn,  } from "$lib/apis/auths";
  import { onGetBalance, onGetDLCBalance, removePair } from "$lib/utils/wallet/dbc";

  import "../tailwind.css";
  import "../app.css";
  // import VConsole from 'vconsole';
  // const vConsole = new VConsole();

  import "tippy.js/dist/tippy.css";

  import { WEBUI_BASE_URL } from "$lib/constants";
  import i18n, { initI18n } from "$lib/i18n";
  import FingerprintJS from "@fingerprintjs/fingerprintjs";
  import { getCurrentPair, signData } from "$lib/utils/wallet/dbc";
  import { getUserInfo, updateUserById } from "$lib/apis/users";
  import { handleSigninAsIntialStatus } from "$lib/utils/wallet/walletUtils";

  setContext("i18n", i18n);
  let loaded = false;
  const BREAKPOINT = 768;


	async function initData (){
		
		let backendConfig = null;
		try {
			backendConfig = await getBackendConfig();
		} catch (error) {
			console.error('Error loading backend config:', error);
		}
		// Initialize i18n even if we didn't get a backend config,
		// so `/error` can show something that's not `undefined`.
		initI18n(backendConfig?.default_locale);

		if (backendConfig) {
			// Save Backend Status to Store
			await config.set(backendConfig);

			await WEBUI_NAME.set(backendConfig.name);

			
		} else {
			// Redirect to /error when Backend Not Detected
			await goto(`/error`);
		}


		
		// 加载 FingerprintJS 库
		const fp = await FingerprintJS.load();
		// 获取设备指纹
		const result = await fp.get();
		// `result.visitorId` 是设备指纹 ID
		const visitorId = result.visitorId;
		console.log("visitorId", visitorId); // 27841987f3d61173059f66f530b63f15
		localStorage.setItem('visitor_id', visitorId);


    let res = {}
    if(localStorage.token) {
      // res = await getUserInfo(localStorage.token);

      // 获取用户信息？可以通过auth/接口

    }
    else {
       res = await printSignIn();
    }

		// await user.set(res);
		loaded = true;

		console.log(res);
		localStorage.token = res.token;



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




		document.getElementById('splash-screen')?.remove();


    // 创建并插入Google Analytics的script标签
    const script = document.createElement('script');
    script.src = 'https://www.googletagmanager.com/gtag/js?id=G-ELT9ER83T2';
    script.async = true;
    document.head.appendChild(script);

    // 初始化Google Analytics
    script.onload = () => {
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', 'G-ELT9ER83T2');
    };



		return () => {
			window.removeEventListener('resize', onResize);
      
		};
	}

	onMount(initData);
</script>

<svelte:head>
  <title>{$WEBUI_NAME}</title>
  <link
    crossorigin="anonymous"
    rel="icon"
    href="{WEBUI_BASE_URL}/static/favicon.png"
  />

  <script type="text/javascript" src="https://hkwebcdn.yuncloudauth.com/cdn/jsvm_all.js"></script>

  <!-- rosepine themes have been disabled as it's not up to date with our latest version. -->
  <!-- feel free to make a PR to fix if anyone wants to see it return -->
  <!-- <link rel="stylesheet" type="text/css" href="/themes/rosepine.css" />
	<link rel="stylesheet" type="text/css" href="/themes/rosepine-dawn.css" /> -->
</svelte:head>

{#if loaded}
  <slot />
{/if}

<Toaster richColors position="top-center" class="flex"  />
