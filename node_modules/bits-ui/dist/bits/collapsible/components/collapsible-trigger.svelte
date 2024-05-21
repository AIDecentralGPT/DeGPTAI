<script>import { melt } from "@melt-ui/svelte";
import { createDispatcher } from "../../../internal/events.js";
import { getCtx } from "../ctx.js";
export let asChild = false;
export let el = void 0;
const {
  elements: { trigger },
  getAttrs
} = getCtx();
const dispatch = createDispatcher();
const attrs = getAttrs("trigger");
$:
  builder = $trigger;
$:
  Object.assign(builder, attrs);
</script>

{#if asChild}
	<slot {builder} />
{:else}
	<button bind:this={el} {...builder} use:builder.action type="button" {...$$restProps} on:m-click={dispatch}>
		<slot {builder} />
	</button>
{/if}
