<script>
  import { WEBUI_BASE_URL } from "$lib/constants";
  import { WEBUI_NAME, user } from "$lib/stores";
  import { goto } from "$app/navigation";
  import { onMount, getContext } from "svelte";

  import dayjs from "dayjs";
  import relativeTime from "dayjs/plugin/relativeTime";
  dayjs.extend(relativeTime);

  import { toast } from "svelte-sonner";

  import {
    getById,
    getList,
    deleteById,
    updateById,
    switchStatus
  } from "$lib/apis/rewarddate";

  import AddRewardDateModal from "$lib/components/rewarddate/AddRewardDateModal.svelte";
  import Pagination from "$lib/components/common/Pagination.svelte";

  const i18n = getContext("i18n");

  let loaded = false;
  let rewarddates = [];

  let total = 0;

  let search = "";
  let status = "";
  let selectedData = null;

  let loading = false;

  let page = 1;

  let showSettingsModal = false;
  let showAddRewardDateModal = false;

  let showUserChatsModal = false;
  let showEditUserModal = false;

  $: if (page || search || status) {
    handleRequest();
  }

  const handleRequest = async () => {
    loading = true;
    const res = await getList(
      localStorage.token,
      page,
      search,
      status
    );
    console.log("rewarddates", res);
    rewarddates = res?.data || [];
    total = res?.total;
    loading = false;
  };

  const switchStatusHandler = async (id) => {
    const res = await switchStatus(localStorage.token, id).catch((error) => {
      toast.error(error);
      return null;
    });
    if (res) {
      handleRequest();
      toast.success($i18n.t("Successfully updated."));
    }
  };

  const deleteHandler = async (id) => {
    const res = await deleteById(localStorage.token, id).catch((error) => {
      toast.error(error);
      return null;
    });
    if (res) {
      handleRequest();
    }
  };

  onMount(async () => {
    handleRequest();
    loaded = true;
  });
</script>

<svelte:head>
  <title>{$i18n.t("Admin Panel")} | {$WEBUI_NAME}</title>
</svelte:head>

<AddRewardDateModal
  bind:show={showAddRewardDateModal}
  on:save={async () => {
    handleRequest();
  }}
/>

<div class=" flex flex-col w-full min-h-screen">
  {#if loaded}
    <div class="flex justify-between px-4 pt-3 mt-0.5 mb-1 w-full">
      <div class="flex items-center text-xl font-semibold">
        {$i18n.t("Reward upkeep")}
      </div>
      <button
        class="self-center"
        on:click={() => {
          goto("/");
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

    <hr class=" my-2 dark:border-gray-850 w-full" />

    <div class="px-6 w-full">
      <div class="mt-0.5 mb-3 gap-1 flex flex-col md:flex-row justify-between">
        <div class="flex md:self-center text-base font-medium px-0.5">
          {$i18n.t("All Reward Range")}
          <div
            class="flex self-center w-[2px] h-5 mx-2.5 bg-gray-200 dark:bg-gray-700"
          />
          <span class="text-base font-medium text-gray-600 dark:text-gray-300"
            >{total}</span
          >
        </div>

        <div class="flex gap-1">
          <input
            class="w-full md:w-60 rounded-xl py-1.5 px-4 text-sm dark:text-gray-300 bg-gray-100 dark:bg-gray-850 outline-none"
            placeholder={$i18n.t("Search")}
            bind:value={search}
          />

          <div class="flex gap-0.5">
            <div class="flex flex-row items-center ml-2">
              <div class="whitespace-nowrap">{$i18n.t("Status")}：</div>
              <select
                class="w-full capitalize rounded-lg py-1.5 pl-4 pr-8 text-sm dark:text-gray-300 bg-gray-100 dark:bg-gray-850 disabled:text-gray-500 dark:disabled:text-gray-500 outline-none"
                on:change={(e) => {
                  page = 1;
                  status = e.target.value;
                }}
              >
                <option value="">{$i18n.t("all")}</option>
                <option value="close">{$i18n.t("Close")}</option>
                <option value="open">{$i18n.t("Open")}</option>
              </select>
            </div>
          </div>
          {#if $user?.role == "admin"}
            <button class="ml-2"
              on:click={() => {
                showAddRewardDateModal = true;
              }}>
              <svg 
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 1024 1024"
                fill="currentColor"
                class="w-6 h-6"
              >
                <path d="M768 460.8h-204.8v-204.8c0-22.528-18.432-40.96-40.96-40.96s-40.96 18.432-40.96 40.96v204.8h-204.8c-22.528 0-40.96 18.432-40.96 40.96s18.432 40.96 40.96 40.96h204.8v204.8c0 22.528 18.432 40.96 40.96 40.96s40.96-18.432 40.96-40.96v-204.8h204.8c22.528 0 40.96-18.432 40.96-40.96s-18.432-40.96-40.96-40.96z" p-id="5628"></path><path d="M512 81.92c237.568 0 430.08 192.512 430.08 430.08s-192.512 430.08-430.08 430.08S81.92 749.568 81.92 512 274.432 81.92 512 81.92m0-81.92C229.376 0 0 229.376 0 512s229.376 512 512 512 512-229.376 512-512S794.624 0 512 0z"/>
              </svg>
            </button>
          {/if}
        </div>
      </div>

      <div class="relative w-full overflow-auto whitespace-nowrap">
        <table
          class="w-full text-sm text-left text-gray-500 dark:text-gray-400 table-auto"
        >
          <thead
            class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-850 dark:text-gray-400"
          >
            <tr>
              <th scope="col" class="px-3 py-3"> {$i18n.t("name")} </th>
              <th scope="col" class="px-3 py-3"> {$i18n.t("starttime")} </th>
              <th scope="col" class="px-3 py-3"> {$i18n.t("endtime")} </th>
              <th scope="col" class="px-3 py-3"> {$i18n.t("Status")} </th>
              <th scope="col" class="px-3 py-3 text-right" />
            </tr>
          </thead>

          {#if loading}
            <tr>
              <td colspan="6">
                <div class="py-[100px] w-full text-center text-lg">
                  Loading...
                </div>
              </td>
            </tr>
          {:else}
            <tbody>
              {#each rewarddates as item}
                <tr
                  class="bg-white border-b text-gray-900 dark:text-white text-xs"
                >
                  <td class="px-3 py-2 min-w-[7rem] w-max">
                    <div class="flex flex-row w-max">
                      <div class=" font-medium self-center">{item.name}</div>
                    </div>
                  </td>
                  <td
                    class="px-3 py-2 font-medium text-gray-900 dark:text-white w-max"
                  >
                    <div class="flex flex-row w-max">
                      <div class=" font-medium self-center">{dayjs(item.start_time).format('YYYY-MM-DD')}</div>
                    </div>
                  </td>
                  <td
                    class="px-3 py-2 font-medium text-gray-900 dark:text-white w-max"
                  >
                    <div class="flex flex-row w-max">
                      <div class=" font-medium self-center">{dayjs(item.end_time).format('YYYY-MM-DD')}</div>
                    </div>
                  </td>
                  <td class=" px-3 py-2">
                    {#if item.open}
                      <button class="bg-green-600 text-gray-50 px-3 py-1 rounded-lg"
                      on:click={() => {
                        switchStatusHandler(item.id);
                      }}>{$i18n.t("Open")}</button>
                    {:else}
                      <button class="bg-red-600 text-gray-50 px-3 py-1 rounded-lg"
                      on:click={() => {
                        switchStatusHandler(item.id);
                      }}>{$i18n.t("Close")}</button> 
                    {/if}
                  </td>

                  <td class=" px-3 py-2">
                    
                  </td>
                </tr>
              {/each}
            </tbody>
          {/if}
        </table>
      </div>

      {#if !loading && rewarddates.length > 0}
        <Pagination bind:page count={total} />
      {/if}
    </div>
  {/if}
</div>

<style>
  .font-mona {
    font-family: "Mona Sans";
  }

  .scrollbar-hidden::-webkit-scrollbar {
    display: none; /* for Chrome, Safari and Opera */
  }

  .scrollbar-hidden {
    -ms-overflow-style: none; /* IE and Edge */
    scrollbar-width: none; /* Firefox */
  }
</style>
