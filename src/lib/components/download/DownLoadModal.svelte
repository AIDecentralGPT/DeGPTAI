<script lang="ts">
  import Modal from "../common/Modal.svelte";
  export let show = false;
  import { getContext } from "svelte";
  import { copyToClipboard, checkPlatform } from "$lib/utils";
  import { toast } from "svelte-sonner";
  const i18n = getContext("i18n");
</script>

<Modal bind:show size="sm">
  <div class="xs:h-auto flex flex-col w-full p-5">
    <div class="flex flex-col pt-10">
      <!-- <div class="flex my-2">
        { $i18n.t("You can copy the website below:") }
      </div> -->
      <div class="flex-1 relative">
        {#if checkPlatform() == "ios"}
          <p
            class="text-ellipsis overflow-hidden whitespace-nowrap pr-[35px] opacity-50
          px-5 py-3 rounded-md w-full leading-3 outline-none border dark:border-none dark:bg-gray-850 text-base"
          >
            https://apps.apple.com/us/app/degpt/id6504377109?platform=iphone
          </p>
          <button
            on:click={async () => {
              const res = await copyToClipboard("https://apps.apple.com/us/app/degpt/id6504377109?platform=iphone", false);
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
        {:else}
          <p
            class="text-ellipsis overflow-hidden whitespace-nowrap pr-[35px] opacity-50
          px-5 py-3 rounded-md w-full leading-3 outline-none border dark:border-none dark:bg-gray-850 text-base"
          >
            https://play.google.com/store/apps/details?id=uni.UNIEF8864C&hl=en
          </p>
          <button
            on:click={async () => {
              const res = await copyToClipboard("https://play.google.com/store/apps/details?id=uni.UNIEF8864C&hl=en", false);
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
        {/if}
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
