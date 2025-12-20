<script lang="ts">
  import { toast } from 'svelte-sonner';
  import tippy from 'tippy.js';
  import auto_render from 'katex/dist/contrib/auto-render.mjs';
  import 'katex/dist/katex.min.css';
  import SearchResults from './ResponseMessage-modules/SearchResults.svelte';
  import MessageContentEdit from './ResponseMessage-modules/MessageContent-edit.svelte';
  import MessageStatus from './ResponseMessage-modules/MessageStatus.svelte';
  import MessageCitations from './ResponseMessage-modules/MessageCitations.svelte';
  import ActionButtons from './ResponseMessage-modules/ActionButtons.svelte';

  import { createEventDispatcher } from 'svelte';
  import { onMount, tick, getContext } from 'svelte';

  const dispatch = createEventDispatcher();

  import { settings, theme } from '$lib/stores';

  import { synthesizeOpenAISpeech } from '$lib/apis/audio';
  import { imageGenerations } from '$lib/apis/images';
  import { approximateToHumanReadable, extractSentences } from '$lib/utils';
  import TopText from './ResponseMessage-modules/top-text.svelte';
  import ProfileImage from './ProfileImage.svelte';
  import Image from '$lib/components/common/Image.svelte';
  import RateComment from './RateComment.svelte';
  import CitationsModal from '$lib/components/chat/Messages/CitationsModal.svelte';
  import { initAudioContext } from '$lib/utils/player/index';

  export let modelfiles = [];
  export let message;
  export let siblings;

  export let isLastMessage = true;

  export let readOnly = false;

  // 重新获取会话
  export let resentMessage: Function;

  export let updateChatMessages: Function;
  export let confirmEditResponseMessage: Function;
  export let showPreviousMessage: Function;
  export let showNextMessage: Function;
  export let rateMessage: Function;

  export let copyToClipboard: Function;
  export let continueGeneration: Function;
  export let regenerateResponse: Function;

  // ... 原有的变量 ...
  let isContinuing = false; // 1. 新增：用于标记是否正在请求继续生成
  let previousContentLength = 0; // 1. 新增：用于记录上一次的内容长度，判断是否有新内容生成

  // 定义一个变量记录点击时的长度
  let continueStartLength = 0;

  $: if (message) {
    // 1. 音频处理 (不变)
    if (message?.audio) {
      PCM_BASE64 = message?.audio;
    }

    // 2. 🔴 彻底解决闪烁问题 🔴
    // 逻辑：AI 正在生成时(done=false)，我们什么都不做，只让 Markdown 文本自然流出。
    // 只有当 AI 彻底说完话(done=true)时，我们才执行一次昂贵的渲染(数学公式+提示框)。
    // 这样就绝对不会闪烁了。
    if (message.done) {
      // 使用 setTimeout 确保 DOM 已经更新完毕后再渲染 LaTeX
      setTimeout(() => {
        renderStyling();
      }, 50);
    }

    // 3. 🔴 彻底解决按钮提前显示问题 🔴
    // 只有当：(处于继续模式) 且 (消息已完成 或 出错)
    if (isContinuing && (message.done || message.error)) {
      // 只有当现在的长度 大于 点击时的长度，才说明生成了新东西且结束了
      // 或者如果出错了，也停止 loading
      if (message.content.length > continueStartLength || message.error) {
        isContinuing = false;
      }
    }
  }

  let edit = false;
  let editedContent = '';
  let tooltipInstance = null;

  let sentencesAudio = {};
  let speaking = null;
  let speakingIdx = null;

  let loadingSpeech = false;
  let generatingImage = false;

  let showRateComment = false;
  let showCitationModal = false;

  let selectedCitation = null;
  let PCM_BASE64: string = '';

  // $: if (message) {
  //   renderStyling();
  //   if (message?.audio) {
  //     PCM_BASE64 = message?.audio;
  //   }
  // }

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
            Math.round(((message.info.eval_count ?? 0) / (message.info.eval_duration / 1000000000)) * 100) / 100
          } tokens` ?? 'N/A'
        }<br/>
					prompt_token/s: ${
            Math.round(
              ((message.info.prompt_eval_count ?? 0) / (message.info.prompt_eval_duration / 1000000000)) * 100
            ) / 100 ?? 'N/A'
          } tokens<br/>
                    total_duration: ${
                      Math.round(((message.info.total_duration ?? 0) / 1000000) * 100) / 100 ?? 'N/A'
                    }ms<br/>
                    load_duration: ${
                      Math.round(((message.info.load_duration ?? 0) / 1000000) * 100) / 100 ?? 'N/A'
                    }ms<br/>
                    prompt_eval_count: ${message.info.prompt_eval_count ?? 'N/A'}<br/>
                    prompt_eval_duration: ${
                      Math.round(((message.info.prompt_eval_duration ?? 0) / 1000000) * 100) / 100 ?? 'N/A'
                    }ms<br/>
                    eval_count: ${message.info.eval_count ?? 'N/A'}<br/>
                    eval_duration: ${
                      Math.round(((message.info.eval_duration ?? 0) / 1000000) * 100) / 100 ?? 'N/A'
                    }ms<br/>
                    approximate_total: ${approximateToHumanReadable(message.info.total_duration)}</span>`,
        allowHTML: true,
      });
    }
  };
  const renderLatex = () => {
    let chatMessageElements = document
      .getElementById(`message-${message.id}`)
      ?.getElementsByClassName('chat-assistant');

    if (chatMessageElements) {
      for (const element of chatMessageElements) {
        try {
          auto_render(element, {
            delimiters: [
              { left: '$$', right: '$$', display: false },
              { left: '$ ', right: ' $', display: false },
              { left: '\\(', right: '\\)', display: false },
              { left: '\\[', right: '\\]', display: false },
              { left: '[ ', right: ' ]', display: false },
            ],
            throwOnError: false,
          });
        } catch (e) {
          console.error('[KaTeX] 渲染报错:', e);
        }
      }
    } else {
      console.warn('[KaTeX] 找不到 DOM 节点，无法渲染');
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

            const voice = voices?.filter((v) => v.name === $settings?.audio?.speaker)?.at(0) ?? undefined;

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

  // 只需要这样
  const editMessageHandler = async () => {
    edit = true;
    editedContent = message.content;
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
        url: `${image.url}`,
      }));

      dispatch('save', message);
    }

    generatingImage = false;
  };

  onMount(async () => {
    await tick();
    renderStyling();
    await initAudioContext();
  });

  // 监听主题变化
  let currentTheme = $theme;
  $: {
    currentTheme = $theme === 'system' || $theme === 'light' ? 'light' : 'dark';
  }

  // 1. 监听页面可见性 (必须有，否则 Svelte 不知道你切回来了)
  let isPageVisible = true;

  onMount(() => {
    const updateVis = () => {
      isPageVisible = document.visibilityState === 'visible';
    };
    // 初始化检测一次
    updateVis();

    return () => document.removeEventListener('visibilitychange', updateVis);
  });

  // 2. 核心逻辑：自动点击“重连”
  // 只要同时满足：页面可见 + 是最后一条 + 报错了 -> 自动重试
  $: if (isPageVisible && isLastMessage && message?.error === true) {
    console.log('检测到连接中断报错，正在自动点击重连...');

    // 这里的 resentMessage 会把 message.error 变成 false，
    // 所以这个 if 里的代码只会执行一次，不会死循环。
    resentMessage(message?.parentId, true);
  }
  $: if (message) {
    console.log('检测到连接中断报错，正在自动点击重连...', message);

    // 这里的 resentMessage 会把 message.error 变成 false，
    // 所以这个 if 里的代码只会执行一次，不会死循环。
    // resentMessage(message?.parentId, true);
  }
</script>

<CitationsModal bind:show={showCitationModal} citation={selectedCitation} />
<div class=" flex w-full message-{message.id}" id="message-{message.id}" dir={$settings.chatDirection}>
  <ProfileImage src="/favicon.png" />

  <div class="w-full overflow-hidden pl-1">
    <!-- 顶部模型以及时间 -->
    <TopText {message} {modelfiles} />

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
    <!-- 工具检索 -->
    {#if message?.toolflag}
      <SearchResults {message} />
    {/if}

    <!-- 文本输出 -->
    <div
      class="prose chat-{message.role} w-full max-w-full dark:prose-invert prose-headings:my-0 prose-p:m-0 prose-p:-mb-6 prose-pre:my-0 prose-table:my-0 prose-blockquote:my-0 prose-img:my-0 prose-ul:-my-4 prose-ol:-my-4 prose-li:-my-3 prose-ul:-mb-6 prose-ol:-mb-8 prose-ol:p-0 prose-li:-mb-4 whitespace-pre-line"
    >
      <div>
        {#if edit === true}
          <!-- 编辑保存 -->
          <MessageContentEdit {message} bind:editedContent {cancelEditMessage} {editMessageConfirmHandler} />
        {:else}
          <div class="w-full">
            <!-- 显示任何状态 -->
            <MessageStatus {message} {isLastMessage} {resentMessage} {isContinuing} />

            <!-- 点击引用 -> 弹窗查看详情 -->
            {#if message.citations}
              <MessageCitations
                {message}
                on:click={(e) => {
                  selectedCitation = e.detail; // e.detail 就是子组件传出来的 citation
                  showCitationModal = true;
                }}
              />
            {/if}
            <ActionButtons
              {message}
              {siblings}
              {isLastMessage}
              {readOnly}
              {loadingSpeech}
              {speaking}
              {generatingImage}
              {isContinuing}
              on:showPrevious={() => showPreviousMessage(message)}
              on:showNext={() => showNextMessage(message)}
              on:edit={() => editMessageHandler()}
              on:copy={() => copyToClipboard(message.content, true)}
              on:image={() => generateImage(message)}
              on:regenerate={() => resentMessage(message?.parentId)}
              on:rate={(e) => {
                rateMessage(message.id, e.detail);
                showRateComment = true;
                window.setTimeout(() => {
                  document.getElementById(`message-feedback-${message.id}`)?.scrollIntoView();
                }, 0);
              }}
              on:speak={async () => {
                toggleSpeakMessage();
              }}
              on:continue={async () => {
                // --- 🟢 这里是关键修改 ---
                // 1. 记录当前文本长度（作为起跑线）
                continueStartLength = message.content.length;
                // 2. 立即开启 Loading 状态
                isContinuing = true;
                // 3. 开始请求
                await continueGeneration();
              }}
            />

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
