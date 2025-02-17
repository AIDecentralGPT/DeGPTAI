<script lang="ts">
  import { toast } from "svelte-sonner";
  import { v4 as uuidv4 } from "uuid";
  import { page } from "$app/stores";
  import { getContext, onMount, tick } from "svelte";

  import {
    WEBUI_NAME,
    tags as _tags,
    chatId,
    chats,
    config,
    inviterId,
    channel,
    modelfiles,
    models,
    pageUpdateNumber,
    settings,
    showNewWalletModal,
    showSidebar,
    showUserVerifyModal,
    user,
    deApiBaseUrl } from "$lib/stores";
  import { copyToClipboard, splitStream, addTextSlowly } from "$lib/utils";

  import {
    addTagById,
    createNewChat,
    deleteTagById,
    getAllChatTags,
    getChatList,
    getTagsById,
    updateChatById,
    conversationRefresh
  } from "$lib/apis/chats";
  import {
    cancelOllamaRequest,
    generateChatCompletion,
  } from "$lib/apis/ollama";
  import {
    generateOpenAIChatCompletion,
    generateTitle,
  } from "$lib/apis/openai";
  import {
    generateDeOpenAIChatCompletion,
    generateDeTitle,
    generateSearchKeyword
  } from "$lib/apis/de";

  import { queryMemory } from "$lib/apis/memories";
  import { createOpenAITextStream } from "$lib/apis/streaming";
  import MessageInput from "$lib/components/chat/MessageInput.svelte";
  import Messages from "$lib/components/chat/Messages.svelte";
  import Navbar from "$lib/components/layout/Navbar.svelte";
  import {
    LITELLM_API_BASE_URL,
    OLLAMA_API_BASE_URL,
    OPENAI_API_BASE_URL,
  } from "$lib/constants";

  import { thirdSearch } from "$lib/apis/thirdsearch";

  let inviter: any = "";
  let channelName: any = "";

  const i18n = getContext("i18n");

  let stopResponseFlag = false;
  let autoScroll = true;
  let processing = "";
  let messagesContainerElement: HTMLDivElement;
  let currentRequestId: any = null;

  let showModelSelector = true;

  let selectedModels = [""];
  let atSelectedModel = "";

  let selectedModelfile = null;
  $: selectedModelfile =
    selectedModels.length === 1 &&
    $modelfiles.filter((modelfile) => modelfile.tagName === selectedModels[0])
      .length > 0
      ? $modelfiles.filter(
          (modelfile) => modelfile.tagName === selectedModels[0]
        )[0]
      : null;

  let selectedModelfiles = {};
  $: selectedModelfiles = selectedModels.reduce((a, tagName, i, arr) => {
    const modelfile =
      $modelfiles.filter((modelfile) => modelfile.tagName === tagName)?.at(0) ??
      undefined;

    return {
      ...a,
      ...(modelfile && { [tagName]: modelfile }),
    };
  }, {});

  let chat = null;
  let tags = [];

  let title = "";
  let prompt = "";
  let files = [];
  let search = false;
  let search_type = "web";
  let messages = [];
  let history = {
    messages: {},
    currentId: null,
  };

  // 触发当前组件初始化
  $: $pageUpdateNumber, initNewChat();
  let firstResAlready = false; // 已经有了第一个响应

  $: if (history.currentId !== null) {
    let _messages = [];

    let currentMessage = history.messages[history.currentId];

    while (currentMessage !== null) {
      _messages.unshift({ ...currentMessage }); // _messages开头添加元素
      currentMessage = currentMessage.parentId !== null ? history.messages[currentMessage.parentId] : null;
    }

    // console.log("_messages", _messages);

    messages = _messages;
  } else {
    messages = [];
  }

  onMount(async () => {
    const queryParams = new URLSearchParams($page.url.search);
    inviter = queryParams.get("inviter");
    channelName = queryParams.get("channel");
    if (inviter) {
      $showNewWalletModal = true;
      $inviterId = inviter;
    }
    if (channelName) {
      await channel.set(channelName);
    }
    const verifyAgain = queryParams.get("verifyAgain");
    if (verifyAgain && $user?.id) {
      $showUserVerifyModal = true;
    }

    await initNewChat();
  });

  //////////////////////////
  // Web functions
  //////////////////////////

  const initNewChat = async () => {
    if (currentRequestId !== null) {
      await cancelOllamaRequest(localStorage.token, currentRequestId);
      currentRequestId = null;
    }
    window.history.replaceState(history.state, "", `/`);
    await chatId.set("");

    autoScroll = true;

    title = "";
    messages = [];
    history = {
      messages: {},
      currentId: null,
    };

    if ($page.url.searchParams.get("models")) {
      selectedModels = $page.url.searchParams.get("models")?.split(",");
    } else if ($settings?.models) {
      selectedModels = $settings?.models;
    } else if ($config?.default_models) {
      selectedModels = $config?.default_models.split(",");
    } else {
      selectedModels = [""];
    }

    if ($page.url.searchParams.get("q")) {
      prompt = $page.url.searchParams.get("q") ?? "";
      if (prompt) {
        await tick();
        submitPrompt(prompt);
      }
    }

    selectedModels = selectedModels.map((modelId) =>
      $models.map((m) => m.id).includes(modelId) ? modelId : ""
    );

    let _settings = JSON.parse(localStorage.getItem("settings") ?? "{}");
    settings.set({
      ..._settings,
    });

    // const chatInput = document.getElementById("chat-textarea");
    // setTimeout(() => chatInput?.focus(), 0);
  };

  const scrollToBottom = async () => {
    await tick();
    if (messagesContainerElement) {
      messagesContainerElement.scrollTop =
        messagesContainerElement.scrollHeight;
    }
  };

  //////////////////////////
  // Ollama functions
  //////////////////////////

  const submitPrompt = async (userPrompt, _user = null) => {
    console.log("submitPrompt", $chatId, userPrompt);

    selectedModels = selectedModels.map((modelId) =>
      $models.map((m) => m.id).includes(modelId) ? modelId : ""
    );
    
    // 校验模型是否支持文件类型
    if (files.length > 0) {
      let imageModels = $models.filter(item => item.support == "image");
      let checkSelectedModels = imageModels.filter(item => selectedModels.includes(item.model))
        .map(item => item.model);
      if (checkSelectedModels.length == 0) {
        toast.error($i18n.t("Not supported"));
        return;
      } else {
        selectedModels = checkSelectedModels;
      }
    }

    console.log("selectedModels", selectedModels);

    // 如果开启网络搜索只选择一个模型回复
    if (search) {
      selectedModels = [selectedModels[0]];
    }

    

    // 校验模型已使用次数
    let modelLimit = {}
    for (const item of selectedModels) {
      const {passed, message} = await conversationRefresh(localStorage.token, item);
      if (!passed) {
        modelLimit[item] = message;
      }  
    }

    // const selectedModelsValid = selectedModels
    if (selectedModels.length < 1) {
      toast.error($i18n.t("Model not selected"));
    } else if (messages.length != 0 && messages.at(-1).done != true) {
      // Response not done
      console.log("wait");
    } else if (files.length > 0 && files.filter((file) => file.upload_status === false).length > 0) {
      // Upload not done
      toast.error(
        $i18n.t(
          `Oops! Hold tight! Your files are still in the processing oven. We're cooking them up to perfection. Please be patient and we'll let you know once they're ready.`
        )
      );
    } else {
      // Reset chat message textarea height
      document.getElementById("chat-textarea").style.height = "";

      // Create user message
      let userMessageId = uuidv4();
      let userMessage = {
        id: userMessageId,
        parentId: messages.length !== 0 ? messages.at(-1).id : null,
        childrenIds: [],
        role: "user",
        user: _user ?? undefined,
        content: userPrompt,
        files: files.length > 0 ? files : undefined,
        models: selectedModels.filter(
          (m, mIdx) => selectedModels.indexOf(m) === mIdx
        ),
        timestamp: Math.floor(Date.now() / 1000), // Unix epoch
      };

      // Add message to history and Set currentId to messageId
      history.messages[userMessageId] = userMessage;
      history.currentId = userMessageId;

      // Append messageId to childrenIds of parent message
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

      // Wait until history/message have been updated
      await tick();

      // Reset chat input textarea
      prompt = "";
      files = [];

      // Create new chat if only one message in messages
      if (messages.length == 2) {
        if ($settings.saveChatHistory ?? true) {
          chat = await createNewChat(localStorage.token, {
            id: $chatId,
            title: $i18n.t("New Chat"),
            models: selectedModels,
            system: $settings.system ?? undefined,
            options: {
              ...($settings.options ?? {}),
            },
            messages: messages,
            history: history,
            tags: [],
            timestamp: Date.now(),
          });
          await chats.set(await getChatList(localStorage.token));
          await chatId.set(chat.id);
        } else {
          await chatId.set("local");
        }
        await tick();
      }
      // Send prompt
      await sendPrompt(userPrompt, userMessageId, responseMap, modelLimit);

    }
  };

  const sendPrompt = async (prompt, parentId, responseMap = null, modelLimit = {}, modelId = null) => {
    const _chatId = JSON.parse(JSON.stringify($chatId));
    await Promise.all(
      // 此判断毫无意义-判断结果就是selectedModels
      (modelId ? [modelId] : atSelectedModel !== "" ? [atSelectedModel.id] : selectedModels).map(async (modelId, index) => {
        console.log("modelId", modelId);
        const model = $models.filter((m) => m.id === modelId).at(0);

        if (model) {
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
          await tick();

          let userContext = null;
          if ($settings?.memory ?? false) {
            if (userContext === null) {
              const res = await queryMemory(localStorage.token, prompt).catch(
                (error) => {
                  toast.error(error);
                  return null;
                }
              );

              if (res) {
                if (res.documents[0].length > 0) {
                  userContext = res.documents.reduce((acc, doc, index) => {
                    const createdAtTimestamp =
                      res.metadatas[index][0].created_at;
                    const createdAtDate = new Date(createdAtTimestamp * 1000)
                      .toISOString()
                      .split("T")[0];
                    acc.push(`${index + 1}. [${createdAtDate}]. ${doc[0]}`);
                    return acc;
                  }, []);
                }

                console.log(userContext);
              }
            }
          }
          responseMessage.userContext = userContext;

          // 校验是否超过次数
          if (modelLimit[model.id]) {
            await handleLimitError(modelLimit[model.id], responseMessage);
          } else {
            // 搜索网页
						await handleSearchWeb(responseMessage, responseMessageId);
						// 文本搜索
            await sendPromptDeOpenAI(model, responseMessageId, _chatId);
          }
          // if (model?.external) {
          // 	await sendPromptOpenAI(model, prompt, responseMessageId, _chatId);
          // } else if (model) {
          // 	await sendPromptOllama(model, prompt, responseMessageId, _chatId);
          // }
        } else {
          console.error($i18n.t(`Model {{modelId}} not found`, {}));
          // toast.error($i18n.t(`Model {{modelId}} not found`, { modelId }));
        }
      })
    );

    // 所有模型响应结束后，还原firstResAlready为初始状态false
    firstResAlready = false;

    // 加载聊天列表（赋值聊天title）
    if (messages.length == 2) {
      window.history.replaceState(history.state, "", `/c/${_chatId}`);
      const _title = await generateDeChatTitle(prompt);
      await setChatTitle(_chatId, _title);
    } else {
      await chats.set(await getChatList(localStorage.token));
    }

  };

  // De的openai走这里！
  const sendPromptDeOpenAI = async (
    model,
    responseMessageId,
    _chatId
  ) => {
    const responseMessage = history.messages[responseMessageId];

    // const docs = messages
    //   .filter((message) => message?.files ?? null)
    //   .map((message) =>
    //     message.files.filter(
    //       (item) => item.type === "doc" || item.type === "collection"
    //     )
    //   )
    //   .flat(1);

    // console.log(docs);

    // 获取上一个对应模型回复的消息
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
      send_message.forEach((item, index) => {
        // 判断不同类型提问不同内容
        if (item?.role != 'user' && item?.search) {
          let preMessage = send_message[index-1].content;
          if (item?.search_type == "youtube") {
            let analyContent = item?.search_content?.videos.map((vItem: any) => vItem?.description).join('\n');
            analyContent = analyContent + "\n" + $i18n.t("Summarize based on the above YouTube search results:") + preMessage;
            send_message[index-1].content = analyContent;
          } else if (item?.search_type == "twitter") {
            let analyContent = item?.search_content?.content.map((tItem: any) => tItem?.full_text).join('\n');
            analyContent = analyContent + "\n" + $i18n.t("Summarize based on the above Twitter search results:") + preMessage;
            send_message[index-1].content = analyContent;
          } else {
            let analyContent = item?.search_content?.web.map((wItem: any) => wItem?.content).join('\n');
            analyContent = analyContent + "\n" + $i18n.t("Summarize based on the above web search results:") + preMessage;
            send_message[index-1].content = analyContent;
          }
        }
      });
      send_message = send_message.filter((item) => item.content != '')
      .map((message, idx, arr) => ({
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
      const [res, controller] = await generateDeOpenAIChatCompletion(
        localStorage.token,
        {
          model: model.id,
          messages: send_message
        },
        $deApiBaseUrl?.url
      );

      // console.log("res controller", res, controller);

      // console.log(
      //   "firstResAlready responseMessageId",
      //   firstResAlready,
      //   responseMessageId
      // );

      // Wait until history/message have been updated
      await tick();

      scrollToBottom();

      if (res && res.ok && res.body) {
        const textStream = await createOpenAITextStream(
          res.body,
          $settings.splitLargeChunks
        );
        responseMessage.replytime = Math.floor(Date.now() / 1000);
        // 判断模型添加think头
        if (model.id == "DeepSeek-R1") {
          responseMessage.think_content = "<think>";
        }
        for await (const update of textStream) {
          const { value, done, citations, error } = update;
          if (error) {
            await handleOpenAIError(error, null, model, responseMessage);
            break;
          }
          // console.log(
          //   "value, done, citations, error",
          //   value,
          //   done,
          //   citations,
          //   error
          // );

          // 第一次响应的时候，把当前的id设置为当前响应的id
          if (value && !firstResAlready) {
            firstResAlready = true;
            history.currentId = responseMessageId;
          }

          if (done || stopResponseFlag || _chatId !== $chatId) {
            responseMessage.done = true;
            messages = messages;

            if (stopResponseFlag) {
              controller.abort("User: Stop Response");
            }

            break;
          }

          if (citations) {
            responseMessage.citations = citations;
            continue;
          }

          if (!firstResAlready && responseMessage.content.length > 0) {
            // 第一次响应的时候，把当前的id设置为当前响应的id
            console.log(
              "模型调用完毕？",
              res,
              model.id,
              firstResAlready,
              responseMessageId,
              responseMessage.content
            );

            firstResAlready = true;
            history.currentId = responseMessageId;
            await tick();
          }

          if (responseMessage.content == "" && value == "\n") {
            continue;
          } else {
            // responseMessage.content += value;
            responseMessage.content = await addTextSlowly(
              responseMessage.content,
              value
            );
            messages = messages;
          }

          if ($settings.notificationEnabled && !document.hasFocus()) {
            // const notification = new Notification(`OpenAI ${model}`, {
            // 	body: responseMessage.content,
            // 	icon: `${WEBUI_BASE_URL}/static/favicon.png`
            // });
          }

          if ($settings.responseAutoCopy) {
            copyToClipboard(responseMessage.content);
          }

          if ($settings.responseAutoPlayback) {
            await tick();
            document
              .getElementById(`speak-button-${responseMessage.id}`)
              ?.click();
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
    
    // 更新聊天记录
    if (_chatId === $chatId) {  
      if ($settings.saveChatHistory ?? true) {
        await updateChatById(localStorage.token, _chatId, {
          messages: messages,
          history: history
        });
      }
    }

    await tick();

    if (autoScroll) {
      scrollToBottom();
    }
  };

  // 校验模型是否有think思考内容
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

  // 获取搜索网页
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

  const handleOpenAIError = async (
    error,
    res: Response | null,
    model,
    responseMessage
  ) => {
    let errorMessage = "";
    let innerError;

    if (error) {
      innerError = error;
    } else if (res !== null) {
      innerError = await res.json();
    }
    console.error(innerError);
    if ("detail" in innerError) {
      toast.error(innerError.detail);
      errorMessage = innerError.detail;
    } else if ("error" in innerError) {
      if ("message" in innerError.error) {
        toast.error(innerError.error.message);
        errorMessage = innerError.error.message;
      } else {
        toast.error(innerError.error);
        errorMessage = innerError.error;
      }
    } else if ("message" in innerError) {
      toast.error(innerError.message);
      errorMessage = innerError.message;
    }

    responseMessage.error = true;
    responseMessage.content =
      $i18n.t(`Uh-oh! There was an issue connecting to {{provider}}.`, {
        provider: model.name ?? model.id,
      }) +
      "\n" +
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
    console.log("stopResponse");
  };

  const regenerateResponse = async (message) => {
    console.log("regenerateResponse");

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
    console.log("continueGeneration");
    const _chatId = JSON.parse(JSON.stringify($chatId));

    if (messages.length != 0 && messages.at(-1).done == true) {
      const responseMessage = history.messages[history.currentId];
      responseMessage.done = false;
      await tick();

      const model = $models.filter((m) => m.id === responseMessage.model).at(0);

      if (model) {
        await sendPromptDeOpenAI(model, responseMessage.id, _chatId);

        // if (model?.external) {
        // 	await sendPromptOpenAI(
        // model,
        // history.messages[responseMessage.parentId].content,
        // responseMessage.id,
        // _chatId
        // 	);
        // } else
        // 	await sendPromptOllama(
        // 		model,
        // 		history.messages[responseMessage.parentId].content,
        // 		responseMessage.id,
        // 		_chatId
        // 	);
      }
    } else {
      console.error($i18n.t(`Model {{modelId}} not found`, {}));
      // toast.error($i18n.t(`Model {{modelId}} not found`, { modelId }));
    }
  };

  const generateDeChatTitle = async (userPrompt) => {
    if ($settings?.title?.auto ?? true) {
      const model = $models.find((model) => model.id === selectedModels[0]);

      const titleModelId =
        model?.external ?? false
          ? $settings?.title?.modelExternal ?? selectedModels[0]
          : $settings?.title?.model ?? selectedModels[0];
      const title = await generateDeTitle(
        localStorage.token,
        $settings?.title?.prompt ??
          $i18n.t(
            "Create a concise, 3-5 word phrase as a header for the following query, strictly adhering to the 3-5 word limit and avoiding the use of the word 'title':"
          ) + " {{prompt}}",
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
      // 获取关键词
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
          ) + " {{prompt}}",
        titleModelId,
        userPrompt,
        titleModel?.external ?? false
          ? titleModel?.source?.toLowerCase() === "litellm"
            ? `${LITELLM_API_BASE_URL}/v1`
            : `${OPENAI_API_BASE_URL}`
          : `${OLLAMA_API_BASE_URL}/v1`
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
      chat = await updateChatById(localStorage.token, _chatId, {
        title: _title,
      });
      await chats.set(await getChatList(localStorage.token));
    }
  };

  const getTags = async () => {
    return await getTagsById(localStorage.token, $chatId).catch(
      async (error) => {
        return [];
      }
    );
  };

  const addTag = async (tagName) => {
    const res = await addTagById(localStorage.token, $chatId, tagName);
    tags = await getTags();

    chat = await updateChatById(localStorage.token, $chatId, {
      tags: tags,
    });

    _tags.set(await getAllChatTags(localStorage.token));
  };

  const deleteTag = async (tagName) => {
    const res = await deleteTagById(localStorage.token, $chatId, tagName);
    tags = await getTags();

    chat = await updateChatById(localStorage.token, $chatId, {
      tags: tags,
    });

    _tags.set(await getAllChatTags(localStorage.token));
  };
</script>

<svelte:head>
  <title>
    {title
      ? `${
          title.length > 30 ? `${title.slice(0, 30)}...` : title
        } | ${$WEBUI_NAME}`
      : `${$WEBUI_NAME}`}
  </title>
</svelte:head>

<div
  class="min-h-screen max-h-screen {$showSidebar
    ? 'md:max-w-[calc(100%-246px)]'
    : ''} w-full max-w-full flex flex-col"
>
  <Navbar
    {title}
    bind:selectedModels
    bind:showModelSelector
    shareEnabled={messages.length > 0}
    {chat}
    {initNewChat}
  />
  <div class="flex flex-col flex-auto">
    <div
      class=" pb-2.5 flex flex-col justify-between w-full flex-auto overflow-auto h-0 max-w-full"
      id="messages-container"
      bind:this={messagesContainerElement}
      on:scroll={(e) => {
        autoScroll =
          messagesContainerElement.scrollHeight -
            messagesContainerElement.scrollTop <=
          messagesContainerElement.clientHeight + 5;
      }}
    >
      <div class=" h-full w-full flex flex-col pt-2 pb-4">
        <Messages
          key={$chatId}
          chatId={$chatId}
          {selectedModels}
          {selectedModelfiles}
          {processing}
          bind:history
          bind:messages
          bind:autoScroll
          bind:prompt
          bottomPadding={files.length > 0}
          suggestionPrompts={selectedModelfile?.suggestionPrompts ??
            $config?.default_prompt_suggestions}
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
