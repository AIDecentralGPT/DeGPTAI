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
	<div class="m-auto w-full px-8 lg:px-20 pb-[120px]">
		<div class="flex justify-start">
			<div class="flex space-x-4 mb-1" in:fade={{ duration: 200 }}></div>
		</div>

		<GetRewards/>

		<div class="w-full bg-1e1e1e padding-10" in:fade={{ duration: 200, delay: 300 }}>
			<Suggestions {suggestionPrompts} {submitPrompt} />
		</div>

		<!-- <a class="flex flex-col w-fit cursor-pointer border border-gray-600 rounded-lg p-4 py-2 mt-8  "  href="https://x.degpt.ai?comefrom=degpt.ai">
			<svg xmlns="http://www.w3.org/2000/svg" width="8em" height="8em" viewBox="0 0 16 16"><path fill="currentColor" d="M12.6.75h2.454l-5.36 6.142L16 15.25h-4.937l-3.867-5.07l-4.425 5.07H.316l5.733-6.57L0 .75h5.063l3.495 4.633L12.601.75Zm-.86 13.028h1.36L4.323 2.145H2.865z"/></svg>
			<div style="color: rgba(184, 142, 86, 1)">
				Twitter Personality
			</div>
		</a> -->
	</div>
{/key}

<style>
.padding-10 {
	padding: 10px;
}
</style>
