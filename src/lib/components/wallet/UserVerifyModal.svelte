<script lang="ts">
  import { getContext, onMount, onDestroy } from "svelte";
  import Modal from "../common/Modal.svelte";
  import { WEBUI_API_BASE_URL } from "$lib/constants";
  import { copyToClipboard } from "$lib/utils";
  import {
    faceliveness,
    facelivenessRes,
    sendCode,
    verifyCode,
    servetime
  } from "$lib/apis/auths";
  import { user } from "$lib/stores";
  import { toast } from "svelte-sonner";
  import QRCode from "qrcode";
  import { goto } from "$app/navigation";

  const i18n = getContext("i18n");

  let socket:any = null;
  let message = "";
  let address = "";

  function initSocket() {
    // 创建 WebSocket 连接
    let socketUrl = '';
    if (WEBUI_API_BASE_URL.includes('https://')) {
      socketUrl = WEBUI_API_BASE_URL.replace('https://', 'wss://')
    } else {
      socketUrl = WEBUI_API_BASE_URL.replace('http://', 'ws://')
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
        user.set(newUser)
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

  function validateEmail(email: string) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  }

  function sendVerificationCode() {
    if (countdown === 0) {
      if (validateEmail(email)) {
        startCountdown();
        sendCode(localStorage.token, email).then((res) => {
          console.log("verification-code:", res);
        });
      } else {
        toast.error("Please enter a valid email address.");
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
        toast.error("Please enter a valid email address.");
        valid = false;
        return;
      }
      if (!code) {
        toast.error("Please enter the verification code.");
        valid = false;
        return;
      }

      await verifyCode(email, code)
        .then((res) => {
          console.log("verifyCode res", res);

          if (true) {
            // setUser({
            //   email: email,
            //   name: name,
            //   image: uploadedImage,
            // });

            email = email;
            current = current + 1;
            faceLiveness();
          } else {
            toast.error(res.detail);
          }
        })
        .catch((error) => {
          console.log(error);
          toast.error(error);
          valid = false;
        });
    } else if (current === 2) {
      // if (!uploadedImage) {
      //   toast.error("Please upload an image.");
      //   valid = false;
      //   return;
      // }

      // 这里可以开始异步检查唯一性了，调异步服务任务
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
      console.log(res);
      faceLivenessInitialData = res;
      if (res.transaction_url) {
        if (isMobile) {
          await goto(res.transaction_url);
        } else {
          faceTime = new Date(res.face_time)
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

  function getQrCode(url) {
    QRCode.toDataURL(url, function (err, url) {
      console.log(url);
      qrcodeUrl = url;
      qrCodeFinish = false;
      checkQrResult = false;
      startQrCountdown()
    });
  }

  // 二维码有效时长
  let showQrTime = '05:00';
  let countdownQrInterval: any = null;
  function startQrCountdown() {
    if (faceTime) {
      // 不为空先清除计时器值
      if (countdownQrInterval) {
        showQrTime = '05:00';
        clearInterval(countdownQrInterval);
      }
      countdownQrInterval = setInterval(() => {
        let comptime = Math.floor((new Date().getTime() - faceTime.getTime() - timeDiff) / 1000);
        let qrcountdown = 300 - comptime;
        let minute = Math.floor(qrcountdown / 60);
        let second = qrcountdown % 60;
        showQrTime = (minute > 9 ? minute : "0" + minute) + ":" + (second > 9 ? second : "0" + second);
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
          $i18n.t("Verification failed, the system detects that your face has been used!")
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
    const userAgent = navigator.userAgent || navigator.vendor || window.opera;

    // 检查是否为移动端设备
    isMobile = /android|iPad|iPhone|iPod|IEMobile|Opera Mini/i.test(userAgent);

    // 时间校准
    serveTime();
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
    initSocket();
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
    if (scoket) {
      socket.close();
    }
  });

</script>

<Modal bind:show size="lg">

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
            <strong>{$i18n.t("Authenticated eamil address:")}</strong>
            <span class="text-primary">{email}</span>
          </div>
        </div>
      {/if}

      {#if current === 1}
        <div class="w-4/5 flex flex-col">
          <!-- flex-wrap gap-2 xl:flex-nowrap  xl:gap-0 -->

          <div
            class="mb-6 pt-0.5 flex justify-start w-full
          flex-col gap-2 items-baseline md:items-center md:flex-row

          "
          >
            <label
              for="email"
              class="block text-sm font-medium dark:bg-zinc-950 dark:text-white bg-white text-black border-gray-300 w-[60px]"
              >Email:</label
            >
            <div class="flex items-center justify-around flex-1 space-x-4">
              <input
                aria-label="email"
                id="emailInput"
                type="email"
                placeholder="Enter email address"
                bind:value={email}
                class="px-4 py-2 dark:bg-zinc-950 dark:text-white bg-white text-black border border-gray-300 rounded-lg flex-1"
              />
              <button
                class="w-[90px] px-4 py-2 dark:bg-white dark:text-zinc-950 bg-black text-gray-100 transition rounded-lg flex items-center justify-center {countdown >
                0
                  ? 'opacity-50 cursor-not-allowed'
                  : ''}"
                type="button"
                on:click={sendVerificationCode}
                disabled={countdown > 0}
              >
                {#if countdown > 0}
                  {countdown}s
                {/if}
                {#if countdown === 0}
                  Send
                {/if}
              </button>
            </div>
          </div>
          <div
            class="mb-6 pt-0.5 w-full flex justify-start
          
          flex-col gap-2 items-baseline md:items-center md:flex-row
          
          "
          >
            <label
              for="code"
              class="block text-sm font-medium dark:bg-zinc-950 dark:text-white bg-white text-black border-gray-300 w-[60px]"
              >Code:</label
            >
            <input
              aria-label="code"
              id="verificationCodeInput"
              type="text"
              placeholder="Enter verification code"
              bind:value={code}
              class="px-4 py-2 dark:bg-zinc-950 dark:text-white bg-white text-black border border-gray-300 rounded-lg flex-1"
            />
          </div>
        </div>
      {/if}

      {#if current === 2}
        <div class="flex flex-col justify-start items-center gap-4">
          {#if !isMobile}
            <div
              class="rounded-lg flex flex-col items-center h-[288px]"
            >
              <div class="flex flex-col items-center">
                {#if qrcodeUrl}
                  <p class="text-center text-gray-100">Please use your mobile phone to scan the QR code below for identity verification</p>
                  <div class="flex justify-center items-center w-[200px] h-[180px] m-2 pos-rel">
                    <img class="w-[160px]" src={qrcodeUrl} alt="" />
                    {#if checkQrResult}
                      <div class="w-[200px] h-[180px] model-styl">
                        <button
                          class=" px-4 py-2 primaryButton text-gray-100 transition rounded-lg w-[100px]"
                          on:click={faceLiveness}>Try again</button
                        > 
                      </div>
                    {/if}
                    {#if qrCodeFinish}
                      <div class="w-[200px] h-[180px] model-styl">
                        <svg xmlns="http://www.w3.org/2000/svg" 
                          class="icon" viewBox="0 0 1024 1024" 
                          version="1.1"  
                          width="100" 
                          height="100">
                            <path d="M512 832c-176.448 0-320-143.552-320-320S335.552 192 512 192s320 143.552 320 320-143.552 320-320 320m0-704C300.256 128 128 300.256 128 512s172.256 384 384 384 384-172.256 384-384S723.744 128 512 128" fill="#4ECA70"></path>
                            <path d="M619.072 429.088l-151.744 165.888-62.112-69.6a32 32 0 1 0-47.744 42.624l85.696 96a32 32 0 0 0 23.68 10.688h0.192c8.96 0 17.536-3.776 23.616-10.4l175.648-192a32 32 0 0 0-47.232-43.2" fill="#4ECA70"></path>
                          </svg>
                      </div>
                    {/if}
                  </div>  
                  {#if checkQrResult}
                    {#if address}
                      <div class="flex flex-row items-center">
                        {$i18n.t("Your face has been used")}
                      </div>
                      <div class="flex">
                        <p class="w-[300px] dark:text-gray-500 dark:bg-gray-650 text-ellipsis overflow-hidden whitespace-nowrap">Wallet Adress: { address }</p>
                        <button
                          on:click={async () => {
                            const res = await copyToClipboard(address);
                            if (res) {
                              toast.success($i18n.t("Copying to clipboard was successful!"));
                            }
                          }}
                          type="button"
                          class="px-3 py-2 text-sm-12 dark:text-gray-300 dark:bg-gray-650 rounded-md fs12">
                          <svg
                            xmlns="http://www.w3.org/2000/svg"
                            width="1em"
                            height="1em"
                            viewBox="0 0 512 512">
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
                        {message}
                      </div>
                    {/if}
                  {:else}
                    {#if qrCodeFinish}
                      <div class="flex flex-row items-center success">
                        <span>{message}<span>
                      </div>
                    {:else}
                      <p class="text-center text-gray-100">QR code is valid for 5 minutes</p>
                      <div class="flex flex-row items-center timesty">
                        <svg xmlns="http://www.w3.org/2000/svg"
                          class="icon" 
                          viewBox="0 0 1024 1024" 
                          version="1.1" 
                          width="20" height="20">
                          <path d="M512 53.333333C258.688 53.333333 53.333333 258.688 53.333333 512S258.688 970.666667 512 970.666667 970.666667 765.312 970.666667 512 765.312 53.333333 512 53.333333z m0 64c217.962667 0 394.666667 176.704 394.666667 394.666667S729.962667 906.666667 512 906.666667 117.333333 729.962667 117.333333 512 294.037333 117.333333 512 117.333333z" fill="#BD9257"/>
                          <path d="M661.333333 554.666667a32 32 0 0 1 3.072 63.850666L661.333333 618.666667h-192a32 32 0 0 1-3.072-63.850667L469.333333 554.666667h192z" fill="#BD9257"/>
                          <path d="M458.666667 288a32 32 0 0 1 31.850666 28.928L490.666667 320v256a32 32 0 0 1-63.850667 3.072L426.666667 576V320a32 32 0 0 1 32-32z" fill="#BD9257"/>
                        </svg>&nbsp;&nbsp;{showQrTime}
                      </div>
                    {/if}
                  {/if}
                {:else}
                  <div class="mt-6 w-[160px] h-[160px] flex justify-center items-center text-white bg-gray-400 rounded-md">
                    <span class="animate-pulse">Loading...</span>
                  </div>
                {/if}
              </div>
            </div>
          {/if}
          {#if isMobile}
            <p>Preparing to switch to the face verification page</p>
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
        <button
          class=" px-4 py-2 primaryButton text-gray-100 transition rounded-lg w-[100px]"
          on:click={previousStep}>Previous</button
        >

        {#if current === 2}
          {#if qrCodeFinish}
            <button
              class="px-4 py-2 primaryButton text-gray-100 transition rounded-lg w-[100px]"
              on:click={getFaceRes}
            >
              Finish</button
            >
          {:else}
            <button disabled
              class="px-4 py-2 primaryButton text-gray-600 transition rounded-lg w-[100px]"
            >
              Finish</button
            >
          {/if}     
        {/if}
        {#if current !== 2}
          <button
            class=" px-4 py-2 primaryButton text-gray-100 transition rounded-lg w-[100px]"
            on:click={nextStep}>Next</button
          >
        {/if}
      </div>
    </div>
  </div>
</Modal>

<style>
.timesty{
  color: #BD9257;
  font-weight: bold;
}
.success {
  color: #4ECA70;
}
.model-styl {
  display: flex;
  justify-content: center;
  align-items: center;
  position: absolute;
  top: 0;
  left: 0;
  background-color: rgba(0,0,0,0.5);
}
.pos-rel {
  position: relative;
}
</style>
