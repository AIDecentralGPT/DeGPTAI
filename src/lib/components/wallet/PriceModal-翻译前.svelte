<script lang="ts">
  import { toast } from "svelte-sonner";
  import Modal from "../common/Modal.svelte";
  export let show = false;
  import { onMount, getContext } from 'svelte';
	const i18n = getContext('i18n');


</script>

<Modal bind:show size="lg">
  <div class="max-h-[80dvh] xs:h-auto flex flex-col">
    <div class=" flex justify-between dark:text-gray-300 px-5 pt-4 pb-2">
			<div class=" text-lg font-medium self-center">{$i18n.t('Upgrade')}</div>
			<button
				class="self-center"
				on:click={() => {
					show = false;
				}}
			>
				<svg
					xmlns="http://www.w3.org/2000/svg"
					viewBox="0 0 20 20"
					fill="currentColor"
					class="w-5 h-5"
				>
					<path
						d="M6.28 5.22a.75.75 0 00-1.06 1.06L8.94 10l-3.72 3.72a.75.75 0 101.06 1.06L10 11.06l3.72 3.72a.75.75 0 101.06-1.06L11.06 10l3.72-3.72a.75.75 0 00-1.06-1.06L10 8.94 6.28 5.22z"
					/>
				</svg>
			</button>
		</div>

    <div class="mx-auto max-w-7xl px-6 lg:px-8 flex-1 overflow-auto">
        <div class="mx-auto max-w-4xl text-center">
            <h2 class=" font-semibold leading-7 primaryText text-2xl	">Pricing</h2>
        </div>

        <div class="isolate mx-auto grid max-w-md grid-cols-1 gap-8 lg:mx-0 lg:max-w-none lg:grid-cols-2 h-8/10 md:h-108 overflow-y-auto">
            <div class="rounded-3xl p-8 ring-1 xl:p-10 ring-gray-200  m-4">
                <h3 id="tier-free" class="text-lg font-semibold leading-8 ">Free</h3>
                <p class="mt-6 flex items-baseline gap-x-1">
                    <!-- Price, update based on frequency toggle state -->
                    <span class="text-4xl font-bold tracking-tight ">$0</span>
                    <!-- Payment frequency, update based on frequency toggle state -->
                    <span class="text-sm font-semibold leading-6 text-gray-400">DGC</span>
                </p>
                <p class="text-sm leading-6 text-gray-400">per user, billed monthly</p>
                <button
                disabled
                class="w-full mt-6 block rounded-md py-2 px-3 text-center text-sm font-semibold leading-6 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 dark:bg-white dark:text-zinc-950 bg-black text-gray-100">Your Current Plan</button>
                <ul role="list" class="mt-8 space-y-3 text-sm leading-6 xl:mt-10 text-gray-400">
                    <li class="flex gap-x-3">
                        <svg class="h-6 w-5 flex-none text-gray-500" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                            <path fill-rule="evenodd" d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z" clip-rule="evenodd" />
                        </svg>
                        Unlimited messages, interactions and history
                    </li>
                    <li class="flex gap-x-3">
                        <svg class="h-6 w-5 flex-none text-gray-500" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                            <path fill-rule="evenodd" d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z" clip-rule="evenodd" />
                        </svg>
                        Access to Llama3-8B, Llama 70B, Qwen1.5-110B, yi1.5-34B
                    </li>
                    <li class="flex gap-x-3">
                        <svg class="h-6 w-5 flex-none text-gray-500" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                            <path fill-rule="evenodd" d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z" clip-rule="evenodd" />
                        </svg>
                        Regular model updates
                    </li>
                    <li class="flex gap-x-3">
                        <svg class="h-6 w-5 flex-none text-gray-500" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                            <path fill-rule="evenodd" d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z" clip-rule="evenodd" />
                        </svg>
                        Access on web, iOS, Android
                    </li>
                </ul>
            </div>
            <div class="rounded-3xl p-8 ring-1 xl:p-10 ring-gray-200  m-4">
                <h3 id="tier-plus" class="text-lg font-semibold leading-8 ">Plus</h3>
                <p class="mt-6 flex items-baseline gap-x-1">
                    <!-- Price, update based on frequency toggle state -->
                    <span class="text-4xl font-bold tracking-tight ">$5</span>
                    <!-- Payment frequency, update based on frequency toggle state -->
                    <span class="text-sm font-semibold leading-6 text-gray-400">DGC</span>
                </p>
                <p class="text-sm leading-6 text-gray-400">per user, billed monthly</p>
                <button 
                on:click={() => {
                    toast.warning("Coming soon...")
                }}
                href="#" aria-describedby="tier-plus" class="mt-6 px-4 py-2 primaryButton text-gray-100 text-sm transition rounded-lg w-full">Upgrade to Plus</button>
                <!-- <button href="#" aria-describedby="tier-plus" class="w-full mt-6 block rounded-md py-2 px-3 text-center text-sm  primaryButton">Upgrade to Plus</button> -->
                <ul role="list" class="mt-8 space-y-3 text-sm leading-6 xl:mt-10 text-gray-400">
                    <li class="flex gap-x-3">
                        <svg class="h-6 w-5 flex-none primaryText" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                            <path fill-rule="evenodd" d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z" clip-rule="evenodd" />
                        </svg>
                        Everything in Free
                    </li>
                    <li class="flex gap-x-3">
                        <svg class="h-6 w-5 flex-none primaryText" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                            <path fill-rule="evenodd" d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z" clip-rule="evenodd" />
                        </svg>
                        Access to Llama 400B
                    </li>
                    <li class="flex gap-x-3">
                        <svg class="h-6 w-5 flex-none primaryText" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                            <path fill-rule="evenodd" d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z" clip-rule="evenodd" />
                        </svg>
                        Regular model updates
                    </li>
                    <li class="flex gap-x-3">
                        <svg class="h-6 w-5 flex-none primaryText" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                            <path fill-rule="evenodd" d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z" clip-rule="evenodd" />
                        </svg>
                        Access on web, iOS, Android
                    </li>
                </ul>
            </div>
        </div>
    </div>
</div>

  
</Modal>

<style>
</style>
