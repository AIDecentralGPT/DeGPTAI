<script lang="ts">
	import { v4 as uuidv4 } from 'uuid';

	import { chats, config, modelfiles, models, settings, user as _user, mobile, deApiBaseUrl, toolflag } from '$lib/stores';
	import { tick, getContext } from 'svelte';

	import { toast } from 'svelte-sonner';
	import { getChatList, updateChatById, conversationRefresh } from '$lib/apis/chats';

	import UserMessage from './Messages/UserMessage.svelte';
	import ResponseMessage from './Messages/ResponseMessage.svelte';
	import Placeholder from './Messages/Placeholder.svelte';
	import Spinner from '../common/Spinner.svelte';
	import { imageGenerations } from '$lib/apis/images';
	import { copyToClipboard, findWordIndices } from '$lib/utils';
	import CompareMessages from './Messages/CompareMessages.svelte';
	import { stringify } from 'postcss';
	import { thirdSearch, getWebContent } from "$lib/apis/thirdsearch";
	import { generateSearchKeyword } from "$lib/apis/de";

	const i18n = getContext('i18n');

	export let chatId = '';
	export let readOnly = false;
	export let sendPrompt: Function;
	export let continueGeneration: Function;
	export let regenerateResponse: Function;

	export let user = $_user;
	export let prompt;
	export let suggestionPrompts = [];
	export let processing = '';
	export let bottomPadding = false;
	export let autoScroll;
	export let history = {};
	export let messages = [];
	export let chatInputPlaceholder = "";

	export let selectedModels;
	export let selectedModelfiles = [];

	$: if (autoScroll && bottomPadding) {
		(async () => {
			await tick();
			scrollToBottom();
		})();
	}

	const scrollToBottom = () => {
		const element = document.getElementById('messages-container');
		element.scrollTop = element.scrollHeight;
	};

	const copyToClipboardWithToast = async (text, isMarkdown) => {
		const res = await copyToClipboard(text, isMarkdown);
		if (res) {
			toast.success($i18n.t('Copying to clipboard was successful!'));
		}
	};

	// 用于判断是否是网络搜索需要重新赋值
	const toolTypes = ["bing", "twitter", "youtube"];

	const confirmEditMessage = async (messageId, content) => {
		let userPrompt = content;
		let userMessageId = uuidv4();

		let userMessage = {
			id: userMessageId,
			parentId: history.messages[messageId].parentId,
			childrenIds: [],
			role: 'user',
			content: userPrompt,
			...(history.messages[messageId].files && { files: history.messages[messageId].files }),
			...(history.messages[messageId].toolflag && { toolflag: history.messages[messageId].toolflag }),
			...(history.messages[messageId].tooltype && { tooltype: history.messages[messageId].tooltype }),
			...(history.messages[messageId].toolInfo && { toolInfo: history.messages[messageId].toolInfo }),
			...(history.messages[messageId].parseInfo && { parseInfo: history.messages[messageId].parseInfo }),
			models: selectedModels.filter((m, mIdx) => selectedModels.indexOf(m) === mIdx)
		};

		let messageParentId = history.messages[messageId].parentId;

		if (messageParentId !== null) {
			history.messages[messageParentId].childrenIds = [
				...history.messages[messageParentId].childrenIds,
				userMessageId
			];
		}

		history.messages[userMessageId] = userMessage;
		history.currentId = userMessageId;

		// Create Simulate ResopnseMessage
		let responseMap: any = {};
		userMessage?.models.forEach(async (modelId:string) => {
      const model = $models.filter((m) => m.id === modelId).at(0);
      if (model) {
        // Create response message
        let responseMessageId = uuidv4();
        let responseMessage = {
          parentId: userMessageId,
          id: responseMessageId,
          toolflag: userMessage?.toolflag,
          tooltype: userMessage?.tooltype,
          parseInfo: toolTypes.includes(userMessage?.tooltype) ? "" : userMessage?.parseInfo,
          keyword: userPrompt,
          childrenIds: [],
          role: "assistant",
          content: "",
          think_content: "",
          model: modelId,
          userContext: null,
          timestamp: Math.floor(Date.now() / 1000), // Unix epoch
        };

        // Add message to history and Set currentId to messageId
        history.messages[responseMessageId] = responseMessage;
        history.currentId = responseMessageId;

        // Append messageId to childrenIds of parent message
        if (userMessageId !== null) {
          history.messages[userMessageId].childrenIds = [
            ...history.messages[userMessageId].childrenIds,
          	responseMessageId,
          ];
        }

        responseMap[modelId] = responseMessage;
      }
    });

		// 校验模型已使用次数
    let modelLimit = {}
		const {passed, data} = await conversationRefresh(localStorage.token, selectedModels[0]);
    if (passed) {
      for (const item of selectedModels) {
        data.forEach((dItem:any) => {
          if(dItem.model == item) {
            if (!dItem.passed) {
              modelLimit[dItem.model] = dItem.message;
            }
          }
      	}) 
    	}
    }

		// 获取网络搜索内容
		if (userMessage?.toolflag) {
			if (userMessage?.tooltype && toolTypes.includes(userMessage?.tooltype)) {

				let response = await handleSearchWeb(userPrompt, userMessage?.tooltype);
				
				// 更新回复解析内容
				userMessage?.models.forEach(async (modelId: string) => {
					// 如果已创建信息赋值web数据
					if (responseMap[modelId]) {
						let responseMessageId = responseMap[modelId].id;
						let responseMessage = responseMap[modelId];
						responseMessage.parseInfo = response;
						history.messages[responseMessageId] = responseMessage;
					}
				});

				// 更新提问解析内容
				userMessage = {
					...userMessage,
					parseInfo: response
				}
				history.messages[userMessageId] = userMessage;
			}
      
      scrollToBottom();
    }

		await tick();
		await sendPrompt(userPrompt, responseMap, modelLimit);
	};

	const resentMessage = async (messageId) => {
		let userMessage = {
			...history.messages[messageId]
		};
		
		if (toolTypes.includes(userMessage?.tooltype)) {
			userMessage = {
				...userMessage,
				parseInfo: ""
			};
		}

		let userPrompt = userMessage?.content;

		// Create Simulate ResopnseMessage
		let responseMap: any = {};
		history.messages[messageId].childrenIds.forEach((responseMessageId: string) => {
			let responseMessage = history.messages[responseMessageId];
			responseMessage = {
				...responseMessage,
				parseInfo: "",
				error: false,
				content: "",
				done: false
			}
			history.messages[responseMessageId] = responseMessage;

			responseMap[responseMessage?.model] = responseMessage;
		});

		// 校验模型已使用次数
    let modelLimit = {}
		const {passed, data} = await conversationRefresh(localStorage.token, selectedModels[0]);
    if (passed) {
      for (const item of selectedModels) {
        data.forEach((dItem:any) => {
          if(dItem.model == item) {
            if (!dItem.passed) {
              modelLimit[dItem.model] = dItem.message;
            }
          }
      	}) 
    	}
    }

		// 获取网络搜索内容
		if (userMessage?.toolflag) {
			if (userMessage?.tooltype && toolTypes.includes(userMessage?.tooltype)) {

				let response = await handleSearchWeb(userPrompt, userMessage?.tooltype);
				
				// 更新回复解析内容
				userMessage?.models.forEach(async (modelId: string) => {
					// 如果已创建信息赋值web数据
					if (responseMap[modelId]) {
						let responseMessageId = responseMap[modelId].id;
						let responseMessage = responseMap[modelId];
						responseMessage.parseInfo = response;
						history.messages[responseMessageId] = responseMessage;
					}
				});

				// 更新提问解析内容
				userMessage = {
					...userMessage,
					parseInfo: response
				}
				history.messages[messageId] = userMessage;
			}
      
      scrollToBottom();
    }

		await tick();
		await sendPrompt(userPrompt, responseMap, modelLimit);
	};

	const updateChatMessages = async () => {
		await tick();
		await updateChatById(localStorage.token, chatId, {
			messages: messages,
			history: history
		});

		await chats.set(await getChatList(localStorage.token));
	};

	const confirmEditResponseMessage = async (messageId, content) => {
		history.messages[messageId].originalContent = history.messages[messageId].content;
		history.messages[messageId].content = content;

		await updateChatMessages();
	};

	const rateMessage = async (messageId, rating) => {
		history.messages[messageId].annotation = {
			...history.messages[messageId].annotation,
			rating: rating
		};

		await updateChatMessages();
	};

	const showPreviousMessage = async (message) => {
		if (message.parentId !== null) {
			let messageId =
				history.messages[message.parentId].childrenIds[
					Math.max(history.messages[message.parentId].childrenIds.indexOf(message.id) - 1, 0)
				];

			if (message.id !== messageId) {
				let messageChildrenIds = history.messages[messageId].childrenIds;

				while (messageChildrenIds.length !== 0) {
					messageId = messageChildrenIds.at(-1);
					messageChildrenIds = history.messages[messageId].childrenIds;
				}

				history.currentId = messageId;
			}
		} else {
			let childrenIds = Object.values(history.messages)
				.filter((message) => message.parentId === null)
				.map((message) => message.id);
			let messageId = childrenIds[Math.max(childrenIds.indexOf(message.id) - 1, 0)];

			if (message.id !== messageId) {
				let messageChildrenIds = history.messages[messageId].childrenIds;

				while (messageChildrenIds.length !== 0) {
					messageId = messageChildrenIds.at(-1);
					messageChildrenIds = history.messages[messageId].childrenIds;
				}

				history.currentId = messageId;
			}
		}

		await tick();

		const element = document.getElementById('messages-container');
		autoScroll = element.scrollHeight - element.scrollTop <= element.clientHeight + 50;

		setTimeout(() => {
			scrollToBottom();
		}, 100);
	};

	const showNextMessage = async (message) => {
		if (message.parentId !== null) {
			let messageId =
				history.messages[message.parentId].childrenIds[
					Math.min(
						history.messages[message.parentId].childrenIds.indexOf(message.id) + 1,
						history.messages[message.parentId].childrenIds.length - 1
					)
				];

			if (message.id !== messageId) {
				let messageChildrenIds = history.messages[messageId].childrenIds;

				while (messageChildrenIds.length !== 0) {
					messageId = messageChildrenIds.at(-1);
					messageChildrenIds = history.messages[messageId].childrenIds;
				}

				history.currentId = messageId;
			}
		} else {
			let childrenIds = Object.values(history.messages)
				.filter((message) => message.parentId === null)
				.map((message) => message.id);
			let messageId =
				childrenIds[Math.min(childrenIds.indexOf(message.id) + 1, childrenIds.length - 1)];

			if (message.id !== messageId) {
				let messageChildrenIds = history.messages[messageId].childrenIds;

				while (messageChildrenIds.length !== 0) {
					messageId = messageChildrenIds.at(-1);
					messageChildrenIds = history.messages[messageId].childrenIds;
				}

				history.currentId = messageId;
			}
		}

		await tick();

		const element = document.getElementById('messages-container');
		autoScroll = element.scrollHeight - element.scrollTop <= element.clientHeight + 50;

		setTimeout(() => {
			scrollToBottom();
		}, 100);
	};

	const messageDeleteHandler = async (messageId) => {
		const messageToDelete = history.messages[messageId];
		const messageParentId = messageToDelete.parentId;
		const messageChildrenIds = messageToDelete.childrenIds ?? [];
		const hasSibling = messageChildrenIds.some(
			(childId) => history.messages[childId]?.childrenIds?.length > 0
		);
		messageChildrenIds.forEach((childId) => {
			const child = history.messages[childId];
			if (child && child.childrenIds) {
				if (child.childrenIds.length === 0 && !hasSibling) {
					// if last prompt/response pair
					history.messages[messageParentId].childrenIds = [];
					history.currentId = messageParentId;
				} else {
					child.childrenIds.forEach((grandChildId) => {
						if (history.messages[grandChildId]) {
							history.messages[grandChildId].parentId = messageParentId;
							history.messages[messageParentId].childrenIds.push(grandChildId);
						}
					});
				}
			}
			// remove response
			history.messages[messageParentId].childrenIds = history.messages[
				messageParentId
			].childrenIds.filter((id) => id !== childId);
		});
		// remove prompt
		history.messages[messageParentId].childrenIds = history.messages[
			messageParentId
		].childrenIds.filter((id) => id !== messageId);
		await updateChatById(localStorage.token, chatId, {
			messages: messages,
			history: history
		});
	};

	// 获取搜索网页
  const handleSearchWeb= async(userPrompt: string, toolType: string) => {
    const ai_keyword = await generateSearchChatKeyword(userPrompt);
    let result = await thirdSearch(localStorage.token, ai_keyword, toolType);
    if (result?.ok) {
      return result.data;
    } else {
			return "";
		}
  }

	const generateSearchChatKeyword = async (userPrompt: string) => {
    if ($settings?.title?.auto ?? true) {
      // 获取关键词
      let send_messages = messages.filter(item => item.role == 'user')
        .map(item => {
					let custmessage = {role: item.role, content: item.content};
					if (item.files) {
						custmessage.content = [{"type": "text","text": item.content}];
						item.files.forEach((fitem:any) => {
              let url = fitem.url;
							custmessage.content.push({"type": "image_url", "image_url": {url}})
						})
					}
					return custmessage;
				});
      send_messages.push({
        role: "user",
        content: $i18n.t("Sort the above user questions in chronological order, filter out repetitive, guiding and valueless key words, obtain the last user question content and only output the user question content, with a maximum of 10 characters")
      });
      const title = await generateSearchKeyword(
				localStorage.token,
        send_messages,
        userPrompt,
        $deApiBaseUrl?.url
      );
      return title;
    } else {
      return `${userPrompt}`;
    }
  };
</script>

<div class="h-full flex mb-16">
	{#if messages.length == 0}
		<Placeholder
			models={selectedModels}
			modelfiles={selectedModelfiles}
			{suggestionPrompts}
			submitPrompt={async (p, idx) => {
				prompt = "";
				let text = p;
				if (p.includes('{{CLIPBOARD}}')) {
					const clipboardText = await navigator.clipboard.readText().catch((err) => {
						toast.error($i18n.t('Failed to read clipboard contents'));
						return '{{CLIPBOARD}}';
					});

					text = p.replaceAll('{{CLIPBOARD}}', clipboardText);
				}

				if (idx == 0) {
					chatInputPlaceholder = text;
				} else {
					prompt = text;
				}
				
				await tick();

				const chatInputElement = document.getElementById('chat-textarea');
				if (chatInputElement) {
					if (idx == 0) {
						chatInputPlaceholder = text;
					} else {
						prompt = text;
					}

					chatInputElement.style.height = '';
					chatInputElement.style.height = Math.min(chatInputElement.scrollHeight, 200) + 'px';
					chatInputElement.focus();

					const words = findWordIndices(prompt);

					if (words.length > 0) {
						const word = words.at(0);
						chatInputElement.setSelectionRange(word?.startIndex, word.endIndex + 1);
					}
				}
				
				await tick();
			}}
		/>
	{:else}
		<div class="w-full pt-2">
			{#key chatId}
				{#each messages as message, messageIdx}
					<div class=" w-full {messageIdx === messages.length - 1 ? ($toolflag ? 'pb-48' : 'pb-28') : ''}">
						<div
							class="flex flex-col justify-between px-6 md:px-20 mb-3 {$settings?.fullScreenMode ?? null
								? 'max-w-full'
								: 'max-w-full'} mx-auto rounded-lg group"
						>
							{#if message.role === 'user'}
								<UserMessage
									on:delete={() => messageDeleteHandler(message.id)}
									{user}
									{readOnly}
									{message}
									isFirstMessage={messageIdx === 0}
									siblings={message.parentId !== null
										? history.messages[message.parentId]?.childrenIds ?? []
										: Object.values(history.messages)
												.filter((message) => message.parentId === null)
												.map((message) => message.id) ?? []}
									{confirmEditMessage}
									{showPreviousMessage}
									{showNextMessage}
									copyToClipboard={copyToClipboardWithToast}
								/>
							{:else if $mobile || (history.messages[message.parentId]?.models?.length ?? 1) === 1}
								{#key message.id}
									<ResponseMessage
										{message}
										modelfiles={selectedModelfiles}
										siblings={history.messages[message.parentId]?.childrenIds ?? []}
										isLastMessage={messageIdx + 1 === messages.length}
										{readOnly}
										{resentMessage}
										{updateChatMessages}
										{confirmEditResponseMessage}
										{showPreviousMessage}
										{showNextMessage}
										{rateMessage}
										copyToClipboard={copyToClipboardWithToast}
										{continueGeneration}
										{regenerateResponse}
										on:save={async (e) => {
											console.log('save', e);
											const message = e.detail;
											history.messages[message.id] = message;
											await updateChatById(localStorage.token, chatId, {
												messages: messages,
												history: history
											});
										}}
									/>
								{/key}
							{:else}
								{#key message.parentId}
									<CompareMessages
										bind:history
										{messages}
										{chatId}
										parentMessage={history.messages[message.parentId]}
										{messageIdx}
										{selectedModelfiles}
										{updateChatMessages}
										{confirmEditResponseMessage}
										{rateMessage}
										copyToClipboard={copyToClipboardWithToast}
										{continueGeneration}
										{regenerateResponse}
										on:change={async () => {
											await updateChatById(localStorage.token, chatId, {
												messages: messages,
												history: history
											});
											if (autoScroll) {
												const element = document.getElementById('messages-container');
												autoScroll =
													element.scrollHeight - element.scrollTop <= element.clientHeight + 50;
												setTimeout(() => {
													scrollToBottom();
												}, 100);
											}
										}}
									/>
								{/key}
							{/if}
						</div>
					</div>
				{/each}

				{#if bottomPadding}
					<div class="pb-40" />
				{/if}
			{/key}
		</div>
	{/if}
</div>