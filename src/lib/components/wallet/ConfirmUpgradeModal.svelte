<script lang="ts">
  import { getContext, tick } from "svelte";
  import { toast } from "svelte-sonner";

  import { getModels as _getModels, checkUniapp } from "$lib/utils";

  import Modal from "../common/Modal.svelte";
  import { user, currentWalletData, downLoadUrl, showDownLoad } from "$lib/stores";
  import { openProServices } from "$lib/apis/users/index.js";

  import { updateWalletData } from "$lib/utils/wallet/walletUtils";
  import { thirdTransferDgc, transferDgc } from "$lib/utils/wallet/ether/dgc"
  import { tranAddress } from "$lib/constants"

  const i18n = getContext("i18n");

  export let show = false;
  let loading = false;

  export let viptype = "basic";
  export let viptime = "month";
  export let money = 3;

  async function upgradeVip() {
    if ($currentWalletData?.walletInfo) {
      loading = true;
      try {
        let response = {ok: false, msg: ""};
        if ($user?.address_type != "threeSide") {
          response = await transferDgc(
            tranAddress,
            money/0.0001,
            $currentWalletData?.walletInfo?.privateKey
          );
        } else {
          response = await thirdTransferDgc(
            $currentWalletData?.walletInfo?.address,
            tranAddress,
            money/0.0001
          );
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
    let result = await openProServices(localStorage.token, tx, Math.round(money/0.0001), viptype, viptime);
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
    <div class="flex flex-col">
      <div class="flex flex-col md:flex-row w-full p-4 px-8 md:space-x-4">
        {#if (floorToFixed(Number($currentWalletData?.dgcBalance), 2) - (money/0.0001)) < 0}
          <div class="w-full">
            <p class="text-md mb-4 w-full">
              {$i18n.t("The amount of DGC is insufficient, an additional {{ num }} DGC needs to be purchased. After the DGC purchase is successful, upgrade to VIP.", {num: money/0.0001})}
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
                    window.open("https://www.drcpad.io/token?name=DGCToken", "_blank");
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
