<script lang="ts">
  import { getContext, createEventDispatcher } from "svelte";
  import { toast } from "svelte-sonner";
  import Modal from "../common/Modal.svelte";
  import { decryptPrivateKey } from "$lib/utils/encrypt"
  import { walletKey } from "$lib/stores";

  const i18n = getContext("i18n");

  const dispatch = createEventDispatcher();

  export let show = false;

  let showPassword = false;
  let password = "";
  let loading = false;

  export let checked = false;
  $: if (show) {
    checked = false;
    loading = false;
  }

  $: buttonStyle = loading ? "background: rgba(184, 142, 86, 0.6)" : "";
  
</script>

<Modal bind:show>
  <!-- min-h-[400px] -->
  <div
    class="text-gray-700 dark:text-gray-100
	"
  >
    <div class=" flex justify-between dark:text-gray-300 px-5 pt-4 pb-1">
      <div class=" text-lg font-medium self-center">
        {$i18n.t("Confirm Password")}
      </div>

      <!-- X 关闭键 -->
      <button
        class="self-center"
        on:click={() => {
          show = false;
          loading = false;
          password = "";
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
    <!-- flex flex-col md:space-x-4 -->
    <div class=" w-full p-4 px-8">
      <!-- 输入密码 -->
      <div class="flex flex-row items-center mb-6 w-full">
        <div class="pt-0.5 max-w-[300px] w-full">
          <div class="flex flex-col w-full">
            <div class="flex-1 w-full relative">
              {#if showPassword}
                <input
                  bind:value={password}
                  type="text"
                  class=" pl-5 pr-10 py-3 rounded-md w-full text-sm outline-none border dark:border-none dark:bg-gray-850"
                  placeholder={$i18n.t("Enter Your Password")}
                  autocomplete="current-password"
                  required
                />
                <!-- 开眼图标 -->
                <button class="absolute right-3 top-1/2 -translate-y-1/2"
                  on:click={() => {
                    showPassword = false
                  }}>
                  <svg xmlns="http://www.w3.org/2000/svg" 
                    class="h-5 w-5" 
                    viewBox="0 0 20 20" 
                    fill="currentColor">
                    <path d="M10 12a2 2 0 100-4 2 2 0 000 4z" />
                    <path fill-rule="evenodd" d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z" clip-rule="evenodd" />
                  </svg>
                </button>
              {:else}
                <input
                  bind:value={password}
                  type="password"
                  class=" pl-5 pr-10 py-3 rounded-md w-full text-sm outline-none border dark:border-none dark:bg-gray-850"
                  placeholder={$i18n.t("Enter Your Password")}
                  autocomplete="current-password"
                  required
                />
                <!-- 闭眼图标 -->
                <button class="absolute right-3 top-1/2 -translate-y-1/2"
                  on:click={() => {
                    showPassword = true
                  }}>
                  <svg xmlns="http://www.w3.org/2000/svg" 
                    class="h-5 w-5" 
                    viewBox="0 0 20 20" 
                    fill="currentColor">
                    <path fill-rule="evenodd" d="M3.707 2.293a1 1 0 00-1.414 1.414l14 14a1 1 0 001.414-1.414l-1.473-1.473A10.014 10.014 0 0019.542 10C18.268 5.943 14.478 3 10 3a9.958 9.958 0 00-4.512 1.074l-1.78-1.781zm4.261 4.26l1.514 1.515a2.003 2.003 0 012.45 2.45l1.514 1.514a4 4 0 00-5.478-5.478z" clip-rule="evenodd" />
                    <path d="M12.454 16.697L9.75 13.992a4 4 0 01-3.742-3.741L2.335 6.578A9.98 9.98 0 00.458 10c1.274 4.057 5.065 7 9.542 7 .847 0 1.669-.105 2.454-.303z" />
                  </svg>
                </button>
              {/if}
            </div>
          </div>
        </div>
      </div>

      <!--  -->
      <!-- style={loading ? "background: rgba(184, 142, 86, 0.6)" : ""} -->

      <div class="flex justify-end">
        <button
          disabled={loading}
          class={" px-4 py-2 primaryButton text-gray-100 transition rounded-lg"}
          style={buttonStyle}
          on:click={async () => {
              if (!password) {
                toast.error($i18n.t(`Please enter the password!`));
                return;
              }
              try {
                await decryptPrivateKey($walletKey?.privateKey, password);
                checked = true;
                dispatch('change', checked);
                show = false;
              } catch(error) {
                toast.error($i18n.t(`Incorrect password`));
                checked = false;
              }
            }}
          >
            <span class="relative">{$i18n.t("Submit")}</span>
        </button>
      </div>
    </div>
  </div>
</Modal>

<style>
</style>
