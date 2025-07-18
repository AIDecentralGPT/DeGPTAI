<script lang="ts">
    import { toast } from "svelte-sonner";
    import Modal from "../common/Modal.svelte";
    export let show = false;
    import { getContext } from "svelte";
    import { copyToClipboard } from "$lib/utils";
    const i18n = getContext("i18n");
    import { user, } from "$lib/stores";
    import { RewardProperties } from "$lib/constants"
  </script>
  
  <Modal bind:show size="lg">
    <div class="max-h-[80vh] xs:h-auto flex flex-col">
  
      <div class=" flex justify-end dark:text-gray-300 px-5 pt-4 pb-1">
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
  
      <div class="  p-6 shadow-md sm:mt-4 mt-0 flex-1">
        <div class="text-center">
          <h2 class="text-2xl font-bold mb-4">{$i18n.t('Invite Friends to Earn DGC Rewards')}</h2>
        </div>
        <div class="flex flex-col md:flex-row justify-between space-x-0 md:space-x-4 items-stretch max-h-[50vh] overflow-y-auto">
          <div
            class="flex-1 text-center p-6 coinType rounded-lg h-full min-h-auto  sm:min-h-[150px]  flex flex-col"
          >
            <div class="icon-wrapper">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="1em"
                height="1em"
                viewBox="0 0 24 24"
              >
                <path
                  fill="currentColor"
                  d="M15.729 3.884c1.434-1.44 3.532-1.47 4.693-.304c1.164 1.168 1.133 3.28-.303 4.72l-2.423 2.433a.75.75 0 0 0 1.062 1.059l2.424-2.433c1.911-1.919 2.151-4.982.303-6.838c-1.85-1.857-4.907-1.615-6.82.304L9.819 7.692c-1.911 1.919-2.151 4.982-.303 6.837a.75.75 0 1 0 1.063-1.058c-1.164-1.168-1.132-3.28.303-4.72z"
                />
                <path
                  fill="currentColor"
                  d="M14.485 9.47a.75.75 0 0 0-1.063 1.06c1.164 1.168 1.133 3.279-.303 4.72l-4.847 4.866c-1.435 1.44-3.533 1.47-4.694.304c-1.164-1.168-1.132-3.28.303-4.72l2.424-2.433a.75.75 0 0 0-1.063-1.059l-2.424 2.433c-1.911 1.92-2.151 4.982-.303 6.838c1.85 1.858 4.907 1.615 6.82-.304l4.847-4.867c1.911-1.918 2.151-4.982.303-6.837"
                />
              </svg>
            </div>
            <h3 class="text-lg font-bold mb-2">01</h3>
            <p class="text-sm">
              {$i18n.t('Invite a friend to create a wallet to earn {{regist}} DGC rewards,you friend will also earn {{invite}} DGC', RewardProperties)}
            </p>
          </div>
          <div class=" flex flex-col justify-center items-center">
            <svg
            class="rotate-90 sm:rotate-0"

              xmlns="http://www.w3.org/2000/svg"
              width="1em"
              height="1em"
              viewBox="0 0 20 20"
              ><path
                fill="currentColor"
                fill-rule="evenodd"
                d="M5 2.643v14.765c.092.32.299.511.619.572c.32.061.633-.024.94-.255l8.107-6.993A.944.944 0 0 0 15 10a.94.94 0 0 0-.334-.73L6.58 2.295c-.232-.197-.639-.383-1.061-.253c-.282.087-.455.287-.519.6"
              /></svg
            >
          </div>
          <div
            class="flex-1 text-center p-6 coinType rounded-lg h-full min-h-auto sm:min-h-[150px]  flex flex-col"
          >
            <div class="icon-wrapper">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="1em"
                height="1em"
                viewBox="0 0 15 15"
              >
                <path
                  fill="none"
                  stroke="currentColor"
                  d="M.5 3.5v9a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-8a1 1 0 0 0-1-1H3m-2.5 0v-1a1 1 0 0 1 1-1h8a1 1 0 0 1 1 1v1H3m-2.5 0H3m6 6h3"
                />
              </svg>
            </div>
            <h3 class="text-lg font-bold mb-2">02</h3>
            <p class="text-sm">
              {$i18n.t('The user you invite must complete wallet creation and KYC verification process before you can receive the reward')}
            </p>
          </div>
          <!-- <div class=" flex flex-col justify-center items-center">
            <svg
            class="rotate-90 sm:rotate-0"
              xmlns="http://www.w3.org/2000/svg"
              width="1em"
              height="1em"
              viewBox="0 0 20 20"
              ><path
                fill="currentColor"
                fill-rule="evenodd"
                d="M5 2.643v14.765c.092.32.299.511.619.572c.32.061.633-.024.94-.255l8.107-6.993A.944.944 0 0 0 15 10a.94.94 0 0 0-.334-.73L6.58 2.295c-.232-.197-.639-.383-1.061-.253c-.282.087-.455.287-.519.6"
              /></svg
            >
          </div>
          <div
            class="flex-1 text-center p-6 coinType rounded-lg h-full min-h-auto sm:min-h-[150px]  flex flex-col"
          >
            <div class="icon-wrapper">
                <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 512 512"><path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="32" d="M176 464h160m-80 0V336m128-112c0-50.64-.08-134.63-.12-160a16 16 0 0 0-16-16l-223.79.26a16 16 0 0 0-16 15.95c0 30.58-.13 129.17-.13 159.79c0 64.28 83 112 128 112S384 288.28 384 224"/><path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="32" d="M128 96H48v16c0 55.22 33.55 112 80 112M384 96h80v16c0 55.22-33.55 112-80 112"/></svg>
            </div>
            <h3 class="text-lg font-bold mb-2">03</h3>
            <p class="text-sm text-gray-600">
              {$i18n.t('If your friends purchase DGC on DeepLink, you will receive a 10% DGC commission reward.')}
            </p>
          </div> -->
        </div>

        <div class="text-center mt-8 flex justify-center gap-4 items-center flex-col md:flex-row">
          <p
            class="
            hidden sm:block
            flex-1
                    text-ellipsis overflow-hidden whitespace-nowrap
                    pr-[35px]
                    px-5 py-3 rounded-md text-sm outline-none border dark:border-none dark:bg-gray-850"
          >
            https://{`${location.host}/invite/${$user?.id}`}
          </p>
          <button
            on:click={async () => {
              const res = await copyToClipboard(`https://${location.host}/invite/${ $user?.id}`);
              if (res) {
                toast.success($i18n.t("Copying to clipboard was successful!"));
              }
            }}
            type="button"
            class="primaryButton rounded-3xl flex gap-1 items-center p-6 py-2 ] mt-4 md:mt-0"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="1em"
              height="1em"
              viewBox="0 0 256 256"
              ><g fill="currentColor"
                ><path
                  d="m223.69 42.18l-58.22 192a8 8 0 0 1-14.92 1.25L108 148l-87.42-42.55a8 8 0 0 1 1.25-14.92l192-58.22a8 8 0 0 1 9.86 9.87"
                  opacity="0.2"
                /><path
                  d="M227.32 28.68a16 16 0 0 0-15.66-4.08h-.15L19.57 82.84a16 16 0 0 0-2.49 29.8L102 154l41.3 84.87a15.86 15.86 0 0 0 14.44 9.13q.69 0 1.38-.06a15.88 15.88 0 0 0 14-11.51l58.2-191.94v-.15a16 16 0 0 0-4-15.66m-69.49 203.17l-.05.14v-.07l-40.06-82.3l48-48a8 8 0 0 0-11.31-11.31l-48 48l-82.33-40.06h-.07h.14L216 40Z"
                /></g
              ></svg
            >
            {$i18n.t('Invite friends now')}
          </button>
        </div>
      </div>
    </div>
  </Modal>
  
  <style>
    .icon-wrapper {
      display: flex;
      align-items: center;
      justify-content: center;
      width: 3em;
      height: 3em;
      border-radius: 50%;
      background-color: rgba(184, 142, 86, 1);
      margin: 0 auto 1em;
    }
  
    .icon-wrapper svg {
      width: 1.5em;
      height: 1.5em;
      fill: white;
    }
  </style>
  