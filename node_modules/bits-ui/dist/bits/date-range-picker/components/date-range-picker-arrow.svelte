<script>import { getCtx } from "../ctx.js";
import { melt } from "@melt-ui/svelte";
export let asChild = false;
export let el = void 0;
export let size = 8;
const {
  elements: { arrow },
  updateOption,
  getPopoverAttrs
} = getCtx();
const attrs = getPopoverAttrs("arrow");
$:
  updateOption("arrowSize", size);
$:
  builder = $arrow;
$:
  Object.assign(builder, attrs);
</script>

{#if asChild}
	<slot {builder} />
{:else}
	<div bind:this={el} {...builder} use:builder.action {...$$restProps} />
{/if}
