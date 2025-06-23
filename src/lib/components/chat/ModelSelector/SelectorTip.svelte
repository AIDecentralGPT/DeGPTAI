<script lang="ts">
  import { DropdownMenu } from "bits-ui";

  import { flyAndScale } from "$lib/utils/transitions";
  import { createEventDispatcher, getContext } from "svelte";

  import Check from "$lib/components/icons/Check.svelte";


  import { mobile } from "$lib/stores";

  const dispatch = createEventDispatcher();

  const i18n = getContext('i18n');

  export let value = "";

  export let items = [{ value: "mango", label: "Mango", "info": {"tip": "mango", "desc": "desc"} }];

  export let selectedList: any = [];

  export let className = "w-[380px]";

  let show = false;

  function changeModel(val:string) {
    // const selModel = selectedList.find((item) => item === val) ?? "";
    // if (selModel) {
    //   if(selectedList.length > 1) {
    //     let index = selectedList.indexOf(selModel);
    //     selectedList.splice(index, 1);
    //   } else {
    //     toast.warning($i18n.t("Please select at least one model."));
    //   }     
    // } else {
    //   if (selectedList.length > 3) {
    //     toast.warning($i18n.t("You can select up to four models at most."));
    //   } else {
    //     selectedList.push(val);
    //   }
    // }
    selectedList = [];
    selectedList.push(val);
    dispatch('childEvent', selectedList);
    show = false;
  }

  let seltype = 1;
  $: {
    if (show) {
      let checkModels = items.filter(item => selectedList.includes(item.value));
      if (checkModels.length > 0) {
        seltype = checkModels[0]?.info?.type;
      } else {
        seltype = 1
      }
    }
  }

</script>

<DropdownMenu.Root bind:open={show}>
  <DropdownMenu.Trigger class="relative text-left">
    <span class="mt-0.5 ml-1 text-[0.7rem] text-gray-500">
      {$i18n.t("Click to select more models")}
    </span>
  </DropdownMenu.Trigger>

  <DropdownMenu.Content
    class=" z-[90] {$mobile ? `w-full max-w-[90%]`: `${className} max-w-[400px]`} justify-start rounded-md  bg-white dark:bg-gray-850 dark:text-white shadow-lg border border-gray-300/30 dark:border-gray-700/50  outline-none "
    transition={flyAndScale}
    side={$mobile ? "bottom" : "bottom-start"}
    sideOffset={4}
  >
    <slot>
      <div class="w-full px-1 my-2 max-h-88 overflow-y-auto max-h-[calc(100vh-200px)]">
        <!-- 基础模型 -->
        <div class="px-2 w-full">
          <button class="flex justify-between items-center cursor-pointer w-full py-1"
            on:click={() => {
              seltype =1;
            }}>
            <span>{$i18n.t("Foundation Model")}</span>
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 1024 1024" 
              version="1.1"
              fill="currentColor"
              class="size-4 {seltype == 1 ? 'rotate-90' : 'none'}">
              <path d="M534.826667 935.466667a47.36 47.36 0 0 1-66.986667-66.773334L835.413333 501.333333 467.84 133.973333a47.36 47.36 0 1 1 66.986667-66.773333l400.64 400.64a47.36 47.36 0 0 1 0 66.986667z"/>
            </svg>
          </button>
          <div class="transition ease-in-out delay-150 py-2 {seltype == 1 ? '' : 'hidden'}">
            {#each items as item (item.value)}
              {#if item?.info?.type == 1}
                <button
                  aria-label="model-item"
                  class="flex item-center w-full text-left font-medium line-clamp-1 select-none items-center rounded-button py-1 pl-2 pr-2 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg cursor-pointer data-[highlighted]:bg-muted"
                  on:click={() => {
                    changeModel(item.value);
                  }}
                >
                  <div class="flex items-center gap-2 mr-1">
                    <div class="flex flex-col line-clamp-1">
                      <span class="text-lg text-gray-900 dark:text-gray-100">{item?.info?.tip}</span>
                      <span class="text-sm text-gray-600 dark:text-gray-500 mt-0.5">{$i18n.t(item?.info?.desc)}</span>
                    </div>
                  </div>
                  <div class="ml-auto">
                    <Check checkFlag={selectedList.find((sitem) => sitem === item.value)??""}/>
                  </div>
                </button>
              {/if}
            {/each}
          </div>
        </div>
        <!-- 高级模型 -->
        <div class="px-2 w-full">
          <button class="flex justify-between items-center cursor-pointer w-full py-1"
            on:click={() => {
              seltype =2;
            }}>
            <span>{$i18n.t("Advanced Model")}</span>
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 1024 1024" 
              version="1.1"
              fill="currentColor"
              class="size-4 {seltype == 2 ? 'rotate-90' : 'none'}">
              <path d="M534.826667 935.466667a47.36 47.36 0 0 1-66.986667-66.773334L835.413333 501.333333 467.84 133.973333a47.36 47.36 0 1 1 66.986667-66.773333l400.64 400.64a47.36 47.36 0 0 1 0 66.986667z"/>
            </svg>
          </button>
          <div class="transition ease-in-out delay-150 py-2 {seltype == 2 ? '' : 'hidden'}">
            {#each items as item (item.value)}
              {#if item?.info?.type == 2}
                <button
                  aria-label="model-item"
                  class="flex item-center w-full text-left font-medium line-clamp-1 select-none items-center rounded-button py-1 pl-2 pr-2 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg cursor-pointer data-[highlighted]:bg-muted"
                  on:click={() => {
                    changeModel(item.value);
                  }}
                >
                  <div class="flex items-center gap-2 mr-1">
                    <div class="flex flex-col line-clamp-1">
                      <span class="text-lg text-gray-900 dark:text-gray-100">{item?.info?.tip}</span>
                      <span class="text-sm text-gray-600 dark:text-gray-500 mt-0.5">{$i18n.t(item?.info?.desc)}</span>
                    </div>
                  </div>
                  <div class="ml-auto">
                    <Check checkFlag={selectedList.find((sitem) => sitem === item.value)??""}/>
                  </div>
                </button>
              {/if}
            {/each}
          </div>
        </div>
        <!-- 顶级模型 -->
        <div class="px-2 w-full">
          <button class="flex justify-between items-center cursor-pointer w-full py-1"
            on:click={() => {
              seltype =3;
            }}>
            <span>{$i18n.t("Top-Level Model")}</span>
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 1024 1024" 
              version="1.1"
              fill="currentColor"
              class="size-4 {seltype == 3 ? 'rotate-90' : 'none'}">
              <path d="M534.826667 935.466667a47.36 47.36 0 0 1-66.986667-66.773334L835.413333 501.333333 467.84 133.973333a47.36 47.36 0 1 1 66.986667-66.773333l400.64 400.64a47.36 47.36 0 0 1 0 66.986667z"/>
            </svg>
          </button>
          <div class="transition ease-in-out delay-150 py-2 {seltype == 3 ? '' : 'hidden'}">
            {#each items as item (item.value)}
              {#if item?.info?.type == 3}
                <button
                  aria-label="model-item"
                  class="flex item-center w-full text-left font-medium line-clamp-1 select-none items-center rounded-button py-1 pl-2 pr-2 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg cursor-pointer data-[highlighted]:bg-muted"
                  on:click={() => {
                    changeModel(item.value);
                  }}
                >
                  <div class="flex items-center gap-2 mr-1">
                    <div class="flex flex-col line-clamp-1">
                      <span class="text-lg text-gray-900 dark:text-gray-100">{item?.info?.tip}</span>
                      <span class="text-sm text-gray-600 dark:text-gray-500 mt-0.5">{$i18n.t(item?.info?.desc)}</span>
                    </div>
                  </div>
                  <div class="ml-auto">
                    <Check checkFlag={selectedList.find((sitem) => sitem === item.value)??""}/>
                  </div>
                </button>
              {/if}
            {/each}
          </div>
        </div>
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