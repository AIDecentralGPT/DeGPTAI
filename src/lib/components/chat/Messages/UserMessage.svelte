<script lang="ts">
	import dayjs from "dayjs";

	import { tick, createEventDispatcher, getContext } from "svelte";
	import Name from "./Name.svelte";
	import ProfileImage from "./ProfileImage.svelte";
	import { modelfiles, settings } from "$lib/stores";
	import Tooltip from "$lib/components/common/Tooltip.svelte";
	import FileSvg from "$lib/components/chat/Messages/FileSvg.svelte";
	import VideoPlayer from "$lib/components/chat/Messages/VideoPlayer.svelte";

	import { user as _user, deApiBaseUrl } from "$lib/stores";
	import Image from "$lib/components/common/Image.svelte";
	import { tranAudioToTxt } from "$lib/apis/de/index";

	const i18n = getContext("i18n");

	const dispatch = createEventDispatcher();

	export let user;
	export let message;
	export let siblings;
	export let isFirstMessage: boolean;
	export let readOnly: boolean;

	export let confirmEditMessage: Function;
	export let showPreviousMessage: Function;
	export let showNextMessage: Function;
	export let copyToClipboard: Function;

	let edit = false;
	let editedContent = "";
	let messageEditTextAreaElement: HTMLTextAreaElement;
	const editMessageHandler = async () => {
		edit = true;
		editedContent = message.content;

		await tick();

		messageEditTextAreaElement.style.height = "";
		messageEditTextAreaElement.style.height = `${messageEditTextAreaElement.scrollHeight}px`;

		// messageEditTextAreaElement?.focus();
	};

	const editMessageConfirmHandler = async () => {
		confirmEditMessage(message.id, editedContent);

		edit = false;
		editedContent = "";
	};

	const cancelEditMessage = () => {
		edit = false;
		editedContent = "";
	};

	const deleteMessageHandler = async () => {
		dispatch("delete", message.id);
	};
	let imageUrl = "";
	let totextflag = false;
	let defaultaudiotxt = "......";
	let audiotxt = "";
	let audiotxtTime: any = null;
	const handelAudioToTxt = async (data: string) => {
		if (audiotxtTime) {
			clearInterval(audiotxtTime);
		}	
		audiotxtTime = setInterval(() => {
			const textLength = defaultaudiotxt.length;
			if (textLength < 6) {
				defaultaudiotxt = ".".repeat(textLength + 1);
			} else {
				defaultaudiotxt = ".";
			}
		}, 300);
		audiotxt = await tranAudioToTxt(localStorage?.token, data, $deApiBaseUrl?.url);
		if (audiotxt == "") {
			audiotxt = $i18n.t("No text recognized");
		}
		clearInterval(audiotxtTime);
		audiotxtTime = null;
	}
</script>

<div class=" flex w-full user-message" dir={$settings.chatDirection}>
	{#if !($settings?.chatBubble ?? true)}
		<ProfileImage
			src={message.user
				? $modelfiles.find((modelfile) => modelfile.tagName === message.user)
						?.imageUrl ?? "/user.png"
				: user?.profile_image_url ?? "/user.png"}
		/>
	{/if}
	<div class="w-full overflow-hidden pl-1">
		{#if !($settings?.chatBubble ?? true)}
			<div>
				<Name>
					{#if message.user}
						{#if $modelfiles
							.map((modelfile) => modelfile.tagName)
							.includes(message.user)}
							{$modelfiles.find(
								(modelfile) => modelfile.tagName === message.user
							)?.title}
						{:else}
							{$i18n.t("You")}
							<span class=" text-gray-500 text-sm font-medium"
								>{message?.user ?? ""}</span
							>
						{/if}
					{:else if $settings.showUsername || $_user.name !== user.name}
						{user.name}
					{:else}
						{$i18n.t("You")}
					{/if}

					{#if message.timestamp}
						<span
							class=" invisible group-hover:visible text-gray-400 text-xs font-medium uppercase"
						>
							{dayjs(message.timestamp * 1000).format($i18n.t("h:mm a"))}
						</span>
					{/if}
				</Name>
			</div>
		{/if}

		<div
			class="prose chat-{message.role} w-full max-w-full flex flex-col justify-end dark:prose-invert prose-headings:my-0 prose-p:my-0 prose-p:-mb-4 prose-pre:my-0 prose-table:my-0 prose-blockquote:my-0 prose-img:my-0 prose-ul:-my-4 prose-ol:-my-4 prose-li:-my-3 prose-ul:-mb-6 prose-ol:-mb-6 prose-li:-mb-4 whitespace-pre-line"
		>
			{#if message.files}
				<div
					class="mt-2.5 mb-1 w-full flex flex-col justify-end overflow-x-auto gap-1 flex-wrap"
				>
					{#each message.files as file}
						<div class={$settings?.chatBubble ?? true ? "self-end" : ""}>
							{#if file.type === "image"}
								<Image
									src={file.url}
									alt="Uploaded Image"
									className="object-cover object-center max-w-96 max-h-64 rounded-lg cursor-pointer"
								/>
								<!-- <img src={file.url} alt="input" class="object-cover object-center max-w-96 max-h-64 rounded-lg cursor-pointer" draggable="false" /> -->
							{:else if file.type === "doc"}
								<button
									class="h-16 w-72 flex items-center space-x-3 px-2.5 dark:bg-gray-850 rounded-xl border border-gray-200 dark:border-none text-left"
									type="button"
								>
									<div class="text-white rounded-lg">
										<FileSvg bind:filename={file.name} />
									</div>

									<div class="flex flex-col justify-center -space-y-0.5">
										<div
											class=" dark:text-gray-100 text-sm font-medium line-clamp-1"
										>
											{file.name}
										</div>

										<div class=" text-gray-500 text-sm">
											{$i18n.t("Document")}
										</div>
									</div>
								</button>
							{:else if file.type === "collection"}
								<button
									class="h-16 w-72 flex items-center space-x-3 px-2.5 dark:bg-gray-600 rounded-xl border border-gray-200 dark:border-none text-left"
									type="button"
								>
									<div class="p-2.5 bg-red-400 text-white rounded-lg">
										<svg
											xmlns="http://www.w3.org/2000/svg"
											viewBox="0 0 24 24"
											fill="currentColor"
											class="w-6 h-6"
										>
											<path
												d="M7.5 3.375c0-1.036.84-1.875 1.875-1.875h.375a3.75 3.75 0 0 1 3.75 3.75v1.875C13.5 8.161 14.34 9 15.375 9h1.875A3.75 3.75 0 0 1 21 12.75v3.375C21 17.16 20.16 18 19.125 18h-9.75A1.875 1.875 0 0 1 7.5 16.125V3.375Z"
											/>
											<path
												d="M15 5.25a5.23 5.23 0 0 0-1.279-3.434 9.768 9.768 0 0 1 6.963 6.963A5.23 5.23 0 0 0 17.25 7.5h-1.875A.375.375 0 0 1 15 7.125V5.25ZM4.875 6H6v10.125A3.375 3.375 0 0 0 9.375 19.5H16.5v1.125c0 1.035-.84 1.875-1.875 1.875h-9.75A1.875 1.875 0 0 1 3 20.625V7.875C3 6.839 3.84 6 4.875 6Z"
											/>
										</svg>
									</div>

									<div class="flex flex-col justify-center -space-y-0.5">
										<div
											class=" dark:text-gray-100 text-sm font-medium line-clamp-1"
										>
											{file?.title ?? `#${file.name}`}
										</div>

										<div class=" text-gray-500 text-sm">
											{$i18n.t("Collection")}
										</div>
									</div>
								</button>
							{/if}
						</div>
					{/each}
				</div>
			{/if}

			{#if message?.toolInfo?.url}
				<div class="w-full flex justify-end mb-2">
					<div
						class="flex flex-row max-w-[200px] bg-gray-100 dark:bg-gray-850 p-3 rounded-full"
					>
						<div class="w-[20px] mr-1">
							<svg
								xmlns="http://www.w3.org/2000/svg"
								viewBox="0 0 1024 1024"
								version="1.1"
								fill="currentColor"
								class="w-5 h-5"
							>
								<path
									d="M512 34.133333a477.866667 477.866667 0 1 0 477.866667 477.866667A477.866667 477.866667 0 0 0 512 34.133333z m0 887.466667c-56.32 0-117.76-106.496-142.336-264.192A1219.584 1219.584 0 0 1 512 648.533333a1155.413333 1155.413333 0 0 1 142.336 9.216C629.76 815.104 568.32 921.6 512 921.6z m0-341.333333a1282.389333 1282.389333 0 0 0-150.528 9.216c-2.048-24.917333-3.072-50.858667-3.072-77.482667s0-52.565333 3.072-77.482667A1282.389333 1282.389333 0 0 0 512 443.733333a1214.122667 1214.122667 0 0 0 150.528-9.557333q3.072 37.888 3.072 77.824t-3.072 77.824A1214.122667 1214.122667 0 0 0 512 580.266667zM102.4 512a406.869333 406.869333 0 0 1 21.504-129.706667 1194.666667 1194.666667 0 0 0 170.666667 41.984c-2.389333 28.330667-3.754667 57.685333-3.754667 87.722667s0 59.392 3.754667 87.722667a1194.666667 1194.666667 0 0 0-170.666667 41.984A406.869333 406.869333 0 0 1 102.4 512zM512 102.4c56.32 0 117.76 106.496 142.336 263.850667A1155.413333 1155.413333 0 0 1 512 375.466667a1219.584 1219.584 0 0 1-142.336-8.874667C394.24 208.896 455.68 102.4 512 102.4z m218.112 321.877333a1194.666667 1194.666667 0 0 0 170.666667-41.984 402.090667 402.090667 0 0 1 0 259.413334 1194.666667 1194.666667 0 0 0-170.666667-41.984c2.389333-28.330667 3.754667-57.685333 3.754667-87.722667s-1.365333-59.392-3.754667-87.722667z m143.018667-105.130666a1173.504 1173.504 0 0 1-150.528 36.864 609.621333 609.621333 0 0 0-77.482667-231.082667 411.648 411.648 0 0 1 228.010667 194.218667zM378.88 124.928a609.621333 609.621333 0 0 0-77.482667 231.082667 1173.504 1173.504 0 0 1-150.528-36.864 411.648 411.648 0 0 1 228.010667-194.218667z m-228.010667 580.266667a1204.906667 1204.906667 0 0 1 150.528-37.205334 611.669333 611.669333 0 0 0 77.482667 231.424 411.648 411.648 0 0 1-228.010667-194.56z m494.250667 193.877333a609.621333 609.621333 0 0 0 77.482667-231.082667 1173.504 1173.504 0 0 1 150.528 36.864 411.648 411.648 0 0 1-228.010667 194.218667z"
								/>
							</svg>
						</div>
						<span
							class="inline-block whitespace-nowrap overflow-hidden text-ellipsis text-sm"
							>{message?.toolInfo?.url}</span
						>
					</div>
				</div>
			{/if}

			{#if message?.toolInfo?.audio}
				<div class="w-full flex justify-end mb-2">
					<div class="flex flex-col">
						<div
							class="flex flex-row max-w-[300px] bg-gray-100 dark:bg-gray-850 p-3 rounded-full"
						>
							<VideoPlayer bind:audioinfo={message.toolInfo.audio} />
						</div>
						<div
							class="flex flex-row max-w-[300px] bg-gray-100 dark:bg-gray-850 px-5 py-3 rounded-[30px] mt-1"
						>
							<div class="flex items-start w-[20px]">
								<button on:click="{async () => {
									if (!totextflag) {
										if (audiotxt == "") {
											await handelAudioToTxt(message.toolInfo.audio.data);
										}	
									}
									totextflag = !totextflag;	
								}}">
									<svg
										xmlns="http://www.w3.org/2000/svg"
										viewBox="0 0 466 465"
										version="1.1"
										width="18"
										height="18"
									>
										<path
											d="M0 0 C1.19 -0 2.38 -0.01 3.61 -0.01 C4.9 -0.01 6.2 -0.01 7.54 -0.01 C8.92 -0.01 10.31 -0.02 11.7 -0.02 C15.46 -0.03 19.22 -0.03 22.98 -0.03 C25.33 -0.03 27.68 -0.04 30.03 -0.04 C38.25 -0.05 46.46 -0.05 54.67 -0.05 C62.31 -0.05 69.95 -0.06 77.6 -0.08 C84.17 -0.09 90.74 -0.1 97.31 -0.1 C101.23 -0.09 105.15 -0.1 109.07 -0.11 C112.76 -0.12 116.45 -0.12 120.14 -0.11 C122.13 -0.11 124.12 -0.12 126.11 -0.13 C139.19 -0.08 150.4 2.92 160.18 12.06 C172.73 25.86 172.52 40.9 172.46 58.51 C172.46 60.69 172.47 62.87 172.47 65.05 C172.47 69.61 172.47 74.16 172.45 78.71 C172.44 84.53 172.45 90.34 172.46 96.16 C172.47 100.65 172.47 105.15 172.46 109.65 C172.46 111.79 172.46 113.93 172.47 116.08 C172.48 119.08 172.47 122.08 172.45 125.09 C172.46 125.96 172.46 126.83 172.47 127.73 C172.3 143.82 163.94 154.9 152.82 165.83 C151.92 166.73 151.02 167.63 150.1 168.55 C147.67 170.99 145.22 173.41 142.77 175.83 C140.21 178.37 137.65 180.92 135.1 183.47 C130.27 188.29 125.43 193.1 120.58 197.9 C115.06 203.38 109.55 208.86 104.05 214.35 C92.73 225.62 81.4 236.88 70.06 248.13 C68.44 244.9 70.09 241.83 71.06 238.51 C71.29 237.71 71.51 236.92 71.75 236.1 C73.04 231.58 74.38 227.06 75.71 222.55 C76.29 220.6 76.86 218.65 77.44 216.7 C77.73 215.7 78.02 214.71 78.32 213.69 C81.58 202.54 84.45 191.29 87.3 180.03 C88.17 176.71 89.12 173.43 90.06 170.13 C88.84 170.14 87.63 170.15 86.37 170.16 C74.87 170.24 63.36 170.3 51.86 170.34 C45.94 170.36 40.03 170.39 34.11 170.44 C28.4 170.48 22.69 170.5 16.98 170.51 C14.8 170.52 12.63 170.53 10.45 170.56 C7.4 170.59 4.34 170.59 1.28 170.59 C0.4 170.6 -0.49 170.62 -1.41 170.63 C-12.54 170.56 -21.19 165.71 -29.04 158.1 C-35.72 151.02 -41.02 142.76 -41.09 132.79 C-41.11 131.49 -41.11 131.49 -41.12 130.17 C-41.12 129.23 -41.13 128.29 -41.13 127.32 C-41.14 126.33 -41.15 125.33 -41.16 124.31 C-41.18 121.01 -41.2 117.71 -41.21 114.41 C-41.22 113.29 -41.22 112.16 -41.23 110.99 C-41.25 105.02 -41.27 99.04 -41.29 93.06 C-41.3 88.12 -41.33 83.19 -41.37 78.25 C-41.42 72.28 -41.44 66.31 -41.45 60.34 C-41.46 58.08 -41.47 55.81 -41.5 53.54 C-41.67 36.48 -40.37 24.12 -28.16 11.27 C-20.28 3.77 -10.82 0.02 0 0 Z "
											fill="#BE9B6C"
											transform="translate(274.9383087158203,27.866287231445313)"
										/>
										<path
											d="M0 0 C14.19 0 28.38 0 43 0 C43.99 6.93 44.98 13.86 46 21 C49.92 33.93 55.38 44.62 64 55 C64.45 55.59 64.89 56.19 65.36 56.8 C75.25 69.45 92.47 78.51 108 82 C108.75 82.2 109.5 82.4 110.28 82.61 C132.26 87.72 153.87 83.28 173 72 C193.37 59.21 205.44 40.47 211.11 17.38 C212.28 11.63 213.11 5.81 214 0 C227.86 0 241.72 0 256 0 C256 9.3 255.89 17.16 254.06 26.06 C253.74 27.66 253.74 27.66 253.4 29.3 C249.79 45.67 242.77 60.43 233 74 C232.43 74.8 231.86 75.6 231.27 76.43 C229.58 78.69 227.82 80.85 226 83 C225.2 83.94 224.4 84.89 223.58 85.86 C204.75 107.53 178.12 121.31 150 126 C150 140.85 150 155.7 150 171 C135.81 171 121.62 171 107 171 C107 156.15 107 141.3 107 126 C101.56 125.01 101.56 125.01 96 124 C73.81 118.43 55.67 107.33 39 92 C38.32 91.39 37.63 90.77 36.93 90.14 C12.04 66.7 1.84 33.07 0 0 Z "
											fill="#BE9B6C"
											transform="translate(20,284)"
										/>
										<path
											d="M0 0 C8.2 6.67 14.58 15.62 16.62 26.12 C16.92 30.05 16.93 33.96 16.93 37.9 C16.94 39.07 16.95 40.23 16.96 41.44 C16.98 45.29 16.99 49.15 17 53 C17 54.34 17 55.67 17.01 57.01 C17.03 64.01 17.05 71.01 17.05 78.01 C17.05 84.5 17.08 90.99 17.13 97.48 C17.16 103.07 17.18 108.67 17.18 114.27 C17.18 117.6 17.19 120.93 17.21 124.26 C17.45 156.47 17.45 156.47 6.57 169.16 C-3.07 178.87 -12.47 183.34 -26 183.44 C-33.51 183.45 -39.83 183.18 -46.38 179.12 C-47.06 178.7 -47.75 178.28 -48.46 177.84 C-57.96 171.31 -65.99 161.6 -68.38 150.12 C-68.47 148.42 -68.51 146.71 -68.52 145 C-68.52 143.97 -68.53 142.93 -68.53 141.87 C-68.53 140.74 -68.53 139.61 -68.54 138.45 C-68.54 137.25 -68.55 136.06 -68.55 134.83 C-68.56 131.56 -68.57 128.28 -68.58 125.01 C-68.58 122.96 -68.58 120.91 -68.59 118.86 C-68.6 112.45 -68.61 106.03 -68.61 99.61 C-68.62 92.22 -68.64 84.83 -68.66 77.44 C-68.69 71.71 -68.7 65.99 -68.7 60.26 C-68.7 56.85 -68.7 53.44 -68.72 50.02 C-68.74 46.21 -68.74 42.39 -68.73 38.58 C-68.74 37.46 -68.75 36.35 -68.76 35.19 C-68.7 23.47 -65.72 15.22 -58.38 6.12 C-57.85 5.47 -57.33 4.82 -56.79 4.15 C-42.25 -12.02 -16.87 -11.8 0 0 Z "
											fill="#BE9B6C"
											transform="translate(174.375,142.875)"
										/>
									</svg>
								</button>
							</div>
							{#if totextflag}
								<span class="ml-1 text-sm {audiotxt != "" ? '' : 'text-[#BE9B6C]'}">{ audiotxt != "" ? audiotxt : defaultaudiotxt }</span>
							{:else}
								<span class="ml-1 text-sm text-[#BE9B6C]">{ defaultaudiotxt }</span>
							{/if}
						</div>
					</div>
				</div>
			{:else if edit === true}
				<div
					class=" w-full bg-gray-50 dark:bg-gray-800 rounded-3xl px-5 py-3 mb-2"
				>
					<textarea
						id="message-edit-{message.id}"
						bind:this={messageEditTextAreaElement}
						class=" bg-transparent outline-none w-full resize-none"
						bind:value={editedContent}
						on:input={(e) => {
							e.target.style.height = "";
							e.target.style.height = `${e.target.scrollHeight}px`;
						}}
						on:keydown={(e) => {
							if (e.key === "Escape") {
								document.getElementById("close-edit-message-button")?.click();
							}

							const isCmdOrCtrlPressed = e.metaKey || e.ctrlKey;
							const isEnterPressed = e.key === "Enter";

							if (isCmdOrCtrlPressed && isEnterPressed) {
								document.getElementById("save-edit-message-button")?.click();
							}
						}}
					/>

					<div
						class=" mt-2 mb-1 flex justify-end space-x-1.5 text-sm font-medium"
					>
						<button
							id="close-edit-message-button"
							class=" px-4 py-2 bg-gray-900 hover:bg-gray-850 text-gray-100 transition rounded-3xl close-edit-message-button"
							on:click={() => {
								cancelEditMessage();
							}}
						>
							{$i18n.t("Cancel")}
						</button>

						<button
							id="save-edit-message-button"
							class="px-4 py-2 bg-white hover:bg-gray-100 text-gray-800 transition rounded-3xl"
							on:click={() => {
								editMessageConfirmHandler();
							}}
						>
							{$i18n.t("Send")}
						</button>
					</div>
				</div>
			{:else}
				<div class="w-full">
					<div
						class="flex {$settings?.chatBubble ?? true
							? 'justify-end'
							: ''} mb-2"
					>
						<div
							class="rounded-3xl {$settings?.chatBubble ?? true
								? `max-w-[90%] px-5 py-2  bg-gray-100 dark:bg-gray-850 ${
										message.files ? 'rounded-tr-lg' : ''
								  }`
								: ''}  "
						>
							<pre id="user-message">{message.content}</pre>
						</div>
					</div>

					<div
						class=" flex {$settings?.chatBubble ?? true
							? 'justify-end'
							: ''}  text-gray-600 dark:text-gray-500"
					>
						{#if !($settings?.chatBubble ?? true)}
							{#if siblings.length > 1}
								<div class="flex self-center" dir="ltr">
									<button
										class="self-center p-1 hover:bg-black/5 dark:hover:bg-white/5 dark:hover:text-white hover:text-black rounded-md transition"
										on:click={() => {
											showPreviousMessage(message);
										}}
									>
										<svg
											xmlns="http://www.w3.org/2000/svg"
											fill="none"
											viewBox="0 0 24 24"
											stroke="currentColor"
											stroke-width="2.5"
											class="size-3.5"
										>
											<path
												stroke-linecap="round"
												stroke-linejoin="round"
												d="M15.75 19.5 8.25 12l7.5-7.5"
											/>
										</svg>
									</button>

									<div
										class="text-sm tracking-widest font-semibold self-center dark:text-gray-100"
									>
										{siblings.indexOf(message.id) + 1}/{siblings.length}
									</div>

									<button
										class="self-center p-1 hover:bg-black/5 dark:hover:bg-white/5 dark:hover:text-white hover:text-black rounded-md transition"
										on:click={() => {
											showNextMessage(message);
										}}
									>
										<svg
											xmlns="http://www.w3.org/2000/svg"
											fill="none"
											viewBox="0 0 24 24"
											stroke="currentColor"
											stroke-width="2.5"
											class="size-3.5"
										>
											<path
												stroke-linecap="round"
												stroke-linejoin="round"
												d="m8.25 4.5 7.5 7.5-7.5 7.5"
											/>
										</svg>
									</button>
								</div>
							{/if}
						{/if}
						{#if !readOnly}
							<Tooltip content={$i18n.t("Edit")} placement="bottom">
								<button
									class="invisible group-hover:visible p-1.5 hover:bg-black/5 dark:hover:bg-white/5 rounded-lg dark:hover:text-white hover:text-black transition edit-user-message-button"
									on:click={() => {
										editMessageHandler();
									}}
								>
									<svg
										xmlns="http://www.w3.org/2000/svg"
										fill="none"
										viewBox="0 0 24 24"
										stroke-width="2.3"
										stroke="currentColor"
										class="w-4 h-4"
									>
										<path
											stroke-linecap="round"
											stroke-linejoin="round"
											d="M16.862 4.487l1.687-1.688a1.875 1.875 0 112.652 2.652L6.832 19.82a4.5 4.5 0 01-1.897 1.13l-2.685.8.8-2.685a4.5 4.5 0 011.13-1.897L16.863 4.487zm0 0L19.5 7.125"
										/>
									</svg>
								</button>
							</Tooltip>
						{/if}

						<Tooltip content={$i18n.t("Copy")} placement="bottom">
							<button
								class="invisible group-hover:visible p-1.5 hover:bg-black/5 dark:hover:bg-white/5 rounded-lg dark:hover:text-white hover:text-black transition"
								on:click={() => {
									copyToClipboard(message.content);
								}}
							>
								<svg
									xmlns="http://www.w3.org/2000/svg"
									fill="none"
									viewBox="0 0 24 24"
									stroke-width="2.3"
									stroke="currentColor"
									class="w-4 h-4"
								>
									<path
										stroke-linecap="round"
										stroke-linejoin="round"
										d="M15.666 3.888A2.25 2.25 0 0013.5 2.25h-3c-1.03 0-1.9.693-2.166 1.638m7.332 0c.055.194.084.4.084.612v0a.75.75 0 01-.75.75H9a.75.75 0 01-.75-.75v0c0-.212.03-.418.084-.612m7.332 0c.646.049 1.288.11 1.927.184 1.1.128 1.907 1.077 1.907 2.185V19.5a2.25 2.25 0 01-2.25 2.25H6.75A2.25 2.25 0 014.5 19.5V6.257c0-1.108.806-2.057 1.907-2.185a48.208 48.208 0 011.927-.184"
									/>
								</svg>
							</button>
						</Tooltip>

						{#if !isFirstMessage && !readOnly}
							<Tooltip content={$i18n.t("Delete")} placement="bottom">
								<button
									class="invisible group-hover:visible p-1 rounded dark:hover:text-white hover:text-black transition"
									on:click={() => {
										deleteMessageHandler();
									}}
								>
									<svg
										xmlns="http://www.w3.org/2000/svg"
										fill="none"
										viewBox="0 0 24 24"
										stroke-width="2"
										stroke="currentColor"
										class="w-4 h-4"
									>
										<path
											stroke-linecap="round"
											stroke-linejoin="round"
											d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0"
										/>
									</svg>
								</button>
							</Tooltip>
						{/if}

						{#if $settings?.chatBubble ?? true}
							{#if siblings.length > 1}
								<div class="flex self-center" dir="ltr">
									<button
										class="self-center p-1 hover:bg-black/5 dark:hover:bg-white/5 dark:hover:text-white hover:text-black rounded-md transition"
										on:click={() => {
											showPreviousMessage(message);
										}}
									>
										<svg
											xmlns="http://www.w3.org/2000/svg"
											fill="none"
											viewBox="0 0 24 24"
											stroke="currentColor"
											stroke-width="2.5"
											class="size-3.5"
										>
											<path
												stroke-linecap="round"
												stroke-linejoin="round"
												d="M15.75 19.5 8.25 12l7.5-7.5"
											/>
										</svg>
									</button>

									<div
										class="text-sm tracking-widest font-semibold self-center dark:text-gray-100"
									>
										{siblings.indexOf(message.id) + 1}/{siblings.length}
									</div>

									<button
										class="self-center p-1 hover:bg-black/5 dark:hover:bg-white/5 dark:hover:text-white hover:text-black rounded-md transition"
										on:click={() => {
											showNextMessage(message);
										}}
									>
										<svg
											xmlns="http://www.w3.org/2000/svg"
											fill="none"
											viewBox="0 0 24 24"
											stroke="currentColor"
											stroke-width="2.5"
											class="size-3.5"
										>
											<path
												stroke-linecap="round"
												stroke-linejoin="round"
												d="m8.25 4.5 7.5 7.5-7.5 7.5"
											/>
										</svg>
									</button>
								</div>
							{/if}
						{/if}
					</div>
				</div>
			{/if}
		</div>
	</div>
</div>
