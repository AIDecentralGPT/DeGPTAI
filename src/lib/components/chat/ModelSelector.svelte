<script lang="ts">
  import { setDefaultModels } from "$lib/apis/configs";
  import { models, settings, user, mobile, deApiBaseUrl } from "$lib/stores";
  import { getContext } from "svelte";
  import { toast } from "svelte-sonner";
  import Selector from "./ModelSelector/Selector.svelte";
  import ModelDeSelector from "./ModelDeSelector.svelte";

  const i18n = getContext("i18n");

  export let className = "w-[30rem]";

  export let selectedModels = [""];
  export let modelsList = [""];
  export let disabled = false;

  export let showSetDefault = true;

  const saveDefaultModel = async () => {
    const hasEmptyModel = selectedModels.filter((it) => it === "");
    if (hasEmptyModel.length) {
      toast.error($i18n.t("Choose a model before saving..."));
      return;
    }
    settings.set({ ...$settings, models: selectedModels });
    localStorage.setItem("settings", JSON.stringify($settings));

    if ($user?.role === "admin") {
      console.log("setting default models globally");
      await setDefaultModels(localStorage.token, selectedModels.join(","));
    }
    toast.success($i18n.t("Default model updated"));
  };

  $: if (selectedModels.length > 0 && $models.length > 0) {
    console.log("==================================");
    selectedModels = selectedModels.map((model) => {
      if (selectedModels.length === 1) {
        return selectedModels[0] === "" ? $models[0]?.model : model;
      } else {
        return $models.map((m) => m.id).includes(model) ? model : ""; 
      }
    });
  }

</script>

<div class="flex flex-col w-full items-center md:items-start">
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
          />
        </div>
      </div>
    </div>
  {/each}
</div>

{#if showSetDefault && !$mobile}
  <div class="text-left mt-0.5 ml-1 text-[0.7rem] text-gray-500">
    <button on:click={saveDefaultModel}> {$i18n.t("Set as default")}</button>
  </div>
{/if}

<ModelDeSelector/>

