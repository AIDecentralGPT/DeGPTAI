<script>import { getCtx } from "../ctx.js";
export let placeholder = "";
export let asChild = false;
export let el = void 0;
const {
  states: { selectedLabel },
  getAttrs
} = getCtx();
const attrs = getAttrs("value");
$:
  label = $selectedLabel;
</script>

{#if asChild}
	<slot {label} {attrs} />
{:else}
	<span bind:this={el} {...$$restProps} {...attrs} data-placeholder={!label ? "" : undefined}>
		{label ? label : placeholder}
	</span>
{/if}
