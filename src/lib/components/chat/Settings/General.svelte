<script lang="ts">
	import { DropdownMenu } from "bits-ui";
	import ChevronDown from "$lib/components/icons/ChevronDown.svelte";
	import { toast } from 'svelte-sonner';
	import { createEventDispatcher, onMount, getContext } from 'svelte';
	import { getLanguages } from '$lib/i18n';
	const dispatch = createEventDispatcher();

	import { models, user, theme, mobile } from '$lib/stores';
	import { updateUserLanguage } from "$lib/apis/users";

	const i18n = getContext('i18n');

	import AdvancedParams from './Advanced/AdvancedParams.svelte';

	export let saveSettings: Function;
	export let getModels: Function;

	// General
	let themes = ['dark', 'light', 'rose-pine dark', 'rose-pine-dawn light', 'oled-dark'];
	let selectedTheme = 'light';
	// let selectedTheme = 'dark';

	let languages = [];
	let lang = $i18n.language;
	let notificationEnabled = false;
	let system = '';

	let showAdvanced = false;

	const toggleNotification = async () => {
		const permission = await Notification.requestPermission();

		if (permission === 'granted') {
			notificationEnabled = !notificationEnabled;
			saveSettings({ notificationEnabled: notificationEnabled });
		} else {
			toast.error(
				'Response notifications cannot be activated as the website permissions have been denied. Please visit your browser settings to grant the necessary access.'
			);
		}
	};

	// Advanced
	let requestFormat = '';
	let keepAlive = null;

	let options = {
		// Advanced
		seed: 0,
		temperature: '',
		repeat_penalty: '',
		repeat_last_n: '',
		mirostat: '',
		mirostat_eta: '',
		mirostat_tau: '',
		top_k: '',
		top_p: '',
		stop: '',
		tfs_z: '',
		num_ctx: '',
		num_predict: ''
	};

	const toggleRequestFormat = async () => {
		if (requestFormat === '') {
			requestFormat = 'json';
		} else {
			requestFormat = '';
		}

		saveSettings({ requestFormat: requestFormat !== '' ? requestFormat : undefined });
	};

	onMount(async () => {
		selectedTheme = localStorage.theme ?? 'light';
		// selectedTheme = localStorage.theme ?? 'dark';
		console.log("localStorage.theme", localStorage.theme);
		

		let settings = JSON.parse(localStorage.getItem('settings') ?? '{}');
		languages = await getLanguages();

		notificationEnabled = settings.notificationEnabled ?? false;
		system = settings.system ?? '';

		requestFormat = settings.requestFormat ?? '';
		keepAlive = settings.keepAlive ?? null;

		options.seed = settings.seed ?? 0;
		options.temperature = settings.temperature ?? '';
		options.repeat_penalty = settings.repeat_penalty ?? '';
		options.top_k = settings.top_k ?? '';
		options.top_p = settings.top_p ?? '';
		options.num_ctx = settings.num_ctx ?? '';
		options = { ...options, ...settings.options };
		options.stop = (settings?.options?.stop ?? []).join(',');
	});

	const applyTheme = (_theme: string) => {
		let themeToApply = _theme === 'oled-dark' ? 'dark' : _theme;

		if (_theme === 'system') {
			themeToApply = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
		}

		if (themeToApply === 'dark' && !_theme.includes('oled')) {
			document.documentElement.style.setProperty('--color-gray-900', '#171717');
			document.documentElement.style.setProperty('--color-gray-950', '#0d0d0d');
		}

		themes
			.filter((e) => e !== themeToApply)
			.forEach((e) => {
				e.split(' ').forEach((e) => {
					document.documentElement.classList.remove(e);
				});
			});

		themeToApply.split(' ').forEach((e) => {
			document.documentElement.classList.add(e);
		});

		console.log(_theme);
	};

	let themeshow = false;
	const themeChangeHandler = (_theme: string) => {
		theme.set(_theme);
		localStorage.setItem('theme', _theme);
		if (_theme.includes('oled')) {
			document.documentElement.style.setProperty('--color-gray-900', '#000000');
			document.documentElement.style.setProperty('--color-gray-950', '#000000');
			document.documentElement.classList.add('dark');
		}
		applyTheme(_theme);
		selectedTheme = localStorage.theme ?? 'light';
		themeshow = false;
	};

	let languageshow = false;
	let langmt = 0;
	let langselView:any;
	$: if (languageshow) {
		if (langselView) {
			const rect = langselView.getBoundingClientRect();
			if (rect.top < 380) {
				langmt = 400 - rect.top;
			} else {
				langmt = 0;
			}
		}
	}

	let isMobile = false;

	const checkUserAgent = () => {
		const userAgent = navigator.userAgent || navigator.vendor || window.opera;
		// 检测常见的移动设备标识
		isMobile = /android|iphone|ipad|iPod|blackberry|opera mini|iemobile|wpdesktop/i.test(userAgent);
		if(isMobile) {
			// themeChangeHandler("dark")
		}
	};

	onMount(() => {
		checkUserAgent();
	});


</script>

<div class="flex flex-col h-full justify-between text-sm">
	<div class="  pr-1.5 overflow-y-scroll max-h-[25rem]">
		<div class="">
			<div class=" mb-1 text-sm font-medium">{$i18n.t('User interface settings')}</div>

			<!-- {#if !isMobile} -->
			<div class="flex w-full justify-between mt-1">
				<div class=" self-center text-xs font-medium">{$i18n.t('Theme')}</div>
				<div class="flex items-center">
					<DropdownMenu.Root bind:open={themeshow}>
						<DropdownMenu.Trigger>
							<div class="flex flex-row justify-end mr-1">
								<span class="text-ellipsis overflow-hidden">
									{#if selectedTheme == "system"}
										⚙️ {$i18n.t('System')}
									{:else if selectedTheme == "dark"}
										🌑 {$i18n.t('Dark')}
									{:else if selectedTheme == "oled-dark"}
										🌃 {$i18n.t('OLED Dark')}
									{:else}
										☀️ {$i18n.t('Light')}
									{/if}
								</span>
								<ChevronDown className=" self-center ml-2 size-3" strokeWidth="2.5" />
							</div>	
						</DropdownMenu.Trigger>
						<DropdownMenu.Content class="z-[10000] rounded-md  bg-white dark:bg-gray-850 dark:text-white 
							shadow-lg border border-gray-300/30 dark:border-gray-700/50  outline-none" 
							side="bottom-end">
							<slot>
								<div class="flex flex-col px-1 py-2">
									<button class="flex justify-between items-center cursor-pointer w-full hover:bg-gray-100 dark:hover:bg-gray-800 py-1 px-6 rounded-lg"
										on:click={() => {
											themeChangeHandler("system")
										}}>
										<span class="text-sm">⚙️ {$i18n.t('System')}</span>
									</button>
									<button class="flex justify-between items-center cursor-pointer w-full hover:bg-gray-100 dark:hover:bg-gray-800 py-1 px-6 rounded-lg"
										on:click={() => {
											themeChangeHandler("dark")
										}}>
										<span class="text-sm">🌑 {$i18n.t('Dark')}</span>
									</button>
									<button class="flex justify-between items-center cursor-pointer w-full hover:bg-gray-100 dark:hover:bg-gray-800 py-1 px-6 rounded-lg"
										on:click={() => {
											themeChangeHandler("oled-dark")
										}}>
										<span class="text-sm">🌃 {$i18n.t('OLED Dark')}</span>
									</button>
									<button class="flex justify-between items-center cursor-pointer w-full hover:bg-gray-100 dark:hover:bg-gray-800 py-1 px-6 rounded-lg"
										on:click={() => {
											themeChangeHandler("light")
										}}>
										<span class="text-sm">☀️ {$i18n.t('Light')}</span>
									</button>
								</div>
								<div class="hidden w-[42rem]" />
      					<div class="hidden w-[32rem]" />
							</slot>
						</DropdownMenu.Content>
					</DropdownMenu.Root>
				</div>
			</div>
			<!-- {/if} -->

			<div class=" flex w-full justify-between mt-1">
				<div class=" self-center text-xs font-medium">{$i18n.t('Language')}</div>
				<div bind:this={langselView} class="flex items-center">
					<DropdownMenu.Root bind:open={languageshow}>
						<DropdownMenu.Trigger>
							<div class="flex flex-row justify-end mr-1">
								<span class="text-ellipsis overflow-hidden">
									{#each languages as language}
										{#if language['code'] == lang}
											{language['title']}
										{/if}
									{/each}
								</span>
								<ChevronDown className=" self-center ml-2 size-3" strokeWidth="2.5" />
							</div>	
						</DropdownMenu.Trigger>
						<DropdownMenu.Content class="z-[10000] rounded-md  bg-white dark:bg-gray-850 dark:text-white 
							shadow-lg border border-gray-300/30 dark:border-gray-700/50  outline-none"
							style="margin-top:{langmt}px"
							avoidCollisions={true}
							collisionPadding={10} 
							side="bottom-end">
							<slot>
								<div class="flex flex-col px-1 py-2">
									{#each languages as language}
										<button class="flex justify-between items-center cursor-pointer w-full hover:bg-gray-100 dark:hover:bg-gray-800 py-1 px-6 rounded-lg"
											on:click={() => {
												lang = language['code'];
												$i18n.changeLanguage(lang);
												updateUserLanguage(localStorage.token, lang);
												languageshow = false;
											}}>
											<span class="text-sm">{language['title']}</span>
										</button>
									{/each}
								</div>
								<div class="hidden w-[42rem]" />
      					<div class="hidden w-[32rem]" />
							</slot>
						</DropdownMenu.Content>
					</DropdownMenu.Root>
				</div>
			</div>
			{#if $i18n.language === 'en-US'}
				<div class="mb-2 text-xs text-gray-400 dark:text-gray-500">
					Couldn't find your language?
					<a
						class=" text-gray-300 font-medium underline"
						href="https://github.com/open-webui/open-webui/blob/main/docs/CONTRIBUTING.md#-translations-and-internationalization"
						target="_blank"
					>
						Help us translate DeGPT!
					</a>
				</div>
			{/if}
			<!-- {#if !$mobile} -->
			{#if false}
				<div>
					<div class=" py-0.5 flex w-full justify-between">
						<div class=" self-center text-xs font-medium">{$i18n.t('Notifications')}</div>

						<button
							class="p-1 px-3 text-xs flex rounded transition"
							on:click={() => {
								toggleNotification();
							}}
							type="button"
						>
							{#if notificationEnabled === true}
								<span class="ml-2 self-center">{$i18n.t('On')}</span>
							{:else}
								<span class="ml-2 self-center">{$i18n.t('Off')}</span>
							{/if}
						</button>
					</div>
				</div>
			{/if}
		</div>

		<hr class=" dark:border-gray-700 my-3" />
		{#if false}
			<div>
				<div class=" my-2.5 text-sm font-medium">{$i18n.t('System Prompt')}</div>
				<textarea
					bind:value={system}
					class="w-full rounded-lg p-4 text-sm dark:text-gray-300 dark:bg-gray-850 outline-none resize-none"
					rows="4"
				/>
			</div>
		{/if}

		<div class="mt-2 space-y-3 pr-1.5">
			<!-- <div class="flex justify-between items-center text-sm">
				<div class="  font-medium">{$i18n.t('Advanced Parameters')}</div>
				<button
					class=" text-xs font-medium text-gray-500"
					type="button"
					on:click={() => {
						showAdvanced = !showAdvanced;
					}}>{showAdvanced ? $i18n.t('Hide') : $i18n.t('Show')}</button
				>
			</div> -->

			{#if showAdvanced}
				<AdvancedParams bind:options />
				<hr class=" dark:border-gray-700" />

				<div class=" py-1 w-full justify-between">
					<div class="flex w-full justify-between">
						<div class=" self-center text-xs font-medium">{$i18n.t('Keep Alive')}</div>

						<button
							class="p-1 px-3 text-xs flex rounded transition"
							type="button"
							on:click={() => {
								keepAlive = keepAlive === null ? '5m' : null;
							}}
						>
							{#if keepAlive === null}
								<span class="ml-2 self-center"> {$i18n.t('Default')} </span>
							{:else}
								<span class="ml-2 self-center"> {$i18n.t('Custom')} </span>
							{/if}
						</button>
					</div>

					{#if keepAlive !== null}
						<div class="flex mt-1 space-x-2">
							<input
								class="w-full rounded-lg py-2 px-4 text-sm dark:text-gray-300 dark:bg-gray-850 outline-none"
								type="text"
								placeholder={$i18n.t("e.g. '30s','10m'. Valid time units are 's', 'm', 'h'.")}
								bind:value={keepAlive}
							/>
						</div>
					{/if}
				</div>

				<div>
					<div class=" py-1 flex w-full justify-between">
						<div class=" self-center text-sm font-medium">{$i18n.t('Request Mode')}</div>

						<button
							class="p-1 px-3 text-xs flex rounded transition"
							on:click={() => {
								toggleRequestFormat();
							}}
						>
							{#if requestFormat === ''}
								<span class="ml-2 self-center"> {$i18n.t('Default')} </span>
							{:else if requestFormat === 'json'}
								<!-- <svg
                            xmlns="http://www.w3.org/2000/svg"
                            viewBox="0 0 20 20"
                            fill="currentColor"
                            class="w-4 h-4 self-center"
                        >
                            <path
                                d="M10 2a.75.75 0 01.75.75v1.5a.75.75 0 01-1.5 0v-1.5A.75.75 0 0110 2zM10 15a.75.75 0 01.75.75v1.5a.75.75 0 01-1.5 0v-1.5A.75.75 0 0110 15zM10 7a3 3 0 100 6 3 3 0 000-6zM15.657 5.404a.75.75 0 10-1.06-1.06l-1.061 1.06a.75.75 0 001.06 1.06l1.06-1.06zM6.464 14.596a.75.75 0 10-1.06-1.06l-1.06 1.06a.75.75 0 001.06 1.06l1.06-1.06zM18 10a.75.75 0 01-.75.75h-1.5a.75.75 0 010-1.5h1.5A.75.75 0 0118 10zM5 10a.75.75 0 01-.75.75h-1.5a.75.75 0 010-1.5h1.5A.75.75 0 015 10zM14.596 15.657a.75.75 0 001.06-1.06l-1.06-1.061a.75.75 0 10-1.06 1.06l1.06 1.06zM5.404 6.464a.75.75 0 001.06-1.06l-1.06-1.06a.75.75 0 10-1.061 1.06l1.06 1.06z"
                            />
                        </svg> -->
								<span class="ml-2 self-center"> {$i18n.t('JSON')} </span>
							{/if}
						</button>
					</div>
				</div>
			{/if}
		</div>
	</div>

	<div class="flex justify-end pt-3 text-sm font-medium">
		<!-- <button
			class="  px-4 py-2 primaryButton text-gray-100 transition rounded-lg"
			on:click={async () => {
				saveSettings({
					system: system !== '' ? system : undefined,
					options: {
						seed: (options.seed !== 0 ? options.seed : undefined) ?? undefined,
						stop: options.stop !== '' ? options.stop.split(',').filter((e) => e) : undefined,
						temperature: options.temperature !== '' ? options.temperature : undefined,
						repeat_penalty: options.repeat_penalty !== '' ? options.repeat_penalty : undefined,
						repeat_last_n: options.repeat_last_n !== '' ? options.repeat_last_n : undefined,
						mirostat: options.mirostat !== '' ? options.mirostat : undefined,
						mirostat_eta: options.mirostat_eta !== '' ? options.mirostat_eta : undefined,
						mirostat_tau: options.mirostat_tau !== '' ? options.mirostat_tau : undefined,
						top_k: options.top_k !== '' ? options.top_k : undefined,
						top_p: options.top_p !== '' ? options.top_p : undefined,
						tfs_z: options.tfs_z !== '' ? options.tfs_z : undefined,
						num_ctx: options.num_ctx !== '' ? options.num_ctx : undefined,
						num_predict: options.num_predict !== '' ? options.num_predict : undefined
					},
					keepAlive: keepAlive ? (isNaN(keepAlive) ? keepAlive : parseInt(keepAlive)) : undefined
				});
				dispatch('save');
			}}
		>
			{$i18n.t('Save')}
		</button> -->
	</div>
</div>
