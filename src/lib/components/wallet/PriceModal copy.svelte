<script lang="ts">
  import Modal from "../common/Modal.svelte";
  export let show = false;

</script>

<Modal bind:show>
  <div class="bg-black text-white">
    <div class="mx-auto max-w-7xl px-6 lg:px-8">
        <div class="mx-auto max-w-4xl text-center">
            <h2 class="text-base font-semibold leading-7 text-indigo-600">Pricing</h2>
        </div>

        <div class="isolate mx-auto grid max-w-md grid-cols-1 gap-8 lg:mx-0 lg:max-w-none lg:grid-cols-2">
            <div class="rounded-3xl p-8 ring-1 xl:p-10 ring-gray-200 bg-black">
                <h3 id="tier-free" class="text-lg font-semibold leading-8 text-white">Free</h3>
                <p class="mt-6 flex items-baseline gap-x-1">
                    <!-- Price, update based on frequency toggle state -->
                    <span class="text-4xl font-bold tracking-tight text-white">$0</span>
                    <!-- Payment frequency, update based on frequency toggle state -->
                    <span class="text-sm font-semibold leading-6 text-gray-400">DGC</span>
                </p>
                <p class="text-sm leading-6 text-gray-400">per user, billed monthly</p>
                <button class="mt-6 block rounded-md py-2 px-3 text-center text-sm font-semibold leading-6 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 bg-gray-500 text-white shadow-sm hover:bg-gray-400 focus-visible:outline-gray-500">Your Current Plan</button>
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
            <div class="rounded-3xl p-8 ring-1 xl:p-10 ring-gray-200 bg-black">
                <h3 id="tier-plus" class="text-lg font-semibold leading-8 text-white">Plus</h3>
                <p class="mt-6 flex items-baseline gap-x-1">
                    <!-- Price, update based on frequency toggle state -->
                    <span class="text-4xl font-bold tracking-tight text-white">$5</span>
                    <!-- Payment frequency, update based on frequency toggle state -->
                    <span class="text-sm font-semibold leading-6 text-gray-400">DGC</span>
                </p>
                <p class="text-sm leading-6 text-gray-400">per user, billed monthly</p>
                <a href="#" aria-describedby="tier-plus" class="mt-6 block rounded-md py-2 px-3 text-center text-sm font-semibold leading-6 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 bg-yellow-500 text-white shadow-sm hover:bg-yellow-400 focus-visible:outline-yellow-500">Upgrade to Plus</a>
                <ul role="list" class="mt-8 space-y-3 text-sm leading-6 xl:mt-10 text-gray-400">
                    <li class="flex gap-x-3">
                        <svg class="h-6 w-5 flex-none text-yellow-500" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                            <path fill-rule="evenodd" d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z" clip-rule="evenodd" />
                        </svg>
                        Everything in Free
                    </li>
                    <li class="flex gap-x-3">
                        <svg class="h-6 w-5 flex-none text-yellow-500" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                            <path fill-rule="evenodd" d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z" clip-rule="evenodd" />
                        </svg>
                        Access to Llama 400B
                    </li>
                    <li class="flex gap-x-3">
                        <svg class="h-6 w-5 flex-none text-yellow-500" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                            <path fill-rule="evenodd" d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z" clip-rule="evenodd" />
                        </svg>
                        Regular model updates
                    </li>
                    <li class="flex gap-x-3">
                        <svg class="h-6 w-5 flex-none text-yellow-500" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
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
