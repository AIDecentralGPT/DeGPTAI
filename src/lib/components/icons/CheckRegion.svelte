<script lang="ts">
	export let className = 'w-4 h-4';
	export let strokeWidth = '1.5';
	export let checkFlag:boolean = false;
</script>

{#if checkFlag}
	<div class="flex justify-center item-center size-4 border region-border-color">
		<svg
			xmlns="http://www.w3.org/2000/svg"
			fill="none"
			viewBox="0 0 24 24"
			stroke-width={strokeWidth}
			stroke="currentColor"
			class={className}
		>
			<path stroke-linecap="round" stroke-linejoin="round" d="m4.5 12.75 6 6 9-13.5" />
		</svg>
	</div>
{:else}
	<div class="flex justify-center item-center size-4 border region-border-color"></div>
{/if}

<style>
.region-border-color {
	border-color: rgba(184, 142, 86, 1);
}
</style>

