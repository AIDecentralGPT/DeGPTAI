<script lang="ts">
  import { getContext } from "svelte";
  import { DateInput, localeFromDateFnsLocale } from "@gregg-cbs/svelte-date-picker";
  
  const i18n = getContext("i18n");

  export let selectedDate: Date;

</script>

<div class="flex">
  <DateInput class="ml-2 rounded-lg dark:text-gray-300 bg-gray-200 dark:bg-gray-850 dark" locale= { localeFromDateFnsLocale($i18n.language) }
    dynamicPositioning={true} format='yyyy-MM-dd' placeholder={$i18n.t("Select date")} bind:value={selectedDate} />
</div>

<style>

</style>