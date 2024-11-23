<script lang="ts">
  import { setDefaultModels } from "$lib/apis/configs";
  import { models, settings, user } from "$lib/stores";
  import { getContext } from "svelte";
  import { toast } from "svelte-sonner";
  import Selector from "./ModelSelector/Selector.svelte";
  import SelectorTip from "./ModelSelector/SelectorTip.svelte";
  import { updateUserModels } from "$lib/apis/users";

  const i18n = getContext("i18n");

  export let selectedModels = [""];

  const saveDefaultModel = async () => {
    settings.set({ ...$settings, models: selectedModels });
    localStorage.setItem("settings", JSON.stringify($settings));
    let selModels = selectedModels.join(",");
    await updateUserModels(localStorage.token, selModels);
  };

  $: if (selectedModels.length > 0 && $models.length > 0) {
    selectedModels = selectedModels.map((model) => {
      if (selectedModels.length === 1) {
        return selectedModels[0] === "" ? $models[0]?.model : model;
      } else {
        return $models.map((m) => m.id).includes(model) ? model : ""; 
      }
    });
  }

  async function updateSelList(list: any) {
    selectedModels = list.detail;
    await saveDefaultModel();
  }

</script>

<div class="flex flex-col w-full items-start md:items-start">
  {#each selectedModels as selectedModel, selectedModelIdx}
    <div class="flex w-full max-w-fit">
      <div class="overflow-hidden w-full">
        <div class="mr-1 max-w-full">
          <Selector
            placeholder={$i18n.t("Select a model")}
            items={$models
              .filter((model) => model.name !== "hr")
              .map((model) => ({
                value: model.id,
                label: model.name,
                info: model,
              }))}
            bind:selectedList={selectedModels}
            selectedModelIdx={selectedModelIdx}
            value={selectedModel}
            on:childEvent={updateSelList}
          />
        </div>
      </div>
    </div>
  {/each}
</div>

<SelectorTip 
  items={$models
    .filter((model) => model.name !== "hr")
    .map((model) => ({
      value: model.id,
      label: model.name,
      info: model,
    }))}
  bind:selectedList={selectedModels}
  on:childEvent={updateSelList}
/>


