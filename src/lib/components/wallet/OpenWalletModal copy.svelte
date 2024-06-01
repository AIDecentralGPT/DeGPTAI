<script lang="ts">
  import {
    exportAccountForKeystore,
    createAccountFromMnemonic,
  } from "../../utils/wallet/dbc.js";
  import { createAccountFromSeed } from "$lib/utils/wallet/dbc.js";
  import { getContext } from "svelte";
  import { toast } from "svelte-sonner";
  import { models, settings, user } from "$lib/stores";

  import { getModels as _getModels } from "$lib/utils";
	import { SUPPORTED_FILE_TYPE, SUPPORTED_FILE_EXTENSIONS, WEBUI_BASE_URL } from '$lib/constants';

  import Modal from "../common/Modal.svelte";

  const i18n = getContext("i18n");

  export let show = false;

  let showPassword = false;
  let password = "123";
  let passwordError = "";
  let walletCreatedData = null; // 创建钱包返回的数据
	let filesInputElement;
	let inputFiles;

  function validatePassword() {
    if (password.length < 8) {
      passwordError = "Password must be at least 8 characters long.";
    } else {
      passwordError = "";
    }
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
        {$i18n.t("Open Wallet ")}
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
      <!-- <button
        class=" px-4 py-2 dark:bg-white dark:text-zinc-950 bg-black text-gray-100 transition rounded-lg"
        on:click={async () => {
          show = false;
        }}
      >
        {$i18n.t("  FINISHED  ")}
      </button>
      <button> Select Wallet File </button> -->


      <button
      class="bg-gray-50 hover:bg-gray-100 text-gray-800 dark:bg-gray-850 dark:text-white dark:hover:bg-gray-800 transition rounded-full p-1.5"
      type="button"
      on:click={() => {
        filesInputElement.click();
      }}
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 16 16"
        fill="currentColor"
        class="w-[1.2rem] h-[1.2rem]"
      >
        <path
          d="M8.75 3.75a.75.75 0 0 0-1.5 0v3.5h-3.5a.75.75 0 0 0 0 1.5h3.5v3.5a.75.75 0 0 0 1.5 0v-3.5h3.5a.75.75 0 0 0 0-1.5h-3.5v-3.5Z"
        />
      </svg>
    </button>

    <input
    bind:this={filesInputElement}
    bind:files={inputFiles}
    type="file"
    hidden
    multiple
    on:change={async () => {
      if (inputFiles && inputFiles.length > 0) {
        const _inputFiles = Array.from(inputFiles);
        _inputFiles.forEach((file) => {
          if (
            ['image/gif', 'image/webp', 'image/jpeg', 'image/png'].includes(file['type'])
          ) {
            let reader = new FileReader();
            reader.onload = (event) => {
              files = [
                ...files,
                {
                  type: 'image',
                  url: `${event.target.result}`
                }
              ];
              inputFiles = null;
              filesInputElement.value = '';
            };
            reader.readAsDataURL(file);
          } else if (
            SUPPORTED_FILE_TYPE.includes(file['type']) ||
            SUPPORTED_FILE_EXTENSIONS.includes(file.name.split('.').at(-1))
          ) {
            uploadDoc(file);
            filesInputElement.value = '';
          } else {
            toast.error(
              $i18n.t(
                `Unknown File Type '{{file_type}}', but accepting and treating as plain text`,
                { file_type: file['type'] }
              )
            );
            uploadDoc(file);
            filesInputElement.value = '';
          }
        });
      } else {
        toast.error($i18n.t(`File not found.`));
      }
    }}
  />

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
