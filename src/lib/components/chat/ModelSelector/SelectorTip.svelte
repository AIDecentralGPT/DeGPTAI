<script lang="ts">
  import { DropdownMenu } from "bits-ui";

  import { flyAndScale } from "$lib/utils/transitions";
  import { createEventDispatcher, getContext } from "svelte";

  import Check from "$lib/components/icons/Check.svelte";


  import { mobile } from "$lib/stores";

  import { toast } from 'svelte-sonner';

  const dispatch = createEventDispatcher();

  const i18n = getContext('i18n');

  export let value = "";

  export let items = [{ value: "mango", label: "Mango", "info": {"tip": "mango", "desc": "desc"} }];

  export let selectedList: any = [];

  export let className = "w-[30rem]";

  let show = false;

  function changeModel(val:string) {
    const selModel = selectedList.find((item) => item === val) ?? "";
    if (selModel) {
      if(selectedList.length > 1) {
        let index = selectedList.indexOf(selModel);
        selectedList.splice(index, 1);
      } else {
        toast.warning($i18n.t("Please select at least one model."));
      }   
    } else {
      if (selectedList.length > 3) {
        toast.warning($i18n.t("You can select up to four models at most."));
      } else {
        selectedList.push(val);
      }
    }
    dispatch('childEvent', selectedList);
  }

</script>

<DropdownMenu.Root bind:open={show}>
  <DropdownMenu.Trigger class="relative text-left">
    <span class="mt-0.5 ml-1 text-[0.7rem] text-gray-500">
      {$i18n.t("Click to select more models")}
    </span>
  </DropdownMenu.Trigger>

  <DropdownMenu.Content
    class=" z-[90] {$mobile ? `w-full`: `${className}`} max-w-[300px] justify-start rounded-md  bg-white dark:bg-gray-850 dark:text-white shadow-lg border border-gray-300/30 dark:border-gray-700/50  outline-none "
    transition={flyAndScale}
    side={$mobile ? "bottom" : "bottom-start"}
    sideOffset={4}
  >
    <slot>
      <div class="px-1 my-2 max-h-88 overflow-y-auto scrollbar-hidden">
        <div class="text-lg px-2 py-1">{$i18n.t("Switch Models")}</div>
        {#each items as item (item.value)}
          <button
            aria-label="model-item"
            class="flex item-center w-full text-left font-medium line-clamp-1 select-none items-center rounded-button py-1 pl-2 pr-2 outline-none transition-all duration-75 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg cursor-pointer data-[highlighted]:bg-muted"
            on:click={() => {
              changeModel(item.value);
            }}
          >
            <div class="flex items-center gap-2">
              <div class="flex flex-col line-clamp-1">
                <span class="text-xs text-gray-900 dark:text-gray-100">{item?.info?.tip}</span>
                <span class="text-xs text-gray-600 dark:text-gray-500">{$i18n.t(item?.info?.desc)}</span>
              </div>
            </div>

            <div class="ml-auto">
              <Check checkFlag={selectedList.find((sitem) => sitem === item.value)??""}/>
            </div>
          </button>
        {/each}
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