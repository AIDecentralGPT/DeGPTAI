<script lang="ts">
  import { getContext, onMount } from "svelte";
  import { toast } from "svelte-sonner";

  import {
    WEBUI_NAME,
    chatId,
    showArchivedChats,
    showSidebar,
    user
  } from "$lib/stores";

  import ShareChatModal from "../chat/ShareChatModal.svelte";
  import ModelSelector from "../chat/ModelSelector.svelte";
  import Tooltip from "../common/Tooltip.svelte";
  import Menu from "./Navbar/Menu.svelte";
  import UserMenu from "./Sidebar/UserMenu.svelte";
  import LanguageMenu from "./Sidebar/LanguageMenu.svelte";
  import MenuLines from "../icons/MenuLines.svelte";
  import { isPro } from "$lib/apis/users";
  import { generateInitialsImage } from '$lib/utils';

  import { getLanguages } from '$lib/i18n';
  const i18n = getContext("i18n");

  export let initNewChat: Function;
  export let title: string = $WEBUI_NAME;
  export let shareEnabled: boolean = false;

  export let chat;
  export let selectedModels;

  export let showModelSelector = true;

  let showShareChatModal = false;
  let showDownloadChatModal = false;

  // 获取用户信息
	const getIsPro = async () => {
    try {
      const userIsPro:boolean = await isPro(localStorage.token); // 发送请求到你的 API
        // if(userIsPro){
        //   user.set({
        //     ...$user,
        //     isPro: userIsPro,
        //   });
        // }

      const newUser = await $user;
			
      await user.set({
        ...newUser,
        isPro: userIsPro,
      });
      
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  }

  let isMobile = false;
  let languages = [];
  onMount(async () => {
    const userAgent = navigator.userAgent || navigator.vendor || window.opera;
    // 检查是否为移动端设备
    isMobile = /android|iPad|iPhone|iPod|IEMobile|Opera Mini/i.test(userAgent);
    console.log("===========================", isMobile);
    languages = await getLanguages();

		await getIsPro();
    
	});


	const demo = async () => {

    // 在调用服务端初始化请求时需要传入该MetaInfo值
    const MetaInfo = window.getMetaInfo();

    console.log("MetaInfo:", MetaInfo);
    toast.success(JSON.stringify(MetaInfo))
    
    // 接下来您进行调用服务端初始化请求获取TransactionUrl
    const TransactionUrl = ''; // 此处值应为调用服务端初始化接口返回的TransactionUrl

    // // 接下来直接跳转TransactionUrl即可开始服务
    // window.location.href = TransactionUrl;

}

</script>



<ShareChatModal bind:show={showShareChatModal} chatId={$chatId} />
<nav id="nav" class=" sticky py-2.5 top-0 flex flex-row justify-center z-30">
  <div class=" flex max-w-full w-full mx-auto px-5 pt-0.5 md:px-[1rem]">
    <div class="flex items-center w-full max-w-full">
      <div
        class="{$showSidebar
          ? 'md:hidden'
          : ''} mr-3 self-start flex flex-none items-center text-gray-600 dark:text-gray-400"
      >
        <button
          id="sidebar-toggle-button"
          class="cursor-pointer px-2 py-2 flex rounded-xl hover:bg-gray-100 dark:hover:bg-gray-850 transition"
          on:click={() => {
            showSidebar.set(!$showSidebar);
          }}
        >
          <div class=" m-auto self-center">
            <MenuLines />
          </div>
        </button>
      </div>
      <div class="flex-1 overflow-hidden max-w-full">
        {#if showModelSelector}
          <ModelSelector bind:selectedModels showSetDefault={!shareEnabled} />
        {/if}
      </div>

      <div
        class="self-start flex flex-none items-center text-gray-600 dark:text-gray-400"
      >
        <!-- <div class="md:hidden flex self-center w-[1px] h-5 mx-2 bg-gray-300 dark:bg-stone-700" /> -->

        {#if shareEnabled}
          <Menu
            {chat}
            {shareEnabled}
            shareHandler={() => {
              showShareChatModal = !showShareChatModal;
            }}
            downloadHandler={() => {
              showDownloadChatModal = !showDownloadChatModal;
            }}
          >
            <button
              class="hidden md:flex cursor-pointer px-2 py-2 rounded-xl hover:bg-gray-100 dark:hover:bg-gray-850 transition"
              id="chat-context-menu-button"
            >
              <div class=" m-auto self-center">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke-width="1.5"
                  stroke="currentColor"
                  class="size-5"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    d="M6.75 12a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0ZM12.75 12a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0ZM18.75 12a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0Z"
                  />
                </svg>
              </div>
            </button>
          </Menu>
        {/if}
        
        <Tooltip content={$i18n.t("New Chat")}>
          <button
            id="new-chat-button"
            class=" flex {$showSidebar
              ? 'md:hidden'
              : ''} cursor-pointer px-2 py-2 rounded-xl hover:bg-gray-100 dark:hover:bg-gray-850 transition"
            on:click={() => {
              initNewChat();
            }}
          >
            <div class=" m-auto self-center">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 20 20"
                fill="currentColor"
                class="w-5 h-5"
              >
                <path
                  d="M5.433 13.917l1.262-3.155A4 4 0 017.58 9.42l6.92-6.918a2.121 2.121 0 013 3l-6.92 6.918c-.383.383-.84.685-1.343.886l-3.154 1.262a.5.5 0 01-.65-.65z"
                />
                <path
                  d="M3.5 5.75c0-.69.56-1.25 1.25-1.25H10A.75.75 0 0010 3H4.75A2.75 2.75 0 002 5.75v9.5A2.75 2.75 0 004.75 18h9.5A2.75 2.75 0 0017 15.25V10a.75.75 0 00-1.5 0v5.25c0 .69-.56 1.25-1.25 1.25h-9.5c-.69 0-1.25-.56-1.25-1.25v-9.5z"
                />
              </svg>
            </div>
          </button>
        </Tooltip>

        <UserMenu
          className="max-w-[200px]"
          role={$user?.role}
          on:show={(e) => {
            if (e.detail === "archived-chat") {
              showArchivedChats.set(true);
            }
          }}
        >
            <button
              class="select-none flex rounded-xl p-1.5 w-full hover:bg-gray-100 dark:hover:bg-gray-850 transition"
              aria-label="User Menu"
            >
              <div class=" self-center">
                <div class="size-8 object-cover rounded-full bg-primary">
                  <img
                    src={ $user.profile_image_url=="" ? generateInitialsImage($user.name) : $user.profile_image_url }
                    alt="profile"
                    class=" rounded-full size-8 object-cover"
                  />
                </div>
              </div>
            </button>
        </UserMenu>
         
        {#if isMobile}
          <LanguageMenu className="max-w-[122px]">
            <button class="text-sm px-1 py-2 flex flex-row items-center">
              <svg class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="5351" width="26" height="26">
                <path d="M472.1 65.7l44.9 36.5c-13.8 13.3-22.9 31.4-24.3 51.6-1.3 18.1-2.7 36.4-4.3 52.8-0.5 0.2-1.1 0.3-1.5 0.5-18 5.3-48.2 14.1-67.3 42.9l-0.3 0.5-0.3 0.5c-16.4 25.6-17.6 56.7-3.1 83.2 16.1 29.4 49.9 49.2 90.7 54-1 1.8-2 3.7-3 5.5-0.4 0.8-0.9 1.6-1.3 2.4-5.7-1.7-11.9-2.7-18.8-2.7-4 0-7.9 0.4-11.8 1.1-4-0.9-9.2-2.2-13.2-3.1-15.4-3.8-31.4-7.8-47.4-7.8-2.6 0-5.2 0.1-7.7 0.3-24.5 2-45.6 15.2-58.5 36.5-17.6 2-33.9 11.4-44.5 25.8-5.4 7.4-16.8 26.9-10.6 53.1 0.3 4.5 0.8 9.5 1.4 15.5 1.1 11.5 2.5 26.3 3.6 44-10.4-5-22-8.8-33.6-9-0.9 0-1.6-0.1-2.1-0.1-1.6-2.7-5.5-10.7-8.3-29.6-3.3-22.4-3.5-49.9-3.5-76.2 0-18.7-5.8-53.7-44.4-77.3-16.9-10.3-36.3-15.8-56.3-15.8-19.4 0-38.3 5.1-55.2 14.7l-2.5-1c3.1-9 6.6-17.9 10.3-26.7 22.6-53.3 54.9-101.3 96-142.4s89.1-73.5 142.4-96c43-18.4 88.1-29.6 134.5-33.7m462.5 343.1l15.7 9.8c6.5 30.5 9.7 61.7 9.7 93.4 0 22.1-1.6 43.9-4.7 65.5l-54.5 48.9c-1.6-2.5-3.3-5-5-7.4-15.1-20.9-30.1-38.4-44.6-51.9-6.9-6.4-11.9-12.6-15-18.5-3.2-6.1-3.5-10.3-3.3-13.3 0.4-7.5 4.3-17 11.4-27.6 11.8-17.5 31.2-36.7 57.7-57.1l37.6-28.8-5-13M449.9 685.2c4.2 2.7 8.8 5.3 13.7 7.6 7.9 3.7 21.7 16.7 31.7 26.1 14.6 13.7 30.4 28.5 49.2 38.2 9.6 22.4 24.3 34.4 38.5 40.6-13.2 17.4-22.3 36.6-29.6 57.6l0.1-7.7-27.4-19.6c-0.2-0.1-20-14.4-41.2-33.7-29.7-27-38.8-42.3-41.2-47.1 0.3-15 2.1-27 3.6-36.8 1.3-7.2 2.6-15.8 2.6-25.2M512 0C229.2 0 0 229.2 0 512s229.2 512 512 512 512-229.2 512-512S794.8 0 512 0z m14.2 325.2c-38.2 0-65.8-20.3-53.3-39.8 15.9-23.9 72.8-10.6 77.9-58.6 2.3-22.2 4.3-47.2 5.8-68.5 0.5-7.7 6.7-13.7 14.4-14.2 37.2-2.7 41-47 6.2-75.3 37.5 5.4 74.1 15.6 109.2 30.5 53.3 22.6 101.3 54.9 142.4 96 37.4 37.4 67.4 80.3 89.6 127.8-5.7-3.6-11.6-5.2-17.4-5.2-28.2 0-54.2 38.4-38 82-133 102-98.9 173.4-55.5 214 12.8 12 25.4 27.4 36.4 42.7 10.6 14.6 17.2 31.5 21 49.2 1.4 6.4 6.4 9.6 13.7 9.6 11 0 27-7.3 43.1-21.7-22.4 50.5-53.6 95.9-92.9 135.2-41.2 41.2-89.1 73.5-142.4 96-24.4 10.3-49.4 18.4-75 24.1-1.5-0.3-3.2-0.4-5-0.4-3.5 0-7.5 0.5-12 1.7 15.5-65.5 22.9-102.4 54.9-130.2 44-38.2 9.7-80.4-24-80.4-1.9 0-3.9 0.1-5.8 0.4-1.5 0.2-2.8 0.3-4 0.3-22.2 0-7.5-34.9-31-36.9-24.8-2.1-57.3-51.4-93.4-68.5-18.9-9-37.5-33.2-66.9-34.5h-1.7c-18.6 0-42.4 11.1-54.4 11.1-4.8 0-7.8-1.8-7.8-6.7 0-57.1-5.9-97.7-6.8-113.8-0.4-5.5-2-7.1-1.1-7.1 1.2 0 7.2 3.2 27.8 3.7h0.4c18.6 0 9.7-38.5 28.1-40 0.8-0.1 1.6-0.1 2.4-0.1 16.4 0 47.5 11.8 63.8 11.8 3.4 0 6.1-0.5 7.9-1.7 0.2-0.1 0.4-0.2 0.7-0.2 8.8 0 43.4 86.3 62.8 86.3 8 0 13.4-14.7 13.4-56 0-17.1-9-46.9 0-63.3 35.1-64.2 67.9-116.7 65.1-124.1-0.9-2.3-11.3-4.4-25-4.4-11.7 0-25.7 1.5-38.3 5.6-9.4 3.1 2.8 17.7-10.2 20.8-8.6 1.9-17.1 2.8-25.1 2.8zM93 430.3c9.7 0 19.4-2.4 27.1-7.6 8-5.3 17.3-8.1 26.5-8.1 7.9 0 15.8 2.1 22.8 6.4 8.1 5 13.8 11.6 13.8 22.8 0 81.6 2.8 168.7 76.9 170 2.2 0 41.2 14.9 59.8 63.3 2.2 5.6 6.5 7.4 12.2 7.4 11.5 0 29-7.4 47.6-7.4 13.9 0 0 23.6 0 74.5C379.8 802 489 880.1 489 880.1c-0.6 32 0.9 58.5 3.3 79.4-53.6-2.3-105.5-14-154.7-34.8-53.3-22.6-101.3-54.9-142.4-96-41.2-41.2-73.5-89.1-96-142.4C75.8 631.2 64 572.5 64 512c0-29 2.7-57.6 8.1-85.5 6.6 2.5 13.8 3.8 20.9 3.8z" data-spm-anchor-id="a313x.search_index.0.i2.23233a81zEGuqd" class="selected" fill="#ffffff"></path>
              </svg>
            </button>
          </LanguageMenu>
        {:else}
          <div class="ml-2">
            <LanguageMenu className="max-w-[122px]">
              <button class="text-sm border-2 border-white rounded-lg px-2 py-0.5 flex flex-row items-center">
                <svg class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="5351" width="16" height="16">
                  <path d="M472.1 65.7l44.9 36.5c-13.8 13.3-22.9 31.4-24.3 51.6-1.3 18.1-2.7 36.4-4.3 52.8-0.5 0.2-1.1 0.3-1.5 0.5-18 5.3-48.2 14.1-67.3 42.9l-0.3 0.5-0.3 0.5c-16.4 25.6-17.6 56.7-3.1 83.2 16.1 29.4 49.9 49.2 90.7 54-1 1.8-2 3.7-3 5.5-0.4 0.8-0.9 1.6-1.3 2.4-5.7-1.7-11.9-2.7-18.8-2.7-4 0-7.9 0.4-11.8 1.1-4-0.9-9.2-2.2-13.2-3.1-15.4-3.8-31.4-7.8-47.4-7.8-2.6 0-5.2 0.1-7.7 0.3-24.5 2-45.6 15.2-58.5 36.5-17.6 2-33.9 11.4-44.5 25.8-5.4 7.4-16.8 26.9-10.6 53.1 0.3 4.5 0.8 9.5 1.4 15.5 1.1 11.5 2.5 26.3 3.6 44-10.4-5-22-8.8-33.6-9-0.9 0-1.6-0.1-2.1-0.1-1.6-2.7-5.5-10.7-8.3-29.6-3.3-22.4-3.5-49.9-3.5-76.2 0-18.7-5.8-53.7-44.4-77.3-16.9-10.3-36.3-15.8-56.3-15.8-19.4 0-38.3 5.1-55.2 14.7l-2.5-1c3.1-9 6.6-17.9 10.3-26.7 22.6-53.3 54.9-101.3 96-142.4s89.1-73.5 142.4-96c43-18.4 88.1-29.6 134.5-33.7m462.5 343.1l15.7 9.8c6.5 30.5 9.7 61.7 9.7 93.4 0 22.1-1.6 43.9-4.7 65.5l-54.5 48.9c-1.6-2.5-3.3-5-5-7.4-15.1-20.9-30.1-38.4-44.6-51.9-6.9-6.4-11.9-12.6-15-18.5-3.2-6.1-3.5-10.3-3.3-13.3 0.4-7.5 4.3-17 11.4-27.6 11.8-17.5 31.2-36.7 57.7-57.1l37.6-28.8-5-13M449.9 685.2c4.2 2.7 8.8 5.3 13.7 7.6 7.9 3.7 21.7 16.7 31.7 26.1 14.6 13.7 30.4 28.5 49.2 38.2 9.6 22.4 24.3 34.4 38.5 40.6-13.2 17.4-22.3 36.6-29.6 57.6l0.1-7.7-27.4-19.6c-0.2-0.1-20-14.4-41.2-33.7-29.7-27-38.8-42.3-41.2-47.1 0.3-15 2.1-27 3.6-36.8 1.3-7.2 2.6-15.8 2.6-25.2M512 0C229.2 0 0 229.2 0 512s229.2 512 512 512 512-229.2 512-512S794.8 0 512 0z m14.2 325.2c-38.2 0-65.8-20.3-53.3-39.8 15.9-23.9 72.8-10.6 77.9-58.6 2.3-22.2 4.3-47.2 5.8-68.5 0.5-7.7 6.7-13.7 14.4-14.2 37.2-2.7 41-47 6.2-75.3 37.5 5.4 74.1 15.6 109.2 30.5 53.3 22.6 101.3 54.9 142.4 96 37.4 37.4 67.4 80.3 89.6 127.8-5.7-3.6-11.6-5.2-17.4-5.2-28.2 0-54.2 38.4-38 82-133 102-98.9 173.4-55.5 214 12.8 12 25.4 27.4 36.4 42.7 10.6 14.6 17.2 31.5 21 49.2 1.4 6.4 6.4 9.6 13.7 9.6 11 0 27-7.3 43.1-21.7-22.4 50.5-53.6 95.9-92.9 135.2-41.2 41.2-89.1 73.5-142.4 96-24.4 10.3-49.4 18.4-75 24.1-1.5-0.3-3.2-0.4-5-0.4-3.5 0-7.5 0.5-12 1.7 15.5-65.5 22.9-102.4 54.9-130.2 44-38.2 9.7-80.4-24-80.4-1.9 0-3.9 0.1-5.8 0.4-1.5 0.2-2.8 0.3-4 0.3-22.2 0-7.5-34.9-31-36.9-24.8-2.1-57.3-51.4-93.4-68.5-18.9-9-37.5-33.2-66.9-34.5h-1.7c-18.6 0-42.4 11.1-54.4 11.1-4.8 0-7.8-1.8-7.8-6.7 0-57.1-5.9-97.7-6.8-113.8-0.4-5.5-2-7.1-1.1-7.1 1.2 0 7.2 3.2 27.8 3.7h0.4c18.6 0 9.7-38.5 28.1-40 0.8-0.1 1.6-0.1 2.4-0.1 16.4 0 47.5 11.8 63.8 11.8 3.4 0 6.1-0.5 7.9-1.7 0.2-0.1 0.4-0.2 0.7-0.2 8.8 0 43.4 86.3 62.8 86.3 8 0 13.4-14.7 13.4-56 0-17.1-9-46.9 0-63.3 35.1-64.2 67.9-116.7 65.1-124.1-0.9-2.3-11.3-4.4-25-4.4-11.7 0-25.7 1.5-38.3 5.6-9.4 3.1 2.8 17.7-10.2 20.8-8.6 1.9-17.1 2.8-25.1 2.8zM93 430.3c9.7 0 19.4-2.4 27.1-7.6 8-5.3 17.3-8.1 26.5-8.1 7.9 0 15.8 2.1 22.8 6.4 8.1 5 13.8 11.6 13.8 22.8 0 81.6 2.8 168.7 76.9 170 2.2 0 41.2 14.9 59.8 63.3 2.2 5.6 6.5 7.4 12.2 7.4 11.5 0 29-7.4 47.6-7.4 13.9 0 0 23.6 0 74.5C379.8 802 489 880.1 489 880.1c-0.6 32 0.9 58.5 3.3 79.4-53.6-2.3-105.5-14-154.7-34.8-53.3-22.6-101.3-54.9-142.4-96-41.2-41.2-73.5-89.1-96-142.4C75.8 631.2 64 572.5 64 512c0-29 2.7-57.6 8.1-85.5 6.6 2.5 13.8 3.8 20.9 3.8z" data-spm-anchor-id="a313x.search_index.0.i2.23233a81zEGuqd" class="selected" fill="#ffffff"></path>
                </svg>
                {#each languages as language }
                  {#if language.code === $i18n.language }
                    <span class="ml-2 text-white">{ language.title }</span>
                  {/if}
                {/each}  
                <svg class="icon ml-1" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" width="12" height="12">
                  <path d="M511.5 789.9 80.6 359c-22.8-22.8-22.8-59.8 0-82.6 22.8-22.8 59.8-22.8 82.6 0l348.3 348.3 348.3-348.3c22.8-22.8 59.8-22.8 82.6 0 22.8 22.8 22.8 59.8 0 82.6L511.5 789.9 511.5 789.9zM511.5 789.9" fill="#ffffff"/>
                </svg>
              </button>
            </LanguageMenu>
          </div>
        {/if}    
      </div>
    </div>
  </div>
</nav>
