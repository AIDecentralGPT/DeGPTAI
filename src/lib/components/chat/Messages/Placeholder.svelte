<script lang="ts">
	import { onMount, getContext } from 'svelte';

	import { fade } from 'svelte/transition';

	import Suggestions from '../MessageInput/Suggestions.svelte';
  	import GetRewards from '$lib/components/wallet/GetRewards.svelte';

	export let models = [];
	export let modelfiles = [];

	export let submitPrompt;
	export let suggestionPrompts;

	let mounted = false;
	let modelfile = null;
	let selectedModelIdx = 0;

	$: modelfile =
		models[selectedModelIdx] in modelfiles ? modelfiles[models[selectedModelIdx]] : null;

	$: if (models.length > 0) {
		selectedModelIdx = models.length - 1;
	}

	onMount(() => {
		mounted = true;
	});
</script>

{#key mounted}
	<div class="m-auto w-full max-w-6xl px-8 lg:px-24 pb-16">
		<div class="flex justify-start">
			<div class="flex space-x-4 mb-1" in:fade={{ duration: 200 }}></div>
		</div>

		<GetRewards/>

		<div class="w-full bg-1e1e1e padding-10" in:fade={{ duration: 200, delay: 300 }}>
			<Suggestions {suggestionPrompts} {submitPrompt} />
		</div>
	</div>
{/key}

<style>
.padding-10 {
	padding: 10px;
}
</style>
