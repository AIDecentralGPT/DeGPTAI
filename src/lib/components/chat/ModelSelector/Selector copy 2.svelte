<script lang="ts">
  import { DropdownMenu } from "bits-ui";

  import { flyAndScale } from "$lib/utils/transitions";
  import { createEventDispatcher, getContext } from "svelte";

  import ChevronDown from "$lib/components/icons/ChevronDown.svelte";
  import Check from "$lib/components/icons/Check.svelte";


  import { user, mobile } from "$lib/stores";
  import { toast } from "svelte-sonner";

  const i18n = getContext("i18n");
  const dispatch = createEventDispatcher();

  export let value = "";
  export let placeholder = "Select a model";
  export let searchEnabled = true;
  export let searchPlaceholder = $i18n.t("Search a model");

  export let items = [{ value: "mango", label: "Mango" }];

  export let selectedList: any = [];

  export let selectedModelIdx = 0;

  export let className = "w-[30rem]";

  let show = false;

  let selectedModel = "";
  $: selectedModel = items.find((item) => item.value === value) ?? "";

  function changeModel(val:string) {
    const selModel = selectedList.find((item) => item === val) ?? "";
    if (selModel) {
      let index = selectedList.indexOf(selModel);
      selectedList.splice(index, 1);
    } else {
      selectedList.push(val);
    }
  }

  let searchValue = "";
  // let ollamaVersion = null;

  // const pullModelHandler = async () => {
  //   const sanitizedModelTag = searchValue
  //     .trim()
  //     .replace(/^ollama\s+(run|pull)\s+/, "");

  //   console.log($MODEL_DOWNLOAD_POOL);
  //   if ($MODEL_DOWNLOAD_POOL[sanitizedModelTag]) {
  //     toast.error(
  //       $i18n.t(`Model {{modelTag}} is already in queue for downloading.`, {
  //         modelTag: sanitizedModelTag,
  //       })
  //     );
  //     return;
  //   }
  //   if (Object.keys($MODEL_DOWNLOAD_POOL).length === 3) {
  //     toast.error(
  //       $i18n.t(
  //         "Maximum of 3 models can be downloaded simultaneously. Please try again later."
  //       )
  //     );
  //     return;
  //   }

  //   const res = await pullModel(
  //     localStorage.token,
  //     sanitizedModelTag,
  //     "0"
  //   ).catch((error) => {
  //     toast.error(error);
  //     return null;
  //   });

  //   if (res) {
  //     const reader = res.body
  //       .pipeThrough(new TextDecoderStream())
  //       .pipeThrough(splitStream("\n"))
  //       .getReader();

  //     while (true) {
  //       try {
  //         const { value, done } = await reader.read();
  //         if (done) break;

  //         let lines = value.split("\n");

  //         for (const line of lines) {
  //           if (line !== "") {
  //             let data = JSON.parse(line);
  //             console.log(data);
  //             if (data.error) {
  //               throw data.error;
  //             }
  //             if (data.detail) {
  //               throw data.detail;
  //             }

  //             if (data.id) {
  //               MODEL_DOWNLOAD_POOL.set({
  //                 ...$MODEL_DOWNLOAD_POOL,
  //                 [sanitizedModelTag]: {
  //                   ...$MODEL_DOWNLOAD_POOL[sanitizedModelTag],
  //                   requestId: data.id,
  //                   reader,
  //                   done: false,
  //                 },
  //               });
  //               console.log(data);
  //             }

  //             if (data.status) {
  //               if (data.digest) {
  //                 let downloadProgress = 0;
  //                 if (data.completed) {
  //                   downloadProgress =
  //                     Math.round((data.completed / data.total) * 1000) / 10;
  //                 } else {
  //                   downloadProgress = 100;
  //                 }

  //                 MODEL_DOWNLOAD_POOL.set({
  //                   ...$MODEL_DOWNLOAD_POOL,
  //                   [sanitizedModelTag]: {
  //                     ...$MODEL_DOWNLOAD_POOL[sanitizedModelTag],
  //                     pullProgress: downloadProgress,
  //                     digest: data.digest,
  //                   },
  //                 });
  //               } else {
  //                 toast.success(data.status);

  //                 MODEL_DOWNLOAD_POOL.set({
  //                   ...$MODEL_DOWNLOAD_POOL,
  //                   [sanitizedModelTag]: {
  //                     ...$MODEL_DOWNLOAD_POOL[sanitizedModelTag],
  //                     done: data.status === "success",
  //                   },
  //                 });
  //               }
  //             }
  //           }
  //         }
  //       } catch (error) {
  //         console.log(error);
  //         if (typeof error !== "string") {
  //           error = error.message;
  //         }

  //         toast.error(error);
  //         // opts.callback({ success: false, error, modelName: opts.modelName });
  //       }
  //     }

  //     if ($MODEL_DOWNLOAD_POOL[sanitizedModelTag].done) {
  //       toast.success(
  //         $i18n.t(`Model {{modelName}} has been successfully downloaded.`, {
  //           modelName: sanitizedModelTag,
  //         })
  //       );

  //       models.set(await getModels(localStorage.token));
  //     } else {
  //       toast.error($i18n.t("Download canceled"));
  //     }

  //     delete $MODEL_DOWNLOAD_POOL[sanitizedModelTag];

  //     MODEL_DOWNLOAD_POOL.set({
  //       ...$MODEL_DOWNLOAD_POOL,
  //     });
  //   }
  // };

  // const cancelModelPullHandler = async (model: string) => {
  //   const { reader, requestId } = $MODEL_DOWNLOAD_POOL[model];
  //   if (reader) {
  //     await reader.cancel();

  //     await cancelOllamaRequest(localStorage.token, requestId);
  //     delete $MODEL_DOWNLOAD_POOL[model];
  //     MODEL_DOWNLOAD_POOL.set({
  //       ...$MODEL_DOWNLOAD_POOL,
  //     });
  //     await deleteModel(localStorage.token, model);
  //     toast.success($i18n.t(`${model} download has been canceled`));
  //   }
  // };
</script>

<DropdownMenu.Root
  bind:open={show}
  onOpenChange={async () => {
    searchValue = "";
    window.setTimeout(
      () => document.getElementById("model-search-input")?.focus(),
      0
    );
  }}
>
  <DropdownMenu.Trigger class="relative w-full" aria-label={placeholder}>
    <div
      class="flex w-full text-left px-0.5 outline-none bg-transparent truncate text-lg font-semibold placeholder-gray-400 focus:outline-none"
    >
      {#if selectedModel}
        {selectedModel.label}
      {:else}
        {placeholder}
      {/if}
      {#if selectedModelIdx == 0}
        <ChevronDown className=" self-center ml-2 size-5" strokeWidth="2.5" />
      {/if}
    </div>
  </DropdownMenu.Trigger>

  <DropdownMenu.Content
    class=" z-[90] {$mobile
      ? `w-full`
      : `${className}`} max-w-[260px] justify-start rounded-md  bg-white dark:bg-gray-850 dark:text-white shadow-lg border border-gray-300/30 dark:border-gray-700/50  outline-none "
    transition={flyAndScale}
    side={$mobile ? "bottom" : "bottom-start"}
    sideOffset={4}
  >
    <slot>
      <div class="px-1 my-2 max-h-64 overflow-y-auto scrollbar-hidden">
        {#each items as item (item.value)}
          <button
            aria-label="model-item"
            class="flex item-center w-full text-left font-medium line-clamp-1 select-none items-center rounded-button py-1 pl-2 pr-2 outline-none transition-all duration-75 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg cursor-pointer data-[highlighted]:bg-muted"
            on:click={() => {
              if (item && item?.info?.isProModel && !$user?.isPro) {
                toast.warning($i18n.t("This is an exclusive service for pro users. \n Please upgrade your pro permissions first!"));
              } else {
                changeModel(item.value);
              }
            }}
          >
            <div class="flex items-center gap-2">
              <div class="flex flex-col line-clamp-1">
                <span class="text-sm text-gray-900 dark:text-gray-100">{item.label}</span>
                <span class="text-xs text-gray-600 dark:text-gray-500">Suitable for most tasks</span>
              </div>
            </div>

            <div class="ml-auto">
              <Check checkFlag={selectedList.find((sitem) => sitem === item.value)??""}/>
            </div>
          </button>
        <!-- {:else}
          <div>
            <div
              class="block px-3 py-2 text-sm text-gray-700 dark:text-gray-100"
            >
              {$i18n.t("No results found")}
            </div>
          </div> -->
        {/each}

        <!-- {#if !(searchValue.trim() in $MODEL_DOWNLOAD_POOL) && searchValue && ollamaVersion && $user?.role === "admin"}
          <button
            class="flex w-full font-medium line-clamp-1 select-none items-center rounded-button py-2 pl-3 pr-1.5 text-sm text-gray-700 dark:text-gray-100 outline-none transition-all duration-75 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg cursor-pointer data-[highlighted]:bg-muted"
            on:click={() => {
              pullModelHandler();
            }}
          >
            {$i18n.t(`Pull "{{searchValue}}" from Ollama.com`, {
              searchValue: searchValue,
            })}
          </button>
        {/if} -->

        <!-- {#each Object.keys($MODEL_DOWNLOAD_POOL) as model}
          <div
            class="flex w-full justify-between font-medium select-none rounded-button py-2 pl-3 pr-1.5 text-sm text-gray-700 dark:text-gray-100 outline-none transition-all duration-75 rounded-lg cursor-pointer data-[highlighted]:bg-muted"
          >
            <div class="flex">
              <div class="-ml-2 mr-2.5 translate-y-0.5">
                <svg
                  class="size-4"
                  viewBox="0 0 24 24"
                  fill="currentColor"
                  xmlns="http://www.w3.org/2000/svg"
                  ><style>
                    .spinner_ajPY {
                      transform-origin: center;
                      animation: spinner_AtaB 0.75s infinite linear;
                    }
                    @keyframes spinner_AtaB {
                      100% {
                        transform: rotate(360deg);
                      }
                    }
                  </style><path
                    d="M12,1A11,11,0,1,0,23,12,11,11,0,0,0,12,1Zm0,19a8,8,0,1,1,8-8A8,8,0,0,1,12,20Z"
                    opacity=".25"
                  /><path
                    d="M10.14,1.16a11,11,0,0,0-9,8.92A1.59,1.59,0,0,0,2.46,12,1.52,1.52,0,0,0,4.11,10.7a8,8,0,0,1,6.66-6.61A1.42,1.42,0,0,0,12,2.69h0A1.57,1.57,0,0,0,10.14,1.16Z"
                    class="spinner_ajPY"
                  /></svg
                >
              </div>

              <div class="flex flex-col self-start">
                <div class="line-clamp-1">
                  Downloading "{model}" {"pullProgress" in
                  $MODEL_DOWNLOAD_POOL[model]
                    ? `(${$MODEL_DOWNLOAD_POOL[model].pullProgress}%)`
                    : ""}
                </div>

                {#if "digest" in $MODEL_DOWNLOAD_POOL[model] && $MODEL_DOWNLOAD_POOL[model].digest}
                  <div
                    class="-mt-1 h-fit text-[0.7rem] dark:text-gray-500 line-clamp-1"
                  >
                    {$MODEL_DOWNLOAD_POOL[model].digest}
                  </div>
                {/if}
              </div>
            </div>

            <div class="mr-2 translate-y-0.5">
              <Tooltip content={$i18n.t("Cancel")}>
                <button
                  class="text-gray-800 dark:text-gray-100"
                  on:click={() => {
                    cancelModelPullHandler(model);
                  }}
                >
                  <svg
                    class="w-4 h-4 text-gray-800 dark:text-white"
                    aria-hidden="true"
                    xmlns="http://www.w3.org/2000/svg"
                    width="24"
                    height="24"
                    fill="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      stroke="currentColor"
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M6 18 17.94 6M18 18 6.06 6"
                    />
                  </svg>
                </button>
              </Tooltip>
            </div>
          </div>
        {/each} -->
      </div>

      <div class="hidden w-[42rem]" />
      <div class="hidden w-[32rem]" />
    </slot>
  </DropdownMenu.Content>
</DropdownMenu.Root>

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
