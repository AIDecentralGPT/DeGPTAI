<script lang="ts">
  import { goto } from "$app/navigation";
  import {
    chats,
    settings,
    chatId,
    tags,
    showSidebar,
    mobile,
    showArchivedChats,
    showNewWalletModal,
    showOpenWalletModal,
    showExportWalletJsonModal,
    showTransferModal,
    showPriceModal,
    showBuyCoinModal,
    showShareModal,
    pageUpdateNumber,
    showRewardDetailModal,
    showRewardsHistoryModal,
    showTransactionsModal,
    showUserVerifyModal,
    showCoinIntruModal,
    showFollowTwitterModal,
    showFollowTGGroupModal
  } from "$lib/stores";
  import { getCurrentPair } from "$lib/utils/wallet/dbc.js";
  import { onMount, getContext } from "svelte";

  const i18n = getContext("i18n");

  import {
    deleteChatById,
    getChatList,
    getChatById,
    getChatListByTagName,
    updateChatById,
    getAllChatTags,
    archiveChatById,
  } from "$lib/apis/chats";
  import { toast } from "svelte-sonner";
  import { WEBUI_BASE_URL } from "$lib/constants";
  import ChatMenu from "./Sidebar/ChatMenu.svelte";
  import ShareChatModal from "../chat/ShareChatModal.svelte";
  import ArchivedChatsModal from "./Sidebar/ArchivedChatsModal.svelte";
  import NewWalletModal from "../wallet/NewWalletModal.svelte";

  import Wallet from "./Sidebar/Wallet.svelte";
  import OpenWalletModal from "../wallet/OpenWalletModal.svelte";
  import ExportWalletJsonModal from "../wallet/ExportWalletJsonModal.svelte";
  import TransferModal from "../wallet/TransferModal.svelte";
  import PriceModal from "../wallet/PriceModal.svelte";
  import BuyCoinModal from "../wallet/BuyCoinModal.svelte";
  import ShareModal from "../wallet/ShareModal.svelte";
  import SocialMedia from "../socialmedia/SocialMedia.svelte";
  import { updateWalletData } from "$lib/utils/wallet/walletUtils.js";
  import RewardsHistoryModal from "../wallet/RewardsHistoryModal.svelte";
  import RewardDetailModal from "../wallet/RewardDetailModal.svelte";
  import TransactionsModal from "../wallet/TransactionsModal.svelte";
  import UserVerifyModal from "../wallet/UserVerifyModal.svelte";
  import CoinIntruModal from "../wallet/CoinIntruModal.svelte";
  import FollowTwitterModal from "../twitter/FollowTwitterModal.svelte";
  import FollowTgGroupModal from "../twitter/FollowTgGroupModal.svelte";

  const BREAKPOINT = 768;

  let navElement;

  let title: string = "UI";
  let search = "";

  let shareChatId = null;

  let selectedChatId = null;

  let chatDeleteId = null;
  let chatTitleEditId = null;
  let chatTitle = "";

  let showShareChatModal = false;

  let filteredChatList = [];

  $: filteredChatList = $chats?.filter((chat) => {
    if (search === "") {
      return true;
    } else {
      let title = chat.title.toLowerCase();
      const query = search.toLowerCase();

      let contentMatches = false;
      // Access the messages within chat.chat.messages
      if (
        chat.chat &&
        chat.chat.messages &&
        Array.isArray(chat.chat.messages)
      ) {
        contentMatches = chat.chat.messages.some((message) => {
          // Check if message.content exists and includes the search query
          return (
            message.content && message.content.toLowerCase().includes(query)
          );
        });
      }

      return title.includes(query) || contentMatches;
    }
  });

  mobile;
  const onResize = () => {
    if ($showSidebar && window.innerWidth < BREAKPOINT) {
      showSidebar.set(false);
    }
  };

  // // 监听pageUpdateNumber变化， 触发当前组件初始化
  // $: if ($pageUpdateNumber !== undefined) {
  //   console.log(
  //     "请求了chatlist"
  //   );

  //   updateChats();
  // }

  $: $pageUpdateNumber, updateChats();

  async function updateChats() {
    const chatList = await getChatList(localStorage.token);
    chats.set(chatList);
    tags.set([]);
  }

  onMount(async () => {
    // 登录账号
    const pair = getCurrentPair();
    console.log("sidebar组件获取pair ", pair);

    if (pair) {
      // 获取钱包面板数据
      updateWalletData(pair);
    }

    // -----------------------原带的逻辑
    mobile.subscribe((e) => {
      if ($showSidebar && e) {
        showSidebar.set(false);
      }

      if (!$showSidebar && !e) {
        showSidebar.set(true);
      }
    });

    showSidebar.set(window.innerWidth > BREAKPOINT);

    window.addEventListener("touchstart", onTouchStart);
    window.addEventListener("touchend", onTouchEnd);

    // return () => {
    //   window.removeEventListener("touchstart", onTouchStart);
    //   window.removeEventListener("touchend", onTouchEnd);
    // };
  });

  let touchstart: any;
  let touchend: any;

  function checkDirection() {
    const screenWidth = window.innerWidth;
    const swipeDistance = Math.abs(touchend.screenX - touchstart.screenX);
    if (touchstart.clientX < 40 && swipeDistance >= screenWidth / 8) {
      if (touchend.screenX < touchstart.screenX) {
        showSidebar.set(false);
      }
      if (touchend.screenX > touchstart.screenX) {
        showSidebar.set(true);
      }
    }
  }

  const onTouchStart = (e: any) => {
    touchstart = e.changedTouches[0];
  };

  const onTouchEnd = (e: any) => {
    touchend = e.changedTouches[0];
    checkDirection();
  };

  // Helper function to fetch and add chat content to each chat
  const enrichChatsWithContent = async (chatList: any) => {
    const enrichedChats: any = await Promise.all(
      chatList.map(async (chat: any) => {
        const chatDetails = await getChatById(
          localStorage.token,
          chat.id
        ).catch((error) => null); // Handle error or non-existent chat gracefully
        if (chatDetails) {
          chat.chat = chatDetails.chat; // Assuming chatDetails.chat contains the chat content
        }
        return chat;
      })
    );
    chats.set(enrichedChats);
  };

  const loadChat = async (id) => {
    goto(`/c/${id}`);
  };

  const editChatTitle = async (id, _title) => {
    if (_title === "") {
      toast.error($i18n.t("Title cannot be an empty string."));
    } else {
      title = _title;

      await updateChatById(localStorage.token, id, {
        title: _title,
      });
      await chats.set(await getChatList(localStorage.token));
    }
  };

  const deleteChat = async (id) => {
    const res = await deleteChatById(localStorage.token, id).catch((error) => {
      toast.error(error);
      chatDeleteId = null;

      return null;
    });

    if (res) {
      if ($chatId === id) {
        goto("/");
      }

      await chats.set(await getChatList(localStorage.token));
    }
  };

  const saveSettings = async (updated) => {
    await settings.set({ ...$settings, ...updated });
    localStorage.setItem("settings", JSON.stringify($settings));
    location.href = "/";
  };

  const archiveChatHandler = async (id) => {
    await archiveChatById(localStorage.token, id);
    await chats.set(await getChatList(localStorage.token));
  };

  let showWalletView = false;
  const showWalletFun = () => {
    showWalletView = true;
  };
  const closeWalletFun = () => {
    showWalletView = false;
  }
</script>

<ShareChatModal bind:show={showShareChatModal} chatId={shareChatId} />
<ArchivedChatsModal
  bind:show={$showArchivedChats}
  on:change={async () => {
    await chats.set(await getChatList(localStorage.token));
  }}
/>

<!-- 创建钱包 -->
{#if showNewWalletModal}
  <NewWalletModal bind:show={$showNewWalletModal} />
{/if}

<!-- 连接钱包 -->
{#if showOpenWalletModal}
  <OpenWalletModal bind:show={$showOpenWalletModal} />
{/if}

<!-- 导出钱包信息 -->
{#if showExportWalletJsonModal}
  <ExportWalletJsonModal bind:show={$showExportWalletJsonModal} />
{/if}

<!-- 转账弹窗 -->
{#if showRewardsHistoryModal}
  <TransferModal bind:show={$showTransferModal} />
{/if}

<PriceModal bind:show={$showPriceModal} />
<BuyCoinModal bind:show={$showBuyCoinModal} />

<!-- 分享弹窗 -->
{#if showRewardsHistoryModal}
  <ShareModal bind:show={$showShareModal} />
{/if}

<!-- 邀请朋友列表（已注释） -->
<!-- {#if showRewardsModal}
  <RewardsModal bind:show={$showRewardsModal} />
{/if} -->

<!-- 奖励记录弹窗 -->
{#if showRewardsHistoryModal}
  <RewardsHistoryModal bind:show={$showRewardsHistoryModal} />
{/if}

<!-- 奖励操作界面 -->
{#if showRewardDetailModal}
  <RewardDetailModal bind:show={$showRewardDetailModal} />
{/if}

<!-- 转账记录弹窗 -->
{#if showTransactionsModal}
  <TransactionsModal bind:show={$showTransactionsModal} />
{/if}

<!-- KYC认证弹窗 -->
{#if showUserVerifyModal}
  <UserVerifyModal bind:show={$showUserVerifyModal} />
{/if}

<!-- KYC认证弹窗 -->
{#if showCoinIntruModal}
  <CoinIntruModal bind:show={$showCoinIntruModal} />
{/if}

<!-- 关注推特弹窗 -->
{#if showFollowTwitterModal}
  <FollowTwitterModal bind:show={$showFollowTwitterModal} />
{/if}
<!-- 关注TG群弹窗 -->
{#if showFollowTGGroupModal}
  <FollowTgGroupModal bind:show={$showFollowTGGroupModal} />
{/if}

<!-- svelte-ignore a11y-no-static-element-interactions -->

{#if $showSidebar}
  <div
    class=" fixed md:hidden z-40 top-0 right-0 left-0 bottom-0 bg-black/60 w-full min-h-screen h-screen flex justify-center overflow-hidden overscroll-contain"
    on:mousedown={() => {
      showSidebar.set(!$showSidebar);
    }}
  />
{/if}

<div
  bind:this={navElement}
  id="sidebar"
  class="h-screen max-h-[100dvh] min-h-screen select-none {$showSidebar
    ? 'md:relative w-[270px]'
    : '-translate-x-[270px] w-[0px]'} bg-gray-50 text-gray-900 dark:bg-gray-950 dark:text-gray-200 text-sm transition fixed z-50 top-0 left-0 rounded-r-2xl
        "
  data-state={$showSidebar}
>
  <!-- <div
  bind:this={navElement}
  id="sidebar"
  class="h-screen max-h-[100dvh] min-h-screen select-none {$showSidebar
    ? 'md:relative w-[340px]'
    : '-translate-x-[340px] w-[0px]'} bg-gray-50 text-gray-900 dark:bg-gray-950 dark:text-gray-200 text-sm transition fixed z-50 top-0 left-0 rounded-r-2xl
        "
  data-state={$showSidebar}
> -->
  <!-- <div
		class="py-2.5 my-auto flex flex-col justify-between h-screen max-h-[100dvh] w-[340px] z-50 {$showSidebar
			? ''
			: 'invisible'}"
	> -->
  <div
    class="py-2.5 my-auto flex flex-col justify-between h-screen max-h-[100dvh] w-[270px] z-50 {$showSidebar
      ? ''
      : 'invisible'}"
  >
    <div
      class="px-2.5 flex justify-between space-x-1 text-gray-600 dark:text-gray-400"
    >
      <a
        id="sidebar-new-chat-button"
        class="flex flex-1 justify-between rounded-xl px-2 py-2 hover:bg-gray-100 dark:hover:bg-gray-850 transition"
        href="/"
        draggable="false"
        on:click={async () => {
          selectedChatId = null;
          await goto("/");
          const newChatButton = document.getElementById("new-chat-button");
          setTimeout(() => {
            newChatButton?.click();

            if ($mobile) {
              showSidebar.set(false);
            }
          }, 0);
        }}
      >
        <div class="self-center mx-1.5">
          <img
            crossorigin="anonymous"
            src="{WEBUI_BASE_URL}/static/favicon.png"
            class=" size-6 -translate-x-1.5 rounded-full"
            alt="logo"
          />
        </div>
        <div
          class=" self-center font-medium text-sm text-gray-850 dark:text-white"
        >
          {$i18n.t("New Chat")}
        </div>
        <div class="self-center ml-auto">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 20 20"
            fill="currentColor"
            class="size-5"
          >
            <path
              d="M5.433 13.917l1.262-3.155A4 4 0 017.58 9.42l6.92-6.918a2.121 2.121 0 013 3l-6.92 6.918c-.383.383-.84.685-1.343.886l-3.154 1.262a.5.5 0 01-.65-.65z"
            />
            <path
              d="M3.5 5.75c0-.69.56-1.25 1.25-1.25H10A.75.75 0 0010 3H4.75A2.75 2.75 0 002 5.75v9.5A2.75 2.75 0 004.75 18h9.5A2.75 2.75 0 0017 15.25V10a.75.75 0 00-1.5 0v5.25c0 .69-.56 1.25-1.25 1.25h-9.5c-.69 0-1.25-.56-1.25-1.25v-9.5z"
            />
          </svg>
        </div>
      </a>

      <button
        class=" cursor-pointer px-2 py-2 flex rounded-xl hover:bg-gray-100 dark:hover:bg-gray-850 transition"
        on:click={() => {
          showSidebar.set(!$showSidebar);
        }}
      >
        <div class=" m-auto self-center">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            stroke-width="2"
            stroke="currentColor"
            class="size-5"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25H12"
            />
          </svg>
        </div>
      </button>
    </div>

    <!-- {#if $user?.role === 'admin'}
			<div class="px-2.5 flex justify-center text-gray-800 dark:text-gray-200">
				<a
					class="flex-grow flex space-x-3 rounded-xl px-2.5 py-2 hover:bg-gray-100 dark:hover:bg-gray-900 transition"
					href="/workspace"
					on:click={() => {
						selectedChatId = null;
						chatId.set('');
					}}
					draggable="false"
				>
					<div class="self-center">
						<svg
							xmlns="http://www.w3.org/2000/svg"
							fill="none"
							viewBox="0 0 24 24"
							stroke-width="2"
							stroke="currentColor"
							class="size-[1.1rem]"
						>
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								d="M13.5 16.875h3.375m0 0h3.375m-3.375 0V13.5m0 3.375v3.375M6 10.5h2.25a2.25 2.25 0 0 0 2.25-2.25V6a2.25 2.25 0 0 0-2.25-2.25H6A2.25 2.25 0 0 0 3.75 6v2.25A2.25 2.25 0 0 0 6 10.5Zm0 9.75h2.25A2.25 2.25 0 0 0 10.5 18v-2.25a2.25 2.25 0 0 0-2.25-2.25H6a2.25 2.25 0 0 0-2.25 2.25V18A2.25 2.25 0 0 0 6 20.25Zm9.75-9.75H18a2.25 2.25 0 0 0 2.25-2.25V6A2.25 2.25 0 0 0 18 3.75h-2.25A2.25 2.25 0 0 0 13.5 6v2.25a2.25 2.25 0 0 0 2.25 2.25Z"
							/>
						</svg>
					</div>

					<div class="flex self-center">
						<div class=" self-center font-medium text-sm">{$i18n.t('Workspace')}</div>
					</div>
				</a>
			</div>
		{/if} -->

    <div class="relative flex flex-col flex-1 overflow-y-auto">
      {#if !($settings.saveChatHistory ?? true)}
        <div
          class="absolute z-40 w-full h-full bg-gray-50/90 dark:bg-black/90 flex justify-center"
        >
          <div class=" text-left px-5 py-2">
            <div class=" font-medium">
              {$i18n.t("Chat History is off for this browser.")}
            </div>
            <div class="text-xs mt-2">
              {$i18n.t(
                "When history is turned off, new chats on this browser won't appear in your history on any of your devices."
              )}
              <span class=" font-semibold"
                >{$i18n.t(
                  "This setting does not sync across browsers or devices."
                )}</span
              >
            </div>

            <div class="mt-3">
              <button
                class="flex justify-center items-center space-x-1.5 px-3 py-2.5 rounded-lg text-xs bg-gray-100 hover:bg-gray-200 transition text-gray-800 font-medium w-full"
                type="button"
                on:click={() => {
                  saveSettings({
                    saveChatHistory: true,
                  });
                }}
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 16 16"
                  fill="currentColor"
                  class="w-3 h-3"
                >
                  <path
                    fill-rule="evenodd"
                    d="M8 1a.75.75 0 0 1 .75.75v6.5a.75.75 0 0 1-1.5 0v-6.5A.75.75 0 0 1 8 1ZM4.11 3.05a.75.75 0 0 1 0 1.06 5.5 5.5 0 1 0 7.78 0 .75.75 0 0 1 1.06-1.06 7 7 0 1 1-9.9 0 .75.75 0 0 1 1.06 0Z"
                    clip-rule="evenodd"
                  />
                </svg>

                <div>{$i18n.t("Enable Chat History")}</div>
              </button>
            </div>
          </div>
        </div>
      {/if}

      <div class="px-2 mt-0.5 mb-2 flex justify-center space-x-2">
        <div class="flex w-full rounded-xl" id="chat-search">
          <div class="self-center pl-3 py-2 rounded-l-xl bg-transparent">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 20 20"
              fill="currentColor"
              class="w-4 h-4"
            >
              <path
                fill-rule="evenodd"
                d="M9 3.5a5.5 5.5 0 100 11 5.5 5.5 0 000-11zM2 9a7 7 0 1112.452 4.391l3.328 3.329a.75.75 0 11-1.06 1.06l-3.329-3.328A7 7 0 012 9z"
                clip-rule="evenodd"
              />
            </svg>
          </div>

          <input
            class="w-full rounded-r-xl py-1.5 pl-2.5 pr-4 text-sm bg-transparent dark:text-gray-300 outline-none"
            placeholder={$i18n.t("Search")}
            bind:value={search}
            on:focus={() => {
              enrichChatsWithContent($chats);
            }}
          />
        </div>
      </div>

      {#if $tags?.length > 0}
        <div class="px-2.5 mb-2 flex gap-1 flex-wrap">
          <button
            class="px-2.5 text-xs font-medium bg-gray-50 dark:bg-gray-900 dark:hover:bg-gray-800 transition rounded-full"
            on:click={async () => {
              await chats.set(await getChatList(localStorage.token));
            }}
          >
            {$i18n.t("all")}
          </button>
          {#each $tags as tag}
            <button
              class="px-2.5 text-xs font-medium bg-gray-50 dark:bg-gray-900 dark:hover:bg-gray-800 transition rounded-full"
              on:click={async () => {
                let chatIds = await getChatListByTagName(
                  localStorage.token,
                  tag.name
                );
                if (chatIds.length === 0) {
                  await tags.set(await getAllChatTags(localStorage.token));
                  chatIds = await getChatList(localStorage.token);
                }
                await chats.set(chatIds);
              }}
            >
              {tag.name}
            </button>
          {/each}
        </div>
      {/if}

      <div
        class="pl-2 my-2 flex-1 flex flex-col space-y-1 overflow-y-auto scrollbar-hidden"
      >
        {#if filteredChatList?.length > 0}
          {#each filteredChatList as chat, idx}
            {#if idx === 0 || (idx > 0 && chat.time_range !== filteredChatList[idx - 1].time_range)}
              <div
                class="w-full pl-2.5 text-xs text-gray-500 dark:text-gray-500 font-medium {idx ===
                0
                  ? ''
                  : 'pt-5'} pb-0.5"
              >
                {$i18n.t(chat.time_range)}
                <!-- localisation keys for time_range to be recognized from the i18next parser (so they don't get automatically removed):
          {$i18n.t('Today')}
          {$i18n.t('Yesterday')}
          {$i18n.t('Previous 7 days')}
          {$i18n.t('Previous 30 days')}
          {$i18n.t('January')}
          {$i18n.t('February')}
          {$i18n.t('March')}
          {$i18n.t('April')}
          {$i18n.t('May')}
          {$i18n.t('June')}
          {$i18n.t('July')}
          {$i18n.t('August')}
          {$i18n.t('September')}
          {$i18n.t('October')}
          {$i18n.t('November')}
          {$i18n.t('December')}
          -->
              </div>
            {/if}

            <div class=" w-full pr-2 relative group">
              {#if chatTitleEditId === chat.id}
                <div
                  class=" w-full flex justify-between rounded-xl px-3 py-2 {chat.id ===
                    $chatId ||
                  chat.id === chatTitleEditId ||
                  chat.id === chatDeleteId
                    ? 'bg-gray-200 dark:bg-gray-900'
                    : chat.id === selectedChatId
                    ? 'bg-gray-100 dark:bg-gray-950'
                    : 'group-hover:bg-gray-100 dark:group-hover:bg-gray-950'}  whitespace-nowrap text-ellipsis"
                >
                  <input
                    bind:value={chatTitle}
                    class=" bg-transparent w-full outline-none mr-10"
                  />
                </div>
              {:else}
                <a
                  class=" w-full flex justify-between rounded-xl px-3 py-2 {chat.id ===
                    $chatId ||
                  chat.id === chatTitleEditId ||
                  chat.id === chatDeleteId
                    ? 'bg-gray-200 dark:bg-gray-900'
                    : chat.id === selectedChatId
                    ? 'bg-gray-100 dark:bg-gray-950'
                    : ' group-hover:bg-gray-100 dark:group-hover:bg-gray-950'}  whitespace-nowrap text-ellipsis"
                  href="/c/{chat.id}"
                  on:click={() => {
                    selectedChatId = chat.id;
                    if ($mobile) {
                      showSidebar.set(false);
                    }
                  }}
                  draggable="false"
                >
                  <div class=" flex self-center flex-1 w-full">
                    <div
                      class=" text-left self-center overflow-hidden w-full h-[20px]"
                    >
                      {chat.title}
                    </div>
                  </div>
                </a>
              {/if}

              <div
                class="

          {chat.id === $chatId ||
                chat.id === chatTitleEditId ||
                chat.id === chatDeleteId
                  ? 'from-gray-200 dark:from-gray-900'
                  : chat.id === selectedChatId
                  ? 'from-gray-100 dark:from-gray-950'
                  : 'invisible group-hover:visible from-gray-100 dark:from-gray-950'}
            absolute right-[10px] top-[10px] pr-2 pl-5 bg-gradient-to-l from-80%

              to-transparent"
              >
                {#if chatTitleEditId === chat.id}
                  <div class="flex self-center space-x-1.5 z-10">
                    <button
                      class=" self-center dark:hover:text-white transition"
                      on:click={() => {
                        editChatTitle(chat.id, chatTitle);
                        chatTitleEditId = null;
                        chatTitle = "";
                      }}
                    >
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        viewBox="0 0 20 20"
                        fill="currentColor"
                        class="w-4 h-4"
                      >
                        <path
                          fill-rule="evenodd"
                          d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z"
                          clip-rule="evenodd"
                        />
                      </svg>
                    </button>
                    <button
                      class=" self-center dark:hover:text-white transition"
                      on:click={() => {
                        chatTitleEditId = null;
                        chatTitle = "";
                      }}
                    >
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        viewBox="0 0 20 20"
                        fill="currentColor"
                        class="w-4 h-4"
                      >
                        <path
                          d="M6.28 5.22a.75.75 0 00-1.06 1.06L8.94 10l-3.72 3.72a.75.75 0 101.06 1.06L10 11.06l3.72 3.72a.75.75 0 101.06-1.06L11.06 10l3.72-3.72a.75.75 0 00-1.06-1.06L10 8.94 6.28 5.22z"
                        />
                      </svg>
                    </button>
                  </div>
                {:else if chatDeleteId === chat.id}
                  <div class="flex self-center space-x-1.5 z-10">
                    <button
                      class=" self-center dark:hover:text-white transition"
                      on:click={() => {
                        deleteChat(chat.id);
                      }}
                    >
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        viewBox="0 0 20 20"
                        fill="currentColor"
                        class="w-4 h-4"
                      >
                        <path
                          fill-rule="evenodd"
                          d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z"
                          clip-rule="evenodd"
                        />
                      </svg>
                    </button>
                    <button
                      class=" self-center dark:hover:text-white transition"
                      on:click={() => {
                        chatDeleteId = null;
                      }}
                    >
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        viewBox="0 0 20 20"
                        fill="currentColor"
                        class="w-4 h-4"
                      >
                        <path
                          d="M6.28 5.22a.75.75 0 00-1.06 1.06L8.94 10l-3.72 3.72a.75.75 0 101.06 1.06L10 11.06l3.72 3.72a.75.75 0 101.06-1.06L11.06 10l3.72-3.72a.75.75 0 00-1.06-1.06L10 8.94 6.28 5.22z"
                        />
                      </svg>
                    </button>
                  </div>
                {:else}
                  <div class="flex self-center space-x-1 z-10">
                    <ChatMenu
                      chatId={chat.id}
                      shareHandler={() => {
                        shareChatId = selectedChatId;
                        showShareChatModal = true;
                      }}
                      archiveChatHandler={() => {
                        archiveChatHandler(chat.id);
                      }}
                      renameHandler={() => {
                        chatTitle = chat.title;
                        chatTitleEditId = chat.id;
                      }}
                      deleteHandler={() => {
                        chatDeleteId = chat.id;
                      }}
                      onClose={() => {
                        selectedChatId = null;
                      }}
                    >
                      <button
                        aria-label="Chat Menu"
                        class=" self-center dark:hover:text-white transition"
                        on:click={() => {
                          selectedChatId = chat.id;
                        }}
                      >
                        <svg
                          xmlns="http://www.w3.org/2000/svg"
                          viewBox="0 0 16 16"
                          fill="currentColor"
                          class="w-4 h-4"
                        >
                          <path
                            d="M2 8a1.5 1.5 0 1 1 3 0 1.5 1.5 0 0 1-3 0ZM6.5 8a1.5 1.5 0 1 1 3 0 1.5 1.5 0 0 1-3 0ZM12.5 6.5a1.5 1.5 0 1 0 0 3 1.5 1.5 0 0 0 0-3Z"
                          />
                        </svg>
                      </button>
                    </ChatMenu>

                    {#if chat.id === $chatId}
                      <button
                        id="delete-chat-button"
                        class="hidden"
                        on:click={() => {
                          chatDeleteId = chat.id;
                        }}
                      >
                        <svg
                          xmlns="http://www.w3.org/2000/svg"
                          viewBox="0 0 16 16"
                          fill="currentColor"
                          class="w-4 h-4"
                        >
                          <path
                            d="M2 8a1.5 1.5 0 1 1 3 0 1.5 1.5 0 0 1-3 0ZM6.5 8a1.5 1.5 0 1 1 3 0 1.5 1.5 0 0 1-3 0ZM12.5 6.5a1.5 1.5 0 1 0 0 3 1.5 1.5 0 0 0 0-3Z"
                          />
                        </svg>
                      </button>
                    {/if}
                  </div>
                {/if}
              </div>
            </div>
          {/each}
        {/if}
      </div>
    </div>
    <div>
      <!-- <hr class=" border-gray-900 mb-1 w-full" /> -->

      <!-- <div class="flex flex-col">
        {#if $user !== undefined}
          <UserMenu
            role={$user?.role}
            on:show={(e) => {
              if (e.detail === 'archived-chat') {
                showArchivedChats.set(true);
              }
            }}
          >
            <button
              class=" flex rounded-xl py-3 px-3.5 w-full hover:bg-gray-100 dark:hover:bg-gray-900 transition"
              on:click={() => {
                showDropdown = !showDropdown;
              }}
            >
              <div class=" self-center mr-3">
                <img
                  src={$user.profile_image_url}
                  class=" max-w-[30px] object-cover rounded-full"
                  alt="User profile"
                />
              </div>
              <div class=" self-center font-semibold">{$user.name}</div>
            </button>
          </UserMenu>
        {/if}
      </div> -->
      <div class="flex flex-row gap-2 px-3">
        <button class="primaryButton px-3 py-2 rounded-lg transition mt-2 mb-2"
          on:mouseover = {showWalletFun}>
          <svg class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" width="18" height="18">
            <path d="M976.896 883.712q0 19.456-6.656 36.352t-18.944 29.696-28.672 19.968-35.84 7.168l-743.424 0q-19.456 0-36.864-7.168t-30.72-19.968-20.992-29.696-7.68-36.352l0-510.976q0-38.912 27.136-66.048t66.048-27.136l743.424 0q38.912 0 66.048 27.136t27.136 66.048l0 139.264-232.448 0q-38.912 0-66.048 26.624t-27.136 65.536q1.024 26.624 11.264 47.104 8.192 17.408 27.136 31.744t54.784 14.336l232.448 0 0 186.368zM837.632 232.448l-464.896 0q55.296-28.672 104.448-55.296 43.008-22.528 84.992-45.056t65.536-34.816q35.84-19.456 64-17.92t47.616 9.728q22.528 11.264 38.912 29.696zM698.368 604.16q0-19.456 13.312-32.768t32.768-13.312 32.768 13.312 13.312 32.768-13.312 33.28-32.768 13.824-32.768-13.824-13.312-33.28z" fill="#ffffff"/>
          </svg>
        </button>
        <button class="primaryButton px-3 py-2 text-gray-100 transition rounded-lg mt-2 mb-2"
          on:click={async () => {
            await goto("/");
            const newChatButton = document.getElementById("new-chat-button");
            setTimeout(() => {
              newChatButton?.click();
              if ($mobile) {
                showSidebar.set(false);
              }
            }, 0);
          }}>
          <svg class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" width="20" height="20">
            <path d="M786.88711111 644.43733333c45.51111111-58.70933333 72.81777778-132.43733333 72.81777778-212.53688888 0-192.05688889-155.648-347.70488889-347.70488889-347.7048889s-347.70488889 155.648-347.70488889 347.7048889c0 80.09955555 27.30666667 153.37244445 72.81777778 212.53688888L84.19555555 797.80977778h142.44977778v142.44977777l177.49333334-177.49333333c33.67822222 10.92266667 70.08711111 17.29422222 107.40622222 17.29422223s73.728-5.91644445 107.40622222-17.29422223l177.49333334 177.49333333v-142.44977777H939.80444445l-152.91733334-153.37244445z m-162.92977778-66.90133333L512 519.28177778l-111.95733333 58.70933333 21.39022222-124.70044444-91.02222222-88.29155556 125.15555555-18.20444444 55.97866667-113.77777778 55.97866666 113.77777778 125.15555556 18.20444444-90.112 88.29155556 21.39022222 124.24533333z" fill="#ffffff"></path>
          </svg>
        </button>
      </div>    
    </div>
  </div>

  <div id="wallet-view" class="min-w-[270px] max-w-[320px] absolute bottom-1 left-1 dark:bg-black bg-white pb-[40px] rounded border-gray-800 transition ease-in-out delay-1500 {showWalletView ? 'scale-100' : 'hidden scale-0'}"
    style="border-width: 1px;"
    on:mouseover={showWalletFun}
    on:mouseleave={closeWalletFun}>
    <!-- 社媒 -->
    <SocialMedia />
    <!-- 钱包 -->
    <Wallet />
  </div>

  <!-- <div
		id="sidebar-handle"
		class=" hidden md:fixed left-0 top-[50dvh] -translate-y-1/2 transition-transform translate-x-[255px] md:translate-x-[340px] rotate-0"
	>
		<Tooltip
			placement="right"
			content={`${$showSidebar ? $i18n.t('Close') : $i18n.t('Open')} ${$i18n.t('sidebar')}`}
			touch={false}
		>
			<button
				id="sidebar-toggle-button"
				class=" group"
				on:click={() => {
					showSidebar.set(!$showSidebar);
				}}
				><span class="" data-state="closed"
					><div
						class="flex h-[72px] w-8 items-center justify-center opacity-50 group-hover:opacity-100 transition"
					>
						<div class="flex h-6 w-6 flex-col items-center">
							<div
								class="h-3 w-1 rounded-full bg-[#0f0f0f] dark:bg-white rotate-0 translate-y-[0.15rem] {$showSidebar
									? 'group-hover:rotate-[15deg]'
									: 'group-hover:rotate-[-15deg]'}"
							/>
							<div
								class="h-3 w-1 rounded-full bg-[#0f0f0f] dark:bg-white rotate-0 translate-y-[-0.15rem] {$showSidebar
									? 'group-hover:rotate-[-15deg]'
									: 'group-hover:rotate-[15deg]'}"
							/>
						</div>
					</div>
				</span>
			</button>
		</Tooltip>
	</div> -->
</div>

<style>
  .scrollbar-hidden:active::-webkit-scrollbar-thumb,
  .scrollbar-hidden:focus::-webkit-scrollbar-thumb,
  .scrollbar-hidden:hover::-webkit-scrollbar-thumb {
    visibility: visible;
  }
  .scrollbar-hidden::-webkit-scrollbar-thumb {
    visibility: hidden;
  }
</style>
