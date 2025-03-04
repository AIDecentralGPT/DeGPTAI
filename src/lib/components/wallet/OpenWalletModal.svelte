<script lang="ts">
  import { getContext, tick } from "svelte";
  import { goto } from "$app/navigation";
  import { channel, user, settings, config } from '$lib/stores';
  import { toast } from "svelte-sonner";
  import Modal from "../common/Modal.svelte";
  import { handleWalletSignIn, unlockWalletWithPrivateKey } from "$lib/utils/wallet/ether/utils.js";
  import { importWallet } from "$lib/utils/wallet/ether/utils.js";
  import { updateWalletData } from "$lib/utils/wallet/walletUtils.js";
  import { getLanguages } from "$lib/i18n/index";

  const i18n = getContext("i18n");

  export let show = false;

  let showPassword = false;
  let password = "";
  let loading = false;
  let filesInputElement: any = null;
  let inputFiles: any = null;
  let encryptedJson: any = null; //
  let privateKey: string = '';
  let openWalletType = "privateKey";

  const uploadJson = async (file: any) => {
    // const res = await importAccountFromKeystore(file);
    // console.log("uploadJson", res);
    // encryptedJson = res; // Retrieve account pairs from the JSON file

    console.log("file", file);
    const reader = new FileReader();
    reader.readAsText(file);
    reader.onload = (e) => {
      try {
        const fileText = e.target?.result;
        if (fileText) {
          encryptedJson = JSON.parse(String(fileText));
        }
      } catch(e) {
        toast.error($i18n.t("Invalid keystore file"));
      }
    };
  }

  const initUserModels = () => {
    if ($user?.models) {
      settings.set({...$settings, models: $user?.models.split(",")});
    } else {
      settings.set({...$settings, models: $config?.default_models.split(",")});
    }
    localStorage.setItem("settings", JSON.stringify($settings));
    goto("/");
    const newChatButton = document.getElementById("new-chat-button");
    setTimeout(() => {
      newChatButton?.click();
    }, 0);
  }

  // Update user language
  async function initLanguage() {
    if ($user?.language) {
      $i18n.changeLanguage($user?.language);
    } else {
      let browserLanguage = navigator.language;
      const languages = await getLanguages();
      let localLanguage = languages.filter(
        (item) => item.code == browserLanguage
      );
      if (localLanguage.length > 0) {
        $i18n.changeLanguage(browserLanguage);
      }
    }
  }

  $: if (!show) {(async () => {
      console.log("show", show);

      password = "";
      privateKey = ""
      showPassword = false;
      inputFiles = null;
      encryptedJson = null;
    })();
  }
</script>

<Modal bind:show>
  <!-- min-h-[400px] -->
  <div class="text-gray-700 dark:text-gray-100">
    <div class=" flex justify-between dark:text-gray-300 px-5 pt-4 pb-1">
      <div class=" text-lg font-medium self-center">
        {$i18n.t("Open Wallet")}
      </div>

      <!-- X close btn -->
      <button
        class="self-center"
        on:click={() => {
          show = false;
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

    <!-- Main -->
    <!-- flex flex-col md:space-x-4 -->
    <div class=" w-full p-4 px-8">
      <div class="flex w-full">
        <label class="mr-4">
          <input
            type="radio"
            bind:group={openWalletType}
            value="privateKey"
            required
          />
          PrivateKey
        </label>
        <label>
          <input
            type="radio"
            bind:group={openWalletType}
            value="keyStore"
            required
          />
          KeyStore
        </label>
      </div>

      {#if openWalletType === "privateKey"}
        <input
          bind:value={privateKey}
          type="text"
          class="my-4  px-5 py-3 rounded-md w-full text-sm outline-none border dark:border-none dark:bg-gray-850"
          placeholder={$i18n.t("Enter Your privateKey")}
          required
        />
        <div class="flex justify-end">
          <button
            disabled={loading}
            class={" px-4 py-2 primaryButton text-gray-100 transition rounded-lg"}
            style={loading ? "background: rgba(184, 142, 86, 0.6)" : ""}
            type="submit"
            on:click={async () => {
              loading = true;
              await tick();
              console.log("The color has changed", loading);

              try {
                const walletImportedRet = await unlockWalletWithPrivateKey(
                  privateKey
                );

                if (!walletImportedRet?.ok) {
                  toast.error($i18n.t(walletImportedRet?.message));
                  loading = false;
                  return;
                }

                // Request the server to log in to the wallet account
                const walletImported = walletImportedRet?.data;
                await handleWalletSignIn({
                  walletImported,
                  password,
                  address_type: "dbc",
                  channel: $channel
                });

                // Update user model
                initUserModels();
                // Update user language
                await initLanguage();

                updateWalletData(walletImported);

                await tick();
                loading = false;

                show = false;
                password = "";
              } catch (error) {
                console.log("error, ", error, error.message);
                toast.error(error.message);
              }
              loading = false;

          
            }}
          >
            {#if loading}
              <span>{$i18n.t("Unlocking")}</span>
            {:else}
              <span>{$i18n.t("Unlock")}</span>
            {/if}
          </button>
        </div>
      {/if}

      {#if openWalletType === "keyStore"}
        <button
          class="my-4 px-4 py-2 dark:bg-white dark:text-zinc-950 bg-black text-gray-100 transition rounded-lg"
          type="button"
          on:click={() => {
            filesInputElement.click();
          }}
        >
          {$i18n.t("Select Wallet File")}
        </button>

        <input
          bind:this={filesInputElement}
          bind:files={inputFiles}
          type="file"
          hidden
          accept=".json"
          on:change={async () => {
            if (inputFiles && inputFiles.length > 0) {
              const file = inputFiles[0]; // Assuming only one file is uploaded
              if (
                file.type === "application/json" ||
                file.name.split(".").pop().toLowerCase() === "json"
              ) {
                uploadJson(file);
                inputFiles = null;
                filesInputElement.value = "";
              } else {
                toast.error(
                  $i18n.t(`Unsupported file type, please upload a JSON file.`)
                );
              }
            } else {
              toast.error($i18n.t(`File not found.`));
            }
          }}
        />
        <!-- input password -->
        {#if encryptedJson}
          <div class="mb-6 pt-0.5 max-w-[300px]">
            <div class="flex flex-col w-full">
              <div class="flex-1 relative">
                {#if showPassword}
                  <input
                    bind:value={password}
                    type="text"
                    class=" px-5 py-3 rounded-md w-full text-sm outline-none border dark:border-none dark:bg-gray-850"
                    placeholder={$i18n.t("Enter Your Password")}
                    autocomplete="current-password"
                    required
                  />
                {:else}
                  <input
                    bind:value={password}
                    type="password"
                    class=" px-5 py-3 rounded-md w-full text-sm outline-none border dark:border-none dark:bg-gray-850"
                    placeholder={$i18n.t("Enter Your Password")}
                    autocomplete="current-password"
                    required
                  />
                {/if}
              </div>
            </div>
          </div>
        {/if}
        {#if encryptedJson}
          <div class="flex justify-end">
            <button
              disabled={loading}
              class={" px-4 py-2 primaryButton text-gray-100 transition rounded-lg"}
              style={loading ? "background: rgba(184, 142, 86, 0.6)" : ""}
              type="submit"
              on:click={async () => {
                loading = true;
                await tick();
                console.log("The color has changed", loading);

                if (password=="") {
                  toast.error($i18n.t("Please input password"));
                  loading = false;
                  return;
                }

                try {
                  const walletImported = await importWallet(
                    encryptedJson,
                    password
                  );

                  // Request the server to log in to the wallet account
                  await handleWalletSignIn({
                    walletImported,
                    password,
                    address_type: "dbc",
                    channel: $channel
                  });

                  // Update user model
                  initUserModels();
                  // Update user language
                  await initLanguage();

                  updateWalletData(walletImported);

                  await tick();
                  loading = false;

                  show = false;
                  password = "";
                } catch (error) {
                  toast.error($i18n.t("Incorrect password"));
                }
                loading = false;

                const lockIndex = 0; // Lock index
              }}
            >
              {#if loading}
                <span>{$i18n.t("Unlocking")}</span>
              {:else}
                <span>{$i18n.t("Unlock")}</span>
              {/if}
            </button>
          </div>
        {/if}
      {/if}

    </div>
  </div>
</Modal>

<style>
</style>