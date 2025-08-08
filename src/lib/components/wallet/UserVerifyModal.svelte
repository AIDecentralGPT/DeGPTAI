<script lang="ts">
  import { getContext, onMount, onDestroy } from "svelte";
  import Modal from "../common/Modal.svelte";
  import { WEBUI_API_BASE_URL, WEBUI_BASE_URL } from "$lib/constants";
  import { copyToClipboard, checkUniapp } from "$lib/utils";
  import {
    faceliveness,
    facelivenessRes,
    sendCode,
    verifyCode,
    servetime,
  } from "$lib/apis/auths";
  import { user, theme, faceUrl } from "$lib/stores";
  import { toast } from "svelte-sonner";
  import QRCode from "qrcode";
  import { goto } from "$app/navigation";
  import { addErrorLog } from "$lib/apis/errorlog";
  import { bindCaptcha } from "$lib/apis/kycrestrict";

  const i18n = getContext("i18n");

  let socket: any = null;
  let message = "";
  let address = "";

  function initSocket() {
    // 创建 WebSocket 连接
    let socketUrl = "";
    if (WEBUI_API_BASE_URL.includes("https://")) {
      socketUrl = WEBUI_API_BASE_URL.replace("https://", "wss://");
    } else {
      socketUrl = WEBUI_API_BASE_URL.replace("http://", "ws://");
    }
    socket = new WebSocket(`${socketUrl}/auths/ws/` + $user?.id);

    // 监听 WebSocket 连接打开事件
    socket.onopen = () => {
      console.log("WebSocket connection established");
    };

    // 监听 WebSocket 错误事件
    socket.onerror = (error) => {
      console.error("WebSocket error: ", error);
    };

    // 监听 WebSocket 连接关闭事件
    socket.onclose = () => {
      console.log("WebSocket connection closed");
    };

    // 监听 WebSocket 消息事件
    socket.addEventListener("message", (event) => {
      // 接收到消息停止倒计时
      clearInterval(countdownQrInterval);
      let data = JSON.parse(event.data);
      if (data.passed) {
        message = "Success!";
        qrCodeFinish = true;
        checkQrResult = false;
        let newUser = JSON.parse(JSON.stringify($user));
        newUser.verified = true;
        user.set(newUser);
      } else {
        message = "Failed, try again";
        address = data.address;
        qrCodeFinish = false;
        checkQrResult = true;
      }
    });
  }

  export let show = false;

  let isMobile = false;

  let current = 1;
  let email = "";
  let code = "";
  let countdown = 0;
  let countdownInterval: any = null;
  let nextLoading = false;

  function validateEmail(email: string) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  }

  async function sendVerificationCode() {
    if (countdown === 0) {
      email = email.trim();
      if (validateEmail(email)) {
        sendCode(localStorage.token, email, $i18n.language).then((res) => {
          if (res.pass) {
            checkCaptcha = false;
            startCountdown();
          } else {
            checkCaptcha = false;
            toast.error($i18n.t(res.message));
          }
        });
      } else {
        checkCaptcha = false;
        toast.error($i18n.t("Please enter a valid email address."));
      }
    }
  }

  function startCountdown() {
    countdown = 60;
    countdownInterval = setInterval(() => {
      countdown -= 1;
      if (countdown === 0) {
        clearInterval(countdownInterval);
      }
    }, 1000);
  }

  async function nextStep() {
    let valid = true;
    qrcodeUrl = "";
    if (current === 1) {
      if (!validateEmail(email)) {
        toast.error($i18n.t("Please enter a valid email address."));
        valid = false;
        return;
      }
      if (!code) {
        toast.error($i18n.t("Please enter the verification code."));
        valid = false;
        return;
      }
      nextLoading = true;
      await verifyCode(localStorage.token, email, code)
        .then(() => {
          email = email;
          current = current + 1;
          faceLiveness();
        })
        .catch((error) => {
          toast.error($i18n.t(error));
          valid = false;
        });
      nextLoading = false;
    } else if (current === 2) {
      show = false;
    }

    if (valid && current < 2) {
      current += 1;
    }
  }

  function previousStep() {
    if (current > 1) {
      current -= 1;
    }
  }

  let qrcodeUrl = "";
  let qrCodeFinish = false;
  let checkQrResult = false;
  let faceTime = new Date();

  function faceLiveness() {
    const MetaInfo = window.getMetaInfo();
    console.log("进入faceliveness", MetaInfo);
    faceliveness(MetaInfo).then(async (res) => {
      faceLivenessInitialData = res;
      if (res.transaction_url) {
        if (isMobile) {
          if (checkUniapp()) {
            faceUrl.set({
              url: res.transaction_url
            })
            goto("/kyc")
          } else {
            await goto(res.transaction_url);
          }
        } else {
          faceTime = new Date(res.face_time);
          getQrCode(res.transaction_url);
        }
      } else {
        toast.error(res.data.message);
      }
    });
  }

  // 时间校准
  let timeDiff = 0;
  function serveTime() {
    servetime().then(async (res) => {
      // 加200毫秒请求时长浮动
      timeDiff = new Date().getTime() - (new Date(res.data).getTime() + 200);
    });
  }

  function getQrCode(url: string) {
    let token = localStorage.token;
    let lang = $i18n.language;
    url = "https://test.degpt.ai/static/kyc/index.html?token=" + token + "&lang=" + lang;
    console.log("============ewm_url==========", url);
    let qrConfig = {
      errorCorrectionLevel: 'M',
      margin: 2,
      width: 300,
      color: {
        dark: '#000000',
        light: '#ffffff'
      }
    };
    QRCode.toDataURL(url, qrConfig, 
      function (err, url) {
        console.log(url);
        qrcodeUrl = url;
        qrCodeFinish = false;
        checkQrResult = false;
        startQrCountdown();
      }
    );
  }

  // 二维码有效时长
  let showQrTime = "05:00";
  let countdownQrInterval: any = null;
  function startQrCountdown() {
    if (faceTime) {
      // 不为空先清除计时器值
      if (countdownQrInterval) {
        showQrTime = "05:00";
        clearInterval(countdownQrInterval);
      }
      countdownQrInterval = setInterval(() => {
        let comptime = Math.floor(
          (new Date().getTime() - faceTime.getTime() - timeDiff) / 1000
        );
        let qrcountdown = 300 - comptime;
        let minute = Math.floor(qrcountdown / 60);
        let second = qrcountdown % 60;
        showQrTime =
          (minute > 9 ? minute : "0" + minute) +
          ":" +
          (second > 9 ? second : "0" + second);
        if (qrcountdown <= 0) {
          clearInterval(countdownQrInterval);
          message = "Time expired, try again";
          qrCodeFinish = false;
          checkQrResult = true;
        }
      }, 1000);
    }
  }

  function getFaceRes() {
    facelivenessRes({
      // transaction_id: faceLivenessInitialData.transaction_id,
      // merchant_biz_id: faceLivenessInitialData.merchant_biz_id,
    }).then((res) => {
      console.log(res);
      if (res?.passed) {
        toast.success($i18n.t("Congratulations on passing the verification!"));
        show = false;
      } else {
        toast.error(
          $i18n.t(
            "Verification failed, the system detects that your face has been used!"
          )
        );
      }
    });
  }

  let faceLivenessInitialData = {
    merchant_biz_id: "",
    transaction_id: "",
    transaction_url: "",
  };

  onMount(() => {
    try {
      const userAgent = navigator.userAgent || navigator.vendor || window.opera;
      // 检查是否为移动端设备
      isMobile = /android|iPad|iPhone|iPod|IEMobile|Opera Mini/i.test(
        userAgent
      );
      // 时间校准
      serveTime();
      // 动态引入图片认证
      importCaptchaJs();
    } catch (error) {
      addErrorLog("kyc认证初始化", error.toString());
    }
  });

  function initParam() {
    current = 1;
    email = "";
    code = "";
    countdown = 0;
    countdownInterval = null;
  }

  // 显示初始化Socket
  $: if (show) {
    try {
      initSocket();
      initParam();
    } catch (error) {
      addErrorLog("socket初始化", error.toString());
    }
  }

  // 隐藏关闭Socket
  $: if (!show) {
    if (socket) {
      socket.close();
    }
    if (countdownQrInterval) {
      clearInterval(countdownQrInterval);
    }
  }

  // 在组件卸载时关闭 WebSocket 连接
  onDestroy(() => {
    if (socket) {
      socket.close();
    }
  });

  // 图片认证相关
  let checkCaptcha = false;
  const CAPTCHA_APP_ID = '199818891'
  const SLIDER_CAPTCHA_JS = 'https://captcha.api.hi.cn/captcha.js';

  // 动态引入验证码的js
  function importCaptchaJs() {  
    let script = document.createElement('script');
    script.type = 'text/javascript';
    script.src = SLIDER_CAPTCHA_JS;
    let head = document.head || document.getElementsByTagName('head')[0];
    head.appendChild(script)
  }

  function openCaptcha() {
    let enableDarkFlag = '';
    if ($theme === "system" || $theme === "light") {
      enableDarkFlag = '';
    } else {
      enableDarkFlag = 'force';
    }
    let lang = $i18n.language;
    let captcha = new FushuActionCaptcha(CAPTCHA_APP_ID, captchaCallBack, {enableDarkMode: enableDarkFlag, userLanguage: lang == 'zh-CN' ? 'zh-CN' : 'en-US'});
    captcha.show();
  }

  async function captchaCallBack(captchaRes: any) {
    checkCaptcha = true;
    if(captchaRes.ret === 0){
      let result = await bindCaptcha(localStorage.token, JSON.stringify(captchaRes));
      if (result) {
        await sendVerificationCode();
      } else {
        checkCaptcha = false;
      }
    } else {
      checkCaptcha = false;
    }
  }

  const mousedownValid = false; 
</script>

<Modal bind:show mousedownValid={ mousedownValid } size="lg">
  <div class="text-gray-700 dark:text-gray-100 px-5 pt-4 pb-4 relative">
    <div class="flex justify-between dark:text-gray-300">
      <div class="text-lg font-medium self-center">
        {$i18n.t("User Authentication")}
      </div>
      <button
        class="self-center"
        on:click={() => {
          show = false;
        }}
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 20 20"
          fill="currentColor"
          class="w-5 h-5"
        >
          <path
            d="M6.28 5.22a.75.75 0 00-1.06 1.06L8.94 10l-3.72 3.72a.75.75 0 101.06 1.06L10 11.06l3.72 3.72a.75.75 0 101.06-1.06L11.06 10l3.72-3.72a.75.75 0 00-1.06-1.06L10 8.94 6.28 5.22z"
          />
        </svg>
      </button>
    </div>

    <div class="flex flex-col gap-4 mt-4 px-2 h-[460px]">
      <div class=" border-primary border-2 rounded-lg p-4">
        <div>
          <strong>{$i18n.t("Authenticated wallet address:")}</strong>
          <span class="text-primary">{$user?.id}</span>
        </div>
        <!-- Only this address can receive rewards if it passes verification. -->
      </div>

      {#if current === 2}
        <div class=" border-primary border-2 rounded-lg p-4">
          <div>
            <strong>{$i18n.t("Authenticated email address:")}</strong>
            <span class="text-primary">{email}</span>
          </div>
        </div>
      {/if}

      {#if current === 1}
        <div class="flex flex-col w-full">
          <!-- flex-wrap gap-2 xl:flex-nowrap  xl:gap-0 -->
          <div class="flex flex-col w-full mb-3">
            <div
              class="flex justify-start gap-2 flex-col md:flex-row md:items-center w-full mb-1 pt-0.5 items-baseline"
            >
              <label
                for="email"
                class="block text-sm font-medium dark:text-white text-black border-gray-300 w-[55px] md:text-right"
                >{$i18n.t("Email")}:</label
              >
              <div
                class="flex justify-between items-center w-full md:flex-1 space-x-4"
              >
                <input
                  aria-label="email"
                  id="emailInput"
                  type="email"
                  placeholder={$i18n.t("Enter email address")}
                  bind:value={email}
                  class="flex-1 min-w-36 px-4 py-2 dark:bg-zinc-950 dark:text-white bg-white text-black border border-gray-300 rounded-lg"
                />
                <button
                  class="w-[90px] px-4 py-2 dark:bg-white dark:text-zinc-950 bg-black text-gray-100 whitespace-nowrap transition rounded-lg flex items-center justify-center {countdown >
                  0
                    ? 'opacity-50 cursor-not-allowed'
                    : ''}"
                  type="button"
                  on:click={async () => { await openCaptcha(); }}
                  disabled={countdown > 0 || checkCaptcha}
                >
                  {#if checkCaptcha}
                    {$i18n.t("Check")}...
                  {:else}
                    {#if countdown > 0}
                      {countdown}s
                    {/if}
                    {#if countdown === 0}
                      {$i18n.t("Send")}
                    {/if}
                  {/if}
                </button>
              </div>
            </div>
          </div>

          <div
            class="flex justify-start gap-2 flex-col items-baseline md:items-center md:flex-row mb-6 pt-0.5 w-full"
          >
            <label
              for="code"
              class="block text-sm font-medium dark:text-white text-black border-gray-300 w-[55px] md:text-right"
              >{$i18n.t("Code")}:</label
            >
            <input
              aria-label="code"
              id="verificationCodeInput"
              type="text"
              placeholder={$i18n.t("Enter verification code")}
              bind:value={code}
              class="px-4 py-2 dark:bg-zinc-950 dark:text-white bg-white text-black border border-gray-300 rounded-lg w-full md:flex-1"
            />
          </div>

          <div class="flex flex-col">
            <div class="flex flex-row items-center">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" version="1.1" fill="#ee6a0c" class="size-[1.6rem]">
                <path d="M228.3 219.4c-11.7-11-30.6-11-42.2 0-11.7 11-11.7 28.8 0 39.7l42.2 39.7c11.7 11 30.6 11 42.2 0 11.7-11 11.7-28.8 0-39.7l-42.2-39.7z m567.4 0l-42.2 39.7c-11.7 11-11.7 28.8 0 39.7 11.7 11 30.6 11 42.2 0l42.2-39.7c11.7-11 11.7-28.8 0-39.7-11.6-11-30.5-11-42.2 0zM153.6 441.7H93.9c-16.5 0-29.9 12.6-29.9 28.1 0 15.5 13.4 28.1 29.9 28.1h59.7c16.5 0 29.9-12.6 29.9-28.1 0-15.5-13.4-28.1-29.9-28.1z m776.5 0h-59.7c-16.5 0-29.9 12.6-29.9 28.1 0 15.5 13.4 28.1 29.9 28.1h59.7c16.5 0 29.9-12.6 29.9-28.1 0-15.5-13.4-28.1-29.9-28.1z m-448-323.1v56.2c0 15.5 13.4 28.1 29.9 28.1s29.9-12.6 29.9-28.1v-56.2c0-15.5-13.4-28.1-29.9-28.1-16.5 0.1-29.9 12.6-29.9 28.1zM243.2 512c0 139.7 120.3 252.9 268.8 252.9S780.8 651.7 780.8 512 660.5 259.1 512 259.1 243.2 372.3 243.2 512z m209.1 393.3c0 15.5 13.4 28.1 29.9 28.1h59.7c16.5 0 29.9-12.6 29.9-28.1 0-15.5-13.4-28.1-29.9-28.1h-59.7c-16.6 0.1-29.9 12.6-29.9 28.1z m-59.8-84.2c0 15.5 13.4 28.1 29.9 28.1h179.2c16.5 0 29.9-12.6 29.9-28.1 0-15.5-13.4-28.1-29.9-28.1H422.4c-16.5 0-29.9 12.5-29.9 28.1z m0 0"/>
              </svg>
              <span class="ml-1 font-bold mt-1">{$i18n.t("Small Tip:")}</span>
            </div>
            <span class="ml-2 mt-2">{$i18n.t("If you're using a Gmail account and can't find the verification code in your Inbox, it's highly likely that it's been filtered into your SpamFolder.")}</span>
          </div>
        </div>
      {/if}

      {#if current === 2}
        <div class="flex flex-col justify-start items-center gap-4">
          {#if !isMobile}
            <div class="rounded-lg flex flex-col items-center h-[288px]">
              <div class="flex flex-col items-center">
                {#if qrcodeUrl}
                  <p class="text-center text-gray-800 dark:text-gray-100">
                    {$i18n.t(
                      "Please use your mobile phone to scan the QR code below for identity verification"
                    )}
                  </p>
                  <div
                    class="flex justify-center items-center w-[200px] h-[180px] m-2 pos-rel"
                  >
                    <img class="w-[160px]" src={qrcodeUrl} alt="" />
                    {#if checkQrResult}
                      <div class="w-[200px] h-[180px] model-styl">
                        <button
                          class=" px-4 py-2 primaryButton text-gray-100 transition rounded-lg w-[100px]"
                          on:click={faceLiveness}>{$i18n.t("Try again")}</button
                        >
                      </div>
                    {/if}
                    {#if qrCodeFinish}
                      <div class="w-[200px] h-[180px] model-styl">
                        <svg
                          xmlns="http://www.w3.org/2000/svg"
                          class="icon"
                          viewBox="0 0 1024 1024"
                          version="1.1"
                          width="100"
                          height="100"
                        >
                          <path
                            d="M512 832c-176.448 0-320-143.552-320-320S335.552 192 512 192s320 143.552 320 320-143.552 320-320 320m0-704C300.256 128 128 300.256 128 512s172.256 384 384 384 384-172.256 384-384S723.744 128 512 128"
                            fill="#4ECA70"
                          />
                          <path
                            d="M619.072 429.088l-151.744 165.888-62.112-69.6a32 32 0 1 0-47.744 42.624l85.696 96a32 32 0 0 0 23.68 10.688h0.192c8.96 0 17.536-3.776 23.616-10.4l175.648-192a32 32 0 0 0-47.232-43.2"
                            fill="#4ECA70"
                          />
                        </svg>
                      </div>
                    {/if}
                  </div>
                  {#if checkQrResult}
                    {#if address}
                      <div class="flex flex-row items-center">
                        {$i18n.t("You have already bound your face KYC with another wallet. Only one wallet can be bound.")}
                      </div>
                      <div class="flex">
                        <p
                          class="w-[300px] dark:text-gray-500 dark:bg-gray-650 text-ellipsis overflow-hidden whitespace-nowrap"
                        >
                          {$i18n.t("Wallet Adress")}: {address}
                        </p>
                        <button
                          on:click={async () => {
                            const res = await copyToClipboard(address);
                            if (res) {
                              toast.success(
                                $i18n.t("Copying to clipboard was successful!")
                              );
                            }
                          }}
                          type="button"
                          class="px-3 py-2 text-sm-12 dark:text-gray-300 dark:bg-gray-650 rounded-md fs12"
                        >
                          <svg
                            xmlns="http://www.w3.org/2000/svg"
                            width="1em"
                            height="1em"
                            viewBox="0 0 512 512"
                          >
                            <rect
                              width="336"
                              height="336"
                              x="128"
                              y="128"
                              fill="none"
                              stroke="currentColor"
                              stroke-linejoin="round"
                              stroke-width="32"
                              rx="57"
                              ry="57"
                            />
                            <path
                              fill="none"
                              stroke="currentColor"
                              stroke-linecap="round"
                              stroke-linejoin="round"
                              stroke-width="32"
                              d="m383.5 128l.5-24a56.16 56.16 0 0 0-56-56H112a64.19 64.19 0 0 0-64 64v216a56.16 56.16 0 0 0 56 56h24"
                            />
                          </svg>
                        </button>
                      </div>
                    {:else}
                      <div class="flex flex-row items-center">
                        {$i18n.t(message)}
                      </div>
                    {/if}
                  {:else if qrCodeFinish}
                    <div class="flex flex-row items-center success">
                      <span>{$i18n.t(message)}<span /></span>
                    </div>
                  {:else}
                    <p class="text-center text-gray-800 dark:text-gray-100">
                      {$i18n.t("QR code is valid for 5 minutes")}
                    </p>
                    <div class="flex flex-row items-center timesty">
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        class="icon"
                        viewBox="0 0 1024 1024"
                        version="1.1"
                        width="20"
                        height="20"
                      >
                        <path
                          d="M512 53.333333C258.688 53.333333 53.333333 258.688 53.333333 512S258.688 970.666667 512 970.666667 970.666667 765.312 970.666667 512 765.312 53.333333 512 53.333333z m0 64c217.962667 0 394.666667 176.704 394.666667 394.666667S729.962667 906.666667 512 906.666667 117.333333 729.962667 117.333333 512 294.037333 117.333333 512 117.333333z"
                          fill="#BD9257"
                        />
                        <path
                          d="M661.333333 554.666667a32 32 0 0 1 3.072 63.850666L661.333333 618.666667h-192a32 32 0 0 1-3.072-63.850667L469.333333 554.666667h192z"
                          fill="#BD9257"
                        />
                        <path
                          d="M458.666667 288a32 32 0 0 1 31.850666 28.928L490.666667 320v256a32 32 0 0 1-63.850667 3.072L426.666667 576V320a32 32 0 0 1 32-32z"
                          fill="#BD9257"
                        />
                      </svg>&nbsp;&nbsp;{showQrTime}
                    </div>
                  {/if}
                {:else}
                  <div
                    class="mt-6 w-[160px] h-[160px] flex justify-center items-center text-white bg-gray-400 rounded-md"
                  >
                    <span class="animate-pulse">Loading...</span>
                  </div>
                {/if}
              </div>
            </div>
          {/if}
          {#if isMobile}
            <div class="text-center">
              <div>
                {$i18n.t("Preparing to switch to the face verification page")}
              </div>
              <div class="flex justify-center mt-2">
                <svg
                  class="animate-spin ml-2"
                  xmlns="http://www.w3.org/2000/svg"
                  width="2em"
                  height="2em"
                  fill="currentColor"
                  viewBox="0 0 1024 1024">
                  <path d="M144.205 202.496a136.678 136.678 0 1 0 273.357 0 136.678 136.678 0 1 0-273.357 0zM41.728 492.902a119.578 119.578 0 1 0 239.155 0 119.578 119.578 0 1 0-239.155 0zM144.23 749.158a102.502 102.502 0 1 0 205.005 0 102.502 102.502 0 1 0-205.005 0zM435.2 861.926a89.6 89.6 0 1 0 179.2 0 89.6 89.6 0 1 0-179.2 0z m289.843-95.666a85.427 85.427 0 1 0 170.855 0 85.427 85.427 0 1 0-170.855 0z m136.704-290.433a68.326 68.326 0 1 0 136.653 0 68.326 68.326 0 1 0-136.653 0zM759.22 219.571a51.251 51.251 0 1 0 102.502 0 51.251 51.251 0 1 0-102.503 0zM512 85.376a34.176 34.176 0 1 0 68.352 0 34.176 34.176 0 1 0-68.352 0z"/>
                </svg>
              </div>
            </div>
          {/if}

          <!-- <button on:click={getFaceRes}> 
              I have completed the face scanning certification
            </button> -->

          <!-- <div class="bg-primary pt-0.5 flex justify-center cursor-pointer items-center w-[160px] h-[160px] text-gray-100 transition rounded-lg">
            <input id="imageInput" type="file" accept="image/*" on:change={handleImageUpload} style="display: none;"/>
            <button class="max-w-full max-h-full" type="button" on:click={triggerImageUpload}>
              <svg xmlns="http://www.w3.org/2000/svg" width="100%" height="120px" viewBox="0 0 24 24"><path fill="currentColor" d="M11.5 15.577v-8.65l-2.33 2.33l-.708-.718L12 5l3.539 3.539l-.708.719L12.5 6.927v8.65zM5 19v-4.038h1V18h12v-3.038h1V19z"/></svg>
            </button>
          </div>
          <div class="flex justify-center w-[160px] h-[160px] items-center overflow-hidden rounded-lg">
            <Image src={imageUrl} alt="Uploaded Image" className=" max-w-full max-h-full rounded-lg"/>
          </div> -->
        </div>
      {/if}

      <div class="flex justify-end gap-4 absolute bottom-8 right-2">
        {#if current !== 1}
          <button
            class=" px-4 py-2 primaryButton text-gray-100 transition rounded-lg w-[100px]"
            on:click={previousStep}>{$i18n.t("Previous")}</button
          >
        {/if}

        {#if current === 2}
          {#if qrCodeFinish}
            <button
              class="px-4 py-2 primaryButton text-gray-100 transition rounded-lg w-[100px]"
              on:click={getFaceRes}
            >
              {$i18n.t("Finish")}</button
            >
          {:else}
            <button
              disabled
              class="px-4 py-2 primaryButton text-gray-600 transition rounded-lg w-[100px] mr-4"
            >
              {$i18n.t("Finish")}</button
            >
          {/if}
        {/if}
        {#if current !== 2}
          <button
            class=" px-4 py-2 flex justify-center items-center primaryButton text-gray-100 transition rounded-lg w-[100px] mr-4"
            disabled={nextLoading}
            on:click={nextStep}
          >
            {#if nextLoading}
              <svg
                class=" w-4 h-4 mr-1"
                viewBox="0 0 24 24"
                fill="currentColor"
                xmlns="http://www.w3.org/2000/svg"
                ><style>
                  .spinner_ajPY {
                    transform-origin: center;
                    animation: spinner_AtaB 0.75s infinite linear;
                  }
                  @keyframes spinner_AtaB {
                    100% {
                      transform: rotate(360deg);
                    }
                  }
                </style><path
                  d="M12,1A11,11,0,1,0,23,12,11,11,0,0,0,12,1Zm0,19a8,8,0,1,1,8-8A8,8,0,0,1,12,20Z"
                  opacity=".25"
                /><path
                  d="M10.14,1.16a11,11,0,0,0-9,8.92A1.59,1.59,0,0,0,2.46,12,1.52,1.52,0,0,0,4.11,10.7a8,8,0,0,1,6.66-6.61A1.42,1.42,0,0,0,12,2.69h0A1.57,1.57,0,0,0,10.14,1.16Z"
                  class="spinner_ajPY"
                /></svg
              >
            {/if}
            {$i18n.t("Next")}
          </button>
        {/if}
      </div>
    </div>
  </div>
</Modal>

<style>
  .timesty {
    color: #bd9257;
    font-weight: bold;
  }
  .success {
    color: #4eca70;
  }
  .model-styl {
    display: flex;
    justify-content: center;
    align-items: center;
    position: absolute;
    top: 0;
    left: 0;
    background-color: rgba(0, 0, 0, 0.5);
  }
  .pos-rel {
    position: relative;
  }
</style>