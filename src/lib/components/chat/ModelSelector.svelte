<script lang="ts">
	import { Collapsible } from 'bits-ui';

	import { setDefaultModels } from '$lib/apis/configs';
	import { models, showSettings, settings, user, mobile } from '$lib/stores';
	import { onMount, tick, getContext } from 'svelte';
	import { toast } from 'svelte-sonner';
	import Selector from './ModelSelector/Selector.svelte';
	import Tooltip from '../common/Tooltip.svelte';

	const i18n = getContext('i18n');

	export let selectedModels = [''];
	export let modelsList= [''];
	export let disabled = false;

	export let showSetDefault = true;

	const saveDefaultModel = async () => {
		const hasEmptyModel = selectedModels.filter((it) => it === '');
		if (hasEmptyModel.length) {
			toast.error($i18n.t('Choose a model before saving...'));
			return;
		}
		settings.set({ ...$settings, models: selectedModels });
		localStorage.setItem('settings', JSON.stringify($settings));

		if ($user?.role === 'admin') {
			console.log('setting default models globally');
			await setDefaultModels(localStorage.token, selectedModels.join(','));
		}
		toast.success($i18n.t('Default model updated'));
	};

	$: if (selectedModels.length > 0 && $models.length > 0) {

		

		selectedModels = selectedModels.map((model) =>{
			if(selectedModels.length === 1) {
				return selectedModels[0] ==='' ? $models[0]?.model : model
			}
			else {
				return 	$models.map((m) => m.id).includes(model) ? model : ''
			}
			
		}
		);
		

		//  modelsList  = $models?.filter((item) => !selectedModels.includes(item.name)  )

		// console.log("$modelsList", $models, modelsList);

	}
</script>

<div class="flex flex-col w-full items-center md:items-start">
	<!-- {#each modelsList as selectedModel, selectedModelIdx} -->
	{#each selectedModels as selectedModel, selectedModelIdx}
		<div class="flex w-full max-w-fit">
			<div class="overflow-hidden w-full">
				<div class="mr-1 max-w-full">
					<Selector
						placeholder={$i18n.t('Select a model')}
						items={$models
							.filter((model) => model.name !== 'hr')
							.map((model) => ({
								value: model.id,
								label: model.name,
								info: model
							}))}
						selectedList = {selectedModels}
						bind:value={selectedModel}
					/>
				</div>
			</div>

			{#if (selectedModelIdx === selectedModels?.length -1 && selectedModels?.length !== $models.length)}
				<div class="  self-center mr-2 disabled:text-gray-600 disabled:hover:text-gray-600">
					<Tooltip content={$i18n.t('Add Model,supports multiple models to answer questions simultaneously.')}>
						<button
							class=" "
							{disabled}
							on:click={() => {
								selectedModels = [...selectedModels, ''];
							}}
						>
							<svg
								xmlns="http://www.w3.org/2000/svg"
								fill="none"
								viewBox="0 0 24 24"
								stroke-width="2"
								stroke="currentColor"
								class="size-3.5"
							>
								<path stroke-linecap="round" stroke-linejoin="round" d="M12 6v12m6-6H6" />
							</svg>
						</button>
					</Tooltip>
				</div>
			{:else}
				<div class="  self-center disabled:text-gray-600 disabled:hover:text-gray-600 mr-2">
					<Tooltip content={$i18n.t('Remove Model')}>
						<button
							{disabled}
							on:click={() => {
								selectedModels.splice(selectedModelIdx, 1);
								selectedModels = selectedModels;
							}}
						>
							<svg
								xmlns="http://www.w3.org/2000/svg"
								fill="none"
								viewBox="0 0 24 24"
								stroke-width="2"
								stroke="currentColor"
								class="size-3.5"
							>
								<path stroke-linecap="round" stroke-linejoin="round" d="M19.5 12h-15" />
							</svg>
						</button>
					</Tooltip>
				</div>
			{/if}
		</div>
	{/each}
</div>

{#if showSetDefault && !$mobile}
	<div class="text-left mt-0.5 ml-1 text-[0.7rem] text-gray-500">
		<button on:click={saveDefaultModel}> {$i18n.t('Set as default')}</button>
	</div>
{/if}