<script lang="ts">
	import { toast } from 'svelte-sonner';
	import dayjs from 'dayjs';
	import { marked } from 'marked';
	import tippy from 'tippy.js';
	import auto_render from 'katex/dist/contrib/auto-render.mjs';
	import 'katex/dist/katex.min.css';

	import { fade } from 'svelte/transition';
	import { createEventDispatcher } from 'svelte';
	import { onMount, tick, getContext } from 'svelte';

	const i18n = getContext('i18n');

	const dispatch = createEventDispatcher();

	import { config, settings, models, theme } from '$lib/stores';

	import { synthesizeOpenAISpeech } from '$lib/apis/audio';
	import { imageGenerations } from '$lib/apis/images';
	import {
		approximateToHumanReadable,
		extractSentences,
		revertSanitizedResponseContent,
		sanitizeResponseContent
	} from '$lib/utils';
	import { WEBUI_BASE_URL } from '$lib/constants';

	import Name from './Name.svelte';
	import ProfileImage from './ProfileImage.svelte';
	import Thinking from './Thinking.svelte';
	import Skeleton from './Skeleton.svelte';
	import CodeBlock from './CodeBlock.svelte';
	import Image from '$lib/components/common/Image.svelte';
	import Tooltip from '$lib/components/common/Tooltip.svelte';
	import RateComment from './RateComment.svelte';
	import CitationsModal from '$lib/components/chat/Messages/CitationsModal.svelte';
	import TwitterEmbed from "$lib/components/twitter/TwitterEmbed.svelte";

	export let modelfiles = [];
	export let message;
	export let siblings;

	export let isLastMessage = true;

	export let readOnly = false;

	export let updateChatMessages: Function;
	export let confirmEditResponseMessage: Function;
	export let showPreviousMessage: Function;
	export let showNextMessage: Function;
	export let rateMessage: Function;

	export let copyToClipboard: Function;
	export let continueGeneration: Function;
	export let regenerateResponse: Function;

	let edit = false;
	let editedContent = '';
	let editTextAreaElement: HTMLTextAreaElement;
	let tooltipInstance = null;

	let sentencesAudio = {};
	let speaking = null;
	let speakingIdx = null;

	let loadingSpeech = false;
	let generatingImage = false;

	let showRateComment = false;
	let showCitationModal = false;

	let selectedCitation = null;

	$: tokens = deepseekAnalysis((message?.think_content??'') + message?.content);

	function deepseekAnalysis(content: any) {
		if (content.startsWith("<think>")) {
			let firstIndex = content.indexOf('</think>');
			if (firstIndex == -1) {
				return [{type: "thinking", raw: content.replace("<think>", "")}];	
			} else {
				let token = content.split('</think>');
				let thinkObj = {type: "thinking", raw: token[0].replace("<think>", "")};
				if (token.length > 1) {
					return [
						thinkObj,
						...marked.lexer(sanitizeResponseContent(token[1]))
					]
				} else {
					return [thinkObj];
				}	
			}
		} else {
			return marked.lexer(sanitizeResponseContent(content));
		}
	}

	const renderer = new marked.Renderer();

	// For code blocks with simple backticks
	renderer.codespan = (code) => {
		return `<code>${code.replaceAll('&amp;', '&')}</code>`;
	};

	const { extensions, ...defaults } = marked.getDefaults() as marked.MarkedOptions & {
		// eslint-disable-next-line @typescript-eslint/no-explicit-any
		extensions: any;
	};

	

	$: if (message) {
		renderStyling();
	}

	const renderStyling = async () => {
		await tick();

		if (tooltipInstance) {
			tooltipInstance[0]?.destroy();
		}

		renderLatex();

		if (message.info) {
			tooltipInstance = tippy(`#info-${message.id}`, {
				content: `<span class="text-xs" id="tooltip-${message.id}">response_token/s: ${
					`${
						Math.round(
							((message.info.eval_count ?? 0) / (message.info.eval_duration / 1000000000)) * 100
						) / 100
					} tokens` ?? 'N/A'
				}<br/>
					prompt_token/s: ${
						Math.round(
							((message.info.prompt_eval_count ?? 0) /
								(message.info.prompt_eval_duration / 1000000000)) *
								100
						) / 100 ?? 'N/A'
					} tokens<br/>
                    total_duration: ${
											Math.round(((message.info.total_duration ?? 0) / 1000000) * 100) / 100 ??
											'N/A'
										}ms<br/>
                    load_duration: ${
											Math.round(((message.info.load_duration ?? 0) / 1000000) * 100) / 100 ?? 'N/A'
										}ms<br/>
                    prompt_eval_count: ${message.info.prompt_eval_count ?? 'N/A'}<br/>
                    prompt_eval_duration: ${
											Math.round(((message.info.prompt_eval_duration ?? 0) / 1000000) * 100) /
												100 ?? 'N/A'
										}ms<br/>
                    eval_count: ${message.info.eval_count ?? 'N/A'}<br/>
                    eval_duration: ${
											Math.round(((message.info.eval_duration ?? 0) / 1000000) * 100) / 100 ?? 'N/A'
										}ms<br/>
                    approximate_total: ${approximateToHumanReadable(
											message.info.total_duration
										)}</span>`,
				allowHTML: true
			});
		}
	};

	const renderLatex = () => {
		let chatMessageElements = document
			.getElementById(`message-${message.id}`)
			?.getElementsByClassName('chat-assistant');

		if (chatMessageElements) {
			for (const element of chatMessageElements) {
				auto_render(element, {
					// customised options
					// • auto-render specific keys, e.g.:
					delimiters: [
						{ left: '$$', right: '$$', display: false },
						{ left: '$ ', right: ' $', display: false },
						{ left: '\\(', right: '\\)', display: false },
						{ left: '\\[', right: '\\]', display: false },
						{ left: '[ ', right: ' ]', display: false }
					],
					// • rendering keys, e.g.:
					throwOnError: false
				});
			}
		}
	};

	const playAudio = (idx) => {
		return new Promise((res) => {
			speakingIdx = idx;
			const audio = sentencesAudio[idx];
			audio.play();
			audio.onended = async (e) => {
				await new Promise((r) => setTimeout(r, 300));

				if (Object.keys(sentencesAudio).length - 1 === idx) {
					speaking = null;

					if ($settings.conversationMode) {
						document.getElementById('voice-input-button')?.click();
					}
				}

				res(e);
			};
		});
	};

	const toggleSpeakMessage = async () => {
		if (speaking) {
			try {
				speechSynthesis.cancel();

				sentencesAudio[speakingIdx].pause();
				sentencesAudio[speakingIdx].currentTime = 0;
			} catch {}

			speaking = null;
			speakingIdx = null;
		} else {
			speaking = true;

			if ($settings?.audio?.TTSEngine === 'openai') {
				loadingSpeech = true;

				const sentences = extractSentences(message.content).reduce((mergedTexts, currentText) => {
					const lastIndex = mergedTexts.length - 1;
					if (lastIndex >= 0) {
						const previousText = mergedTexts[lastIndex];
						const wordCount = previousText.split(/\s+/).length;
						if (wordCount < 2) {
							mergedTexts[lastIndex] = previousText + ' ' + currentText;
						} else {
							mergedTexts.push(currentText);
						}
					} else {
						mergedTexts.push(currentText);
					}
					return mergedTexts;
				}, []);

				console.log(sentences);

				sentencesAudio = sentences.reduce((a, e, i, arr) => {
					a[i] = null;
					return a;
				}, {});

				let lastPlayedAudioPromise = Promise.resolve(); // Initialize a promise that resolves immediately

				for (const [idx, sentence] of sentences.entries()) {
					const res = await synthesizeOpenAISpeech(
						localStorage.token,
						$settings?.audio?.speaker,
						sentence,
						$settings?.audio?.model
					).catch((error) => {
						toast.error(error);

						speaking = null;
						loadingSpeech = false;

						return null;
					});

					if (res) {
						const blob = await res.blob();
						const blobUrl = URL.createObjectURL(blob);
						const audio = new Audio(blobUrl);
						sentencesAudio[idx] = audio;
						loadingSpeech = false;
						lastPlayedAudioPromise = lastPlayedAudioPromise.then(() => playAudio(idx));
					}
				}
			} else {
				let voices = [];
				const getVoicesLoop = setInterval(async () => {
					voices = await speechSynthesis.getVoices();
					if (voices.length > 0) {
						clearInterval(getVoicesLoop);

						const voice =
							voices?.filter((v) => v.name === $settings?.audio?.speaker)?.at(0) ?? undefined;

						const speak = new SpeechSynthesisUtterance(message.content);

						speak.onend = () => {
							speaking = null;
							if ($settings.conversationMode) {
								document.getElementById('voice-input-button')?.click();
							}
						};
						speak.voice = voice;
						speechSynthesis.speak(speak);
					}
				}, 100);
			}
		}
	};

	const editMessageHandler = async () => {
		edit = true;
		editedContent = message.content;

		await tick();

		editTextAreaElement.style.height = '';
		editTextAreaElement.style.height = `${editTextAreaElement.scrollHeight}px`;
	};

	const editMessageConfirmHandler = async () => {
		if (editedContent === '') {
			editedContent = ' ';
		}

		confirmEditResponseMessage(message.id, editedContent);

		edit = false;
		editedContent = '';

		await tick();
		renderStyling();
	};

	const cancelEditMessage = async () => {
		edit = false;
		editedContent = '';
		await tick();
		renderStyling();
	};

	const generateImage = async (message) => {
		generatingImage = true;
		const res = await imageGenerations(localStorage.token, message.content).catch((error) => {
			toast.error(error);
		});
		console.log(res);

		if (res) {
			message.files = res.map((image) => ({
				type: 'image',
				url: `${image.url}`
			}));

			dispatch('save', message);
		}

		generatingImage = false;
	};

	// 加载twitter组件
	let isTwitterScriptLoaded = false;
	const loadTwitterScript = () => {
    if (isTwitterScriptLoaded) return;
    const script = document.createElement('script');
    script.src = 'https://platform.twitter.com/widgets.js';
    script.charset = 'utf-8';
    script.async = true;
    script.onload = () => {
      isTwitterScriptLoaded = true;
    };
    document.head.appendChild(script);
  };

	onMount(async () => {
		await tick();
		renderStyling();
		loadTwitterScript();
	});

	// 格式化模型名字
	const formatModelName = (model) => {
		// console.log("models", $models);
		const modelName = $models.filter((item) => item.model === model)?.[0]?.name || model
		
		return modelName
	}

	// 校验图片模型
	const checkModelImage = (model) => {
		// console.log("models", $models);
		const checkModel = $models.filter((item) => item?.model === model);
		if (checkModel.length > 0 && checkModel[0]?.support === 'image') {
			return true;
		} else {
			return false;
		}
	}


	$: webShow = webFlag;
	let webFlag = false;
	// 隐藏web搜索
	const handleWebHidden = () => {
		webFlag = !webFlag;
	}

	let thinkHiden = false;

	function highlightedText(content: string, keyword: string) {
		let keywords = keyword.split("/");
		keywords.forEach((item) => {
			const regex = new RegExp(item, "gi");
			content = content.replace(regex, match => `<span style="color: rgba(184, 142, 86, 1);">${match}</span>`);
		})
    return content;
  }

	// 监听主题变化
	let currentTheme = $theme;
	$: {
		currentTheme = ($theme === "system" || $theme === "light") ? 'light' : 'dark';
	}

</script>

<CitationsModal bind:show={showCitationModal} citation={selectedCitation} />
{#key message.id}
	<div
		class=" flex w-full message-{message.id}"
		id="message-{message.id}"
		dir={$settings.chatDirection}
	>
		<ProfileImage
			src={modelfiles[message.model]?.imageUrl ??
				($i18n.language === 'dg-DG' ? `/doge.png` : `${WEBUI_BASE_URL}/static/favicon.png`)}
		/>

		<div class="w-full overflow-hidden pl-1">
			<!-- {console.log("modelfiles", modelfiles, message)} -->
			<Name>
				{#if message.model in modelfiles}
					{modelfiles[message.model]?.title}
				{:else}
					{message.model ? ` ${formatModelName(message.model)}` : ''}
				{/if}
				{#if message.content == ''}
					<Thinking/>
				{:else}
					{#if message?.replytime && checkModelImage(message.model)}
						<span class="text-xs">{ $i18n.t("Last for {{ time }} seconds", {time:(message?.replytime - message?.timestamp) % 60}) }</span>
					{/if}	
				{/if}
				{#if message.timestamp}
					<span
						class=" self-center invisible group-hover:visible text-gray-400 text-xs font-medium uppercase"
					>
						{dayjs(message.timestamp * 1000).format($i18n.t('h:mm a'))}
					</span>
				{/if}
			</Name>

			{#if message.files}
				<div class="my-2.5 w-full flex overflow-x-auto gap-2 flex-wrap">
					{#each message.files as file}
						<div>
							{#if file.type === 'image'}
								<Image src={file.url} />
							{/if}
						</div>
					{/each}
				</div>
			{/if}
			<!-- 网络搜索 -->
			{#if message?.search}
				{#if message?.search_type == 'web'}
					<!-- 网站搜索 -->
					{#if message?.search_content?.web}
						<div class="flex flex-col w-full rounded-2xl bg-gray-100 dark:bg-gray-800 my-2">
							<div class="flex justify-between items-center h-[45px] p-4">
								<div class="flex flex-row items-center text-sm font-bold">
									<div class="flex items-center bg-gray-50 dark:bg-gray-600 rounded-full size-[2rem] p-1.5">
										<svg
                      xmlns="http://www.w3.org/2000/svg"
                      viewBox="0 0 1024 1024"
                      class="w-[1rem] h-[1rem]" 
                      fill="#D0A870">
                      <path d="M512 0a512 512 0 0 0-512 512c0 136.768 53.248 265.344 149.952 362.048C243.712 967.68 392.512 1024 510.336 1024c12.672 0 47.616-1.536 70.144-4.544a40.576 40.576 0 0 0 35.2-43.968 40 40 0 0 0-45.12-35.456 432.96 432.96 0 0 1-20.608 2.304V88.32c70.656 29.184 133.376 133.44 160.128 273.216a40 40 0 0 0 78.592-15.04c-16.512-86.272-45.376-162.048-83.968-220.992a432.448 432.448 0 0 1 239.232 385.472c1.984 53.952 77.44 54.656 80 1.024V512A511.936 511.936 0 0 0 512 0zM313.216 128.512c-60.544 97.024-89.6 210.752-96.384 343.488h-135.04a432.832 432.832 0 0 1 231.424-343.488zM81.92 552h135.04c6.72 132.8 35.84 246.4 96.32 343.488A432.832 432.832 0 0 1 81.92 552z m388.096 383.616c-119.488-57.92-165.504-240.832-173.056-383.616h173.056v383.616z m0-463.616H296.96c7.552-142.592 53.568-325.76 173.056-383.616v383.616z m547.84 293.504a80 80 0 0 1-73.28 50.496h-36.992l72.448 150.656a40 40 0 1 1-72.064 34.624l-100.032-208a40 40 0 0 1 36.032-57.28h99.392a3.072 3.072 0 0 0 0.64-1.728l-210.816-190.144a1.28 1.28 0 0 0-0.192-0.128c-0.192 0-0.704 0.192-0.96 0.448v298.816c0 1.088 1.664 2.432 2.56 2.752 52.672 2.752 52.096 77.952-0.576 80h-0.256a83.712 83.712 0 0 1-81.728-82.752V544.768c0-31.68 17.856-59.712 46.656-73.088 28.8-13.44 61.888-9.088 86.272 11.392l216.896 195.84c22.144 23.36 28.224 56.576 16 86.592z"/>
                    </svg>
									</div>
									<div class="flex flex-col ml-1">
										<span class="text-sm">{ $i18n.t("Web Search") }</span>
										<span class="text-xs"> {message?.search_content?.web.length} Results</span>
									</div>
								</div>
								<button on:click={() => {
									handleWebHidden();
								}}>
									<svg 
										xmlns="http://www.w3.org/2000/svg"
										viewBox="0 0 15 15"
										width="15" height="15"  
										fill="currentColor"  
										class="h-4 w-4 shrink-0 text-muted-foreground transition-transform duration-200 { webShow ? 'rotate-180' : 'rotate-0'}">
										<path d="M3.13523 6.15803C3.3241 5.95657 3.64052 5.94637 3.84197 6.13523L7.5 9.56464L11.158 6.13523C11.3595 5.94637 11.6759 5.95657 11.8648 6.15803C12.0536 6.35949 12.0434 6.67591 11.842 6.86477L7.84197 10.6148C7.64964 10.7951 7.35036 10.7951 7.15803 10.6148L3.15803 6.86477C2.95657 6.67591 2.94637 6.35949 3.13523 6.15803Z" fill-rule="evenodd" clip-rule="evenodd"/>
									</svg>
								</button>
							</div>	
							<div class="w-full transition ease-in-out delay-150 overflow-x-auto {webShow ? 'h-0' : 'h-auto'}">
								<div class="flex flex-row px-4 mr-2">
									{#each message?.search_content?.web ?? [] as item}
										<div class="flex flex-col rounded-2xl bg-white dark:bg-black mx-2 mb-4 p-4">
											<div class="flex flex-row">
												<div class="w-9 h-9 rounded-lg bg-neutral-100 dark:bg-neutral-800 flex items-center justify-center overflow-hidden">
													<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="currentColor" class="w-[1.2rem] h-[1.2rem] s-Fb8Dy0t5csK5">
														<path d="M8.75 3.75a.75.75 0 0 0-1.5 0v3.5h-3.5a.75.75 0 0 0 0 1.5h3.5v3.5a.75.75 0 0 0 1.5 0v-3.5h3.5a.75.75 0 0 0 0-1.5h-3.5v-3.5Z" class="s-Fb8Dy0t5csK5"></path>
													</svg>
												</div>
												<div class="ml-2">
													<div class="w-[300px] text-sm font-bold line-clamp-1 text-ellipsis">{@html highlightedText(item.title, message?.search_content?.keyword??"")}</div>
													<div class="flex flex-row items-center w-[300px] text-xs">
														<a class="flex-start text-gray-500 font-bold line-clamp-1 text-ellipsis max-w-[200px]" href="{item.url}" target="_blank">{item.url}</a>
														<svg 
															xmlns="http://www.w3.org/2000/svg" 
															width="55" 
															height="55" 
															viewBox="0 0 24 24" 
															fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" 
															class="lucide lucide-external-link h-3 w-3 ml-2">
															<path d="M15 3h6v6"></path><path d="M10 14 21 3"/>
															<path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>
														</svg>
													</div>
												</div>
											</div>
											<div class="text-xs text-gray-500 w-[300px] line-clamp-3 text-ellipsis mt-1">{@html highlightedText(item.content, message?.search_content?.keyword??"")}</div>
										</div>
									{/each}
								</div>
							</div>
							<!-- {:else}
								<div class="bg-white rounded-2xl mx-4 mb-4 p-2">
									<Skeleton />
								</div>			 -->	
						</div>
					{/if}
					<!-- 图片搜索 -->
					{#if message?.search_content?.images}
						<div class="flex flex-wrap mt-3">
							{#each message?.search_content?.images ?? [] as item}
								{#if item?.url}
									<div class="flex flex-col p-1 lg:w-1/5 w-1/3 aspect-square">
										<Image src={item.url} alt="Uploaded Image" className="object-cover object-center w-full aspect-square rounded-lg cursor-pointer"/>
									</div>
								{/if}
							{/each}
						</div>
					{/if}
				{/if}
				{#if message?.search_type == 'youtube'}
					<!-- youtube搜索 -->
					{#if message?.search_content?.videos}
						<div class="flex flex-col w-full rounded-xl bg-gray-100 dark:bg-gray-800 my-2">
							<div class="flex justify-between items-center p-4">
								<div class="flex flex-row items-center text-sm font-bold">
									<div class="flex items-center bg-gray-50 dark:bg-gray-600 rounded-full size-[2rem] p-1.5">
										<svg
                      xmlns="http://www.w3.org/2000/svg"
                      viewBox="0 0 1024 1024"
                      class="w-[1rem] h-[1rem]" 
                      fill="#D0A870">
                      	<path d="M759.466667 187.349333c-55.765333-3.797333-145.493333-6.016-246.272-6.016-99.456 0-191.744 2.261333-246.869334 6.016-178.645333 12.202667-179.285333 156.928-180.096 324.864 0.810667 167.509333 1.450667 312.192 180.138667 324.48 55.253333 3.712 147.669333 5.973333 247.210667 5.973334h0.042666c100.650667 0 190.250667-2.176 245.888-5.973334 178.645333-12.245333 179.285333-156.970667 180.096-324.906666-0.853333-167.552-1.536-312.277333-180.138666-324.437334z m-5.845334 564.181334c-52.949333 3.626667-142.72 5.802667-240.042666 5.802666h-0.042667c-97.706667 0-187.989333-2.176-241.408-5.802666-79.36-5.461333-99.626667-29.696-100.565333-239.317334 0.938667-210.048 21.205333-234.325333 100.565333-239.701333 53.290667-3.669333 143.402667-5.845333 241.024-5.845333 97.450667 0 187.349333 2.176 240.469333 5.845333 79.36 5.376 99.626667 29.610667 100.565334 239.274667-0.938667 210.090667-21.205333 234.325333-100.565334 239.744z"/>
                        <path d="M416.896 640l256-128.256-256-127.744z"/>
                    </svg>
									</div>
									<div class="flex flex-col ml-1">
										<span class="text-sm">{ $i18n.t("YouTube Search") }</span>
										<span class="text-xs"> {message?.search_content?.videos.length} videos</span>
									</div>
								</div>
								<button on:click={() => {
									handleWebHidden();
								}}>
									<svg 
										xmlns="http://www.w3.org/2000/svg"
										viewBox="0 0 15 15"
										width="15" height="15"  
										fill="currentColor"  
										class="h-4 w-4 shrink-0 text-muted-foreground transition-transform duration-200 { webShow ? 'rotate-180' : 'rotate-0'}">
										<path d="M3.13523 6.15803C3.3241 5.95657 3.64052 5.94637 3.84197 6.13523L7.5 9.56464L11.158 6.13523C11.3595 5.94637 11.6759 5.95657 11.8648 6.15803C12.0536 6.35949 12.0434 6.67591 11.842 6.86477L7.84197 10.6148C7.64964 10.7951 7.35036 10.7951 7.15803 10.6148L3.15803 6.86477C2.95657 6.67591 2.94637 6.35949 3.13523 6.15803Z" fill-rule="evenodd" clip-rule="evenodd"/>
									</svg>
								</button>
							</div>	
							<div class="w-full transition ease-in-out delay-150 overflow-x-auto {webShow ? 'h-0' : 'h-auto'}">
								<div class="flex flex-row px-4 mr-2">
									{#each message?.search_content?.videos ?? [] as item}
										<div class="flex flex-col rounded-xl bg-white dark:bg-black mx-2 mb-4 pb-2">
											<a class="flex flex-col w-[230px]" href="{item.video_url}" target="_blank">
												<img class="rounded-t-xl drag-none" src={item.thumbnail_url} alt=""/>
												<div class="px-3 py-2">
													<span class="line-clamp-2 text-ellipsis">{item.title}</span>
													<div class="flex flex-row items-center mt-1">
														<div class="w-[20px]">
															<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-user-round h-4 w-4 text-red-500">
																<circle cx="12" cy="8" r="5"></circle>
																<path d="M20 21a8 8 0 0 0-16 0"></path>
															</svg>
														</div>
														<span class="ml-1 line-clamp-1 text-ellipsis text-sm">{item.channel_title}</span>
													</div>
												</div>
											</a>
										</div>
									{/each}
								</div>
							</div>
						</div>
					{/if}
				{/if}
				{#if message?.search_type == 'twitter'}
					<!-- twitter搜索 -->
					{#if message?.search_content?.content}
						<div class="flex flex-col w-full rounded-xl bg-gray-100 dark:bg-gray-800 my-2">
							<div class="flex justify-between items-center p-4">
								<div class="flex flex-row items-center text-sm font-bold">
									<div class="flex items-center bg-gray-50 dark:bg-gray-600 rounded-full size-[2rem] p-1.5">
										<svg
											xmlns="http://www.w3.org/2000/svg"
											viewBox="0 0 1024 1024"
											class="w-[1.5rem] h-[1.5rem]" 
											fill="#D0A870">
											<path d="M761.759375 122h132.320625L605 452.4003125 945.08 902H678.8L470.24 629.3196875 231.599375 902H99.2l309.1996875-353.4L82.16 122h273.0403125l188.52 249.24z m-46.4390625 700.8h73.32L315.359375 197.0403125h-78.680625z"/>
										</svg>
									</div>
									<div class="flex flex-col ml-1">
										<span class="text-sm">{ $i18n.t("Twitter Search") }</span>
										<span class="text-xs"> {message?.search_content?.content.length} tweets</span>
									</div>
								</div>
								<button on:click={() => {
									handleWebHidden();
								}}>
									<svg 
										xmlns="http://www.w3.org/2000/svg"
										viewBox="0 0 15 15"
										width="15" height="15"  
										fill="currentColor"  
										class="h-4 w-4 shrink-0 text-muted-foreground transition-transform duration-200 { webShow ? 'rotate-180' : 'rotate-0'}">
										<path d="M3.13523 6.15803C3.3241 5.95657 3.64052 5.94637 3.84197 6.13523L7.5 9.56464L11.158 6.13523C11.3595 5.94637 11.6759 5.95657 11.8648 6.15803C12.0536 6.35949 12.0434 6.67591 11.842 6.86477L7.84197 10.6148C7.64964 10.7951 7.35036 10.7951 7.15803 10.6148L3.15803 6.86477C2.95657 6.67591 2.94637 6.35949 3.13523 6.15803Z" fill-rule="evenodd" clip-rule="evenodd"/>
									</svg>
								</button>
							</div>	
							<div class="w-full transition ease-in-out delay-150 overflow-x-auto overflow-y-hidden {webShow ? 'h-0' : 'h-auto'}">
								<div class="flex flex-row px-4 mr-2">
									{#each message?.search_content?.content ?? [] as item}
										<!-- 带自定义选项 -->
										 	<div class="mr-1 h-[300px]">
												<TwitterEmbed tweetId="{item.id_str}" theme={currentTheme} isTwitterScriptLoaded={isTwitterScriptLoaded}/>
										 	</div>
									{/each}
								</div>
							</div>
						</div>
					{/if}
				{/if}
			{/if}
			
			<!-- 文本输出 -->
			<div
					class="prose chat-{message.role} w-full max-w-full dark:prose-invert prose-headings:my-0 prose-p:m-0 prose-p:-mb-6 prose-pre:my-0 prose-table:my-0 prose-blockquote:my-0 prose-img:my-0 prose-ul:-my-4 prose-ol:-my-4 prose-li:-my-3 prose-ul:-mb-6 prose-ol:-mb-8 prose-ol:p-0 prose-li:-mb-4 whitespace-pre-line"
				>
				<div>
					{#if edit === true}
						<div class="w-full bg-gray-50 dark:bg-gray-800 rounded-3xl px-5 py-3 my-2">
							<textarea
								id="message-edit-{message.id}"
								bind:this={editTextAreaElement}
								class=" bg-transparent outline-none w-full resize-none"
								bind:value={editedContent}
								on:input={(e) => {
									e.target.style.height = '';
									e.target.style.height = `${e.target.scrollHeight}px`;
								}}
							/>

							<div class=" mt-2 mb-1 flex justify-end space-x-1.5 text-sm font-medium">
								<button
									id="close-edit-message-button"
									class=" px-4 py-2 bg-gray-900 hover:bg-gray-850 text-gray-100 transition rounded-3xl"
									on:click={() => {
										cancelEditMessage();
									}}
								>
									{$i18n.t('Cancel')}
								</button>

								<button
									id="save-edit-message-button"
									class="px-4 py-2 bg-white hover:bg-gray-100 text-gray-800 transition rounded-3xl"
									on:click={() => {
										editMessageConfirmHandler();
									}}
								>
									{$i18n.t('Save')}
								</button>
							</div>
						</div>
					{:else}
						<div class="w-full">
							{#if message?.error === true}
								<div
									class="flex mt-2 mb-4 space-x-2 border px-4 py-3 border-red-800 bg-red-800/30 font-medium rounded-lg"
								>
									<svg
										xmlns="http://www.w3.org/2000/svg"
										fill="none"
										viewBox="0 0 24 24"
										stroke-width="1.5"
										stroke="currentColor"
										class="w-5 h-5 self-center"
									>
										<path
											stroke-linecap="round"
											stroke-linejoin="round"
											d="M12 9v3.75m9-.75a9 9 0 11-18 0 9 9 0 0118 0zm-9 3.75h.008v.008H12v-.008z"
										/>
									</svg>

									<div class=" self-center">
										{message.content}
									</div>
								</div>
							{:else if message.content === ''}
								<Skeleton />
							{:else}
								{#each tokens as token, tokenIdx}
									{#if token.type === 'thinking'}
										<button class="flex"
											on:click={() => {
											  thinkHiden = !thinkHiden;
											}}>
											{#if message.done}
												<div class="flex flex-wrap">
													<span class="flex-start">{ $i18n.t("have thought deeply") } </span>
													<span class="flex-start">({ $i18n.t("Last for {{ time }} seconds", {time:(message?.replytime - message?.timestamp) % 60}) })</span>
												</div>
											{:else}
												<span>{ $i18n.t("thinking...") }</span>
											{/if}
											<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" 
												class=" self-center ml-2 size-5 transition duration-150 {thinkHiden ? 'rotate-180' : ''}">
												<path stroke-linecap="round" stroke-linejoin="round" d="m19.5 8.25-7.5 7.5-7.5-7.5"></path>
											</svg>
										</button>
										<div class="border-l-2 border-slate-200 pl-3 my-2 transition duration-150 {thinkHiden?'hidden':''}">
											{@html marked.parse(token.raw, {
												...defaults,
												gfm: true,
												breaks: true,
												renderer
											})}
										</div>	
									{:else if token.type === 'code'}
										<CodeBlock
											id={`${message.id}-${tokenIdx}`}
											lang={token.lang}
											code={revertSanitizedResponseContent(token.text)}
										/>
									{:else}
										{@html marked.parse(token.raw, {
											...defaults,
											gfm: true,
											breaks: true,
											renderer
										})}
									{/if}
								{/each}
							{/if}

							{#if message.citations}
								<div class="mt-1 mb-2 w-full flex gap-1 items-center">
									{#each message.citations.reduce((acc, citation) => {
										citation.document.forEach((document, index) => {
											const metadata = citation.metadata?.[index];
											const id = metadata?.source ?? 'N/A';

											const existingSource = acc.find((item) => item.id === id);

											if (existingSource) {
												existingSource.document.push(document);
												existingSource.metadata.push(metadata);
											} else {
												acc.push( { id: id, source: citation?.source, document: [document], metadata: metadata ? [metadata] : [] } );
											}
										});
										return acc;
									}, []) as citation, idx}
										<div class="flex gap-1 text-xs font-semibold">
											<button
												class="flex dark:text-gray-300 py-1 px-1 bg-gray-50 hover:bg-gray-100 dark:bg-gray-850 dark:hover:bg-gray-800 transition rounded-xl"
												on:click={() => {
													showCitationModal = true;
													selectedCitation = citation;
												}}
											>
												<div class="bg-white dark:bg-gray-700 rounded-full size-4">
													{idx + 1}
												</div>
												<div class="flex-1 mx-2 line-clamp-1">
													{citation.source.name}
												</div>
											</button>
										</div>
									{/each}
								</div>
							{/if}

							{#if message.done || siblings.length > 1}
								<div
									class=" flex flex-col overflow-x-auto buttons text-gray-600 dark:text-gray-500"
								>
									{#if siblings.length > 1}
										<div class="flex justify-start min-w-fit mr-4" dir="ltr">
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
												class="text-sm tracking-widest font-semibold self-center dark:text-gray-100 min-w-fit"
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
											{#if message.done}
												<div class="truncate">{ $i18n.t("Generated by") } {siblings.length} {siblings.length > 1 ? 'LLMs' : 'LLM'}</div>
											{:else}
												<div class="truncate">{ $i18n.t("Generating by") } {siblings.length} {siblings.length > 1 ? 'LLMs' : 'LLM'}</div>
											{/if}
										</div>
									{/if}

									{#if message.done}
										<div class="flex justify-start min-w-fit mr-4">
											{#if !readOnly}
												<Tooltip content={$i18n.t('Edit')} placement="bottom">
													<button
														class="{isLastMessage
															? 'visible'
															: 'invisible group-hover:visible'} p-1.5 hover:bg-black/5 dark:hover:bg-white/5 rounded-lg dark:hover:text-white hover:text-black transition"
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

											<Tooltip content={$i18n.t('Copy')} placement="bottom">
												<button
													class="{isLastMessage
														? 'visible'
														: 'invisible group-hover:visible'} p-1.5 hover:bg-black/5 dark:hover:bg-white/5 rounded-lg dark:hover:text-white hover:text-black transition copy-response-button"
													on:click={() => {
														copyToClipboard(message.content, true);
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

											<Tooltip content={$i18n.t('Read Aloud')} placement="bottom">
												<button
													id="speak-button-{message.id}"
													class="{isLastMessage
														? 'visible'
														: 'invisible group-hover:visible'} p-1.5 hover:bg-black/5 dark:hover:bg-white/5 rounded-lg dark:hover:text-white hover:text-black transition"
													on:click={() => {
														if (!loadingSpeech) {
															toggleSpeakMessage(message);
														}
													}}
												>
													{#if loadingSpeech}
														<svg
															class=" w-4 h-4"
															fill="currentColor"
															viewBox="0 0 24 24"
															xmlns="http://www.w3.org/2000/svg"
															><style>
																.spinner_S1WN {
																	animation: spinner_MGfb 0.8s linear infinite;
																	animation-delay: -0.8s;
																}
																.spinner_Km9P {
																	animation-delay: -0.65s;
																}
																.spinner_JApP {
																	animation-delay: -0.5s;
																}
																@keyframes spinner_MGfb {
																	93.75%,
																	100% {
																		opacity: 0.2;
																	}
																}
															</style><circle class="spinner_S1WN" cx="4" cy="12" r="3" /><circle
																class="spinner_S1WN spinner_Km9P"
																cx="12"
																cy="12"
																r="3"
															/><circle
																class="spinner_S1WN spinner_JApP"
																cx="20"
																cy="12"
																r="3"
															/></svg
														>
													{:else if speaking}
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
																d="M17.25 9.75 19.5 12m0 0 2.25 2.25M19.5 12l2.25-2.25M19.5 12l-2.25 2.25m-10.5-6 4.72-4.72a.75.75 0 0 1 1.28.53v15.88a.75.75 0 0 1-1.28.53l-4.72-4.72H4.51c-.88 0-1.704-.507-1.938-1.354A9.009 9.009 0 0 1 2.25 12c0-.83.112-1.633.322-2.396C2.806 8.756 3.63 8.25 4.51 8.25H6.75Z"
															/>
														</svg>
													{:else}
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
																d="M19.114 5.636a9 9 0 010 12.728M16.463 8.288a5.25 5.25 0 010 7.424M6.75 8.25l4.72-4.72a.75.75 0 011.28.53v15.88a.75.75 0 01-1.28.53l-4.72-4.72H4.51c-.88 0-1.704-.507-1.938-1.354A9.01 9.01 0 012.25 12c0-.83.112-1.633.322-2.396C2.806 8.756 3.63 8.25 4.51 8.25H6.75z"
															/>
														</svg>
													{/if}
												</button>
											</Tooltip>

											{#if $config.images && !readOnly}
												<Tooltip content="Generate Image" placement="bottom">
													<button
														class="{isLastMessage
															? 'visible'
															: 'invisible group-hover:visible'}  p-1.5 hover:bg-black/5 dark:hover:bg-white/5 rounded-lg dark:hover:text-white hover:text-black transition"
														on:click={() => {
															if (!generatingImage) {
																generateImage(message);
															}
														}}
													>
														{#if generatingImage}
															<svg
																class=" w-4 h-4"
																fill="currentColor"
																viewBox="0 0 24 24"
																xmlns="http://www.w3.org/2000/svg"
																><style>
																	.spinner_S1WN {
																		animation: spinner_MGfb 0.8s linear infinite;
																		animation-delay: -0.8s;
																	}
																	.spinner_Km9P {
																		animation-delay: -0.65s;
																	}
																	.spinner_JApP {
																		animation-delay: -0.5s;
																	}
																	@keyframes spinner_MGfb {
																		93.75%,
																		100% {
																			opacity: 0.2;
																		}
																	}
																</style><circle class="spinner_S1WN" cx="4" cy="12" r="3" /><circle
																	class="spinner_S1WN spinner_Km9P"
																	cx="12"
																	cy="12"
																	r="3"
																/><circle
																	class="spinner_S1WN spinner_JApP"
																	cx="20"
																	cy="12"
																	r="3"
																/></svg
															>
														{:else}
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
																	d="m2.25 15.75 5.159-5.159a2.25 2.25 0 0 1 3.182 0l5.159 5.159m-1.5-1.5 1.409-1.409a2.25 2.25 0 0 1 3.182 0l2.909 2.909m-18 3.75h16.5a1.5 1.5 0 0 0 1.5-1.5V6a1.5 1.5 0 0 0-1.5-1.5H3.75A1.5 1.5 0 0 0 2.25 6v12a1.5 1.5 0 0 0 1.5 1.5Zm10.5-11.25h.008v.008h-.008V8.25Zm.375 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Z"
																/>
															</svg>
														{/if}
													</button>
												</Tooltip>
											{/if}

											{#if message.info}
												<Tooltip content={$i18n.t('Generation Info')} placement="bottom">
													<button
														class=" {isLastMessage
															? 'visible'
															: 'invisible group-hover:visible'} p-1.5 hover:bg-black/5 dark:hover:bg-white/5 rounded-lg dark:hover:text-white hover:text-black transition whitespace-pre-wrap"
														on:click={() => {
															console.log(message);
														}}
														id="info-{message.id}"
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
																d="M11.25 11.25l.041-.02a.75.75 0 011.063.852l-.708 2.836a.75.75 0 001.063.853l.041-.021M21 12a9 9 0 11-18 0 9 9 0 0118 0zm-9-3.75h.008v.008H12V8.25z"
															/>
														</svg>
													</button>
												</Tooltip>
											{/if}

											{#if !readOnly}
												<Tooltip content={$i18n.t('Good Response')} placement="bottom">
													<button
														class="{isLastMessage
															? 'visible'
															: 'invisible group-hover:visible'} p-1.5 hover:bg-black/5 dark:hover:bg-white/5 rounded-lg {message
															?.annotation?.rating === 1
															? 'bg-gray-100 dark:bg-gray-800'
															: ''} dark:hover:text-white hover:text-black transition"
														on:click={() => {
															rateMessage(message.id, 1);
															showRateComment = true;

															window.setTimeout(() => {
																document
																	.getElementById(`message-feedback-${message.id}`)
																	?.scrollIntoView();
															}, 0);
														}}
													>
														<svg
															stroke="currentColor"
															fill="none"
															stroke-width="2.3"
															viewBox="0 0 24 24"
															stroke-linecap="round"
															stroke-linejoin="round"
															class="w-4 h-4"
															xmlns="http://www.w3.org/2000/svg"
															><path
																d="M14 9V5a3 3 0 0 0-3-3l-4 9v11h11.28a2 2 0 0 0 2-1.7l1.38-9a2 2 0 0 0-2-2.3zM7 22H4a2 2 0 0 1-2-2v-7a2 2 0 0 1 2-2h3"
															/></svg
														>
													</button>
												</Tooltip>

												<Tooltip content={$i18n.t('Bad Response')} placement="bottom">
													<button
														class="{isLastMessage
															? 'visible'
															: 'invisible group-hover:visible'} p-1.5 hover:bg-black/5 dark:hover:bg-white/5 rounded-lg {message
															?.annotation?.rating === -1
															? 'bg-gray-100 dark:bg-gray-800'
															: ''} dark:hover:text-white hover:text-black transition"
														on:click={() => {
															rateMessage(message.id, -1);
															showRateComment = true;
															window.setTimeout(() => {
																document
																	.getElementById(`message-feedback-${message.id}`)
																	?.scrollIntoView();
															}, 0);
														}}
													>
														<svg
															stroke="currentColor"
															fill="none"
															stroke-width="2.3"
															viewBox="0 0 24 24"
															stroke-linecap="round"
															stroke-linejoin="round"
															class="w-4 h-4"
															xmlns="http://www.w3.org/2000/svg"
															><path
																d="M10 15v4a3 3 0 0 0 3 3l4-9V2H5.72a2 2 0 0 0-2 1.7l-1.38 9a2 2 0 0 0 2 2.3zm7-13h2.67A2.31 2.31 0 0 1 22 4v7a2.31 2.31 0 0 1-2.33 2H17"
															/></svg
														>
													</button>
												</Tooltip>
											{/if}

											{#if isLastMessage && !readOnly}
												<Tooltip content={$i18n.t('Continue Response')} placement="bottom">
													<button
														type="button"
														class="{isLastMessage
															? 'visible'
															: 'invisible group-hover:visible'} p-1.5 hover:bg-black/5 dark:hover:bg-white/5 rounded-lg dark:hover:text-white hover:text-black transition regenerate-response-button"
														on:click={() => {
															continueGeneration();
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
																d="M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z"
															/>
															<path
																stroke-linecap="round"
																stroke-linejoin="round"
																d="M15.91 11.672a.375.375 0 0 1 0 .656l-5.603 3.113a.375.375 0 0 1-.557-.328V8.887c0-.286.307-.466.557-.327l5.603 3.112Z"
															/>
														</svg>
													</button>
												</Tooltip>

												<Tooltip content={$i18n.t('Regenerate')} placement="bottom">
													<button
														type="button"
														class="{isLastMessage
															? 'visible'
															: 'invisible group-hover:visible'} p-1.5 hover:bg-black/5 dark:hover:bg-white/5 rounded-lg dark:hover:text-white hover:text-black transition regenerate-response-button"
														on:click={() => {
															regenerateResponse(message);
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
																d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0l3.181 3.183a8.25 8.25 0 0013.803-3.7M4.031 9.865a8.25 8.25 0 0113.803-3.7l3.181 3.182m0-4.991v4.99"
															/>
														</svg>
													</button>
												</Tooltip>
											{/if}
										</div>
									{/if}
								</div>
							{/if}

							{#if message.done && showRateComment}
								<RateComment
									messageId={message.id}
									bind:show={showRateComment}
									bind:message
									on:submit={() => {
										updateChatMessages();
									}}
								/>
							{/if}
						</div>
					{/if}
				</div>
			</div>
		</div>
	</div>
{/key}

<style>
	.buttons::-webkit-scrollbar {
		display: none; /* for Chrome, Safari and Opera */
	}

	.buttons {
		-ms-overflow-style: none; /* IE and Edge */
		scrollbar-width: none; /* Firefox */
	}

	.drag-none {
    -webkit-user-drag: none;
    -moz-user-drag: none;
    -ms-user-drag: none;
    user-drag: none;
  }
</style>
