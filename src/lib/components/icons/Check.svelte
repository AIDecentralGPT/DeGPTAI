<script lang="ts">
<<<<<<< HEAD
	export let className = 'w-4 h-4';
	export let strokeWidth = '1.5';
=======
	export let className = 'w-4.5 h-4.5';
	export let strokeWidth = '2';
>>>>>>> fingerprintAuth-out
	export let checkFlag = false;
</script>

{#if checkFlag}
<<<<<<< HEAD
	<div class="flex justify-center item-center size-4 border border-grey-600 dark:border-grey-100">
=======
	<div class="flex justify-center item-center size-5">
>>>>>>> fingerprintAuth-out
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
<<<<<<< HEAD
	<div class="flex justify-center item-center size-4 border border-grey-600 dark:border-grey-100"></div>
=======
	<div class="flex justify-center item-center size-5"></div>
>>>>>>> fingerprintAuth-out
{/if}

