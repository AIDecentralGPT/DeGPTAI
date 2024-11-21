<script lang="ts">
  import { getContext, tick } from "svelte";
  import { toast } from "svelte-sonner";

  import { getModels as _getModels } from "$lib/utils";

  import Modal from "../common/Modal.svelte";
  import {
    currentWalletData,
    showConfirmUpgradeModal,
    user,
  } from "$lib/stores";
  import {
    checkMoney,
    authSigner,
    payForVip,
  } from "$lib/utils/wallet/ether/modelabi.js";
  import { openProServices, isPro } from "$lib/apis/users/index.js";

  import { getAccount } from "@wagmi/core";
  import { config } from "$lib/utils/wallet/walletconnect/index";

  const i18n = getContext("i18n");

  export let show = false;
  let loading = false;
  let showTip = false;
  let step = 0;
  let progress = 0;
  let progressInterval: NodeJS.Timeout;

  function startProgress() {
    progressInterval = setInterval(() => {
      if (step == 0 && progress <= 10) {
        if (progress < 10) {
          progress < 10 ? progress++ : (progress = 10);
        } else {
          progress = 10;
        }
      } else if (step == 1 && progress <= 20) {
        if (progress < 20) {
          progress < 10 ? (progress = 10) : progress++;
        } else {
          progress = 20;
        }
      } else if (step == 2 && progress <= 30) {
        if (progress < 30) {
          progress < 20 ? (progress = 20) : progress++;
        } else {
          progress = 30;
        }
      } else if (step == 3 && progress <= 80) {
        if (progress < 80) {
          progress < 30 ? (progress = 30) : progress++;
        } else {
          progress = 80;
        }
      } else if (step == 4 && progress <= 99) {
        if (progress < 99) {
          progress < 80 ? (progress = 80) : progress++;
        } else {
          progress = 99;
        }
      } else if (step == 5) {
        progress = 100;
      }
    }, 800);
  }

  async function handleUpgrade() {
    if (progressInterval) {
      clearInterval(progressInterval);
    }
    startProgress();
    if ($currentWalletData && $currentWalletData?.walletInfo?.address) {
    } else {
      toast.error($i18n.t("Please log in to your wallet first!"));
      return;
    }
    step = 1;

    let checkRet = await checkMoney($currentWalletData?.walletInfo?.address);
    if (!checkRet?.ok) {
      toast.error($i18n.t(checkRet.message));
      loading = false;
      showTip = false;
      return;
    }
    step = 2;

    let signerRet = await authSigner($currentWalletData, $user?.address_type);
    if (!signerRet?.ok) {
      toast.error($i18n.t(signerRet?.message));
      loading = false;
      showTip = false;
      return;
    }
    step = 3;

    if ($user?.address_type != "dbc") {
      const account = await getAccount(config);
      const provider = await account?.connector?.getProvider();
      if (provider?.namespace) {
        showTip = true;
      }
    }

    // 更新合约VIP
    let result = await payForVip(signerRet?.data);
    step = 4;
    if (result?.ok) {
      let res = await openProServices(
        localStorage.token,
        result?.data?.hash,
        0
      );
      if (res) {
        toast.success(
          $i18n.t("Congratulations on successfully upgrading pro!")
        );
        $showConfirmUpgradeModal = false;
        show = false;
        const userPro = await isPro(localStorage.token); // 发送请求到你的 API
        if (userPro && userPro.is_pro) {
          user.set({
            ...$user,
            isPro: userPro.is_pro,
            proEndDate: userPro.end_date,
          });
        }
      }
    } else {
      toast.error($i18n.t(result.message));
    }
    step = 5;
    clearInterval(progressInterval);
    loading = false;
    showTip = false;
  }
</script>

<Modal bind:show>
  <!-- min-h-[400px] -->
  <div
    class="text-gray-700 dark:text-gray-100
	"
  >
    <div class=" flex justify-between dark:text-gray-300 px-5 pt-4 pb-1">
      <div class=" text-lg font-medium self-center">
        {$i18n.t("Upgrade ")}
      </div>

      <!-- X 关闭键 -->
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

    <!-- 主体 -->
    <div class="flex flex-col md:flex-row w-full p-4 px-8 md:space-x-4">
      <div class="w-full">
        <p class="text-md mb-4 w-full">
          {$i18n.t("Are you sure to become a distinguished Plus member?")}
        </p>
        {#if showTip}
          <p class="text-sm mb-4 w-full text-gray-400 dark:text-gray-600">
            *{$i18n.t(
              "Please open the mobile app and approve the transaction request."
            )}
          </p>
        {/if}
        <!-- 提交按钮 -->
        <div class="flex justify-end my-4">
          <button
            disabled={loading}
            class=" px-4 py-2 primaryButton text-gray-100 transition rounded-lg"
            style={loading ? "background: rgba(184, 142, 86, 0.6)" : ""}
            type="submit"
            on:click={async () => {
              loading = true;
              step = 0;
              progress = 0;
              await tick();
              try {
                await handleUpgrade();
                loading = false;
              } catch (error) {
                loading = false;
              }
              // toast.success("Upgrade Successfully!");
            }}
          >
            {#if loading}
              <span>{progress}% {$i18n.t("Upgrading")}</span>
            {:else}
              <span>{$i18n.t("Yes")}</span>
            {/if}
          </button>
        </div>
      </div>
    </div>
  </div>
</Modal>

<style>
  input::-webkit-outer-spin-button,
  input::-webkit-inner-spin-button {
    /* display: none; <- Crashes Chrome on hover */
    -webkit-appearance: none;
    margin: 0; /* <-- Apparently some margin are still there even though it's hidden */
  }

  .tabs::-webkit-scrollbar {
    display: none; /* for Chrome, Safari and Opera */
  }

  .tabs {
    -ms-overflow-style: none; /* IE and Edge */
    scrollbar-width: none; /* Firefox */
  }

  input[type="number"] {
    -moz-appearance: textfield; /* Firefox */
  }

  .text-red-500 {
    color: #f56565; /* 使用常见的错误红色 */
  }
</style>
