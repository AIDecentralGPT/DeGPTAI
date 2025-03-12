<script lang="ts">
	import { DropdownMenu } from "bits-ui";
	import { createEventDispatcher, getContext } from "svelte";

	import { flyAndScale } from "$lib/utils/transitions";
	import { goto } from "$app/navigation";
	import ArchiveBox from "$lib/components/icons/ArchiveBox.svelte";
	import { user, showSettings } from "$lib/stores";
	import { fade, slide } from "svelte/transition";

	const i18n = getContext("i18n");

	export let show = false;
	export let role = "";
	export let className = "max-w-[240px]";

	const dispatch = createEventDispatcher();
</script>

<DropdownMenu.Root
	bind:open={show}
	onOpenChange={(state) => {
		dispatch("change", state);
	}}
>
	<DropdownMenu.Trigger>
		<slot />
	</DropdownMenu.Trigger>

	<slot name="content">
		<DropdownMenu.Content
			class="w-full {className} text-sm rounded-xl px-1 py-1.5 border border-gray-300/30 dark:border-gray-700/50 z-50 bg-white dark:bg-gray-850 dark:text-white shadow"
			sideOffset={8}
			side="bottom"
			align="start"
			transition={(e) => fade(e, { duration: 100 })}
		>
			<button
				class="flex rounded-md py-2 px-3 w-full hover:bg-gray-50 dark:hover:bg-gray-800 transition"
				on:click={async () => {
					await showSettings.set(true);
					show = false;
				}}
			>
				<div class=" self-center mr-3">
					<svg
						xmlns="http://www.w3.org/2000/svg"
						fill="none"
						viewBox="0 0 24 24"
						stroke-width="1.5"
						stroke="currentColor"
						class="w-5 h-5"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							d="M10.343 3.94c.09-.542.56-.94 1.11-.94h1.093c.55 0 1.02.398 1.11.94l.149.894c.07.424.384.764.78.93.398.164.855.142 1.205-.108l.737-.527a1.125 1.125 0 011.45.12l.773.774c.39.389.44 1.002.12 1.45l-.527.737c-.25.35-.272.806-.107 1.204.165.397.505.71.93.78l.893.15c.543.09.94.56.94 1.109v1.094c0 .55-.397 1.02-.94 1.11l-.893.149c-.425.07-.765.383-.93.78-.165.398-.143.854.107 1.204l.527.738c.32.447.269 1.06-.12 1.45l-.774.773a1.125 1.125 0 01-1.449.12l-.738-.527c-.35-.25-.806-.272-1.203-.107-.397.165-.71.505-.781.929l-.149.894c-.09.542-.56.94-1.11.94h-1.094c-.55 0-1.019-.398-1.11-.94l-.148-.894c-.071-.424-.384-.764-.781-.93-.398-.164-.854-.142-1.204.108l-.738.527c-.447.32-1.06.269-1.45-.12l-.773-.774a1.125 1.125 0 01-.12-1.45l.527-.737c.25-.35.273-.806.108-1.204-.165-.397-.505-.71-.93-.78l-.894-.15c-.542-.09-.94-.56-.94-1.109v-1.094c0-.55.398-1.02.94-1.11l.894-.149c.424-.07.765-.383.93-.78.165-.398.143-.854-.107-1.204l-.527-.738a1.125 1.125 0 01.12-1.45l.773-.773a1.125 1.125 0 011.45-.12l.737.527c.35.25.807.272 1.204.107.397-.165.71-.505.78-.929l.15-.894z"
						/>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
						/>
					</svg>
				</div>
				<div class=" self-center font-medium">{$i18n.t("Settings")}</div>
			</button>

			{#if $user?.role === 'admin'}
				<button
					class="flex rounded-md py-2 px-3 w-full hover:bg-gray-50 dark:hover:bg-gray-800 transition"
					on:click={ async () => {
						goto("/statistics");
					}}
				>
					<div class=" self-center mr-3">
						<svg
							xmlns="http://www.w3.org/2000/svg"
							viewBox="0 0 1024 1024"
							fill="currentColor"
							class="w-5 h-5">
							<path d="M510.8 961.2C263.5 961.2 62.4 760 62.4 512.7S263.5 64.2 510.8 64.2s448.5 201.2 448.5 448.5-201.2 448.5-448.5 448.5z m0-837.2c-214.3 0-388.7 174.4-388.7 388.7s174.4 388.7 388.7 388.7S899.5 727 899.5 512.7 725.2 124 510.8 124z"/>
							<path d="M316.5 636.7V388.8c0-14 11.5-25.5 25.5-25.5h8.7c14 0 25.5 11.5 25.5 25.5v247.9c0 14-11.5 25.5-25.5 25.5H342c-14 0-25.5-11.5-25.5-25.5zM436.1 636.7V448.6c0-14 11.5-25.5 25.5-25.5h8.7c14 0 25.5 11.5 25.5 25.5v188.1c0 14-11.5 25.5-25.5 25.5h-8.7c-14 0-25.5-11.5-25.5-25.5zM555.7 636.7V388.8c0-14 11.5-25.5 25.5-25.5h8.7c14 0 25.5 11.5 25.5 25.5v247.9c0 14-11.5 25.5-25.5 25.5h-8.7c-14 0-25.5-11.5-25.5-25.5zM675.3 636.7V508.4c0-14 11.5-25.5 25.5-25.5h8.7c14 0 25.5 11.5 25.5 25.5v128.3c0 14-11.5 25.5-25.5 25.5h-8.7c-14 0-25.5-11.5-25.5-25.5z"/>
						</svg>
					</div>
					<div class=" self-center font-medium">{$i18n.t("Dashboard")}</div>
				</button>
			{/if}

			<!-- <button
				class="flex rounded-md py-2 px-3 w-full hover:bg-gray-50 dark:hover:bg-gray-800 transition"
				on:click={() => {
					dispatch('show', 'archived-chat');
					show = false;
				}}
			>
				<div class=" self-center mr-3">
					<ArchiveBox className="size-5" strokeWidth="1.5" />
				</div>
				<div class=" self-center font-medium">{$i18n.t('Archived Chats')}</div>
			</button> -->

			{#if role === "admin"}
				<button
					class="flex rounded-md py-2 px-3 w-full hover:bg-gray-50 dark:hover:bg-gray-800 transition"
					on:click={() => {
						goto("/admin");
						show = false;
					}}
				>
					<div class=" self-center mr-3">
						<svg
							xmlns="http://www.w3.org/2000/svg"
							fill="none"
							viewBox="0 0 24 24"
							stroke="currentColor"
							class="w-5 h-5"
						>
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								d="M17.982 18.725A7.488 7.488 0 0012 15.75a7.488 7.488 0 00-5.982 2.975m11.963 0a9 9 0 10-11.963 0m11.963 0A8.966 8.966 0 0112 21a8.966 8.966 0 01-5.982-2.275M15 9.75a3 3 0 11-6 0 3 3 0 016 0z"
							/>
						</svg>
					</div>
					<div class=" self-center font-medium">{$i18n.t("User Report")}</div>
				</button>
			{/if}

			{#if $user?.role === 'admin'}
				<button
					class="flex rounded-md py-2 px-3 w-full hover:bg-gray-50 dark:hover:bg-gray-800 transition"
					on:click={ async () => {
						goto("/rewardup");
					}}
				>
					<div class=" self-center mr-3">
						<svg
							xmlns="http://www.w3.org/2000/svg"
							viewBox="0 0 1024 1024"
							fill="currentColor"
							class="w-5 h-5"
						>
							<path d="M512 64c247.424 0 448 200.576 448 448s-200.576 448-448 448S64 759.424 64 512 264.576 64 512 64z m0 64C299.936 128 128 299.936 128 512s171.936 384 384 384 384-171.936 384-384S724.064 128 512 128z m0 128c139.104 0 256 58.432 256 144 0 22.72-8.224 43.488-22.912 61.76 14.72 18.4 22.912 39.168 22.912 61.536 0 21.792-7.584 41.824-21.184 59.584 13.664 17.824 21.184 37.856 21.184 59.328 0 85.568-116.896 144-256 144-139.104 0-256-58.432-256-144 0-21.536 7.52-41.568 21.184-59.392-13.6-17.728-21.184-37.76-21.184-59.52 0-22.4 8.16-43.168 22.88-61.536C264.224 443.52 256 422.72 256 400 256 314.432 372.896 256 512 256z m-185.76 368.256a32.448 32.448 0 0 0-6.24 17.952c0 38.144 83.68 80 192 80s192-41.856 192-80c0-5.664-2.016-11.712-6.208-17.92l-5.632 3.104c-46.592 25.28-110.592 39.904-180.16 39.904-72.384 0-138.752-15.808-185.76-43.04z m369.28-122.016l-3.36 1.856C645.568 529.376 581.568 544 512 544c-71.232 0-136.64-15.328-183.488-41.76-5.76 7.296-8.512 14.464-8.512 21.056 0 38.176 83.68 80 192 80s192-41.824 192-80c0-6.592-2.752-13.76-8.48-21.056zM512 320c-108.32 0-192 41.856-192 80s83.68 80 192 80 192-41.856 192-80-83.68-80-192-80z"/>
						</svg>
					</div>
					<div class=" self-center font-medium">{$i18n.t("Reward upkeep")}</div>
				</button>
			{/if}

			<!-- <hr class=" dark:border-gray-800 my-2 p-0" /> -->

			<!-- <button
				class="flex rounded-md py-2 px-3 w-full hover:bg-gray-50 dark:hover:bg-gray-800 transition"
				on:click={() => {
					// localStorage.removeItem('token');
					// location.href = '/auth';
					show = false;
				}}
			>
				<div class=" self-center mr-3">
					<svg
						xmlns="http://www.w3.org/2000/svg"
						viewBox="0 0 20 20"
						fill="currentColor"
						class="w-5 h-5"
					>
						<path
							fill-rule="evenodd"
							d="M3 4.25A2.25 2.25 0 015.25 2h5.5A2.25 2.25 0 0113 4.25v2a.75.75 0 01-1.5 0v-2a.75.75 0 00-.75-.75h-5.5a.75.75 0 00-.75.75v11.5c0 .414.336.75.75.75h5.5a.75.75 0 00.75-.75v-2a.75.75 0 011.5 0v2A2.25 2.25 0 0110.75 18h-5.5A2.25 2.25 0 013 15.75V4.25z"
							clip-rule="evenodd"
						/>
						<path
							fill-rule="evenodd"
							d="M6 10a.75.75 0 01.75-.75h9.546l-1.048-.943a.75.75 0 111.004-1.114l2.5 2.25a.75.75 0 010 1.114l-2.5 2.25a.75.75 0 11-1.004-1.114l1.048-.943H6.75A.75.75 0 016 10z"
							clip-rule="evenodd"
						/>
					</svg>
				</div>
				<div class=" self-center font-medium">{$i18n.t('Sign Out')}</div>
			</button> -->

			<!-- <DropdownMenu.Item class="flex items-center px-3 py-2 text-sm  font-medium">
				<div class="flex items-center">Profile</div>
			</DropdownMenu.Item> -->
		</DropdownMenu.Content>
	</slot>
</DropdownMenu.Root>
