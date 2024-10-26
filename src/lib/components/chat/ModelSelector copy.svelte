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
		selectedModels = selectedModels.map((model) =>
			$models.map((m) => m.id).includes(model) ? model : ''
		);
	}

	function handleModelChange(event, index) {
		selectedModels[index] = event.detail.value;
		selectedModels = [...selectedModels];
	}

	function removeModel(index) {
		selectedModels.splice(index, 1);
		selectedModels = [...selectedModels];
	}

	function addModel() {
		if (selectedModels.includes('')) {
			toast.error($i18n.t('Remove empty model selection before adding a new one.'));
			return;
		}
		selectedModels = [...selectedModels, ''];
	}

	function getAvailableModels() {
		return $models
			.filter((model) => model.name !== 'hr' && !selectedModels.includes(model.id))
			.map((model) => ({
				value: model.id,
				label: model.name,
				info: model
			}));
	}
</script>

<div class="flex flex-col w-full items-center md:items-start">
	{#each selectedModels as selectedModel, selectedModelIdx}
		<div class="flex w-full max-w-fit">
			<div class="overflow-hidden w-full">
				<div class="mr-1 max-w-full">
					<Selector
						placeholder={$i18n.t('Select a model')}
						items={getAvailableModels()}
						value={selectedModel}
						on:change={(event) => handleModelChange(event, selectedModelIdx)}
					/>
				</div>
			</div>

			{#if selectedModelIdx === 0}
				<div class="self-center mr-2 disabled:text-gray-600 disabled:hover:text-gray-600">
					<Tooltip content={$i18n.t('Add Model')}>
						<button
							class=""
							on:click={addModel}
							{disabled}

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
				<div class="self-center disabled:text-gray-600 disabled:hover:text-gray-600 mr-2">
					<Tooltip content={$i18n.t('Remove Model')}>
						<button
							on:click={() => removeModel(selectedModelIdx)}
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
