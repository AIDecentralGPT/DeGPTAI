<script lang="ts">
  import { toast } from "svelte-sonner";
  import { v4 as uuidv4 } from "uuid";
  import { page } from "$app/stores";
  import { onMount, getContext, tick } from "svelte";

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
    switchModel,
    deApiBaseUrl,
    toolflag,
    tooltype } from "$lib/stores";
  import { copyToClipboard, addTextSlowly } from "$lib/utils";

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
  } from "$lib/apis/ollama";
  import {
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

  import { thirdSearch, getWebContent } from "$lib/apis/thirdsearch";
  import { analysisImageInfo } from "$lib/apis/rag";
    import { FilterTypeNotSupportedError } from "viem";

  let inviter: any = "";
  let channelName: any = "";

  const i18n = getContext("i18n");

  let stopResponseFlag = false;
  let autoScroll = true;
  let processing = "";
  let messagesContainerElement: HTMLDivElement;
  let currentRequestId: any = null;

  let showModelSelector = true;
  let deepsearch = false;

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
  let fileFlag = false;
  let messages = [];
  let history = {
    messages: {},
    currentId: null,
  };

  let webInfo = {url:""};

  let chatInputPlaceholder = "";

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

    // 触发直接发送消息
    if ($switchModel.status) {
      prompt = $switchModel.content;
      $toolflag = $switchModel.toolFlag;
      $tooltype = $switchModel.toolType;
      switchModel.set({content: "", toolFlag: false, toolType: 'web', status: false});
      await submitPrompt(prompt, null, $user);
    }
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
    await toolflag.set(false);
    await tooltype.set("");

    autoScroll = true;

    title = "";
    prompt = "";
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
  const submitPrompt = async (userPrompt, userToolInfo,_user = null) => {
    console.log("submitPrompt", $chatId, userPrompt);
    if (!$toolflag) {
      chatInputPlaceholder = "";
    }

    selectedModels = selectedModels.map((modelId) =>
      $models.map((m) => m.id).includes(modelId) ? modelId : ""
    );
    
    // 校验模型是否支持文件类型
    let currModel = $models.filter(item => selectedModels.includes(item?.model));
    if (files.length > 0 && (files[0].type == "image" || (files[0]?.image??[]).length > 0)) {
      if (currModel[0]?.support == "text") {
        let imageModels = $models.filter(item => item?.type == currModel[0]?.type && item?.support == "image");
        selectedModels = [imageModels[0]?.model];
      }
      fileFlag = true;
    } else {
      // 校验历史记录是否有图片
      let checkMessages = messages.filter(item => item.role == "user" && Array.isArray(item.files));
      if (checkMessages.length > 0) {
        if (currModel[0]?.support == "text") {
          let imageModels = $models.filter(item => item?.type == currModel[0]?.type && item?.support == "image");
          selectedModels = [imageModels[0]?.model];
        }
        fileFlag = true;
      } else{
        fileFlag = false;
      }
    }

    // console.log("selectedModels", selectedModels);

    // 如果开启网络搜索只选择一个模型回复
    if ($toolflag) {
      selectedModels = [selectedModels[0]];
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
        imageinfo: "",
        content: userPrompt,
        files: files.length > 0 ? files : undefined,
        toolflag: $toolflag,
        tooltype: $tooltype,
        toolInfo: userToolInfo, // 直接传过来数据
        parseInfo: "", // 解析后数据
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
            toolflag: $toolflag,
            tooltype: $tooltype,
            parseInfo: "",
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

      // Reset chat input textarea
      prompt = "";
      files = [];
      webInfo = {url:""};

      scrollToBottom();

      // 校验图片获取图片信息
      // await analysisimageinfo(userMessageId);

      // 代码有调用接口，放到try中可方便捕获异常
      try {
        // 校验模型已使用次数
        let modelLimit:any = {}
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

        // Wait until history/message have been updated
        await tick();

        // 获取工具操作内容
        if ($toolflag) {
          if ($tooltype == "webread") {
            // 网页分析
            if ((userToolInfo?.url??"").length > 0) {
              let webResult = await getWebContent(localStorage.token, userToolInfo?.url);
              if (webResult?.ok) {
                // 更新UserMessge信息
                userMessage.parseInfo = webResult?.data;
                history.messages[userMessageId] = userMessage;
              } 
              await tick();
            }
          } else if ($tooltype == "translate") {
              // 更新UserMessge信息
              userMessage.parseInfo = userToolInfo?.trantip;
              history.messages[userMessageId] = userMessage;
              await tick();
          } else {
            let searchData = await handleSearchWeb(userPrompt);

            // 更新UserMessge信息
            userMessage.parseInfo = searchData;
            history.messages[userMessageId] = userMessage;

            // 更新回复会话搜索信息
            Object.keys(responseMap).map(async (modelId) => {
              const model = $models.filter((m) => m.id === modelId).at(0);  
              if (responseMap[model?.id]) {
                let responseMessageId = responseMap[model?.id].id;
                let responseMessage = responseMap[model?.id];
                responseMessage.parseInfo = searchData;
                history.messages[responseMessageId] = responseMessage;
              }
            });
            await tick();
          }
          
          scrollToBottom();
        }

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
        await sendPrompt(userPrompt, responseMap, modelLimit);

      } catch (err) {
        const _chatId = JSON.parse(JSON.stringify($chatId));
        Object.keys(responseMap).map(async (modelId) => {
          const model = $models.filter((m) => m.id === modelId).at(0);
          let responseMessage = responseMap[model?.id];
          await handleOpenAIError(err, null, model, responseMessage);

          // 更新消息到数据库
          await updateChatMessage(responseMessage, _chatId);

          await tick();
          
          if (autoScroll) {
            scrollToBottom();
          }
        })  
      }  
    }
  };

  const sendPrompt = async (prompt, responseMap = null, modelLimit = {}, modelId = null, reload = false) => {
    const _chatId = JSON.parse(JSON.stringify($chatId));
    await Promise.all(
      (modelId ? [modelId] : atSelectedModel !== '' ? [atSelectedModel.id] : Object.keys(responseMap)).map(
        async (modelId) => {
          const model = $models.filter((m) => m.id === modelId).at(0);
          if (model) {
            // 创建响应消息
            let responseMessage = responseMap[model?.id];
            let responseMessageId = responseMessage?.id;

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
              // 文本搜索
              await sendPromptDeOpenAI(model, responseMessageId, _chatId, reload);
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
  const sendPromptDeOpenAI = async (model, responseMessageId, _chatId, reload) => {
    const responseMessage = history.messages[responseMessageId];

    // 获取上一个对应模型回复的消息(每次只选一个模型可去除)
    // const modelmessage = messages;
    // if (messages.length > 2) {
    //   let checkmessage = modelmessage[messages.length - 3];
    //   let checkchildrenIds = history.messages[checkmessage.parentId]?.childrenIds;
    //   if (checkchildrenIds) {
    //     checkchildrenIds.forEach(item => {
    //       let sonMessage = history.messages[item];
    //       if (sonMessage.model == model.id) {
    //         checkmessage.content = sonMessage.content;
    //       }
    //     });
    //   }
    // }
    
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
            ...messages,
        ].filter((message) => message);
      
      // 判断是否需要重新赋值
			send_message.forEach((item, index) => {
        // 判断不同类型提问不同内容
        if (item?.role == 'user' && item?.toolflag) {
          if (item?.tooltype == "webread") {
            let analyContent = "网页标题：" + item?.parseInfo?.title;
            analyContent = "；网页内容：" + item?.parseInfo?.content;
            analyContent = analyContent + "\n" + item?.content;
            item.content = analyContent;
          } else if (item?.tooltype == "translate") {
            let analyContent = item?.content + "\n" + item?.parseInfo;
            item.content = analyContent;
          } else if (item?.tooltype == "youtube") {
						if (item?.parseInfo?.videos) {
							let analyContent = item?.parseInfo?.videos.map((vItem: any) => vItem?.description).join('\n');
							analyContent = analyContent + "\n" + $i18n.t("Summarize based on the above YouTube search results:");
							item.content = analyContent + item.content;
						}
          } else if (item?.tooltype == "twitter") {
						if (item?.parseInfo?.content) {
							let analyContent = item?.parseInfo?.content.map((tItem: any) => tItem?.full_text).join('\n');
							analyContent = analyContent + "\n" + $i18n.t("Summarize based on the above Twitter search results:");
							item.content = analyContent + item.content;
						}
          } else if (item?.tooltype == "bing") {
						if (item?.parseInfo?.web) {
							let analyContent = item?.parseInfo?.web.map((wItem: any) => wItem?.content).join('\n');
							analyContent = analyContent + "\n" + $i18n.t("Summarize based on the above web search results:");
							item.content = analyContent + item.content;
						}
          }
        } 
        // else if (item?.role != 'user' && docs.length > 0) {
        //   if (docs[0].image.length > 0) {
        //     let content = [];
        //     if (docs[0].text[0]?.page_content.length > 0) {
        //       let analyContent = "";
        //       docs[0].text.forEach(item => {
        //         analyContent = analyContent + item?.page_content + "\n";
        //       });
        //       content.push({type: "text", text: "文档内容：" + analyContent + send_message[index-1].content});
        //     } else {
        //       content.push({type: "text", text: send_message[index-1].content});
        //     }
        //     content.push({type: "image_url", image_url: {url: docs[0].image[0]}});
        //     send_message[index-1].content = content;
        //   } else {
        //     let analyContent = "";
        //     docs[0].text.forEach(item => {
        //         analyContent = analyContent + item?.page_content + "\n";
        //     });
        //     send_message[index-1].content = "文档内容：" + analyContent + send_message[index-1].content;
        //   }
        // }
      });
			// 过滤掉error和 content为空数据
			send_message = send_message.filter(item =>!item.error).filter(item=> item.content != "");

      // 处理图片文件消息
      send_message = send_message.map((message, idx, arr) => ({
        role: message.role,
        ...((message.files?.filter((file) => file.type === "image" || file.type === "doc").length > 0 ?? false) &&
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
                  .filter((file) => file.type === "image" || file.type === "doc")
                    .map((file) => (
                      file.type === "image" ?
                      {
                        type: "image_url",
                        image_url: {
                          url: file.url,
                        },
                      } : {
                        type: "file",
                        file: {
                          filename: file.name,
                          file_data: file.url,
                        },
                      }
                    )),
              ],
            }
          : {
            content:
              arr.length - 1 !== idx
                ? message.content
                : message?.raContent ?? message.content,
          }),
      }));

      // 发送内容添加 nothink 内容
      // if (!model.think && model.id == "Qwen3-235B-A22B-FP8") {
      //   send_message[send_message.length-1].content = "/nothink" + send_message[send_message.length-1].content;
      // }
      const [res, controller] = await generateDeOpenAIChatCompletion(
        localStorage.token,
        {
          model: fileFlag ? model.imagemodel : model.textmodel,
          messages: send_message,
          enable_thinking: model.think,
          reload: reload,
          audio: false
        },
        $deApiBaseUrl?.url,
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
        // 重新加载提示取消
        if (reload) {
          responseMessage.reload = false;
        }
        const textStream = await createOpenAITextStream(
          res.body,
          $settings.splitLargeChunks
        );
        responseMessage.replytime = Math.floor(Date.now() / 1000);
        // 判断模型添加think头
        let first_think = false;
        if (model.think) {
          responseMessage.think_content = "<think>";
        }

        for await (const update of textStream) {
          let { value, audio, done, citations, error, think } = update;
          // 校验是否思考过程
          if (model.think && think) {
            first_think = true;
          }
          if (model.think && first_think && !think) {
            first_think = false;
            responseMessage.content = await addTextSlowly(
              (text: string) => {
                responseMessage.content = text;
              },
              responseMessage.content,
              "</think>",
              model.id,
            );
            messages = messages;
          }

          // 赋值语音模型
          if (responseMessage.audio) {
            responseMessage.audio = audio
          } else {
            responseMessage.audio = responseMessage.audio + audio
          }
          
  
          // if (value.includes("：")) {
          //   console.log("=================", value);
          //   error = "测试错误";
          // }

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
              (text: string) => {
                responseMessage.content = text;
              },
              responseMessage.content,
              value,
              model.id
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
        console.log("=====================================")
      } else {
        await handleOpenAIError(null, res, model, responseMessage);
      }
    } catch (error) {
      await handleOpenAIError(error, null, model, responseMessage);
    }

    // 更新消息到数据库
    await updateChatMessage(responseMessage, _chatId);

    await tick();

    if (autoScroll) {
      scrollToBottom();
    }
  };

  // 更新消息到数据库
  const updateChatMessage = async (responseMessage: any, _chatId) => {
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
  }

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
  const handleSearchWeb= async(userPrompt: string) => {
    const ai_keyword = await generateSearchChatKeyword(userPrompt);
    let result = await thirdSearch(localStorage.token, ai_keyword, $tooltype);
    if (result?.ok) {
      return result.data;
    } else {
      return "";
    }
  }

  // 获取图片描述
  const analysisimageinfo = async(messageId: string) => {
    let userMessage = history.messages[messageId];
    if (userMessage.files) {
      if (userMessage.files.length > 0 && (userMessage.files[0].type == "image" || (userMessage.files[0]?.image??[]).length > 0)) {
        let result = await analysisImageInfo(localStorage.token, userMessage.files[0].url);
        userMessage.imageinfo = result;
        history.messages[messageId] = userMessage;
      }
    }
    await tick();
  }

  const handleOpenAIError = async (
    error,
    res: Response | null,
    model,
    responseMessage
  ) => {
    // let errorMessage = "";
    // let innerError;

    // if (error) {
    //   innerError = error;
    // } else if (res !== null) {
    //   innerError = await res.json();
    // }
    // console.error(innerError);
    // if ("detail" in innerError) {
    //   toast.error(innerError.detail);
    //   errorMessage = innerError.detail;
    // } else if ("error" in innerError) {
    //   if ("message" in innerError.error) {
    //     toast.error(innerError.error.message);
    //     errorMessage = innerError.error.message;
    //   } else {
    //     toast.error(innerError.error);
    //     errorMessage = innerError.error;
    //   }
    // } else if ("message" in innerError) {
    //   toast.error(innerError.message);
    //   errorMessage = innerError.message;
    // }

    responseMessage.error = true;
    responseMessage.errmsg = "It seems that you are offline. Please reconnect to send messages.";
      // $i18n.t(`Uh-oh! There was an issue connecting to {{provider}}.`, {
      //   provider: model.name ?? model.id,
      // }) +
      // "\n" +
      // errorMessage;
    responseMessage.done = true;
    messages = messages;
  };

  const handleLimitError = async (content: string, responseMessage: any) => {
    responseMessage.content = $i18n.t(content);
    responseMessage.replytime = Math.floor(Date.now() / 1000);
    responseMessage.warning = true;
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
        await sendPromptDeOpenAI(model, responseMessage.id, _chatId, false);

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
      let send_messages = messages.filter(item => item.content != '')
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
          messagesContainerElement.clientHeight + 45;
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
          bind:chatInputPlaceholder
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
  bind:webInfo
  bind:deepsearch
  bind:prompt
  bind:autoScroll
  bind:chatInputPlaceholder
  bind:selectedModel={atSelectedModel}
  {messages}
  {submitPrompt}
  {stopResponse}
/>