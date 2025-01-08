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
              const res = await copyToClipboard(
                "https://apps.apple.com/us/app/degpt/id6504377109?platform=iphone",
                false
              );
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
              const res = await copyToClipboard(
                "https://play.google.com/store/apps/details?id=uni.UNIEF8864C&hl=en",
                false
              );
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
    <div class="flex justify-center pt-5">
      {#if checkPlatform() == "ios"}
        <button
          class="flex flex-row items-center rounded-full px-4 py-2 primaryButton text-gray-100"
          on:click={() => {
            window.open(
              "https://apps.apple.com/us/app/degpt/id6504377109?platform=iphone",
              "_blank"
            );
          }}
        >
          <svg
            class="icon fill-white"
            viewBox="0 0 1024 1024"
            version="1.1"
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
          >
            <path
              d="M631.125333 128c6.698667 44.074667-11.861333 87.210667-36.266666 117.76-26.154667 32.725333-71.168 58.069333-114.858667 56.746667-8.021333-42.154667 12.416-85.632 37.248-114.858667 27.221333-32.213333 73.941333-56.917333 113.877333-59.648z m131.157334 620.117333c22.528-33.408 30.890667-50.261333 48.384-87.936-127.104-46.805333-147.456-221.696-21.674667-288.853333-38.4-46.506667-92.288-73.557333-143.146667-73.557333-36.693333 0-61.824 9.301333-84.650666 17.706666-19.029333 6.997333-36.437333 13.44-57.685334 13.44-22.954667 0-43.264-7.04-64.512-14.421333-23.338667-8.106667-47.872-16.64-78.293333-16.64-57.130667 0-117.888 33.792-156.416 91.52-54.186667 81.365333-44.970667 234.24 42.922667 364.501333 31.36 46.592 73.301333 98.986667 128.213333 99.413334 22.741333 0.256 37.930667-6.314667 54.314667-13.44 18.773333-8.149333 39.168-17.066667 74.496-17.194667 35.498667-0.213333 55.594667 8.746667 74.069333 17.066667 16 7.082667 30.805333 13.696 53.376 13.44 54.912-0.426667 99.2-58.453333 130.56-105.045334z"
            />
          </svg>
          <span class="truncate">App Store</span>
        </button>
      {:else}
        <button
          class="flex flex-row items-center rounded-full px-4 py-2 mr-3 primaryButton text-gray-100"
          on:click={() => {
            window.open("https://play.google.com/store/apps/details?id=uni.UNIEF8864C&hl=en", "_blank");
          }}
        >
          <svg
            class="icon mr-1 fill-white"
            viewBox="0 0 1024 1024"
            version="1.1"
            xmlns="http://www.w3.org/2000/svg"
            width="20"
            height="20"
          >
            <path
              d="M808.398269 218.955161c20.458525 11.691232 27.566623 37.753501 15.876521 58.213157l-65.330296 114.329713c119.461015 74.88989 203.198446 202.202702 217.966199 350.95283 2.492185 25.107214-17.227161 46.882472-42.457572 46.882472H85.333333c-25.230411 0-44.949757-21.775258-42.457571-46.882472 14.120124-142.220715 91.287453-264.84528 202.445704-340.790817l-71.137484-124.491726c-11.691232-20.459656-4.583135-46.521925 15.876521-58.213157 20.459656-11.691232 46.523055-4.583135 58.214287 15.876521l71.589581 125.281766c58.218808-25.812486 122.559011-40.113448 190.028856-40.113448 60.891832 0 119.233837 11.648283 172.825431 32.893457l67.465324-118.061775c11.691232-20.459656 37.754631-27.567753 58.214287-15.876521zM317.895488 554.666667c-23.563302 0-42.666667 19.102234-42.666667 42.666666s19.103364 42.666667 42.666667 42.666667c23.565563 0 42.666667-19.102234 42.666667-42.666667s-19.101104-42.666667-42.666667-42.666666z m384 0c-23.563302 0-42.666667 19.102234-42.666667 42.666666s19.103364 42.666667 42.666667 42.666667c23.565563 0 42.666667-19.102234 42.666667-42.666667s-19.101104-42.666667-42.666667-42.666666z"
            />
          </svg>
          <span class="truncate">Android</span>
        </button>
      {/if}
    </div>
  </div>
</Modal>
