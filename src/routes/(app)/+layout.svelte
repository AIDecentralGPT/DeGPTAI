<script lang="ts">
	import { onMount, getContext } from "svelte";
	import { openDB, deleteDB } from "idb";
	import fileSaver from "file-saver";
	const { saveAs } = fileSaver;

	import { goto } from "$app/navigation";

	import { getModels as _getModels } from "$lib/utils";

	import {
		user,
		showSettings,
		settings,
		models,
		showChangelog,
		config,
		channel,
		chats,
		tags,
		initPageFlag
	} from "$lib/stores";
	import { page } from "$app/stores";

	import SettingsModal from "$lib/components/chat/SettingsModal.svelte";
	import Sidebar from "$lib/components/layout/Sidebar.svelte";
	import ShortcutsModal from "$lib/components/chat/ShortcutsModal.svelte";
	import Tooltip from "$lib/components/common/Tooltip.svelte";
	import FingerprintJS from "@fingerprintjs/fingerprintjs";
	import { updateWalletData } from "$lib/utils/wallet/walletUtils";
	import { getUserInfo, isPro } from "$lib/apis/users";
	import { unlockWalletWithPrivateKey } from "$lib/utils/wallet/ether/utils";
	import { signOut } from "$lib/utils/wallet/ether/utils";
	import { getLanguages } from "$lib/i18n/index";
	import { getChatList } from "$lib/apis/chats";

	const i18n = getContext("i18n");

	let loaded = false;
	let showShortcutsButtonElement: HTMLButtonElement;
	let DB = null;
	let localDBChats = [];

	let showShortcuts = false;

	const getModels = async () => {
		// console.log("_getModels(localStorage.token)", _getModels(localStorage.token));

		return _getModels(localStorage.token);
	};

	async function checkLogin() {
    // 加载 FingerprintJS 库
    const fp = await FingerprintJS.load();
    // 获取设备指纹
    const result = await fp.get();
    // `result.visitorId` 是设备指纹 ID
    const visitorId = result.visitorId;
    console.log("visitorId", visitorId); // 27841987f3d61173059f66f530b63f15
    localStorage.setItem("visitor_id", visitorId);

		// 初始化访客
		await user.set({
			id: visitorId,
			name: visitorId,
			profile_image_url: "",
			role: "visitor"
		});

    if (localStorage?.token) {
      // 获取缓存用户信息
      try {
        let localUser = JSON.parse(localStorage?.user);
        if (localUser?.address_type == "dbc") {
          getUserInfo(localStorage.token).then(async (res) => {
						if (res?.id === localUser?.id) {
							const vipInfo = await isPro(localStorage.token);
							await user.set({
								...localUser,
								vipInfo: vipInfo ?? [],
								models: res?.models,
								verified: res?.verified,
								language: res?.language
							});
						}
						localStorage.user = JSON.stringify($user);

						// 校验钱包
						if (localStorage.walletImported) {
							let walletImported = JSON.parse(localStorage.walletImported);
							if (walletImported) {
								const walletImportedInfo = await unlockWalletWithPrivateKey(
									walletImported?.privateKey
								);
								updateWalletData(walletImportedInfo?.data);
							}
						}
						// 更新用户模型
						await initUserModels();
						// 更新系统语言
						await initLanguage();
						// 更新用户聊天记录
						// await updateChats();
						// 初始化完成
						$initPageFlag = true;
					});
          
        } else {
          signOut($channel).then(async() => {
						// 更新用户模型
						await initUserModels();
						// 更新系统语言
						await initLanguage();
						// 更新用户聊天记录
						await updateChats();
						// 初始化完成
						$initPageFlag = true;
					});
          
        }
      } catch (error) {
        signOut($channel).then(async() => {
					// 更新用户模型
					await initUserModels();
					// 更新系统语言
					await initLanguage();
					// 更新用户聊天记录
					await updateChats();
					// 初始化完成
					$initPageFlag = true;
				});
      }
    } else {
      signOut($channel).then(async() => {
				// 更新用户模型
				await initUserModels();
				// 更新系统语言
				await initLanguage();
				// 更新用户聊天记录
				await updateChats();
				// 初始化完成
				$initPageFlag = true;
			});
    }
  }

	// 更新用户模型
  const initUserModels = async() => {
    if ($user?.models) {
      settings.set({ ...$settings, models: $user?.models.split(",") });
    } else {
      settings.set({
        ...$settings,
        models: $config?.default_models.split(","),
      });
    }
    localStorage.setItem("settings", JSON.stringify($settings));
    goto("/");
    const newChatButton = document.getElementById("new-chat-button");
    setTimeout(() => {
      newChatButton?.click();
    }, 0);
  };

	// 更新用户语言
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

	// 更新用户聊天记录
	async function updateChats() {
    if (localStorage.token){
			chats.set([]);
			tags.set([]);
      getChatList(localStorage.token).then(chatList => {
				chats.set(chatList);
			}); 
    } 
  }

	onMount(async () => {
		const queryParams = new URLSearchParams($page.url.search);
		let channelName = queryParams.get("channel");
		if (channelName) {
			await channel.set(channelName);
		}
		if ($config) {
			// 用户登陆校验
			await checkLogin();
		}

		if ($user === undefined) {
			await signOut($channel);
			await models.set(await getModels());
		} else if (
			["user", "admin", "walletUser", "visitor"].includes($user?.role)
		) {
			try {
				// Check if IndexedDB exists
				DB = await openDB("Chats", 1);

				if (DB) {
					const chats = await DB.getAllFromIndex("chats", "timestamp");
					localDBChats = chats.map(
						(item, idx) => chats[chats.length - 1 - idx]
					);

					if (localDBChats.length === 0) {
						await deleteDB("Chats");
					}
				}

				console.log(DB);
			} catch (error) {
				// IndexedDB Not Found
			}

			await models.set(await getModels());
			await settings.set(JSON.parse(localStorage.getItem("settings") ?? "{}"));

			// await modelfiles.set(await getModelfiles(localStorage.token));
			// await prompts.set(await getPrompts(localStorage.token));
			// await documents.set(await getDocs(localStorage.token));
			// await tags.set(await getAllChatTags(localStorage.token));

			// modelfiles.subscribe(async () => {
			// 	// should fetch models
			// 	await models.set(await getModels());
			// });

			document.addEventListener("keydown", function (event) {
				const isCtrlPressed = event.ctrlKey || event.metaKey; // metaKey is for Cmd key on Mac
				// Check if the Shift key is pressed
				const isShiftPressed = event.shiftKey;

				// Check if Ctrl + Shift + O is pressed
				if (
					isCtrlPressed &&
					isShiftPressed &&
					event.key.toLowerCase() === "o"
				) {
					event.preventDefault();
					console.log("newChat");
					document.getElementById("sidebar-new-chat-button")?.click();
				}

				// Check if Shift + Esc is pressed
				if (isShiftPressed && event.key === "Escape") {
					event.preventDefault();
					console.log("focusInput");
					document.getElementById("chat-textarea")?.focus();
				}

				// Check if Ctrl + Shift + ; is pressed
				if (isCtrlPressed && isShiftPressed && event.key === ";") {
					event.preventDefault();
					console.log("copyLastCodeBlock");
					const button = [
						...document.getElementsByClassName("copy-code-button"),
					]?.at(-1);
					button?.click();
				}

				// Check if Ctrl + Shift + C is pressed
				if (
					isCtrlPressed &&
					isShiftPressed &&
					event.key.toLowerCase() === "c"
				) {
					event.preventDefault();
					console.log("copyLastResponse");
					const button = [
						...document.getElementsByClassName("copy-response-button"),
					]?.at(-1);
					console.log(button);
					button?.click();
				}

				// Check if Ctrl + Shift + S is pressed
				if (
					isCtrlPressed &&
					isShiftPressed &&
					event.key.toLowerCase() === "s"
				) {
					event.preventDefault();
					console.log("toggleSidebar");
					document.getElementById("sidebar-toggle-button")?.click();
				}

				// Check if Ctrl + Shift + Backspace is pressed
				if (isCtrlPressed && isShiftPressed && event.key === "Backspace") {
					event.preventDefault();
					console.log("deleteChat");
					document.getElementById("delete-chat-button")?.click();
				}

				// Check if Ctrl + . is pressed
				if (isCtrlPressed && event.key === ".") {
					event.preventDefault();
					console.log("openSettings");
					showSettings.set(!$showSettings);
				}

				// Check if Ctrl + / is pressed
				if (isCtrlPressed && event.key === "/") {
					event.preventDefault();
					console.log("showShortcuts");
					showShortcutsButtonElement.click();
				}
			});

			if ($user?.role === "admin") {
				showChangelog.set(localStorage.version !== $config.version);
			}
		}

		loaded = true;
	});
</script>

<div class=" hidden lg:flex fixed bottom-0 right-0 px-3 py-3 z-10">
	<Tooltip content={$i18n.t("Help")} placement="left">
		<button
			id="show-shortcuts-button"
			bind:this={showShortcutsButtonElement}
			class="text-gray-600 dark:text-gray-300 bg-gray-300/20 w-6 h-6 flex items-center justify-center text-xs rounded-full"
			on:click={() => {
				showShortcuts = !showShortcuts;
			}}
		>
			?
		</button>
	</Tooltip>
</div>

<ShortcutsModal bind:show={showShortcuts} />
<SettingsModal bind:show={$showSettings} />
<!-- <ChangelogModal bind:show={$showChangelog} /> -->

<div class="app relative">
	<div
		class=" text-gray-700 dark:text-gray-100 bg-white dark:bg-gray-900 min-h-screen overflow-auto flex flex-row"
	>
		{#if loaded}
			{#if false}
				<div class="fixed w-full h-full flex z-[999]">
					<div
						class="absolute w-full h-full backdrop-blur-lg bg-white/10 dark:bg-gray-900/50 flex justify-center"
					>
						<div class="m-auto pb-10 flex flex-col justify-center">
							<div class="max-w-md">
								<div
									class="text-center dark:text-white text-2xl font-medium z-50"
								>
									Account Activation Pending<br /> Contact Admin for WebUI Access
								</div>

								<div
									class=" mt-4 text-center text-sm dark:text-gray-200 w-full"
								>
									Your account status is currently pending activation. To access
									the WebUI, please reach out to the administrator. Admins can
									manage user statuses from the Admin Panel.
								</div>

								<div class=" mt-6 mx-auto relative group w-fit">
									<button
										class="relative z-20 flex px-5 py-2 rounded-full bg-white border border-gray-100 dark:border-none hover:bg-gray-100 text-gray-700 transition font-medium text-sm"
										on:click={async () => {
											location.href = "/";
										}}
									>
										{$i18n.t("Check Again")}
									</button>

									<!-- <button
										class="text-xs text-center w-full mt-2 text-gray-400 underline"
										on:click={async () => {
											// localStorage.removeItem('token');
											// location.href = '/auth';
										}}>{$i18n.t('Sign Out')}</button
									> -->
								</div>
							</div>
						</div>
					</div>
				</div>
			{:else if localDBChats.length > 0}
				<div class="fixed w-full h-full flex z-50">
					<div
						class="absolute w-full h-full backdrop-blur-md bg-white/20 dark:bg-gray-900/50 flex justify-center"
					>
						<div class="m-auto pb-44 flex flex-col justify-center">
							<div class="max-w-md">
								<div
									class="text-center dark:text-white text-2xl font-medium z-50"
								>
									Important Update<br /> Action Required for Chat Log Storage
								</div>

								<div
									class=" mt-4 text-center text-sm dark:text-gray-200 w-full"
								>
									{$i18n.t(
										"Saving chat logs directly to your browser's storage is no longer supported. Please take a moment to download and delete your chat logs by clicking the button below. Don't worry, you can easily re-import your chat logs to the backend through"
									)}
									<span class="font-semibold dark:text-white"
										>{$i18n.t("Settings")} > {$i18n.t("Chats")} > {$i18n.t(
											"Import Chats"
										)}</span
									>. {$i18n.t(
										"This ensures that your valuable conversations are securely saved to your backend database. Thank you!"
									)}
								</div>

								<div class=" mt-6 mx-auto relative group w-fit">
									<button
										class="relative z-20 flex px-5 py-2 rounded-full bg-white border border-gray-100 dark:border-none hover:bg-gray-100 transition font-medium text-sm"
										on:click={async () => {
											let blob = new Blob([JSON.stringify(localDBChats)], {
												type: "application/json",
											});
											saveAs(blob, `chat-export-${Date.now()}.json`);

											const tx = DB.transaction("chats", "readwrite");
											await Promise.all([tx.store.clear(), tx.done]);
											await deleteDB("Chats");

											localDBChats = [];
										}}
									>
										Download & Delete
									</button>

									<button
										class="text-xs text-center w-full mt-2 text-gray-400 underline"
										on:click={async () => {
											localDBChats = [];
										}}>{$i18n.t("Close")}</button
									>
								</div>
							</div>
						</div>
					</div>
				</div>
			{/if}
			<Sidebar />
			<slot />
		{/if}
	</div>
</div>

<style>
	.loading {
		display: inline-block;
		clip-path: inset(0 1ch 0 0);
		animation: l 1s steps(3) infinite;
		letter-spacing: -0.5px;
	}

	@keyframes l {
		to {
			clip-path: inset(0 -1ch 0 0);
		}
	}

	pre[class*="language-"] {
		position: relative;
		overflow: auto;

		/* make space  */
		margin: 5px 0;
		padding: 1.75rem 0 1.75rem 1rem;
		border-radius: 10px;
	}

	pre[class*="language-"] button {
		position: absolute;
		top: 5px;
		right: 5px;

		font-size: 0.9rem;
		padding: 0.15rem;
		background-color: #828282;

		border: ridge 1px #7b7b7c;
		border-radius: 5px;
		text-shadow: #c4c4c4 0 0 2px;
	}

	pre[class*="language-"] button:hover {
		cursor: pointer;
		background-color: #bcbabb;
	}
</style>
