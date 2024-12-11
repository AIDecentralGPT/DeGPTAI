<script lang="ts">
  import Modal from "../common/Modal.svelte";
  export let show = false;
  import { getContext } from "svelte";
  import { copyToClipboard } from "$lib/utils";
  import { toast } from "svelte-sonner";
  const i18n = getContext("i18n");
</script>

<Modal bind:show size="sm">
  <div class="xs:h-auto flex flex-col w-full p-5">
    <div class=" flex justify-between dark:text-gray-300 pb-1">
      <div class=" text-base font-medium self-center">
        {$i18n.t("Download")}
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
    <div class="flex flex-col pt-2">
      <div class="flex my-2">
        { $i18n.t("You can copy the website below:") }
      </div>
      <div class="flex-1 relative">
        <p
          class="text-ellipsis overflow-hidden whitespace-nowrap pr-[35px] opacity-50
          px-5 py-3 rounded-md w-full leading-3 outline-none border dark:border-none dark:bg-gray-850 text-base"
        >
          https://www.decentralgpt.org/
        </p>
        <button
          on:click={async () => {
            const res = await copyToClipboard("https://www.decentralgpt.org/");
            if (res) {
              toast.success($i18n.t("Copying to clipboard was successful!"));
            }
          }}
          type="button"
          class="absolute inset-y-0 right-0 px-3 py-2 leading-3 dark:text-gray-300 dark:bg-gray-650 rounded-md text-xs"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="1em"
            height="1em"
            viewBox="0 0 512 512"
            ><rect
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
            /><path
              fill="none"
              stroke="currentColor"
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="32"
              d="m383.5 128l.5-24a56.16 56.16 0 0 0-56-56H112a64.19 64.19 0 0 0-64 64v216a56.16 56.16 0 0 0 56 56h24"
            /></svg
          >
        </button>
      </div>
    </div>
    <div class="text-center pt-5">
      <button
        class="primaryButton px-5 py-1 rounded-lg"
        on:click={() => {
          show = false;
        }}
      >
        {$i18n.t("Close")}
      </button>
    </div>
  </div>
</Modal>
