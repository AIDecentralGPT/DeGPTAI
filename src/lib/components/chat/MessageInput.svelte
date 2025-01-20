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
  } from "$lib/stores";
  import { blobToFile, calculateSHA256, findWordIndices } from "$lib/utils";

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
  import Suggestions from "./MessageInput/Suggestions.svelte";
  import AddFilesPlaceholder from "../AddFilesPlaceholder.svelte";
  import Documents from "./MessageInput/Documents.svelte";
  import Models from "./MessageInput/Models.svelte";
  import Tooltip from "../common/Tooltip.svelte";
  import XMark from "$lib/components/icons/XMark.svelte";
  import { user as userStore } from "$lib/stores";

  const i18n = getContext("i18n");

  export let submitPrompt: Function;
  export let stopResponse: Function;

  export let autoScroll = true;
  export let selectedModel = "";

  let chatTextAreaElement: HTMLTextAreaElement;
  let filesInputElement: any;

  let promptsElement: any;
  let documentsElement: any;
  let modelsElement: any;

  let inputFiles: any;
  let dragged = false;

  let user: any = null;
  let chatInputPlaceholder = "";

  // 文件选择
  export let files: any[] = [];

  // 搜索网页开启标志
  export let search = false;

  export let fileUploadEnabled = true;
  // export let speechRecognitionEnabled = true;

  export let prompt = "";
  export let messages: any[] = [];

  let speechRecognition: any;

  $: if (prompt) {
    if (chatTextAreaElement) {
      chatTextAreaElement.style.height = "";
      chatTextAreaElement.style.height =
        Math.min(chatTextAreaElement.scrollHeight, 200) + "px";
    }
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
          submitPrompt(prompt, user);
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
              submitPrompt(prompt, user);
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
      upload_status: false,
      error: "",
    };

    try {
      files = [...files, doc];

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

          <Models
            bind:this={modelsElement}
            bind:prompt
            bind:user
            bind:chatInputPlaceholder
            {messages}
            on:select={(e) => {
              selectedModel = e.detail;
              chatTextAreaElement?.focus();
            }}
          />

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
                class=" px-2 py-1 dark:bg-white dark:text-zinc-950 bg-black text-gray-100 transition rounded-lg"
                on:click={async () => {
                  $showOpenWalletModal = true;
                }}
              >
                {$i18n.t("Open Wallet")}
              </button>

              <button
                class=" px-2 py-1 dark:bg-white dark:text-zinc-950 bg-black text-gray-100 transition rounded-lg"
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
            accept="image/*"
            hidden
            multiple
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
                          ...files,
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
            class=" flex flex-col relative w-full rounded-3xl px-1.5 bg-gray-100 dark:bg-gray-850 dark:text-gray-100"
            on:submit|preventDefault={() => {
              submitPrompt(prompt, user);
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
                        <div class="p-2.5 bg-red-400 text-white rounded-lg">
                          {#if file.upload_status}
                            <svg
                              xmlns="http://www.w3.org/2000/svg"
                              viewBox="0 0 24 24"
                              fill="currentColor"
                              class="w-6 h-6"
                            >
                              <path
                                fill-rule="evenodd"
                                d="M5.625 1.5c-1.036 0-1.875.84-1.875 1.875v17.25c0 1.035.84 1.875 1.875 1.875h12.75c1.035 0 1.875-.84 1.875-1.875V12.75A3.75 3.75 0 0 0 16.5 9h-1.875a1.875 1.875 0 0 1-1.875-1.875V5.25A3.75 3.75 0 0 0 9 1.5H5.625ZM7.5 15a.75.75 0 0 1 .75-.75h7.5a.75.75 0 0 1 0 1.5h-7.5A.75.75 0 0 1 7.5 15Zm.75 2.25a.75.75 0 0 0 0 1.5H12a.75.75 0 0 0 0-1.5H8.25Z"
                                clip-rule="evenodd"
                              />
                              <path
                                d="M12.971 1.816A5.23 5.23 0 0 1 14.25 5.25v1.875c0 .207.168.375.375.375H16.5a5.23 5.23 0 0 1 3.434 1.279 9.768 9.768 0 0 0-6.963-6.963Z"
                              />
                            </svg>
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
                      submitPrompt(prompt, user);
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

                    const editButton = [
                      ...document.getElementsByClassName(
                        "edit-user-message-button"
                      ),
                    ]?.at(-1);

                    console.log(userMessageElement);

                    userMessageElement.scrollIntoView({ block: "center" });
                    editButton?.click();
                  }

                  if (
                    ["/", "#", "@"].includes(prompt.charAt(0)) &&
                    e.key === "ArrowUp"
                  ) {
                    e.preventDefault();

                    (
                      promptsElement ||
                      documentsElement ||
                      modelsElement
                    ).selectUp();

                    const commandOptionButton = [
                      ...document.getElementsByClassName(
                        "selected-command-option-button"
                      ),
                    ]?.at(-1);
                    commandOptionButton.scrollIntoView({ block: "center" });
                  }

                  if (
                    ["/", "#", "@"].includes(prompt.charAt(0)) &&
                    e.key === "ArrowDown"
                  ) {
                    e.preventDefault();

                    (
                      promptsElement ||
                      documentsElement ||
                      modelsElement
                    ).selectDown();

                    const commandOptionButton = [
                      ...document.getElementsByClassName(
                        "selected-command-option-button"
                      ),
                    ]?.at(-1);
                    commandOptionButton.scrollIntoView({ block: "center" });
                  }

                  if (
                    ["/", "#", "@"].includes(prompt.charAt(0)) &&
                    e.key === "Enter"
                  ) {
                    e.preventDefault();

                    const commandOptionButton = [
                      ...document.getElementsByClassName(
                        "selected-command-option-button"
                      ),
                    ]?.at(-1);

                    if (commandOptionButton) {
                      commandOptionButton?.click();
                    } else {
                      document.getElementById("send-message-button")?.click();
                    }
                  }

                  if (
                    ["/", "#", "@"].includes(prompt.charAt(0)) &&
                    e.key === "Tab"
                  ) {
                    e.preventDefault();

                    const commandOptionButton = [
                      ...document.getElementsByClassName(
                        "selected-command-option-button"
                      ),
                    ]?.at(-1);

                    commandOptionButton?.click();
                  } else if (e.key === "Tab") {
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
                on:paste={(e) => {
                  const clipboardData = e.clipboardData || window.clipboardData;

                  if (clipboardData && clipboardData.items) {
                    for (const item of clipboardData.items) {
                      if (item.type.indexOf("image") !== -1) {
                        const blob = item.getAsFile();
                        const reader = new FileReader();

                        reader.onload = function (e) {
                          files = [
                            ...files,
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
                  {#if fileUploadEnabled}
                    <div class="self-star mb-2 ml-1 mr-1">
                      <Tooltip content={$i18n.t("Attach files")}>
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
                      </Tooltip>
                    </div>
                  {/if}
                  <!-- 网络搜索 -->
                  <div class="self-star mb-2 ml-1 mr-1">
                    <Tooltip content={$i18n.t("Search the web")}>
                      <button
                        class="flex flex-row items-center bg-gray-50 hover:bg-[#333333cc] text-gray-800 dark:bg-gray-800 dark:text-white dark:hover:bg-[#ffffffcc] transition rounded-full px-3 py-1.5
                         {search ? 'bg-[#333333] dark:bg-[#ffffff]' : 'bg-gray-50 dark:bg-gray-800'}"
                        type="button"
                        on:click={() => {
                          search = !search;
                        }}
                      >
                        <svg
                          xmlns="http://www.w3.org/2000/svg"
                          viewBox="0 0 1024 1024"
                          class="w-[1rem] h-[1rem]" 
                          fill="#D0A870">
                          <path d="M512 0a512 512 0 0 0-512 512c0 136.768 53.248 265.344 149.952 362.048C243.712 967.68 392.512 1024 510.336 1024c12.672 0 47.616-1.536 70.144-4.544a40.576 40.576 0 0 0 35.2-43.968 40 40 0 0 0-45.12-35.456 432.96 432.96 0 0 1-20.608 2.304V88.32c70.656 29.184 133.376 133.44 160.128 273.216a40 40 0 0 0 78.592-15.04c-16.512-86.272-45.376-162.048-83.968-220.992a432.448 432.448 0 0 1 239.232 385.472c1.984 53.952 77.44 54.656 80 1.024V512A511.936 511.936 0 0 0 512 0zM313.216 128.512c-60.544 97.024-89.6 210.752-96.384 343.488h-135.04a432.832 432.832 0 0 1 231.424-343.488zM81.92 552h135.04c6.72 132.8 35.84 246.4 96.32 343.488A432.832 432.832 0 0 1 81.92 552z m388.096 383.616c-119.488-57.92-165.504-240.832-173.056-383.616h173.056v383.616z m0-463.616H296.96c7.552-142.592 53.568-325.76 173.056-383.616v383.616z m547.84 293.504a80 80 0 0 1-73.28 50.496h-36.992l72.448 150.656a40 40 0 1 1-72.064 34.624l-100.032-208a40 40 0 0 1 36.032-57.28h99.392a3.072 3.072 0 0 0 0.64-1.728l-210.816-190.144a1.28 1.28 0 0 0-0.192-0.128c-0.192 0-0.704 0.192-0.96 0.448v298.816c0 1.088 1.664 2.432 2.56 2.752 52.672 2.752 52.096 77.952-0.576 80h-0.256a83.712 83.712 0 0 1-81.728-82.752V544.768c0-31.68 17.856-59.712 46.656-73.088 28.8-13.44 61.888-9.088 86.272 11.392l216.896 195.84c22.144 23.36 28.224 56.576 16 86.592z"/>
                        </svg>
                        <span class="ml-1 text-sm font-bold text-[#D0A870]">{$i18n.t("search")}</span>
                      </button>
                    </Tooltip>
                  </div>  
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
</style>
