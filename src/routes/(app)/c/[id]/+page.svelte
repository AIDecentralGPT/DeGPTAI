<script lang="ts">
	import { v4 as uuidv4 } from 'uuid';
	import { toast } from 'svelte-sonner';

	import { onMount, tick, getContext } from 'svelte';
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import {
		models,
		modelfiles,
		user,
		settings,
		chats,
		chatId,
		config,
		WEBUI_NAME,
		tags as _tags,
		showSidebar,
		deApiBaseUrl
	} from '$lib/stores';
	import { copyToClipboard, splitStream, convertMessagesToHistory, addTextSlowly } from '$lib/utils';

	import { generateChatCompletion, cancelOllamaRequest } from '$lib/apis/ollama';
	import { generateDeOpenAIChatCompletion, generateDeTitle, generateSearchKeyword } from '$lib/apis/de';
	import {
		addTagById,
		createNewChat,
		deleteTagById,
		getAllChatTags,
		getChatById,
		getChatList,
		getTagsById,
		updateChatById,
		conversationRefresh
	} from '$lib/apis/chats';
	import { generateOpenAIChatCompletion, generateTitle } from '$lib/apis/openai';

	import MessageInput from '$lib/components/chat/MessageInput.svelte';
	import Messages from '$lib/components/chat/Messages.svelte';
	import Navbar from '$lib/components/layout/Navbar.svelte';

	import {
		LITELLM_API_BASE_URL,
		OPENAI_API_BASE_URL,
		OLLAMA_API_BASE_URL,
		WEBUI_BASE_URL
	} from '$lib/constants';
	import { createOpenAITextStream } from '$lib/apis/streaming';
	import { queryMemory } from '$lib/apis/memories';
	import { thirdSearch } from "$lib/apis/thirdsearch"

	const i18n = getContext('i18n');

	let loaded = false;

	let stopResponseFlag = false;
	let autoScroll = true;
	let processing = '';
	let messagesContainerElement: HTMLDivElement;
	let currentRequestId = null;

	// let chatId = $page.params.id;
	let showModelSelector = true;
	let selectedModels = [''];
	let atSelectedModel = '';

	let selectedModelfile = null;

	$: selectedModelfile =
		selectedModels.length === 1 &&
		$modelfiles.filter((modelfile) => modelfile.tagName === selectedModels[0]).length > 0
			? $modelfiles.filter((modelfile) => modelfile.tagName === selectedModels[0])[0]
			: null;

	let selectedModelfiles = {};
	$: selectedModelfiles = selectedModels.reduce((a, tagName, i, arr) => {
		const modelfile =
			$modelfiles.filter((modelfile) => modelfile.tagName === tagName)?.at(0) ?? undefined;

		return {
			...a,
			...(modelfile && { [tagName]: modelfile })
		};
	}, {});

	let chat = null;
	let tags = [];

	let title = '';
	let prompt = '';
	let files = [];
	let search = false;
	let search_type = "web";
	let messages = [];
	let history = {
		messages: {},
		currentId: null
	};
	let firstResAlready = false // The first response has already been received

	$: if (history.currentId !== null) {
		let _messages = [];

		let currentMessage = history.messages[history.currentId];
		while (currentMessage !== null) {
			_messages.unshift({ ...currentMessage });
			currentMessage =
				currentMessage.parentId !== null ? history.messages[currentMessage.parentId] : null;
		}

		
		// _messages.pop()
		// console.log("messages = _messages;", _messages);

		messages = _messages;
	} else {
		messages = [];
	}

	$: if ($page.params.id) {
		(async () => {
			if (await loadChat()) {
				await tick();
				loaded = true;

				window.setTimeout(() => scrollToBottom(), 0);
				// const chatInput = document.getElementById('chat-textarea');
				// chatInput?.focus();
			} else {
				await goto('/');
			}
		})();
	}

	//////////////////////////
	// Web functions
	//////////////////////////

	const loadChat = async () => {
		await chatId.set($page.params.id);
		chat = await getChatById(localStorage.token, $chatId).catch(async (error) => {
			await goto('/');
			return null;
		});

		if (chat) {
			tags = await getTags();
			const chatContent = chat.chat;

			if (chatContent) {
				console.log(chatContent);

				// selectedModels =
				// 	(chatContent?.models ?? undefined) !== undefined
				// 		? chatContent.models
				// 		: [chatContent.models ?? ''];
				selectedModels = $settings?.models;
				
				history =
					(chatContent?.history ?? undefined) !== undefined
						? chatContent.history
						: convertMessagesToHistory(chatContent.messages);
				title = chatContent.title;

				let _settings = JSON.parse(localStorage.getItem('settings') ?? '{}');
				await settings.set({
					..._settings,
					system: chatContent.system ?? _settings.system,
					options: chatContent.options ?? _settings.options
				});
				autoScroll = true;
				await tick();

				if (messages.length > 0) {
					history.messages[messages.at(-1).id].done = true;
				}
				await tick();

				return true;
			} else {
				return null;
			}
		}
	};

	const scrollToBottom = async () => {
		await tick();
		if (messagesContainerElement) {
			messagesContainerElement.scrollTop = messagesContainerElement.scrollHeight;
		}
	};

	//////////////////////////
	// Ollama functions
	//////////////////////////
let monitorLog = [];
// 2. Click the submit button to trigger the check
const submitPrompt = async (userPrompt, _user = null) => {
	console.log('submitPrompt', $chatId);
	console.log("Click", firstResAlready);
	monitorLog = [];
	monitorLog.push({fun: "start", time: new Date()});

	selectedModels = selectedModels.map((modelId) =>
    $models.map((m) => m.id).includes(modelId) ? modelId : ""
  );
    
  // Verify if the model supports file types
  if (files.length > 0) {
    let imageModels = $models.filter(item => item.support == "image");
    let checkSelectedModels = imageModels.filter(item => selectedModels.includes(item.model)).map(item => item.model);
    if (checkSelectedModels.length == 0) {
      toast.error($i18n.t("Not supported"));
      return;
    } else {
			selectedModels = checkSelectedModels;
		}
  }

  console.log("selectedModels", selectedModels);

	// If only one model is selected for online search reply
	if (search) {
    selectedModels = [selectedModels[0]];
  }
			
	firstResAlready = false // When starting a new conversation, also restore firstResAlready to its initial state of false
	await tick()

	if (selectedModels.includes('')) {
		toast.error($i18n.t('Model not selected'));
	} else 
	if (messages.length != 0 && messages.at(-1).done != true) {
		// Response not completed
		console.log('wait');
	} else if (
		files.length > 0 &&
		files.filter((file) => file.upload_status === false).length > 0
	) {
		// Upload incomplete
		toast.error(
			`Oops! Hold tight! Your files are still in the processing oven. We're cooking them up to perfection. Please be patient and we'll let you know once they're ready.`
		);
	} else {
		// Reset the height of the chat message text area
		document.getElementById('chat-textarea').style.height = '';

		// Create user message
		let userMessageId = uuidv4();
		let userMessage = {
			id: userMessageId,
			parentId: messages.length !== 0 ? messages.at(-1).id : null,
			childrenIds: [],
			role: 'user',
			user: _user ?? undefined,
			content: userPrompt,
			files: files.length > 0 ? files : undefined,
			timestamp: Math.floor(Date.now() / 1000), // Unix epoch
			models: selectedModels
		};

		// Add the message to the history and set the current ID to messageId
		history.messages[userMessageId] = userMessage;
		history.currentId = userMessageId;

		// Attach messageId to the childrenIds of the parent message
		if (messages.length !== 0) {
			history.messages[messages.at(-1).id].childrenIds.push(userMessageId);
		}

		// Create Simulate ResopnseMessage
		let responseMap: any = {};
    selectedModels.map(async (modelId) => {
      const model = $models.filter((m) => m.id === modelId).at(0);
      if (model) {
        // Create response message
        let responseMessageId = uuidv4();
        let responseMessage = {
          parentId: userMessageId,
          id: responseMessageId,
					search: search,
					search_type: search_type,
					search_content: {},
					keyword: userPrompt,
          childrenIds: [],
          role: "assistant",
          content: "",
					think_content: "",
          model: model.id,
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
        responseMap[model?.id] = responseMessage;
      }
    });

		scrollToBottom();
		
		monitorLog.push({fun: "checkLimit-start", time: new Date()});
		// Verify the number of times the model has been used
		let modelLimit:any = {}
    const {passed, data} = await conversationRefresh(localStorage.token, selectedModels);
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
		monitorLog.push({fun: "checkLimit-end", time: new Date()});

		// Waiting for history/message update to complete
		await tick();

		// Reset chat input text area
		prompt = '';
		files = [];
		monitorLog.push({fun: "newchat-start", time: new Date()});
		// If there is only one message in the messages, create a new chat
		if (messages.length == 2) {
			if ($settings.saveChatHistory ?? true) {
				// 3\1. Create a new session
				chat = await createNewChat(localStorage.token, {
					id: $chatId,
					title: $i18n.t('New Chat'),
					models: selectedModels,
					system: $settings.system ?? undefined,
					options: {
						...($settings.options ?? {})
					},
					messages: messages,
					history: history,
					timestamp: Date.now()
				});
				await chats.set(await getChatList(localStorage.token));
				await chatId.set(chat.id);
			} else {
				await chatId.set('local');
			}
			await tick();
		}
		monitorLog.push({fun: "newchat-end", time: new Date()});
		// Send a reminder
		await sendPrompt(userPrompt, userMessageId, responseMap, modelLimit);

	}
};

	// 3\2. Continue chatting session
	const sendPrompt = async (prompt, parentId, responseMap, modelLimit, modelId = null) => {
		const _chatId = JSON.parse(JSON.stringify($chatId));
		monitorLog.push({fun: "chat-start", time: new Date()});
		// Make requests for each model
		await Promise.all(
			(modelId ? [modelId] : atSelectedModel !== '' ? [atSelectedModel.id] : selectedModels).map(
				async (modelId) => {
					console.log('modelId', modelId);
					const model = $models.filter((m) => m.id === modelId).at(0);
					monitorLog.push({fun: model?.id + "-start", time: new Date()});
					if (model) {
						// Create response message
						let responseMessageId = uuidv4();
						let responseMessage = {}
						if (responseMap[model?.id]) {
							responseMessageId = responseMap[model?.id].id;
							responseMessage = responseMap[model?.id];
						} else {
							// Create response message
							responseMessage = {
								parentId: parentId,
								id: responseMessageId,
								search: search,
								search_type: search_type,
								search_content: {},
								keyword: prompt,
								childrenIds: [],
								role: "assistant",
								content: "",
								think_content: "",
								model: model.id,
								userContext: null,
								timestamp: Math.floor(Date.now() / 1000), // Unix epoch
							};

							// Add message to history and Set currentId to messageId
							history.messages[responseMessageId] = responseMessage;
							history.currentId = responseMessageId;

							// Append messageId to childrenIds of parent message
							if (parentId !== null) {
								history.messages[parentId].childrenIds = [
									...history.messages[parentId].childrenIds,
									responseMessageId,
								];
							}
						}

						// Waiting for history/message update to complete
						await tick();

						let userContext = null;
						if ($settings?.memory ?? false) {
							if (userContext === null) {
								const res = await queryMemory(localStorage.token, prompt).catch((error) => {
									toast.error(error);
									return null;
								});

								if (res) {
									if (res.documents[0].length > 0) {
										userContext = res.documents.reduce((acc, doc, index) => {
											const createdAtTimestamp = res.metadatas[index][0].created_at;
											const createdAtDate = new Date(createdAtTimestamp * 1000)
												.toISOString()
												.split('T')[0];
											acc.push(`${index + 1}. [${createdAtDate}]. ${doc[0]}`);
											return acc;
										}, []);
									}

									console.log(userContext);
								}
							}
						}
						responseMessage.userContext = userContext;

						console.log("responseMessage:", responseMessage);
						
						// Verify if the number of times has been exceeded
						if (modelLimit[model.id]) {
							await handleLimitError(modelLimit[model.id], responseMessage)
						} else {
							monitorLog.push({fun: model?.id + "search-start", time: new Date()});
							// Search website
							handleSearchWeb(responseMessage, responseMessageId);
							monitorLog.push({fun: model?.id + "search-end", time: new Date()});
							// Text search
							monitorLog.push({fun: model?.id + "de-start", time: new Date()});
							await sendPromptDeOpenAI(model, responseMessageId, _chatId);
							monitorLog.push({fun: model?.id + "de-end", time: new Date()});
						}

					} else {
						console.error($i18n.t(`Model {{modelId}} not found`, { }));

						// toast.error($i18n.t(`Model {{modelId}} not found`, { modelId }));
					}
					
				}
			)
		);

		// After all model responses are completed, restore firstResAlready to its initial state false
    firstResAlready = false;

    // Load chat list (assign chat title)
    if (messages.length == 2) {
      window.history.replaceState(history.state, "", `/c/${_chatId}`);
      const _title = await generateDeChatTitle(prompt);
      await setChatTitle(_chatId, _title);
    } else {
      await chats.set(await getChatList(localStorage.token));
    }
	};

	// Dialogue with DeGpt
	const sendPromptDeOpenAI = async (model, responseMessageId, _chatId) => {
			
		const responseMessage = history.messages[responseMessageId];
		const docs = messages
			.filter((message) => message?.files ?? null)
			.map((message) =>
				message.files.filter((item) => item.type === 'doc' || item.type === 'collection')
			)
			.flat(1);

		console.log(docs);

		// Retrieve the reply message from the previous corresponding model
    const modelmessage = messages;
    if (messages.length > 2) {
      let checkmessage = modelmessage[messages.length - 3];
      let checkchildrenIds = history.messages[checkmessage.parentId]?.childrenIds;
      if (checkchildrenIds) {
        checkchildrenIds.forEach(item => {
          let sonMessage = history.messages[item];
          if (sonMessage.model == model.id) {
            checkmessage.content = sonMessage.content;
          }
        });
      }
    }

		scrollToBottom();

		console.log("$settings.system", $settings.system, );
		
		try {
			let send_message = [
        $settings.system || (responseMessage?.userContext ?? null)
          ? {
              role: "system",
              content: `${$settings?.system ?? ""}${
              responseMessage?.userContext ?? null
                ? `\n\nUser Context:\n${(responseMessage?.userContext ?? []).join("\n")}` : ""}`,
            } : undefined,
            ...modelmessage,
        ].filter((message) => message);
			
			// Determine whether to reassign the value through network search
			send_message.forEach((item, index) => {
        // Determine different types of questions with different content
        if (item?.role != 'user' && item?.search) {
          let preMessage = send_message[index-1].content;
          if (item?.search_type == "youtube") {
						if (item?.search_content?.videos) {
							let analyContent = item?.search_content?.videos.map((vItem: any) => vItem?.description).join('\n');
							analyContent = analyContent + "\n" + $i18n.t("Summarize based on the above YouTube search results:") + preMessage;
							send_message[index-1].content = analyContent;
						}
          } else if (item?.search_type == "twitter") {
						if (item?.search_content?.content) {
							let analyContent = item?.search_content?.content.map((tItem: any) => tItem?.full_text).join('\n');
							analyContent = analyContent + "\n" + $i18n.t("Summarize based on the above Twitter search results:") + preMessage;
							send_message[index-1].content = analyContent;
						}
          } else {
						if (item?.search_content?.web) {
							let analyContent = item?.search_content?.web.map((wItem: any) => wItem?.content).join('\n');
							analyContent = analyContent + "\n" + $i18n.t("Summarize based on the above web search results:") + preMessage;
							send_message[index-1].content = analyContent;
						}
          }
        }
      });
			// Filter out data with errors and empty content
			send_message = send_message.filter(item =>!item.error).filter(item=> item.content != "");

      send_message = send_message.map((message, idx, arr) => ({
        role: message.role,
        ...((message.files?.filter((file) => file.type === "image").length > 0 ?? false) &&
        message.role === "user"
          ? {
              content: [
                {
                  type: "text",
                  text:
                    arr.length - 1 !== idx
                      ? message.content
                      : message?.raContent ?? message.content,
                },
                ...message.files
                  .filter((file) => file.type === "image")
                    .map((file) => ({
                      type: "image_url",
                      image_url: {
                        url: file.url,
                      },
                    })),
              ],
            }
          : {
            content:
              arr.length - 1 !== idx
                ? message.content
                : message?.raContent ?? message.content,
            }),
      }));

			monitorLog.push({fun: model?.id + "de-send-start", time: new Date()});
			const [res, controller] = await generateDeOpenAIChatCompletion(
				localStorage.token,
				{
					model: model.id,
					messages: send_message,
				},
				$deApiBaseUrl?.url,
				monitorLog
			);



			// Wait until history/message have been updated
			await tick();

			scrollToBottom();

			// 6. Create an OpenAI dialogue data stream
			if (res && res.ok && res.body) {
				const textStream = await createOpenAITextStream(res.body, $settings.splitLargeChunks);
				responseMessage.replytime = Math.floor(Date.now() / 1000);
				// Add a think header to the judgment model
        if (model.id == "DeepSeek-R1") {
          responseMessage.think_content = "<think>";
        }
				for await (const update of textStream) {
					const { value, done, citations, error } = update;

					if(value && !firstResAlready) { 
						// When responding for the first time, set the current ID to the current response ID
						firstResAlready = true;
						history.currentId = responseMessageId;
					}
					if (error) {
						await handleOpenAIError(error, null, model, responseMessage);
						break;
					}
					if (done || stopResponseFlag || _chatId !== $chatId) {
						responseMessage.done = true;
						messages = messages;

						if (stopResponseFlag) {
							controller.abort('User: Stop Response');
						}

						break;
					}

					if (citations) {
						responseMessage.citations = citations;
						continue;
					}



			if(!firstResAlready && responseMessage.content.length > 0) { 
				// When responding for the first time, set the current ID to the current response ID
				console.log("Model call completed？", res, model.id, firstResAlready, responseMessageId, responseMessage.content);
				
				firstResAlready = true;
				history.currentId = responseMessageId;
				await tick();

			}

					if (responseMessage.content == '' && value == '\n') {
						continue;
					} else {
						// responseMessage.content += value;
						responseMessage.content = await addTextSlowly(
							responseMessage.content, 
							value,
							model.id
						);
						messages = messages;
					}

					// if ($settings.notificationEnabled && !document.hasFocus()) {
					// 	const notification = new Notification(`OpenAI ${model}`, {
					// 		body: responseMessage.content,
					// 		icon: `${WEBUI_BASE_URL}/static/favicon.png`
					// 	});
					// }

					if ($settings.responseAutoCopy) {
						copyToClipboard(responseMessage.content);
					}

					if ($settings.responseAutoPlayback) {
						await tick();
						document.getElementById(`speak-button-${responseMessage.id}`)?.click();
					}

					if (autoScroll) {
						scrollToBottom();
					}
				}
			} else {
				await handleOpenAIError(null, res, model, responseMessage);
			}
		} catch (error) {
			await handleOpenAIError(error, null, model, responseMessage);
		}

		await checkThinkContent(responseMessage);
		messages = messages;

		stopResponseFlag = false;

		monitorLog.push({fun: model?.id + "de-send-end", time: new Date()});

		// Update chat history
		if (_chatId === $chatId) {  
      if ($settings.saveChatHistory ?? true) {
        await updateChatById(localStorage.token, _chatId, {
          messages: messages,
          history: history
        });
      }
    }

		monitorLog.push({fun: model?.id + "update-chat", time: new Date()});
    addErrorLog(_chatId + "conversation", JSON.stringify(monitorLog));

		await tick();

		if (autoScroll) {
			scrollToBottom();
		}
	};


	const sendPromptOllama = async (model, userPrompt, responseMessageId, _chatId) => {
		model = model.id;
		const responseMessage = history.messages[responseMessageId];

		// Wait until history/message have been updated
		await tick();

		// Scroll down
		scrollToBottom();

		const messagesBody = [
			$settings.system || (responseMessage?.userContext ?? null)
				? {
						role: 'system',
						content: `${$settings?.system ?? ''}${
							responseMessage?.userContext ?? null
								? `\n\nUser Context:\n${(responseMessage?.userContext ?? []).join('\n')}`
								: ''
						}`
				  }
				: undefined,
			...messages
		]
			.filter((message) => message)
			.map((message, idx, arr) => {
				// Prepare the base message object
				const baseMessage = {
					role: message.role,
					content: arr.length - 2 !== idx ? message.content : message?.raContent ?? message.content
				};

				// Extract and format image URLs if any exist
				const imageUrls = message.files
					?.filter((file) => file.type === 'image')
					.map((file) => file.url.slice(file.url.indexOf(',') + 1));

				// Add images array only if it contains elements
				if (imageUrls && imageUrls.length > 0 && message.role === 'user') {
					baseMessage.images = imageUrls;
				}

				return baseMessage;
			});

		let lastImageIndex = -1;

		// Find the index of the last object with images
		messagesBody.forEach((item, index) => {
			if (item.images) {
				lastImageIndex = index;
			}
		});

		// Remove images from all but the last one
		messagesBody.forEach((item, index) => {
			if (index !== lastImageIndex) {
				delete item.images;
			}
		});

		const docs = messages
			.filter((message) => message?.files ?? null)
			.map((message) =>
				message.files.filter((item) => item.type === 'doc' || item.type === 'collection')
			)
			.flat(1);

		const [res, controller] = await generateChatCompletion(localStorage.token, {
			model: model,
			messages: messagesBody,
			options: {
				...($settings.options ?? {}),
				stop:
					$settings?.options?.stop ?? undefined
						? $settings.options.stop.map((str) =>
								decodeURIComponent(JSON.parse('"' + str.replace(/\"/g, '\\"') + '"'))
						  )
						: undefined
			},
			format: $settings.requestFormat ?? undefined,
			keep_alive: $settings.keepAlive ?? undefined,
			docs: docs.length > 0 ? docs : undefined,
			citations: docs.length > 0
		});

		if (res && res.ok) {
			console.log('controller', controller);

			const reader = res.body
				.pipeThrough(new TextDecoderStream())
				.pipeThrough(splitStream('\n'))
				.getReader();

			while (true) {
				const { value, done } = await reader.read();
				if (done || stopResponseFlag || _chatId !== $chatId) {
					responseMessage.done = true;
					messages = messages;

					if (stopResponseFlag) {
						controller.abort('User: Stop Response');
						await cancelOllamaRequest(localStorage.token, currentRequestId);
					}

					currentRequestId = null;

					break;
				}

				try {
					let lines = value.split('\n');

					for (const line of lines) {
						if (line !== '') {
							console.log(line);
							let data = JSON.parse(line);

							if ('citations' in data) {
								responseMessage.citations = data.citations;
								continue;
							}

							if ('detail' in data) {
								throw data;
							}

							if ('id' in data) {
								console.log(data);
								currentRequestId = data.id;
							} else {
								if (data.done == false) {
									if (responseMessage.content == '' && data.message.content == '\n') {
										continue;
									} else {
										responseMessage.content += data.message.content;
										messages = messages;
									}
								} else {
									responseMessage.done = true;

									if (responseMessage.content == '') {
										responseMessage.error = true;
										responseMessage.content =
											'Oops! No text generated from Ollama, Please try again.';
									}

									responseMessage.context = data.context ?? null;
									responseMessage.info = {
										total_duration: data.total_duration,
										load_duration: data.load_duration,
										sample_count: data.sample_count,
										sample_duration: data.sample_duration,
										prompt_eval_count: data.prompt_eval_count,
										prompt_eval_duration: data.prompt_eval_duration,
										eval_count: data.eval_count,
										eval_duration: data.eval_duration
									};
									messages = messages;

									// if ($settings.notificationEnabled && !document.hasFocus()) {
									// 	const notification = new Notification(
									// 		selectedModelfile
									// 			? `${
									// 					selectedModelfile.title.charAt(0).toUpperCase() +
									// 					selectedModelfile.title.slice(1)
									// 			  }`
									// 			: `${model}`,
									// 		{
									// 			body: responseMessage.content,
									// 			icon: selectedModelfile?.imageUrl ?? `${WEBUI_BASE_URL}/static/favicon.png`
									// 		}
									// 	);
									// }

									if ($settings.responseAutoCopy) {
										copyToClipboard(responseMessage.content);
									}

									if ($settings.responseAutoPlayback) {
										await tick();
										document.getElementById(`speak-button-${responseMessage.id}`)?.click();
									}
								}
							}
						}
					}
				} catch (error) {
					console.log(error);
					if ('detail' in error) {
						toast.error(error.detail);
					}
					break;
				}

				if (autoScroll) {
					scrollToBottom();
				}
			}

			if ($chatId == _chatId) {
				if ($settings.saveChatHistory ?? true) {
					chat = await updateChatById(localStorage.token, _chatId, {
						messages: messages,
						history: history
					});
					await chats.set(await getChatList(localStorage.token));
				}
			}
		} else {
			if (res !== null) {
				const error = await res.json();
				console.log(error);
				if ('detail' in error) {
					toast.error(error.detail);
					responseMessage.content = error.detail;
				} else {
					toast.error(error.error);
					responseMessage.content = error.error;
				}
			} else {
				toast.error(
					$i18n.t(`Uh-oh! There was an issue connecting to {{provider}}.`, { provider: 'Ollama' })
				);
				responseMessage.content = $i18n.t(`Uh-oh! There was an issue connecting to {{provider}}.`, {
					provider: 'Ollama'
				});
			}

			responseMessage.error = true;
			responseMessage.content = $i18n.t(`Uh-oh! There was an issue connecting to {{provider}}.`, {
				provider: 'Ollama'
			});
			responseMessage.done = true;
			messages = messages;
		}

		stopResponseFlag = false;
		await tick();

		if (autoScroll) {
			scrollToBottom();
		}

		if (messages.length == 2 && messages.at(1).content !== '') {
			window.history.replaceState(history.state, '', `/c/${_chatId}`);
			const _title = await generateChatTitle(userPrompt);
			await setChatTitle(_chatId, _title);
		}
	};

	const generateDeChatTitle = async (userPrompt) => {
		if ($settings?.title?.auto ?? true) {
			const model = $models.find((model) => model.id === selectedModels[0]);

			const titleModelId =
				model?.external ?? false
					? $settings?.title?.modelExternal ?? selectedModels[0]
					: $settings?.title?.model ?? selectedModels[0];
			const titleModel = $models.find((model) => model.id === titleModelId);

			console.log(titleModel);
			const title = await generateDeTitle(
				localStorage.token,
				$settings?.title?.prompt ??
					$i18n.t(
						"Create a concise, 3-5 word phrase as a header for the following query, strictly adhering to the 3-5 word limit and avoiding the use of the word 'title':"
					) + ' {{prompt}}',
				titleModelId,
				userPrompt,
				$deApiBaseUrl?.url
			);

			return title;
		} else {
			return `${userPrompt}`;
		}
	};

	const generateSearchChatKeyword = async (userPrompt: string) => {
    if ($settings?.title?.auto ?? true) {
      // Get keywords
      let send_messages = messages.filter(item => item.role == 'user')
        .map(item => ({role: item.role, content: item.content}));
      send_messages.push({
        role: "user",
        content: $i18n.t("Obtain what the content of the final question is about, and only output the content it is about")
      })
      const title = await generateSearchKeyword(
        send_messages,
        $deApiBaseUrl?.url
      );
      return title;
    } else {
      return `${userPrompt}`;
    }
  };

	// 5. Send a request to OpenAI
	const sendPromptOpenAI = async (model, userPrompt, responseMessageId, _chatId) => {
		const responseMessage = history.messages[responseMessageId];

		const docs = messages
			.filter((message) => message?.files ?? null)
			.map((message) =>
				message.files.filter((item) => item.type === 'doc' || item.type === 'collection')
			)
			.flat(1);

		console.log(docs);

		scrollToBottom();

		try {
			const [res, controller] = await generateOpenAIChatCompletion(
				localStorage.token,
				{
					model: model.id,
					stream: true,
					messages: [
						$settings.system || (responseMessage?.userContext ?? null)
							? {
									role: 'system',
									content: `${$settings?.system ?? ''}${
										responseMessage?.userContext ?? null
											? `\n\nUser Context:\n${(responseMessage?.userContext ?? []).join('\n')}`
											: ''
									}`
							  }
							: undefined,
						...messages
					]
						.filter((message) => message)
						.map((message, idx, arr) => ({
							role: message.role,
							...((message.files?.filter((file) => file.type === 'image').length > 0 ?? false) &&
							message.role === 'user'
								? {
										content: [
											{
												type: 'text',
												text:
													arr.length - 1 !== idx
														? message.content
														: message?.raContent ?? message.content
											},
											...message.files
												.filter((file) => file.type === 'image')
												.map((file) => ({
													type: 'image_url',
													image_url: {
														url: file.url
													}
												}))
										]
								  }
								: {
										content:
											arr.length - 1 !== idx
												? message.content
												: message?.raContent ?? message.content
								  })
						})),
					seed: $settings?.options?.seed ?? undefined,
					stop:
						$settings?.options?.stop ?? undefined
							? $settings.options.stop.map((str) =>
									decodeURIComponent(JSON.parse('"' + str.replace(/\"/g, '\\"') + '"'))
							  )
							: undefined,
					temperature: $settings?.options?.temperature ?? undefined,
					top_p: $settings?.options?.top_p ?? undefined,
					num_ctx: $settings?.options?.num_ctx ?? undefined,
					frequency_penalty: $settings?.options?.repeat_penalty ?? undefined,
					max_tokens: $settings?.options?.num_predict ?? undefined,
					docs: docs.length > 0 ? docs : undefined,
					citations: docs.length > 0
				},
				model?.source?.toLowerCase() === 'litellm'
					? `${LITELLM_API_BASE_URL}/v1`
					: `${OPENAI_API_BASE_URL}`
			);

			// Wait until history/message have been updated
			await tick();

			scrollToBottom();

			// 6. Create an OpenAI dialogue data stream
			if (res && res.ok && res.body) {
				const textStream = await createOpenAITextStream(res.body, $settings.splitLargeChunks);

				for await (const update of textStream) {
					const { value, done, citations, error } = update;
					if (error) {
						await handleOpenAIError(error, null, model, responseMessage);
						break;
					}
					if (done || stopResponseFlag || _chatId !== $chatId) {
						responseMessage.done = true;
						messages = messages;

						if (stopResponseFlag) {
							controller.abort('User: Stop Response');
						}

						break;
					}

					if (citations) {
						responseMessage.citations = citations;
						continue;
					}

					if (responseMessage.content == '' && value == '\n') {
						continue;
					} else {
						responseMessage.content += value;
						messages = messages;
					}

					// if ($settings.notificationEnabled && !document.hasFocus()) {
					// 	const notification = new Notification(`OpenAI ${model}`, {
					// 		body: responseMessage.content,
					// 		icon: `${WEBUI_BASE_URL}/static/favicon.png`
					// 	});
					// }

					if ($settings.responseAutoCopy) {
						copyToClipboard(responseMessage.content);
					}

					if ($settings.responseAutoPlayback) {
						await tick();
						document.getElementById(`speak-button-${responseMessage.id}`)?.click();
					}

					if (autoScroll) {
						scrollToBottom();
					}
				}

				if ($chatId == _chatId) {
					if ($settings.saveChatHistory ?? true) {
						chat = await updateChatById(localStorage.token, _chatId, {
							messages: messages,
							history: history
						});
						await chats.set(await getChatList(localStorage.token));
					}
				}
			} else {
				await handleOpenAIError(null, res, model, responseMessage);
			}
		} catch (error) {
			await handleOpenAIError(error, null, model, responseMessage);
		}
		messages = messages;

		stopResponseFlag = false;
		await tick();

		if (autoScroll) {
			scrollToBottom();
		}

		if (messages.length == 2) {
			window.history.replaceState(history.state, '', `/c/${_chatId}`);

			const _title = await generateChatTitle(userPrompt);
			await setChatTitle(_chatId, _title);
		}
	};

	// Verify if the model has thought content
  const checkThinkContent = async(responseMessage: any) => {
		let checkMessage = responseMessage.think_content + responseMessage.content;
    if (checkMessage.startsWith("<think>")) {
      const startIndex = checkMessage.indexOf('<think>');
      const nextSearchIndex = startIndex + '<think>'.length;
      const endIndex = checkMessage.indexOf('</think>', nextSearchIndex);
      let extracted;
      let remaining;
      if (endIndex === -1) {
        extracted = checkMessage.slice(startIndex);
        remaining = checkMessage.slice(0, startIndex);
      } else {
        extracted = checkMessage.slice(startIndex, endIndex + '</think>'.length);
        remaining = checkMessage.slice(0, startIndex) + checkMessage.slice(endIndex + '</think>'.length);
      }
      responseMessage.content = remaining;
      responseMessage.think_content = extracted;
    }
  }

	// Get search webpage
  const handleSearchWeb= async(responseMessage: any, responseMessageId: string) => {
    if (search) {
			const ai_keyword = await generateSearchChatKeyword(responseMessage.keyword);
      let result = await thirdSearch(localStorage.token, ai_keyword, responseMessage.search_type);
      if (result?.ok) {
        responseMessage.search_content = result.data;
				history.messages[responseMessageId] = responseMessage;
      }
    }
    await tick();
    scrollToBottom();
  }

	const handleOpenAIError = async (error, res: Response | null, model, responseMessage) => {
		let errorMessage = '';
		let innerError;

		if (error) {
			innerError = error;
		} else if (res !== null) {
			innerError = await res.json();
		}
		console.error(innerError);
		if ('detail' in innerError) {
			toast.error(innerError.detail);
			errorMessage = innerError.detail;
		} else if ('error' in innerError) {
			if ('message' in innerError.error) {
				toast.error(innerError.error.message);
				errorMessage = innerError.error.message;
			} else {
				toast.error(innerError.error);
				errorMessage = innerError.error;
			}
		} else if ('message' in innerError) {
			toast.error(innerError.message);
			errorMessage = innerError.message;
		}

		responseMessage.error = true;
		responseMessage.content =
			$i18n.t(`Uh-oh! There was an issue connecting to {{provider}}.`, {
				provider: model.name ?? model.id
			}) +
			'\n' +
			errorMessage;
		responseMessage.done = true;

		messages = messages;
	};

	const handleLimitError = async (content: string, responseMessage: any) => {
    responseMessage.content = content;
    responseMessage.replytime = Math.floor(Date.now() / 1000);
    responseMessage.error = true;
    responseMessage.done = true;
    messages = messages;
    scrollToBottom();
    await updateChatById(localStorage.token, $chatId, {
      messages: messages,
      history: history
    });
  }

	const stopResponse = () => {
		stopResponseFlag = true;
		console.log('stopResponse');
	};

	const regenerateResponse = async (message) => {
		console.log('regenerateResponse');

		if (messages.length != 0) {
			let userMessage = history.messages[message.parentId];
			let userPrompt = userMessage.content;

			if ((userMessage?.models ?? [...selectedModels]).length == 1) {
				await sendPrompt(userPrompt, userMessage.id);
			} else {
				await sendPrompt(userPrompt, userMessage.id, message.model);
			}
		}
	};

	const continueGeneration = async () => {
		console.log('continueGeneration');
		const _chatId = JSON.parse(JSON.stringify($chatId));

		if (messages.length != 0 && messages.at(-1).done == true) {
			const responseMessage = history.messages[history.currentId];
			responseMessage.done = false;
			await tick();

			const model = $models.filter((m) => m.id === responseMessage.model).at(0);

			if (model) {
				// if (model?.external) {
				// 	await sendPromptOpenAI(
				// 		model,
				// 		history.messages[responseMessage.parentId].content,
				// 		responseMessage.id,
				// 		_chatId
				// 	);
				// } else
				// 	await sendPromptOllama(
				// 		model,
				// 		history.messages[responseMessage.parentId].content,
				// 		responseMessage.id,
				// 		_chatId
				// 	);
				await sendPromptDeOpenAI(
					model,
					responseMessage.id,
					_chatId
				);
			}
		} else {
console.error($i18n.t(`Model {{modelId}} not found`, { }));
// toast.error($i18n.t(`Model {{modelId}} not found`, { modelId }));
		}
	};

	const generateChatTitle = async (userPrompt) => {
		if ($settings?.title?.auto ?? true) {
			const model = $models.find((model) => model.id === selectedModels[0]);

			const titleModelId =
				model?.external ?? false
					? $settings?.title?.modelExternal ?? selectedModels[0]
					: $settings?.title?.model ?? selectedModels[0];
			const titleModel = $models.find((model) => model.id === titleModelId);

			console.log(titleModel);
			const title = await generateTitle(
				localStorage.token,
				$settings?.title?.prompt ??
					$i18n.t(
						"Create a concise, 3-5 word phrase as a header for the following query, strictly adhering to the 3-5 word limit and avoiding the use of the word 'title':"
					) + ' {{prompt}}',
				titleModelId,
				userPrompt,
				model?.urls?.[0]

				// titleModel?.external ?? false
				// 	? titleModel?.source?.toLowerCase() === 'litellm'
				// 		? `${LITELLM_API_BASE_URL}/v1`
				// 		: `${OPENAI_API_BASE_URL}`
				// 	: `${OLLAMA_API_BASE_URL}/v1`
			);

			return title;
		} else {
			return `${userPrompt}`;
		}
	};

	const setChatTitle = async (_chatId, _title) => {
		if (_chatId === $chatId) {
			title = _title;
		}

		if ($settings.saveChatHistory ?? true) {
			chat = await updateChatById(localStorage.token, _chatId, { title: _title });
			await chats.set(await getChatList(localStorage.token));
		}
	};

	const getTags = async () => {
		return await getTagsById(localStorage.token, $chatId).catch(async (error) => {
			return [];
		});
	};

	const addTag = async (tagName) => {
		const res = await addTagById(localStorage.token, $chatId, tagName);
		tags = await getTags();

		chat = await updateChatById(localStorage.token, $chatId, {
			tags: tags
		});

		_tags.set(await getAllChatTags(localStorage.token));
	};

	const deleteTag = async (tagName) => {
		const res = await deleteTagById(localStorage.token, $chatId, tagName);
		tags = await getTags();

		chat = await updateChatById(localStorage.token, $chatId, {
			tags: tags
		});

		_tags.set(await getAllChatTags(localStorage.token));
	};

	onMount(async () => {
		if (!($settings.saveChatHistory ?? true)) {
			await goto('/');
		}
	});
</script>

<svelte:head>
	<title>
		{title
			? `${title.length > 30 ? `${title.slice(0, 30)}...` : title} | ${$WEBUI_NAME}`
			: `${$WEBUI_NAME}`}
	</title>
</svelte:head>

{#if loaded}

	<div
		class="min-h-screen max-h-screen {$showSidebar
			? 'md:max-w-[calc(100%-246px)]'
			: ''} w-full max-w-full flex flex-col"
	>
		<Navbar
			{title}
			{chat}
			bind:selectedModels
			bind:showModelSelector
			shareEnabled={messages.length > 0}
			initNewChat={async () => {
				if (currentRequestId !== null) {
					await cancelOllamaRequest(localStorage.token, currentRequestId);
					currentRequestId = null;
				}
				goto('/');
			}}
		/>
		<div class="flex flex-col flex-auto">
			<div
				class=" pb-2.5 flex flex-col justify-between w-full flex-auto overflow-auto h-0 max-w-full"
				id="messages-container"
				bind:this={messagesContainerElement}
				on:scroll={(e) => {
					autoScroll =
						messagesContainerElement.scrollHeight - messagesContainerElement.scrollTop <=
						messagesContainerElement.clientHeight + 5;
				}}
			>
				<div class=" h-full w-full flex flex-col py-4">
					<Messages
						chatId={$chatId}
						{selectedModels}
						{selectedModelfiles}
						{processing}
						bind:history
						bind:messages
						bind:autoScroll
						bind:prompt
						bottomPadding={files.length > 0}
						{sendPrompt}
						{continueGeneration}
						{regenerateResponse}
					/>
				</div>
			</div>
		</div>
	</div>




	<MessageInput
		bind:files
		bind:search
		bind:search_type
		bind:prompt
		bind:autoScroll
		bind:selectedModel={atSelectedModel}
		{messages}
		{submitPrompt}
		{stopResponse}
	/>
{/if}
