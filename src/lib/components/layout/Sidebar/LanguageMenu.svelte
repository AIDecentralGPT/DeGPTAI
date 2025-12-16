<script lang="ts">
	import { DropdownMenu } from 'bits-ui';
	import { createEventDispatcher, onMount, getContext} from 'svelte';
	import { fade } from 'svelte/transition';
	import { getLanguages } from '$lib/i18n';

	export let show = false;
	export let className = 'max-w-[122px]';

	const dispatch = createEventDispatcher();

	const i18n = getContext('i18n');

	let isMobile = false;
	let languages = [];
  	onMount(async () => {
		const userAgent = navigator.userAgent || navigator.vendor || window.opera;
		// 检查是否为移动端设备
		isMobile = /android|iPad|iPhone|iPod|IEMobile|Opera Mini/i.test(userAgent);

		languages = await getLanguages();
	});
</script>

<DropdownMenu.Root
	bind:open={show}
	onOpenChange={(state) => {
		dispatch('change', state);
	}}
>
	<DropdownMenu.Trigger>
		<slot />
	</DropdownMenu.Trigger>

	<slot name="content">
		<DropdownMenu.Content
			class="w-full { className } text-sm rounded-xl px-1 py-1 border border-gray-300/30 dark:border-gray-700/50 z-50 bg-white dark:bg-gray-850 dark:text-white shadow"
			sideOffset={8}
			side="bottom"
			align="start"
			transition={(e) => fade(e, { duration: 100 })}
		>
			{#each languages as language}
				<button
					class="flex rounded-md py-1 px-2 w-full hover:bg-gray-50 dark:hover:bg-gray-800 transition"
					on:click={async () => {
						$i18n.changeLanguage(language.code);
						show = false;
					}}
				>
					<div class="self-center font-medium">{language['title']}</div>
				</button>
			{/each}
		</DropdownMenu.Content>
	</slot>
</DropdownMenu.Root>
