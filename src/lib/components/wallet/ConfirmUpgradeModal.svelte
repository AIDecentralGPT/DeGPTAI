<script lang="ts">
  import { getContext, tick } from "svelte";
  import { toast } from "svelte-sonner";

  import { getModels as _getModels, checkUniapp } from "$lib/utils";

  import Modal from "../common/Modal.svelte";
  import { user, currentWalletData, downLoadUrl, showDownLoad, walletKey, checkPasswordShow, binanceFlag } from "$lib/stores";
  import { openProServices } from "$lib/apis/users/index.js";

  import { updateWalletData } from "$lib/utils/wallet/walletUtils";
  import { thirdTransferDgc, transferDgc } from "$lib/utils/wallet/ether/dgc"
  import { tranAddress } from "$lib/constants"
  import CheckPasswordModal from "$lib/components/wallet/CheckPasswordModal.svelte"
  import { binanceTransferDgc } from "$lib/utils/wallet/ether/binance";

  const i18n = getContext("i18n");

  export let show = false;
  let loading = false;

  export let viptype = "basic";
  export let viptime = "month";
  export let money = 3;
  export let rate = 0.00001

  let checkPassword = false;
  async function upgradeVip() {
    if ($binanceFlag) {
      await toUpgradeVip();
    } else {
      if ($walletKey?.checked) {
        await toUpgradeVip();
      } else {
        $checkPasswordShow = true;
      }
    }
    
  }

  function checkPasswordResult(event: any) {
    if (event?.detail) {
      toUpgradeVip();
    }
  }

  async function toUpgradeVip() {
    if ($currentWalletData?.walletInfo) {
      loading = true;
      try {
        let response = {ok: false, msg: ""};
        if ($binanceFlag){
          response = await binanceTransferDgc(
            $currentWalletData?.walletInfo?.address,
            tranAddress,
            Math.round(money/rate)
          )
        } else {
          if ($user?.address_type != "threeSide") {
            response = await transferDgc(
              tranAddress,
              Math.round(money/rate),
              $currentWalletData?.walletInfo?.privateKey
            );
          } else {
            response = await thirdTransferDgc(
              $currentWalletData?.walletInfo?.address,
              tranAddress,
              Math.round(money/rate)
            );
          }
        }
        if (response?.ok) {
          if (response?.data?.hash) {
            await uploadVip(response?.data?.hash)
          }
        } else {
          toast.error($i18n.t(response?.msg))
        }
        
      } catch (error) {
        loading = false;
        toast.error(error?.message);
      }
      loading = false;
      updateWalletData($currentWalletData?.walletInfo)
    }
  } 

  async function uploadVip(tx: string) {
    let result = await openProServices(localStorage.token, tx, Math.round(money/0.0001), viptype, viptime, $binanceFlag);
    if (result?.ok) {
      user.set({
        ...$user,
        vipInfo: result?.data,
      });
      toast.success($i18n.t("VIP Upgrade Successful!"));
      show = false;
    } else {
      toast.error($i18n.t("Failed to upgrade to VIP!"));
    }
  }

  function floorToFixed(num, digits) {
    let pow = Math.pow(10, digits);
    return (Math.floor(num * pow) / pow).toFixed(digits);
  }

  function formatUSNumber(num, digits) {
    const options = {
      style: 'decimal',
      minimumFractionDigits: 0,  // 最少 0 位小数
      maximumFractionDigits: digits,  // 最多 2 位小数
    };
    return new Intl.NumberFormat('en-US', options).format(num);
  }

  $: if(show) {
    checkPassword = false;
    loading = false;
  }
</script>

{#if $checkPasswordShow}
  <CheckPasswordModal bind:show={$checkPasswordShow} bind:checked={checkPassword} on:change={checkPasswordResult}/>
{:else}
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
      <div class="flex flex-col">
        <div class="flex flex-col md:flex-row w-full p-4 px-8 md:space-x-4">
          {#if (floorToFixed(Number($currentWalletData?.dgcBalance), 2) - (money/rate)) < 0}
            <div class="w-full">
              <p class="text-md mb-4 w-full">
                {$i18n.t("The amount of DGC is insufficient, an additional {{ num }} DGC needs to be purchased. After the DGC purchase is successful, upgrade to VIP.", { num: Math.round(money/rate) })}
              </p>
              <div class="flex justify-end my-4">
                <button
                  disabled={loading}
                  class=" px-4 py-2 primaryButton text-gray-100 transition rounded-lg"
                  style={loading ? "background: rgba(184, 142, 86, 0.6)" : ""}
                  type="submit"
                  on:click={async () => {
                    // 用新标签打开
                    if (checkUniapp()) {
                      $downLoadUrl = "https://www.drcpad.io/token?name=DGCToken";
                      $showDownLoad = true;
                      show = false;
                    } else {
                      show = false;
                      if ($binanceFlag) {
                        window.open("https://www.binance.com/en/crypto/buy/USD/BNB", "_blank");    
                      } else {
                        window.open("https://www.drcpad.io/token?name=DGCToken", "_blank");
                      }     
                    }
                  }}
                >
                  <span>{$i18n.t("Recharge DGC")}</span>
                </button>
              </div>
            </div>
          {:else}
            <div class="w-full">
              <p class="text-md mb-4 w-full">
                {$i18n.t("Are you sure to become a distinguished member?")}
              </p>
              <div class="flex justify-end my-4">
                <button
                  disabled={loading}
                  class=" px-4 py-2 primaryButton text-gray-100 transition rounded-lg"
                  style={loading ? "background: rgba(184, 142, 86, 0.6)" : ""}
                  type="submit"
                  on:click={async () => {
                    loading = true;
                    await tick();
                    await upgradeVip();
                  }}
                >
                  {#if loading}
                    <span>{$i18n.t("Upgrading")}</span>
                  {:else}
                    <span>{$i18n.t("Yes")}</span>
                  {/if}
                </button>
              </div>
            </div>
          {/if}
        </div>
      </div>
    </div>
  </Modal>
{/if}

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
