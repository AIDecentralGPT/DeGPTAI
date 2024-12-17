<script>
  import "../polyfills"; // 必须在其他代码之前引入
  import { onMount, setContext } from "svelte";
  import {
    config,
    user,
    theme,
    WEBUI_NAME,
    mobile,
    deApiBaseUrl,
    inviterId,
    channel,
    settings,
  } from "$lib/stores";
  import { page } from "$app/stores";
  import { goto } from "$app/navigation";
  import { Toaster } from "svelte-sonner";

  import { getBackendConfig } from "$lib/apis";

  import "../tailwind.css";
  import "../app.css";

  // 打开调试模式
  import VConsole from "vconsole";
  const vConsole = new VConsole();

  import "tippy.js/dist/tippy.css";

  import { WEBUI_BASE_URL } from "$lib/constants";
  import i18n, { initI18n } from "$lib/i18n";
  import FingerprintJS from "@fingerprintjs/fingerprintjs";
  import { getUserInfo, isPro } from "$lib/apis/users";
  import { updateWalletData } from "$lib/utils/wallet/walletUtils";
  import { unlockWalletWithPrivateKey } from "$lib/utils/wallet/ether/utils";
  import { getRegionInfo, getRegionDict } from "$lib/apis/utils/index";
  import { getLanguages } from "$lib/i18n/index";
  import { signOut } from "$lib/utils/wallet/ether/utils";
  import { addErrorLog } from '$lib/apis/errorlog';

  setContext("i18n", i18n);
  let loaded = false;
  const BREAKPOINT = 768;

  async function initData() {
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
    } else {
      // Redirect to /error when Backend Not Detected
      await goto(`/error`);
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

    document.getElementById("splash-screen")?.remove();

    // 创建并插入Google Analytics的script标签
    const script = document.createElement("script");
    script.src = "https://www.googletagmanager.com/gtag/js?id=G-ELT9ER83T2";
    script.async = true;
    document.head.appendChild(script);

    // 初始化Google Analytics
    script.onload = () => {
      window.dataLayer = window.dataLayer || [];
      function gtag() {
        dataLayer.push(arguments);
      }
      gtag("js", new Date());
      gtag("config", "G-ELT9ER83T2");
    };

    return () => {
      window.removeEventListener("resize", onResize);
    };
  }

  // 获取请求携带参数
  async function initUrlParam() {
    const queryParams = new URLSearchParams($page.url.search);

    // 获取邀请信息
    let inviterVal = queryParams.get("inviter");
    if (inviterVal) {
      await inviterId.set(inviterVal);
    }
    // 获取渠道
    let channelName = queryParams.get("channel");
    if (channelName) {
      await channel.set(channelName);
    }
  }

  async function checkLogin() {
    // 加载 FingerprintJS 库
    const fp = await FingerprintJS.load();
    // 获取设备指纹
    const result = await fp.get();
    // `result.visitorId` 是设备指纹 ID
    const visitorId = result.visitorId;
    console.log("visitorId", visitorId); // 27841987f3d61173059f66f530b63f15
    localStorage.setItem("visitor_id", visitorId);

    if (localStorage?.token) {
      // 获取缓存用户信息
      let localUser = null;
      try {
        localUser = JSON.parse(localStorage?.user);
        if (localUser?.address_type == "dbc") {
          let res = await getUserInfo(localStorage.token);
          if (res?.id === localUser?.id) {
            const proInfo = await isPro(localStorage.token);
            await user.set({
              ...localUser,
              token: res?.token,
              isPro: proInfo ? proInfo.is_pro : false,
              proEndDate: proInfo ? proInfo.end_date : null,
              models: res?.models,
            });
          }
          localStorage.user = JSON.stringify($user);

          // 校验钱包
          if (localStorage.walletImported) {
            let walletImported = JSON.parse(localStorage.walletImported);
            if (walletImported) {
              const walletImportedInfo = await unlockWalletWithPrivateKey(
                walletImported?.privateKey
              );
              updateWalletData(walletImportedInfo?.data);
            }
          }
        } else {
          await signOut($channel);
          // 更新用户模型
          await initUserModels();
        }
      } catch (error) {
        await signOut($channel);
        // 更新用户模型
        await initUserModels();
      }
    } else {
      await signOut($channel);
      // 更新用户模型
      await initUserModels();
    }
  }

  async function intiLocationInfo() {
    await getRegionInfo().then((data) => {
      const regionDict = getRegionDict();
      if (data) {
        regionDict.Singapore.forEach((item) => {
          if (item === data?.country) {
            deApiBaseUrl.set({
              name: "Singapore",
              url: "https://singapore-chat.degpt.ai/api",
            });
          }
        });
        regionDict.Korea.forEach((item) => {
          if (item === data?.country) {
            deApiBaseUrl.set({
              name: "Korea",
              url: "https://korea-chat.degpt.ai/api",
            });
          }
        });
      }
    });
  }

  async function initLanguage() {
    let browserLanguage = navigator.language;
    const languages = await getLanguages();
    let localLanguage = languages.filter(
      (item) => item.code == browserLanguage
    );
    if (localLanguage.length > 0) {
      $i18n.changeLanguage(browserLanguage);
    }
  }

  // 更新用户模型
  const initUserModels = async () => {
    if ($user?.models) {
      settings.set({ ...$settings, models: $user?.models.split(",") });
    } else {
      settings.set({
        ...$settings,
        models: $config?.default_models.split(","),
      });
    }
    localStorage.setItem("settings", JSON.stringify($settings));
    goto("/");
    const newChatButton = document.getElementById("new-chat-button");
    setTimeout(() => {
      newChatButton?.click();
    }, 0);
  };

  onMount(async () => {
    try {
      let currentAddress = window.location.href;
      await initData();
      await initLanguage();
      if (currentAddress.indexOf("userVerifying") < 0) {
        await initUrlParam();
        await checkLogin();
        loaded = true;
        await intiLocationInfo();
        await initUserModels();
      } else {
        loaded = true;
      }
    } catch (error) {
      addErrorLog("首页初始化", error.toString());
    }
  });
</script>

<svelte:head>
  <title>{$WEBUI_NAME}</title>
  <link
    crossorigin="anonymous"
    rel="icon"
    href="{WEBUI_BASE_URL}/static/favicon.png"
  />

  <script
    type="text/javascript"
    src="https://hkwebcdn.yuncloudauth.com/cdn/jsvm_all.js"
  ></script>

  <!-- rosepine themes have been disabled as it's not up to date with our latest version. -->
  <!-- feel free to make a PR to fix if anyone wants to see it return -->
  <!-- <link rel="stylesheet" type="text/css" href="/themes/rosepine.css" />
	<link rel="stylesheet" type="text/css" href="/themes/rosepine-dawn.css" /> -->
</svelte:head>

{#if loaded}
  <slot />
{/if}

<Toaster richColors position="top-center" class="flex" />
