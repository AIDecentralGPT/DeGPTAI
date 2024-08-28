<script lang="ts">
  import { getContext, onMount, onDestroy } from "svelte";
  import Modal from "../common/Modal.svelte";
  import Image from "../common/Image.svelte";
  import {
    faceliveness,
    facelivenessRes,
    sendCode,
    verifyCode,
  } from "$lib/apis/auths";
  import { user } from "$lib/stores";
  import { WEBUI_BASE_URL } from "$lib/constants";

  import { toast } from "svelte-sonner";
  import QRCode from "qrcode";
  import { goto } from "$app/navigation";

  const i18n = getContext("i18n");

  let socket;
  let messages = [];
  onMount(() => {
    // 创建 WebSocket 连接
    socket = new WebSocket("wss://test.degpt.ai/api/v1/auths/ws");

    // 监听 WebSocket 连接打开事件
    socket.addEventListener("open", () => {
      console.log("WebSocket 连接已打开");
    });

    // 监听 WebSocket 消息事件
    socket.addEventListener("message", (event) => {
      // 将收到的消息添加到 messages 列表中
      messages = [...messages, event.data];
    });

    // 监听 WebSocket 连接关闭事件
    socket.addEventListener("close", () => {
      console.log("WebSocket 连接已关闭");
    });

    // 监听 WebSocket 错误事件
    socket.addEventListener("error", (error) => {
      console.error("WebSocket 发生错误:", error);
    });
  });

  // 在组件卸载时关闭 WebSocket 连接
  onDestroy(() => {
    socket.close();
  });

  // 向服务器发送消息的函数
  function sendMessage() {
    if (socket && socket.readyState === WebSocket.OPEN) {
      socket.send("Hello Server!");
    } else {
      console.error("WebSocket 连接不可用");
    }
  }

  export let show = false;

  // 用于存储上传的图片
  let uploadedImage: File | null = null;
  let imageUrl: string | undefined = `${WEBUI_BASE_URL}/static/example.png`;

  let current = 1;
  let email = "";
  let code = "";
  let countdown = 0;
  let countdownInterval: any = null;

  function handleImageUpload(event: Event) {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files[0]) {
      uploadedImage = input.files[0];
      imageUrl = URL.createObjectURL(uploadedImage);
    }
  }

  function triggerImageUpload() {
    document.getElementById("imageInput")?.click();
  }

  function validateEmail(email: string) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  }

  function sendVerificationCode() {
    if (countdown === 0) {
      if (validateEmail(email)) {
        startCountdown();
        sendCode(email).then((res) => {
          console.log(123321, res);
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

  let qrcodeUrl = "";

  function getQrCode(url) {
    QRCode.toDataURL(url, function (err, url) {
      console.log(url);
      qrcodeUrl = url;
    });
  }

  async function nextStep() {
    let valid = true;

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

  let faceLivenessInitialData = {
    merchant_biz_id: "",
    transaction_id: "",
    transaction_url: "",
  };

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
          getQrCode(res.transaction_url);
        }
      } else {
        toast.error(res.data.message);
      }
    });
  }

  function getFaceRes() {
    facelivenessRes({
      // transaction_id: faceLivenessInitialData.transaction_id,
      // merchant_biz_id: faceLivenessInitialData.merchant_biz_id,
    }).then((res) => {
      console.log(res);
      if (res?.passed) {
        toast.success("Congratulations on passing the verification!");
        show = false;
      } else {
        toast.error(
          "Verification failed, the system detects that your face has been used!"
        );
      }
    });
  }

  let isMobile = false;

  onMount(() => {
    const userAgent = navigator.userAgent || navigator.vendor || window.opera;

    // 检查是否为移动端设备
    isMobile = /android|iPad|iPhone|iPod|IEMobile|Opera Mini/i.test(userAgent);
  });
</script>

<Modal bind:show size="lg">
  <button on:click={sendMessage}>发送消息</button>

  <!-- <button on:click={getQrCode}> show qrcode </button> -->

  <!-- <button on:click={faceLiveness}> 2. 活体检测 </button> -->

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
              class=" bg-white p-6 rounded-lg shadow-lg flex flex-col items-center h-[248px] justify-end"
            >
              <div class="">
                {#if qrcodeUrl}
                  <img class="w-[160px]" src={qrcodeUrl} alt="" />
                {:else}
                  <div
                    class="w-[160px] h-[160px] flex justify-center items-center text-white bg-gray-400 rounded-md"
                  >
                    <span class="animate-pulse">Loading...</span>
                  </div>
                {/if}
              </div>
              <p class="mt-4 text-center text-gray-700">Scan this QR code!</p>
            </div>
          {/if}
          {#if isMobile}
            <p>Preparing to jump to the face verification page</p>
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
          <button
            class=" px-4 py-2 primaryButton text-gray-100 transition rounded-lg w-[100px]"
            on:click={getFaceRes}
          >
            Finish</button
          >
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
