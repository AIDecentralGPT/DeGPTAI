<script>import { getCtx } from "../ctx.js";
import { melt } from "@melt-ui/svelte";
export let asChild = false;
export let el = void 0;
const {
  elements: { corner },
  getAttrs
} = getCtx();
const bitsAttrs = getAttrs("corner");
$:
  attrs = {
    ...$$restProps,
    ...bitsAttrs
  };
$:
  builder = $corner;
$:
  Object.assign(builder, attrs);
</script>

{#if asChild}
	<slot {builder} />
{:else}
	<div {...builder} use:builder.action bind:this={el}>
		<slot {builder} />
	</div>
{/if}
