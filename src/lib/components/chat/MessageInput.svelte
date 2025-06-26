<script lang="ts">
  import { toast } from "svelte-sonner";
  import { onMount, tick, getContext } from "svelte";
  import {
    mobile,
    modelfiles,
    settings,
    showNewWalletModal,
    showOpenWalletModal,
    showSidebar,
    toolflag,
    tooltype
  } from "$lib/stores";
  import { blobToFile, findWordIndices, checkPlatform } from "$lib/utils";

  import {
    uploadDocToVectorDB,
    uploadWebToVectorDB,
    uploadYoutubeTranscriptionToVectorDB,
  } from "$lib/apis/rag";
  import {
    SUPPORTED_FILE_TYPE,
    SUPPORTED_FILE_EXTENSIONS,
    WEBUI_BASE_URL,
  } from "$lib/constants";

  import { transcribeAudio } from "$lib/apis/audio";

  import Prompts from "./MessageInput/PromptCommands.svelte";
  import AddFilesPlaceholder from "../AddFilesPlaceholder.svelte";
  import Documents from "./MessageInput/Documents.svelte";
  import Models from "./MessageInput/Models.svelte";
  import UrlModels from "./MessageInput/UrlModels.svelte";
  import Tools from "./MessageInput/Tools.svelte";
  import ToolsSelect from "./MessageInput/ToolsSelect.svelte";
  import Tooltip from "../common/Tooltip.svelte";
  import XMark from "$lib/components/icons/XMark.svelte";
  import { user as userStore } from "$lib/stores";
  import FileSvg from '$lib/components/chat/Messages/FileSvg.svelte';

  const i18n = getContext("i18n");

  export let submitPrompt: Function;
  export let stopResponse: Function;

  export let autoScroll = true;
  export let selectedModel = "";
  // export let deepsearch = false;

  let chatTextAreaElement: HTMLTextAreaElement;
  let filesInputElement: any;

  let promptsElement: any;
  let documentsElement: any;
  let modelsElement: any;
  let urlPromptElement: any;

  let inputFiles: any;
  let dragged = false;

  let user: any = null;

  // 文件选择
  export let files: any[] = [];
  export let toolInfo: any = {url: "", trantip: ""};

  export let fileUploadEnabled = true;
  // export let speechRecognitionEnabled = true;

  export let prompt = "";
  export let chatInputPlaceholder = "";
  export let messages: any[] = [];

  // 要翻译的语言
  let tranlang = "";

  let speechRecognition: any;
  

  let selectUrlUserPrompt = [
		"Analyze the content of the web page",
    "Summarize the web page",
    "Extract the key data from the web page",
		"Tell me what the web page is about",
		"Write an original article referring to the web page"
	];

  $: if (prompt) {
    if (chatTextAreaElement) {
      chatTextAreaElement.style.height = "";
      chatTextAreaElement.style.height =
        Math.min(chatTextAreaElement.scrollHeight, 200) + "px";
    }
  }

  $: if(chatInputPlaceholder) {
    if (chatTextAreaElement) {
      chatTextAreaElement.style.height = "";
      chatTextAreaElement.style.height =
        Math.min(chatTextAreaElement.scrollHeight, 200) + "px";
    }
  }

  $: if (toolflag) {
    files = [];
  }

  let mediaRecorder: any;
  let audioChunks: any[] = [];
  let isRecording = false;
  const MIN_DECIBELS = -45;

  const scrollToBottom = () => {
    const element = document.getElementById("messages-container");
    element.scrollTop = element.scrollHeight;
  };

  const startRecording = async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);
    mediaRecorder.onstart = () => {
      isRecording = true;
      console.log("Recording started");
    };
    mediaRecorder.ondataavailable = (event) => audioChunks.push(event.data);
    mediaRecorder.onstop = async () => {
      isRecording = false;
      console.log("Recording stopped");

      // Create a blob from the audio chunks
      const audioBlob = new Blob(audioChunks, { type: "audio/wav" });

      const file = blobToFile(audioBlob, "recording.wav");

      const res = await transcribeAudio(localStorage.token, file).catch(
        (error) => {
          toast.error(error);
          return null;
        }
      );

      if (res) {
        prompt = res.text;
        await tick();
        chatTextAreaElement?.focus();

        if (prompt !== "" && $settings?.speechAutoSend === true) {
          submitPrompt(prompt, toolInfo, user);
        }
      }

      // saveRecording(audioBlob);
      audioChunks = [];
    };

    // Start recording
    mediaRecorder.start();

    // Monitor silence
    monitorSilence(stream);
  };

  const monitorSilence = (stream) => {
    const audioContext = new AudioContext();
    const audioStreamSource = audioContext.createMediaStreamSource(stream);
    const analyser = audioContext.createAnalyser();
    analyser.minDecibels = MIN_DECIBELS;
    audioStreamSource.connect(analyser);

    const bufferLength = analyser.frequencyBinCount;
    const domainData = new Uint8Array(bufferLength);

    let lastSoundTime = Date.now();

    const detectSound = () => {
      analyser.getByteFrequencyData(domainData);

      if (domainData.some((value) => value > 0)) {
        lastSoundTime = Date.now();
      }

      if (isRecording && Date.now() - lastSoundTime > 3000) {
        mediaRecorder.stop();
        audioContext.close();
        return;
      }

      window.requestAnimationFrame(detectSound);
    };

    window.requestAnimationFrame(detectSound);
  };

  const saveRecording = (blob) => {
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    document.body.appendChild(a);
    a.style = "display: none";
    a.href = url;
    a.download = "recording.wav";
    a.click();
    window.URL.revokeObjectURL(url);
  };

  const speechRecognitionHandler = () => {
    // Check if SpeechRecognition is supported

    if (isRecording) {
      if (speechRecognition) {
        speechRecognition.stop();
      }

      if (mediaRecorder) {
        mediaRecorder.stop();
      }
    } else {
      isRecording = true;

      if ($settings?.audio?.STTEngine ?? "" !== "") {
        startRecording();
      } else {
        if (
          "SpeechRecognition" in window ||
          "webkitSpeechRecognition" in window
        ) {
          // Create a SpeechRecognition object
          speechRecognition = new (window.SpeechRecognition ||
            window.webkitSpeechRecognition)();

          // Set continuous to true for continuous recognition
          speechRecognition.continuous = true;

          // Set the timeout for turning off the recognition after inactivity (in milliseconds)
          const inactivityTimeout = 3000; // 3 seconds

          let timeoutId;
          // Start recognition
          speechRecognition.start();

          // Event triggered when speech is recognized
          speechRecognition.onresult = async (event) => {
            // Clear the inactivity timeout
            clearTimeout(timeoutId);

            // Handle recognized speech
            console.log(event);
            const transcript =
              event.results[Object.keys(event.results).length - 1][0]
                .transcript;

            prompt = `${prompt}${transcript}`;

            await tick();
            chatTextAreaElement?.focus();

            // Restart the inactivity timeout
            timeoutId = setTimeout(() => {
              console.log("Speech recognition turned off due to inactivity.");
              speechRecognition.stop();
            }, inactivityTimeout);
          };

          // Event triggered when recognition is ended
          speechRecognition.onend = function () {
            // Restart recognition after it ends
            console.log("recognition ended");
            isRecording = false;
            if (prompt !== "" && $settings?.speechAutoSend === true) {
              submitPrompt(prompt, toolInfo, user);
            }
          };

          // Event triggered when an error occurs
          speechRecognition.onerror = function (event) {
            console.log(event);
            toast.error(
              $i18n.t(`Speech recognition error: {{error}}`, {
                error: event.error,
              })
            );
            isRecording = false;
          };
        } else {
          toast.error(
            $i18n.t("SpeechRecognition API is not supported in this browser.")
          );
        }
      }
    }
  };

  const uploadDoc = async (file) => {
    console.log(file);

    const doc = {
      type: "doc",
      name: file.name,
      collection_name: "",
      anaylis_type: "file",
      upload_status: false,
      text: "",
      image: [],
      error: "",
    };

    try {
      // files = [...files, doc];
      files = [doc];
      if (["audio/mpeg", "audio/wav"].includes(file["type"])) {
        const res = await transcribeAudio(localStorage.token, file).catch(
          (error) => {
            toast.error(error);
            return null;
          }
        );

        if (res) {
          console.log(res);
          const blob = new Blob([res.text], { type: "text/plain" });
          file = blobToFile(blob, `${file.name}.txt`);
        }
      }

      const res = await uploadDocToVectorDB(localStorage.token, "", file);

      if (res) {
        doc.upload_status = true;
        doc.collection_name = res.collection_name;
        doc.anaylis_type = res.anaylis_type
        doc.text = res.text;
        doc.image = res.image;
        files = files;
      }
    } catch (e) {
      // Remove the failed doc from the files array
      files = files.filter((f) => f.name !== file.name);
      toast.error(e);
    }
  };

  const uploadWeb = async (url) => {
    console.log(url);

    const doc = {
      type: "doc",
      name: url,
      collection_name: "",
      upload_status: false,
      url: url,
      error: "",
    };

    try {
      files = [...files, doc];
      const res = await uploadWebToVectorDB(localStorage.token, "", url);

      if (res) {
        doc.upload_status = true;
        doc.collection_name = res.collection_name;
        files = files;
      }
    } catch (e) {
      // Remove the failed doc from the files array
      files = files.filter((f) => f.name !== url);
      toast.error(e);
    }
  };

  const uploadYoutubeTranscription = async (url) => {
    console.log(url);

    const doc = {
      type: "doc",
      name: url,
      collection_name: "",
      upload_status: false,
      url: url,
      error: "",
    };

    try {
      files = [...files, doc];
      const res = await uploadYoutubeTranscriptionToVectorDB(
        localStorage.token,
        url
      );

      if (res) {
        doc.upload_status = true;
        doc.collection_name = res.collection_name;
        files = files;
      }
    } catch (e) {
      // Remove the failed doc from the files array
      files = files.filter((f) => f.name !== url);
      toast.error(e);
    }
  };

  onMount(() => {
    // window.setTimeout(() => chatTextAreaElement?.focus(), 0);

    const dropZone = document.querySelector("body");

    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === "Escape") {
        console.log("Escape");
        dragged = false;
      }
    };

    const onDragOver = (e) => {
      e.preventDefault();
      dragged = true;
    };

    const onDragLeave = () => {
      dragged = false;
    };

    const onDrop = async (e) => {
      e.preventDefault();
      console.log(e);

      if (e.dataTransfer?.files) {
        const inputFiles = Array.from(e.dataTransfer?.files);

        if (inputFiles && inputFiles.length > 0) {
          inputFiles.forEach((file) => {
            if (["image/gif", "image/webp", "image/jpeg", "image/png"].includes(file["type"])) {
              let reader = new FileReader();
              reader.onload = (event) => {
                const img = new Image();
                img.onload = function() {
                  const canvas = document.createElement('canvas');
                  let ctx = canvas.getContext('2d');
                  canvas.width = img.width;
                  canvas.height = img.height;
                  ctx?.drawImage(img, 0, 0);
                  let compressedDataUrl;
                  let quality = 1; // 初始质量为 1，表示无损
                  while (true) {
                    compressedDataUrl = canvas.toDataURL(file?.type, quality);
                    if (compressedDataUrl.length <= 300 * 1024) {
                      break;
                    }
                    quality -= 0.1; // 逐渐降低质量
                    if (quality < 0) {
                      break; // 防止质量过低
                    }
                  }
                  files = [
                    ...files,
                    {
                      type: "image",
                      url: compressedDataUrl,
                    },
                  ];
                };
                img.src = event.target.result;
              };
              reader.readAsDataURL(file);
            } else if (
              SUPPORTED_FILE_TYPE.includes(file["type"]) ||
              SUPPORTED_FILE_EXTENSIONS.includes(file.name.split(".").at(-1))
            ) {
              uploadDoc(file);
            } else {
              toast.error(
                $i18n.t(
                  `Unknown File Type {{file_type}}, but accepting and treating as plain text`,
                  { file_type: file["type"] }
                )
              );
              uploadDoc(file);
            }
          });
        } else {
          toast.error($i18n.t(`File not found.`));
        }
      }

      dragged = false;
    };

    window.addEventListener("keydown", handleKeyDown);

    dropZone?.addEventListener("dragover", onDragOver);
    dropZone?.addEventListener("drop", onDrop);
    dropZone?.addEventListener("dragleave", onDragLeave);

    return () => {
      window.removeEventListener("keydown", handleKeyDown);

      dropZone?.removeEventListener("dragover", onDragOver);
      dropZone?.removeEventListener("drop", onDrop);
      dropZone?.removeEventListener("dragleave", onDragLeave);
    };
  });

  // const know_ext = ".gif,.webp,.jpeg,.png,.jpg,.pdf,.ppt,.pptx,.doc,.docx,.rtf,.xls,.xlsx,.csv,.txt," + 
  //   ".log,.xml,.ini,.json,.md,.html,.htm,.css,.ts,.js,.cpp,.asp,.aspx,.config,.sql,.plsql,.py,.go,.vue,.java,.c," + 
  //   ".cs,.h,.hsc,.bash,.swift,.svelte,.env,.r,.lua,.m,.mm,.perl,.rb,.rs,.db2,.scala,.dockerfile,.yml,.zip,.rar";
  const know_ext = "image/*,application/pdf,application/msword,application/vnd.ms-powerpoint,application/vnd.ms-excel,text/*," +
         "text/markdown,text/html,text/css,application/javascript,text/x-csrc,text/x-c++,text/x-python," +
         "text/x-java-source,text/x-csharp,text/x-shellscript,text/x-swift,application/x-zip-compressed,application/x-rar-compressed"
</script>

{#if dragged}
  <div
    class="fixed {$showSidebar
      ? 'left-0 md:left-[246px] md:w-[calc(100%-246px)]'
      : 'left-0'}  w-full h-full flex z-50 touch-none pointer-events-none"
    id="dropzone"
    role="region"
    aria-label="Drag and Drop Container"
  >
    <div
      class="absolute w-full h-full backdrop-blur bg-gray-800/40 flex justify-center"
    >
      <div class="m-auto pt-64 flex flex-col justify-center">
        <div class="max-w-md">
          <AddFilesPlaceholder />
        </div>
      </div>
    </div>
  </div>
{/if}

<div
  class="fixed bottom-0 {$showSidebar
    ? 'left-0 md:left-[246px]'
    : 'left-0'} right-0"
>
  <div class="w-full">
    <div
      class="px-2.5 md:px-16 -mb-0.5 mx-auto inset-x-0 bg-transparent flex justify-center"
    >
      <div class="flex flex-col w-full">
        <div class="relative">
          {#if autoScroll === false && messages.length > 0}
            <div
              class=" absolute -top-12 left-0 right-0 flex justify-center z-30"
            >
              <button
                class=" bg-white border border-gray-100 dark:border-none dark:bg-white/20 p-1.5 rounded-full"
                on:click={() => {
                  autoScroll = true;
                  scrollToBottom();
                }}
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                  class="w-5 h-5"
                >
                  <path
                    fill-rule="evenodd"
                    d="M10 3a.75.75 0 01.75.75v10.638l3.96-4.158a.75.75 0 111.08 1.04l-5.25 5.5a.75.75 0 01-1.08 0l-5.25-5.5a.75.75 0 111.08-1.04l3.96 4.158V3.75A.75.75 0 0110 3z"
                    clip-rule="evenodd"
                  />
                </svg>
              </button>
            </div>
          {/if}
        </div>

        <div class="w-full relative">
          {#if prompt.charAt(0) === "/"}
            <Prompts bind:this={promptsElement} bind:prompt />
          {:else if prompt.charAt(0) === "#"}
            <Documents
              bind:this={documentsElement}
              bind:prompt
              on:youtube={(e) => {
                console.log(e);
                uploadYoutubeTranscription(e.detail);
              }}
              on:url={(e) => {
                console.log(e);
                uploadWeb(e.detail);
              }}
              on:select={(e) => {
                console.log(e);
                files = [
                  ...files,
                  {
                    type: e?.detail?.type ?? "doc",
                    ...e.detail,
                    upload_status: true,
                  },
                ];
              }}
            />
          {/if}

          <!-- 屏蔽调@弹出model选择 -->
          <!-- <Models
            bind:this={modelsElement}
            bind:prompt
            bind:user
            bind:chatInputPlaceholder
            {messages}
            on:select={(e) => {
              selectedModel = e.detail;
              chatTextAreaElement?.focus();
            }}
          /> -->

          {#if selectedModel !== ""}
            <div
              class="px-3 py-2.5 text-left w-full flex justify-between items-center absolute bottom-0 left-0 right-0 bg-gradient-to-t from-50% from-white dark:from-gray-900"
            >
              <div class="flex items-center gap-2 text-sm dark:text-gray-500">
                <img
                  crossorigin="anonymous"
                  alt="model profile"
                  class="size-5 max-w-[28px] object-cover rounded-full"
                  src={$modelfiles.find(
                    (modelfile) => modelfile.tagName === selectedModel.id
                  )?.imageUrl ??
                    ($i18n.language === "dg-DG"
                      ? `/doge.png`
                      : `${WEBUI_BASE_URL}/static/favicon.png`)}
                />
                <div>
                  Talking to <span class=" font-medium"
                    >{selectedModel.name}
                  </span>
                </div>
              </div>
              <div>
                <button
                  class="flex items-center"
                  on:click={() => {
                    selectedModel = "";
                  }}
                >
                  <XMark />
                </button>
              </div>
            </div>
          {/if}
          {#if $toolflag}
            <UrlModels
              bind:this={urlPromptElement}
              bind:prompt
              bind:selectUrlUserPrompt={selectUrlUserPrompt}
              on:select={(e) => {
                let selectedUserPrompt = e.detail.prompt;
                let analysisUrl = e.detail.url;
                submitPrompt(selectedUserPrompt, {url: analysisUrl}, user);
              }}
            />
          {/if}
        </div>
      </div>
    </div>

    <div class="bg-white dark:bg-gray-900">
      <div class="px-2.5 md:px-20 mx-auto inset-x-0">
        {#if messages?.filter((item) => item.role === "assistant").length >= 5 && $userStore?.role === "visitor"}
          <div
            class="flex gap-1 items-center flex-wrap flex-1 justify-between mb-2 p-4 px-6 bg-gray-50 hover:bg-gray-100 dark:bg-gray-850 dark:hover:bg-gray-800 rounded-3xl transition group"
          >
            <span>
              {$i18n.t(
                "Get smarter replies, upload files and pictures, and enjoy more features."
              )}
            </span>

            <div class="flex gap-2">
              <button
                class=" px-2 py-1 primaryButton text-gray-100 transition rounded-lg"
                on:click={async () => {
                  $showOpenWalletModal = true;
                }}
              >
                {$i18n.t("Open Wallet")}
              </button>

              <button
                class=" px-2 py-1 primaryButton text-gray-100 transition rounded-lg"
                on:click={async () => {
                  $showNewWalletModal = true;
                }}
              >
                {$i18n.t("Create Wallet")}
              </button>
            </div>
          </div>
        {/if}

        <div class=" pb-4">
          <input
            bind:this={filesInputElement}
            bind:files={inputFiles}
            type="file"
            accept={know_ext}
            hidden
            on:change={() => {
              if (inputFiles && inputFiles.length > 0) {
                const _inputFiles = Array.from(inputFiles);
                _inputFiles.forEach((file) => {
                  if (["image/gif","image/webp","image/jpeg","image/png"].includes(file["type"])) {
                    let reader = new FileReader();
                    reader.onload = (event) => {
                      const img = new Image();
                      img.onload = function() {
                        const canvas = document.createElement('canvas');
                        let ctx = canvas.getContext('2d');
                        canvas.width = img.width;
                        canvas.height = img.height;
                        ctx?.drawImage(img, 0, 0);
                        let compressedDataUrl;
                        let quality = 1; // 初始质量为 1，表示无损
                        while (true) {
                          compressedDataUrl = canvas.toDataURL('image/jpeg', quality);
                          if (compressedDataUrl.length <= 200 * 1024) {
                            break;
                          }
                          quality -= 0.1; // 逐渐降低质量
                          if (quality < 0.1) {
                            break; // 防止质量过低
                          }
                        };  
                        files = [
                          // ...files,
                          {
                            type: "image",
                            url: compressedDataUrl,
                          },
                        ];
                      };
                      img.src = event.target.result;
                      inputFiles = null;
                      filesInputElement.value = "";
                    };
                    reader.readAsDataURL(file);
                  } else if (
                    SUPPORTED_FILE_TYPE.includes(file["type"]) ||
                    SUPPORTED_FILE_EXTENSIONS.includes(
                      file.name.split(".").at(-1)
                    )
                  ) {
                    uploadDoc(file);
                    filesInputElement.value = "";
                  } else {
                    toast.error(
                      $i18n.t(
                        `Unknown File Type {{file_type}}, but accepting and treating as plain text`,
                        { file_type: file["type"] }
                      )
                    );
                    uploadDoc(file);
                    filesInputElement.value = "";
                  }
                });
              } else {
                toast.error($i18n.t(`File not found.`));
              }
            }}
          />
          <form
            dir={$settings?.chatDirection ?? "LTR"}
            class=" flex flex-col relative w-full rounded-3xl px-1.5 bg-gray-100 dark:bg-gray-850 dark:text-gray-100 button-select-none"
            on:submit|preventDefault={() => {
              if($toolflag && $tooltype == "translate") {
                toolInfo.trantip = $i18n.t("Translate to") + " " + tranlang;
              }
              submitPrompt(prompt, toolInfo, user);
            }}
          >
            {#if files.length > 0}
              <div class="mx-2 mt-2 mb-1 flex flex-wrap gap-2">
                {#each files as file, fileIdx}
                  <div class=" relative group">
                    {#if file.type === "image"}
                      <img
                        src={file.url}
                        alt="input"
                        class=" h-16 w-16 rounded-xl object-cover"
                      />
                    {:else if file.type === "doc"}
                      <div
                        class="h-16 w-[15rem] flex items-center space-x-3 px-2.5 dark:bg-gray-600 rounded-xl border border-gray-200 dark:border-none"
                      >
                        <div class="text-white rounded-lg {file.upload_status?'':'p-2.5 bg-red-400'}">
                          {#if file.upload_status}
                            <FileSvg bind:filename={file.name}/>
                          {:else}
                            <svg
                              class=" w-6 h-6 translate-y-[0.5px]"
                              fill="currentColor"
                              viewBox="0 0 24 24"
                              xmlns="http://www.w3.org/2000/svg"
                              ><style>
                                .spinner_qM83 {
                                  animation: spinner_8HQG 1.05s infinite;
                                }
                                .spinner_oXPr {
                                  animation-delay: 0.1s;
                                }
                                .spinner_ZTLf {
                                  animation-delay: 0.2s;
                                }
                                @keyframes spinner_8HQG {
                                  0%,
                                  57.14% {
                                    animation-timing-function: cubic-bezier(
                                      0.33,
                                      0.66,
                                      0.66,
                                      1
                                    );
                                    transform: translate(0);
                                  }
                                  28.57% {
                                    animation-timing-function: cubic-bezier(
                                      0.33,
                                      0,
                                      0.66,
                                      0.33
                                    );
                                    transform: translateY(-6px);
                                  }
                                  100% {
                                    transform: translate(0);
                                  }
                                }
                              </style><circle
                                class="spinner_qM83"
                                cx="4"
                                cy="12"
                                r="2.5"
                              /><circle
                                class="spinner_qM83 spinner_oXPr"
                                cx="12"
                                cy="12"
                                r="2.5"
                              /><circle
                                class="spinner_qM83 spinner_ZTLf"
                                cx="20"
                                cy="12"
                                r="2.5"
                              /></svg
                            >
                          {/if}
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
                      </div>
                    {:else if file.type === "collection"}
                      <div
                        class="h-16 w-[15rem] flex items-center space-x-3 px-2.5 dark:bg-gray-600 rounded-xl border border-gray-200 dark:border-none"
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
                      </div>
                    {/if}

                    <div class=" absolute -top-1 -right-1">
                      <button
                        class=" bg-gray-400 text-white border border-white rounded-full group-hover:visible invisible transition"
                        type="button"
                        on:click={() => {
                          files.splice(fileIdx, 1);
                          files = files;
                        }}
                      >
                        <svg
                          xmlns="http://www.w3.org/2000/svg"
                          viewBox="0 0 20 20"
                          fill="currentColor"
                          class="w-4 h-4"
                        >
                          <path
                            d="M6.28 5.22a.75.75 0 00-1.06 1.06L8.94 10l-3.72 3.72a.75.75 0 101.06 1.06L10 11.06l3.72 3.72a.75.75 0 101.06-1.06L11.06 10l3.72-3.72a.75.75 0 00-1.06-1.06L10 8.94 6.28 5.22z"
                          />
                        </svg>
                      </button>
                    </div>
                  </div>
                {/each}
              </div>
              {#if files[0]?.type === "image"}
                <div class="flex flex-wrap gap-2 mt-1">
                  <button class="flex items-center bg-white dark:bg-gray-950 ml-2 px-2 py-1 text-sm rounded-lg"
                    on:click={() => {
                      prompt = $i18n.t("What does this picture mean?");
                    }}>
                    <span class="mr-1">{ $i18n.t("What does this picture mean?") }</span>
                    <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="none" viewBox="0 0 24 24">
                      <path fill="currentColor" fill-rule="evenodd" d="M12.793 3.793a1 1 0 0 1 1.414 0l7.5 7.5a1 1 0 0 1 0 1.414l-7.5 7.5a1 1 0 0 1-1.414-1.414L18.586 13H3a1 1 0 1 1 0-2h15.586l-5.793-5.793a1 1 0 0 1 0-1.414" clip-rule="evenodd"/>
                    </svg>
                  </button>
                  <button class="flex items-center bg-white dark:bg-gray-950 ml-2 px-2 py-1 text-sm rounded-lg"
                    on:click={() => {
                      prompt = $i18n.t("Explain this picture");
                    }}>
                    <span class="mr-1">{ $i18n.t("Explain this picture") }</span>
                    <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="none" viewBox="0 0 24 24">
                      <path fill="currentColor" fill-rule="evenodd" d="M12.793 3.793a1 1 0 0 1 1.414 0l7.5 7.5a1 1 0 0 1 0 1.414l-7.5 7.5a1 1 0 0 1-1.414-1.414L18.586 13H3a1 1 0 1 1 0-2h15.586l-5.793-5.793a1 1 0 0 1 0-1.414" clip-rule="evenodd"/>
                    </svg>
                  </button>
                  <button class="flex items-center bg-white dark:bg-gray-950 ml-2 px-2 py-1 text-sm rounded-lg"
                    on:click={() => {
                      prompt = $i18n.t("What is the main idea of this picture?");
                    }}>
                    <span class="mr-1">{ $i18n.t("What is the main idea of this picture?") }</span>
                    <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="none" viewBox="0 0 24 24">
                      <path fill="currentColor" fill-rule="evenodd" d="M12.793 3.793a1 1 0 0 1 1.414 0l7.5 7.5a1 1 0 0 1 0 1.414l-7.5 7.5a1 1 0 0 1-1.414-1.414L18.586 13H3a1 1 0 1 1 0-2h15.586l-5.793-5.793a1 1 0 0 1 0-1.414" clip-rule="evenodd"/>
                    </svg>
                  </button>
                  <button class="flex items-center bg-white dark:bg-gray-950 ml-2 px-2 py-1 text-sm rounded-lg"
                    on:click={() => {
                      prompt = $i18n.t("What does the symbol in the picture represent?");
                    }}>
                    <span class="mr-1">{ $i18n.t("What does the symbol in the picture represent?") }</span>
                    <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="none" viewBox="0 0 24 24">
                      <path fill="currentColor" fill-rule="evenodd" d="M12.793 3.793a1 1 0 0 1 1.414 0l7.5 7.5a1 1 0 0 1 0 1.414l-7.5 7.5a1 1 0 0 1-1.414-1.414L18.586 13H3a1 1 0 1 1 0-2h15.586l-5.793-5.793a1 1 0 0 1 0-1.414" clip-rule="evenodd"/>
                    </svg>
                  </button>
                  <button class="flex items-center bg-white dark:bg-gray-950 ml-2 px-2 py-1 text-sm rounded-lg"
                    on:click={() => {
                      prompt = $i18n.t("Help me solve problems");
                    }}>
                    <span class="mr-1">{ $i18n.t("Help me solve problems") }</span>
                    <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="none" viewBox="0 0 24 24">
                      <path fill="currentColor" fill-rule="evenodd" d="M12.793 3.793a1 1 0 0 1 1.414 0l7.5 7.5a1 1 0 0 1 0 1.414l-7.5 7.5a1 1 0 0 1-1.414-1.414L18.586 13H3a1 1 0 1 1 0-2h15.586l-5.793-5.793a1 1 0 0 1 0-1.414" clip-rule="evenodd"/>
                    </svg>
                  </button>
                </div>
              {/if}
              {#if files[0]?.type === "doc" && files[0]?.upload_status}
                {#if files[0]?.anaylis_type == "progrem"}
                  <div class="flex flex-wrap gap-2 mt-1">
                    <button class="flex items-center bg-white dark:bg-gray-950 ml-2 px-2 py-1 text-sm rounded-lg"
                      on:click={() => {
                        prompt = $i18n.t("Introduce the code in the file");
                      }}>
                      <span class="mr-1">{ $i18n.t("Introduce the code in the file") }</span>
                      <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="none" viewBox="0 0 24 24">
                        <path fill="currentColor" fill-rule="evenodd" d="M12.793 3.793a1 1 0 0 1 1.414 0l7.5 7.5a1 1 0 0 1 0 1.414l-7.5 7.5a1 1 0 0 1-1.414-1.414L18.586 13H3a1 1 0 1 1 0-2h15.586l-5.793-5.793a1 1 0 0 1 0-1.414" clip-rule="evenodd"/>
                      </svg>
                    </button>
                    <button class="flex items-center bg-white dark:bg-gray-950 ml-2 px-2 py-1 text-sm rounded-lg"
                      on:click={() => {
                        prompt = $i18n.t("What's the main purpose of the file's code");
                      }}>
                      <span class="mr-1">{ $i18n.t("What's the main purpose of the file's code") }</span>
                      <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="none" viewBox="0 0 24 24">
                        <path fill="currentColor" fill-rule="evenodd" d="M12.793 3.793a1 1 0 0 1 1.414 0l7.5 7.5a1 1 0 0 1 0 1.414l-7.5 7.5a1 1 0 0 1-1.414-1.414L18.586 13H3a1 1 0 1 1 0-2h15.586l-5.793-5.793a1 1 0 0 1 0-1.414" clip-rule="evenodd"/>
                      </svg>
                    </button>
                    <button class="flex items-center bg-white dark:bg-gray-950 ml-2 px-2 py-1 text-sm rounded-lg"
                      on:click={() => {
                        prompt = $i18n.t("Optimize the code in the file");
                      }}>
                      <span class="mr-1">{ $i18n.t("Optimize the code in the file") }</span>
                      <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="none" viewBox="0 0 24 24">
                        <path fill="currentColor" fill-rule="evenodd" d="M12.793 3.793a1 1 0 0 1 1.414 0l7.5 7.5a1 1 0 0 1 0 1.414l-7.5 7.5a1 1 0 0 1-1.414-1.414L18.586 13H3a1 1 0 1 1 0-2h15.586l-5.793-5.793a1 1 0 0 1 0-1.414" clip-rule="evenodd"/>
                      </svg>
                    </button>
                  </div>
                {:else}
                  <div class="flex flex-wrap gap-2 mt-1">
                    <button class="flex items-center bg-white dark:bg-gray-950 ml-2 px-2 py-1 text-sm rounded-lg"
                      on:click={() => {
                        prompt = $i18n.t("Summarize the content of this document");
                      }}>
                      <span class="mr-1">{ $i18n.t("Summarize the content of this document") }</span>
                      <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="none" viewBox="0 0 24 24">
                        <path fill="currentColor" fill-rule="evenodd" d="M12.793 3.793a1 1 0 0 1 1.414 0l7.5 7.5a1 1 0 0 1 0 1.414l-7.5 7.5a1 1 0 0 1-1.414-1.414L18.586 13H3a1 1 0 1 1 0-2h15.586l-5.793-5.793a1 1 0 0 1 0-1.414" clip-rule="evenodd"/>
                      </svg>
                    </button>
                    <button class="flex items-center bg-white dark:bg-gray-950 ml-2 px-2 py-1 text-sm rounded-lg"
                      on:click={() => {
                        prompt = $i18n.t("Generate a brief summary");
                      }}>
                      <span class="mr-1">{ $i18n.t("Generate a brief summary") }</span>
                      <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="none" viewBox="0 0 24 24">
                        <path fill="currentColor" fill-rule="evenodd" d="M12.793 3.793a1 1 0 0 1 1.414 0l7.5 7.5a1 1 0 0 1 0 1.414l-7.5 7.5a1 1 0 0 1-1.414-1.414L18.586 13H3a1 1 0 1 1 0-2h15.586l-5.793-5.793a1 1 0 0 1 0-1.414" clip-rule="evenodd"/>
                      </svg>
                    </button>
                    <button class="flex items-center bg-white dark:bg-gray-950 ml-2 px-2 py-1 text-sm rounded-lg"
                      on:click={() => {
                        prompt = $i18n.t("Extract document key info");
                      }}>
                      <span class="mr-1">{ $i18n.t("Extract document key info") }</span>
                      <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="none" viewBox="0 0 24 24">
                        <path fill="currentColor" fill-rule="evenodd" d="M12.793 3.793a1 1 0 0 1 1.414 0l7.5 7.5a1 1 0 0 1 0 1.414l-7.5 7.5a1 1 0 0 1-1.414-1.414L18.586 13H3a1 1 0 1 1 0-2h15.586l-5.793-5.793a1 1 0 0 1 0-1.414" clip-rule="evenodd"/>
                      </svg>
                    </button>
                    <button class="flex items-center bg-white dark:bg-gray-950 ml-2 px-2 py-1 text-sm rounded-lg"
                      on:click={() => {
                        prompt = $i18n.t("Polish the content of the document");
                      }}>
                      <span class="mr-1">{ $i18n.t("Polish the content of the document") }</span>
                      <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="none" viewBox="0 0 24 24">
                        <path fill="currentColor" fill-rule="evenodd" d="M12.793 3.793a1 1 0 0 1 1.414 0l7.5 7.5a1 1 0 0 1 0 1.414l-7.5 7.5a1 1 0 0 1-1.414-1.414L18.586 13H3a1 1 0 1 1 0-2h15.586l-5.793-5.793a1 1 0 0 1 0-1.414" clip-rule="evenodd"/>
                      </svg>
                    </button>
                    <button class="flex items-center bg-white dark:bg-gray-950 ml-2 px-2 py-1 text-sm rounded-lg"
                      on:click={() => {
                        prompt = $i18n.t("Generate an analysis report");
                      }}>
                      <span class="mr-1">{ $i18n.t("Generate an analysis report") }</span>
                      <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="none" viewBox="0 0 24 24">
                        <path fill="currentColor" fill-rule="evenodd" d="M12.793 3.793a1 1 0 0 1 1.414 0l7.5 7.5a1 1 0 0 1 0 1.414l-7.5 7.5a1 1 0 0 1-1.414-1.414L18.586 13H3a1 1 0 1 1 0-2h15.586l-5.793-5.793a1 1 0 0 1 0-1.414" clip-rule="evenodd"/>
                      </svg>
                    </button>
                  </div>
                {/if}
              {/if}
            {/if}

            {#if $tooltype != ""}
              <ToolsSelect bind:inputplaceholder={chatInputPlaceholder} bind:tranLang={tranlang}/>
            {/if}
            <div class="flex flex-col">
              <textarea
                id="chat-textarea"
                bind:this={chatTextAreaElement}
                class="scrollbar-hidden bg-gray-100 dark:bg-gray-850 dark:text-gray-100 outline-none w-full py-3 px-3 {fileUploadEnabled
                  ? ''
                  : ' pl-4'} rounded-xl resize-none h-[48px]"
                placeholder={chatInputPlaceholder !== ""
                  ? chatInputPlaceholder
                  : isRecording
                  ? $i18n.t("Listening...")
                  : $i18n.t("Send a Message")}
                bind:value={prompt}
                on:keypress={(e) => {
                  if (
                    !$mobile ||
                    !(
                      "ontouchstart" in window ||
                      navigator.maxTouchPoints > 0 ||
                      navigator.msMaxTouchPoints > 0
                    )
                  ) {
                    if (e.keyCode == 13 && !e.shiftKey) {
                      e.preventDefault();
                    }
                    if (prompt !== "" && e.keyCode == 13 && !e.shiftKey) {
                      submitPrompt(prompt, toolInfo, user);
                    }
                  }
                }}
                on:keydown={async (e) => {
                  const isCtrlPressed = e.ctrlKey || e.metaKey; // metaKey is for Cmd key on Mac

                  // Check if Ctrl + R is pressed
                  if (
                    prompt === "" &&
                    isCtrlPressed &&
                    e.key.toLowerCase() === "r"
                  ) {
                    e.preventDefault();
                    console.log("regenerate");

                    const regenerateButton = [
                      ...document.getElementsByClassName(
                        "regenerate-response-button"
                      ),
                    ]?.at(-1);

                    regenerateButton?.click();
                  }

                  if (prompt === "" && e.key == "ArrowUp") {
                    e.preventDefault();
                    const userMessageElement = [
                      ...document.getElementsByClassName("user-message"),
                    ]?.at(-1);
                    // 开启新的edit
                    // const editButton = [
                    //   ...document.getElementsByClassName(
                    //     "edit-user-message-button"
                    //   ),
                    // ]?.at(-1);
                    userMessageElement?.scrollIntoView({ block: "center" });
                    // editButton?.click();
                    const textarea = document.getElementById("chat-textarea");
                    if (textarea) {
                      textarea.value = (userMessageElement?.innerText) ?? "";
                    }
                  }

                  // if (
                  //   ["/", "#", "@"].includes(prompt.charAt(0)) &&
                  //   e.key === "ArrowUp"
                  // ) {
                  //   e.preventDefault();

                  //   (
                  //     promptsElement ||
                  //     documentsElement ||
                  //     modelsElement
                  //   ).selectUp();

                  //   const commandOptionButton = [
                  //     ...document.getElementsByClassName(
                  //       "selected-command-option-button"
                  //     ),
                  //   ]?.at(-1);
                  //   commandOptionButton.scrollIntoView({ block: "center" });
                  // }

                  // if (
                  //   ["/", "#", "@"].includes(prompt.charAt(0)) &&
                  //   e.key === "ArrowDown"
                  // ) {
                  //   e.preventDefault();

                  //   (
                  //     promptsElement ||
                  //     documentsElement ||
                  //     modelsElement
                  //   ).selectDown();

                  //   const commandOptionButton = [
                  //     ...document.getElementsByClassName(
                  //       "selected-command-option-button"
                  //     ),
                  //   ]?.at(-1);
                  //   commandOptionButton.scrollIntoView({ block: "center" });
                  // }

                  // if (
                  //   ["/", "#", "@"].includes(prompt.charAt(0)) &&
                  //   e.key === "Enter"
                  // ) {
                  //   e.preventDefault();

                  //   const commandOptionButton = [
                  //     ...document.getElementsByClassName(
                  //       "selected-command-option-button"
                  //     ),
                  //   ]?.at(-1);

                  //   if (commandOptionButton) {
                  //     commandOptionButton?.click();
                  //   } else {
                  //     document.getElementById("send-message-button")?.click();
                  //   }
                  // }

                  // if (
                  //   ["/", "#", "@"].includes(prompt.charAt(0)) &&
                  //   e.key === "Tab"
                  // ) {
                  //   e.preventDefault();

                  //   const commandOptionButton = [
                  //     ...document.getElementsByClassName(
                  //       "selected-command-option-button"
                  //     ),
                  //   ]?.at(-1);

                  //   commandOptionButton?.click();
                  // } else 
                  if (e.key === "Tab") {
                    const words = findWordIndices(prompt);
                    if (words.length > 0) {
                      const word = words.at(0);
                      const fullPrompt = prompt;

                      prompt = prompt.substring(0, word?.endIndex + 1);
                      await tick();

                      e.target.scrollTop = e.target.scrollHeight;
                      prompt = fullPrompt;
                      await tick();

                      e.preventDefault();
                      e.target.setSelectionRange(
                        word?.startIndex,
                        word.endIndex + 1
                      );
                    }

                    e.target.style.height = "";
                    e.target.style.height =
                      Math.min(e.target.scrollHeight, 200) + "px";
                  }

                  if ((prompt.startsWith("https://") || prompt.startsWith("http://"))
                     && e.key === "ArrowUp") {
                    e.preventDefault();

                    (urlPromptElement).selectUp();
                    const commandOptionButton = [
                      ...document.getElementsByClassName(
                        "selected-command-option-button"
                      ),
                    ]?.at(-1);
                    commandOptionButton.scrollIntoView({ block: "center" });
                  }
                  if ((prompt.startsWith("https://") || prompt.startsWith("http://"))
                     && e.key === "ArrowDown") {
                    e.preventDefault();

                    (urlPromptElement).selectDown();
                    const commandOptionButton = [
                      ...document.getElementsByClassName(
                        "selected-command-option-button"
                      ),
                    ]?.at(-1);
                    commandOptionButton.scrollIntoView({ block: "center" });
                  }

                  if (e.key === "Escape") {
                    console.log("Escape");
                    selectedModel = "";
                  }
                }}
                rows="1"
                on:input={(e) => {
                  e.target.style.height = "";
                  e.target.style.height =
                    Math.min(e.target.scrollHeight, 200) + "px";
                  user = null;
                }}
                on:focus={(e) => {
                  e.target.style.height = "";
                  e.target.style.height =
                    Math.min(e.target.scrollHeight, 200) + "px";
                }}
                on:paste={async (e) => {
                  const clipboardData = e.clipboardData || window.clipboardData;

                  if (clipboardData && clipboardData.items) {
                    for (const item of clipboardData.items) {
                      if (item.type.indexOf("image") !== -1) {
                        const blob = item.getAsFile();
                        const reader = new FileReader();

                        reader.onload = function (e) {
                          files = [
                            // ...files,
                            {
                              type: "image",
                              url: `${e.target.result}`,
                            },
                          ];
                        };

                        reader.readAsDataURL(blob);
                      }
                    }
                  }
                }}
              />
              <div class="flex justify-between">
                <div class="flex flex-row">
                  <!-- 图片上传 -->
                  {#if fileUploadEnabled && !$toolflag}
                    <div class="self-star mb-2 ml-1 mr-1">
                      <button
                        class="bg-gray-50 hover:bg-gray-200 text-gray-800 dark:bg-gray-800 dark:text-white dark:hover:bg-gray-700 transition rounded-full p-1.5"
                        type="button"
                        on:click={() => {
                          filesInputElement.click();
                        }}
                      >
                        <svg
                          xmlns="http://www.w3.org/2000/svg"
                          viewBox="0 0 16 16"
                          fill="currentColor"
                          class="w-[1.2rem] h-[1.2rem]"
                        >
                          <path
                            d="M8.75 3.75a.75.75 0 0 0-1.5 0v3.5h-3.5a.75.75 0 0 0 0 1.5h3.5v3.5a.75.75 0 0 0 1.5 0v-3.5h3.5a.75.75 0 0 0 0-1.5h-3.5v-3.5Z"
                          />
                        </svg>
                      </button>
                      <!-- <Tooltip content={$i18n.t("Attach files")}></Tooltip> -->
                    </div>
                  {/if}

                  <!-- 工具组件 -->
                  <div class="self-star mb-2 ml-1 mr-1">
                    <Tools bind:inputplaceholder={chatInputPlaceholder}/>
                  </div>

                  <!-- 深度搜索 -->
                  <!-- <div class="self-star mb-2 ml-1 mr-1">
                    <button class="flex flex-row items-center transition rounded-full cursor-pointer px-3 py-1.5
                      {deepsearch ? 'bg-[#D0A870] text-white' : 'bg-white text-gray-800 dark:bg-gray-800 dark:text-white'}"
                      type="button"
                      on:click={async (event) => {
                        event.stopPropagation();
                        deepsearch = !deepsearch;
                      }}>
                      <svg 
                        xmlns="http://www.w3.org/2000/svg"
                        viewBox="0 0 20 20"
                        class="w-[1.1rem] h-[1.1rem]"
                        fill="currentColor">
                        <path d="M2.656 17.344c-1.016-1.015-1.15-2.75-.313-4.925.325-.825.73-1.617 1.205-2.365L3.582 10l-.033-.054c-.5-.799-.91-1.596-1.206-2.365-.836-2.175-.703-3.91.313-4.926.56-.56 1.364-.86 2.335-.86 1.425 0 3.168.636 4.957 1.756l.053.034.053-.034c1.79-1.12 3.532-1.757 4.957-1.757.972 0 1.776.3 2.335.86 1.014 1.015 1.148 2.752.312 4.926a13.892 13.892 0 0 1-1.206 2.365l-.034.054.034.053c.5.8.91 1.596 1.205 2.365.837 2.175.704 3.911-.311 4.926-.56.56-1.364.861-2.335.861-1.425 0-3.168-.637-4.957-1.757L10 16.415l-.053.033c-1.79 1.12-3.532 1.757-4.957 1.757-.972 0-1.776-.3-2.335-.86zm13.631-4.399c-.187-.488-.429-.988-.71-1.492l-.075-.132-.092.12a22.075 22.075 0 0 1-3.968 3.968l-.12.093.132.074c1.308.734 2.559 1.162 3.556 1.162.563 0 1.006-.138 1.298-.43.3-.3.436-.774.428-1.346-.008-.575-.159-1.264-.449-2.017zm-6.345 1.65l.058.042.058-.042a19.881 19.881 0 0 0 4.551-4.537l.043-.058-.043-.058a20.123 20.123 0 0 0-2.093-2.458 19.732 19.732 0 0 0-2.458-2.08L10 5.364l-.058.042A19.883 19.883 0 0 0 5.39 9.942L5.348 10l.042.059c.631.874 1.332 1.695 2.094 2.457a19.74 19.74 0 0 0 2.458 2.08zm6.366-10.902c-.293-.293-.736-.431-1.298-.431-.998 0-2.248.429-3.556 1.163l-.132.074.12.092a21.938 21.938 0 0 1 3.968 3.968l.092.12.074-.132c.282-.504.524-1.004.711-1.492.29-.753.442-1.442.45-2.017.007-.572-.129-1.045-.429-1.345zM3.712 7.055c.202.514.44 1.013.712 1.493l.074.13.092-.119a21.94 21.94 0 0 1 3.968-3.968l.12-.092-.132-.074C7.238 3.69 5.987 3.262 4.99 3.262c-.563 0-1.006.138-1.298.43-.3.301-.436.774-.428 1.346.007.575.159 1.264.448 2.017zm0 5.89c-.29.753-.44 1.442-.448 2.017-.008.572.127 1.045.428 1.345.293.293.736.431 1.298.431.997 0 2.247-.428 3.556-1.162l.131-.074-.12-.093a21.94 21.94 0 0 1-3.967-3.968l-.093-.12-.074.132a11.712 11.712 0 0 0-.71 1.492z" fill="currentColor" stroke="currentColor" stroke-width=".1"/>
                        <path d="M10.706 11.704A1.843 1.843 0 0 1 8.155 10a1.845 1.845 0 1 1 2.551 1.704z" fill="currentColor" stroke="currentColor" stroke-width=".2"/>
                      </svg>
                      <span class="text-sm ml-1">{$i18n.t("Deep Research")}</span>
                    </button>
                  </div> -->
                </div>
                
                <div class="self-end mb-2 flex space-x-1 mr-1">
                  {#if messages.length == 0 || messages.at(-1).done == true}
                    <!-- <Tooltip content={$i18n.t("Record voice")}>
                      {#if speechRecognitionEnabled}
                        <button
                          id="voice-input-button"
                          class=" text-gray-600 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-850 transition rounded-full p-1.5 mr-0.5 self-center"
                          type="button"
                          on:click={() => {
                            speechRecognitionHandler();
                          }}
                        >
                          {#if isRecording}
                            <svg
                              class=" w-5 h-5 translate-y-[0.5px]"
                              fill="currentColor"
                              viewBox="0 0 24 24"
                              xmlns="http://www.w3.org/2000/svg"
                              ><style>
                                .spinner_qM83 {
                                  animation: spinner_8HQG 1.05s infinite;
                                }
                                .spinner_oXPr {
                                  animation-delay: 0.1s;
                                }
                                .spinner_ZTLf {
                                  animation-delay: 0.2s;
                                }
                                @keyframes spinner_8HQG {
                                  0%,
                                  57.14% {
                                    animation-timing-function: cubic-bezier(
                                      0.33,
                                      0.66,
                                      0.66,
                                      1
                                    );
                                    transform: translate(0);
                                  }
                                  28.57% {
                                    animation-timing-function: cubic-bezier(
                                      0.33,
                                      0,
                                      0.66,
                                      0.33
                                    );
                                    transform: translateY(-6px);
                                  }
                                  100% {
                                    transform: translate(0);
                                  }
                                }
                              </style><circle
                                class="spinner_qM83"
                                cx="4"
                                cy="12"
                                r="2.5"
                              /><circle
                                class="spinner_qM83 spinner_oXPr"
                                cx="12"
                                cy="12"
                                r="2.5"
                              /><circle
                                class="spinner_qM83 spinner_ZTLf"
                                cx="20"
                                cy="12"
                                r="2.5"
                              /></svg
                            >
                          {:else}
                            <svg
                              xmlns="http://www.w3.org/2000/svg"
                              viewBox="0 0 20 20"
                              fill="currentColor"
                              class="w-5 h-5 translate-y-[0.5px]"
                            >
                              <path d="M7 4a3 3 0 016 0v6a3 3 0 11-6 0V4z" />
                              <path
                                d="M5.5 9.643a.75.75 0 00-1.5 0V10c0 3.06 2.29 5.585 5.25 5.954V17.5h-1.5a.75.75 0 000 1.5h4.5a.75.75 0 000-1.5h-1.5v-1.546A6.001 6.001 0 0016 10v-.357a.75.75 0 00-1.5 0V10a4.5 4.5 0 01-9 0v-.357z"
                              />
                            </svg>
                          {/if}
                        </button>
                      {/if}
                    </Tooltip> -->
  
                    <Tooltip content={$i18n.t("Send message")}>
                      <button
                        id="send-message-button"
                        class="{prompt !== ''
                          ? 'bg-black text-white hover:bg-gray-900 dark:bg-white dark:text-black dark:hover:bg-gray-100 '
                          : 'text-white bg-gray-300 dark:text-gray-900 dark:bg-gray-700 disabled'} transition rounded-full p-1.5 self-center"
                        type="submit"
                        disabled={prompt === ""}
                      >
                        <svg
                          xmlns="http://www.w3.org/2000/svg"
                          viewBox="0 0 16 16"
                          fill="currentColor"
                          class="w-5 h-5"
                        >
                          <path
                            fill-rule="evenodd"
                            d="M8 14a.75.75 0 0 1-.75-.75V4.56L4.03 7.78a.75.75 0 0 1-1.06-1.06l4.5-4.5a.75.75 0 0 1 1.06 0l4.5 4.5a.75.75 0 0 1-1.06 1.06L8.75 4.56v8.69A.75.75 0 0 1 8 14Z"
                            clip-rule="evenodd"
                          />
                        </svg>
                      </button>
                    </Tooltip>
                  {:else}
                    <button
                      class="bg-white hover:bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-white dark:hover:bg-gray-800 transition rounded-full p-1.5"
                      on:click={stopResponse}
                    >
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        viewBox="0 0 24 24"
                        fill="currentColor"
                        class="w-5 h-5"
                      >
                        <path
                          fill-rule="evenodd"
                          d="M2.25 12c0-5.385 4.365-9.75 9.75-9.75s9.75 4.365 9.75 9.75-4.365 9.75-9.75 9.75S2.25 17.385 2.25 12zm6-2.438c0-.724.588-1.312 1.313-1.312h4.874c.725 0 1.313.588 1.313 1.313v4.874c0 .725-.588 1.313-1.313 1.313H9.564a1.312 1.312 0 01-1.313-1.313V9.564z"
                          clip-rule="evenodd"
                        />
                      </svg>
                    </button>
                  {/if}
                </div>
              </div>  
            </div>
          </form>

          <!-- <div class="mt-1.5 text-xs text-gray-500 text-center">
            {$i18n.t("LLMs can make mistakes. Verify important information.")}
          </div> -->
        </div>
      </div>
    </div>
  </div>
</div>

<style>
  .scrollbar-hidden:active::-webkit-scrollbar-thumb,
  .scrollbar-hidden:focus::-webkit-scrollbar-thumb,
  .scrollbar-hidden:hover::-webkit-scrollbar-thumb {
    visibility: visible;
  }
  .scrollbar-hidden::-webkit-scrollbar-thumb {
    visibility: hidden;
  }
  .button-select-none {
    -webkit-touch-callout: none; /* 禁止系统默认菜单 */
    -webkit-user-select: none; /* Safari 浏览器禁止选择 */
    -khtml-user-select: none; /* 早期浏览器 */
    -moz-user-select: none; /* Firefox 浏览器禁止选择 */
    -ms-user-select: none; /* IE 浏览器禁止选择 */
    user-select: none; /* 标准语法，禁止选择 */
  }
</style>
