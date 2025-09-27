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
              {:else}
                <input
                  bind:value={password}
                  type="password"
                  class=" pl-5 pr-10 py-3 rounded-md w-full text-sm outline-none border dark:border-none dark:bg-gray-850"
                  placeholder={$i18n.t("Enter Your Password")}
                  autocomplete="current-password"
                  required
                />
              {/if}
              <button
                type="button"
                class="absolute inset-y-0 right-0 px-3 py-2 text-sm dark:text-gray-300 dark:bg-gray-850 rounded-md"
                on:click={() => (showPassword = !showPassword)}
                >
                  {#if showPassword}
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width="1em"
                      height="1em"
                      viewBox="0 0 512 512"
                      ><path
                        fill="none"
                        stroke="currentColor"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="32"
                        d="M255.66 112c-77.94 0-157.89 45.11-220.83 135.33a16 16 0 0 0-.27 17.77C82.92 340.8 161.8 400 255.66 400c92.84 0 173.34-59.38 221.79-135.25a16.14 16.14 0 0 0 0-17.47C428.89 172.28 347.8 112 255.66 112"
                      /><circle
                        cx="256"
                        cy="256"
                        r="80"
                        fill="none"
                        stroke="currentColor"
                        stroke-miterlimit="10"
                        stroke-width="32"
                      /></svg
                    >
                  {:else}
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width="1em"
                      height="1em"
                      viewBox="0 0 24 24"
                      ><g
                        fill="none"
                        stroke="currentColor"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        ><path
                          d="M9.88 9.88a3 3 0 1 0 4.24 4.24m-3.39-9.04A10 10 0 0 1 12 5c7 0 10 7 10 7a13.2 13.2 0 0 1-1.67 2.68"
                        /><path
                          d="M6.61 6.61A13.5 13.5 0 0 0 2 12s3 7 10 7a9.74 9.74 0 0 0 5.39-1.61M2 2l20 20"
                        /></g
                      ></svg
                    >
                  {/if}
                </button>
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
