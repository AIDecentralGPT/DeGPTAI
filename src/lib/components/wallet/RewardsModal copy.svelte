<script lang="ts">
  import { onMount } from "svelte";
  import { fade } from "svelte/transition";
  import dayjs from "dayjs";
  import { getContext } from "svelte";
  import { getCurrentPair } from "$lib/utils/wallet/dbc";
  import { getUsersInvited } from "$lib/apis/users";
  import Modal from "../common/Modal.svelte";
  const i18n = getContext("i18n");

  export let show = true;

  let modalElement = null;
  let mounted = false;

  let users = [];
let currentPair
  const handleKeyDown = (event: KeyboardEvent) => {
    if (event.key === "Escape") {
      show = false;
    }
  };

  onMount(async () => {
    mounted = true;

    const pair = getCurrentPair();
		currentPair = getCurrentPair();
    console.log("pair?.address", pair?.address);
    users = await getUsersInvited(localStorage.token, pair?.address);
    console.log("users", users);
  });

  $: if (mounted) {
    if (show) {
      window.addEventListener("keydown", handleKeyDown);
      document.body.style.overflow = "hidden";
    } else {
      window.removeEventListener("keydown", handleKeyDown);
      document.body.style.overflow = "unset";
    }
  }
</script>

{#if show}
  <!-- svelte-ignore a11y-click-events-have-key-events -->
  <!-- svelte-ignore a11y-no-static-element-interactions -->
  <Modal bind:show size="lg">
    <div
      class=" m-auto rounded-2xl max-w-full mx-2 bg-gray-50 dark:bg-gray-900 shadow-3xl p-4"
      on:mousedown={(e) => {
        e.stopPropagation();
      }}
    >
      <h1 class="text-xl font-semibold mb-4">{$i18n.t("view reward")}</h1>
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead>
            <tr>
              <th
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider whitespace-nowrap"
                >{$i18n.t("address invited")}</th
              >
              <!-- <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider whitespace-nowrap">{$i18n.t('role')}</th> -->
              <!-- <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider whitespace-nowrap">{$i18n.t('name')}</th> -->

              <!-- <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider whitespace-nowrap">{$i18n.t('email')}</th> -->
              <th
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider whitespace-nowrap"
                >{$i18n.t("lastActive")}</th
              >
              <th
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider whitespace-nowrap"
                >{$i18n.t("createdAt")}</th
              >
              <th
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider whitespace-nowrap"
                >{$i18n.t("rewards amount")}</th
              >
              <th
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider whitespace-nowrap"
                >{$i18n.t("notes")}</th
              >
            </tr>
          </thead>
          <tbody
            class="bg-white border-b dark:bg-gray-900 dark:border-gray-700 text-xs"
          >
            {#if users.length > 0}
              {#each users as user}
                <tr>
                  <td class="px-6 py-4 whitespace-nowrap flex items-center">
                    <img
                      src={user.profile_image_url}
                      alt="profile"
                      class="w-6 h-6 rounded-full mr-2"
                    />
                    {user.id}</td
                  >
                  <!-- <td class="px-6 py-4 whitespace-nowrap">{user.role}</td> -->
                  <!-- <td class="px-6 py-4 whitespace-nowrap flex items-center"><img src={user.profile_image_url} alt="profile" class="w-6 h-6 rounded-full mr-2"/>{user.name}</td> -->

                  <!-- <td class="px-6 py-4 whitespace-nowrap">{user.email}</td> -->
                  <td class="px-6 py-4 whitespace-nowrap"
                    >{dayjs(user.last_active_at * 1000).format(
                      "YYYY-MM-DD HH:mm:ss"
                    )}</td
                  >
                  <td class="px-6 py-4 whitespace-nowrap"
                    >{dayjs(user.created_at * 1000).format(
                      "YYYY-MM-DD HH:mm:ss"
                    )}</td
                  >
                  <td class="px-6 py-4 whitespace-nowrap">{"0DGC"}</td>
                  <!-- <td class="px-6 py-4 whitespace-nowrap">{('500DGC')}</td> -->
                  <td class="px-6 py-4 whitespace-nowrap"
                    >{$i18n.t("invite new user")}</td
                  >
                </tr>
              {/each}
            {:else}
              <div>
                You haven't invited any partners yet, click the button below to
                invite them
								<div class="text-center mt-8 flex justify-center gap-4 items-center flex-col md:flex-row">
									<p
										class="
										hidden sm:block
										flex-1
														text-ellipsis overflow-hidden whitespace-nowrap
														pr-[35px]
														px-5 py-3 rounded-md text-sm outline-none border dark:border-none dark:bg-gray-850"
									>
										{`${location.host}?inviter=${currentPair?.address}`}
									</p>
									<button
										on:click={async () => {
											const res = await copyToClipboard(`${location.host}?inviter=${currentPair?.address}`);
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
            {/if}
          </tbody>
        </table>
      </div>
    </div>
  </Modal>
{/if}

<style>
  .modal-content {
    animation: scaleUp 0.1s ease-out forwards;
  }

  @keyframes scaleUp {
    from {
      transform: scale(0.985);
      opacity: 0;
    }
    to {
      transform: scale(1);
      opacity: 1;
    }
  }
</style>
