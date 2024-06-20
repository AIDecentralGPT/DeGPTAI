<script lang="ts">
	import { onMount } from 'svelte';
	import { fade } from 'svelte/transition';
	import dayjs from 'dayjs';
	import { getContext } from 'svelte';
  import { getCurrentPair } from '$lib/utils/wallet/dbc';
  import { getUsersInvited } from '$lib/apis/users';
  import Modal from '../common/Modal.svelte';
	const i18n = getContext('i18n');

	export let show = true;

	let modalElement = null;
	let mounted = false;



	let users = []

	const handleKeyDown = (event: KeyboardEvent) => {
		if (event.key === 'Escape') {
			show = false;
		}
	};

	onMount(async () => {
		mounted = true;


		const pair = getCurrentPair()
		console.log("pair?.address", pair?.address);
		users = await getUsersInvited(localStorage.token, pair?.address);
		console.log("users", users);

	});

	$: if (mounted) {
		if (show) {
			window.addEventListener('keydown', handleKeyDown);
			document.body.style.overflow = 'hidden';
		} else {
			window.removeEventListener('keydown', handleKeyDown);
			document.body.style.overflow = 'unset';
		}
	}

	
</script>

{#if show}
	<!-- svelte-ignore a11y-click-events-have-key-events -->
	<!-- svelte-ignore a11y-no-static-element-interactions -->
	<Modal bind:show size="lg"
	>
		<div
			class=" m-auto rounded-2xl max-w-full  mx-2 bg-gray-50 dark:bg-gray-900 shadow-3xl p-4"
			on:mousedown={(e) => {
				e.stopPropagation();
			}}
		>
			<h1 class="text-xl font-semibold mb-4">{$i18n.t('view reward')}</h1>
			<div class="overflow-x-auto">
				<table class="min-w-full divide-y divide-gray-200">
					<thead>
						<tr>   
							<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider whitespace-nowrap">{$i18n.t('address invited')}</th>
							<!-- <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider whitespace-nowrap">{$i18n.t('role')}</th> -->
							<!-- <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider whitespace-nowrap">{$i18n.t('name')}</th> -->


							<!-- <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider whitespace-nowrap">{$i18n.t('email')}</th> -->
							<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider whitespace-nowrap">{$i18n.t('lastActive')}</th>
							<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider whitespace-nowrap">{$i18n.t('createdAt')}</th>
							<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider whitespace-nowrap">{$i18n.t('rewards amount')}</th>
							<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider whitespace-nowrap">{$i18n.t('notes')}</th>
				
						</tr>
					</thead>
					<tbody class="bg-white border-b dark:bg-gray-900 dark:border-gray-700 text-xs ">
						{#each users as user}
							<tr>
								<td class="px-6 py-4 whitespace-nowrap flex items-center">
									<img src={user.profile_image_url} alt="profile" class="w-6 h-6 rounded-full mr-2"/>
									{user.id}</td>
								<!-- <td class="px-6 py-4 whitespace-nowrap">{user.role}</td> -->
								<!-- <td class="px-6 py-4 whitespace-nowrap flex items-center"><img src={user.profile_image_url} alt="profile" class="w-6 h-6 rounded-full mr-2"/>{user.name}</td> -->
							
							
								<!-- <td class="px-6 py-4 whitespace-nowrap">{user.email}</td> -->
								<td class="px-6 py-4 whitespace-nowrap">{dayjs(user.last_active_at * 1000).format('YYYY-MM-DD HH:mm:ss')}</td>
								<td class="px-6 py-4 whitespace-nowrap">{dayjs(user.created_at * 1000).format('YYYY-MM-DD HH:mm:ss')}</td>
								<td class="px-6 py-4 whitespace-nowrap">{('0DGC')}</td>
								<!-- <td class="px-6 py-4 whitespace-nowrap">{('500DGC')}</td> -->
								<td class="px-6 py-4 whitespace-nowrap">{$i18n.t('invite new user')}</td>

								
							</tr>
						{/each}
					</tbody>
				</table>
			</div>
		</div>
	</Modal>
{/if}

<style>
	.modal-content {
		animation: scaleUp 0.1s ease-out forwards;
	}

	@keyframes scaleUp {
		from {
			transform: scale(0.985);
			opacity: 0;
		}
		to {
			transform: scale(1);
			opacity: 1;
		}
	}
</style>
