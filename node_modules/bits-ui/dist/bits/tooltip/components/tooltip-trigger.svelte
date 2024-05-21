<script>import { melt } from "@melt-ui/svelte";
import { createDispatcher } from "../../../internal/index.js";
import { getCtx } from "../ctx.js";
export let asChild = false;
export let id = void 0;
export let el = void 0;
const {
  elements: { trigger },
  ids,
  getAttrs
} = getCtx();
const dispatch = createDispatcher();
const attrs = getAttrs("trigger");
$:
  if (id) {
    ids.trigger.set(id);
  }
$:
  builder = $trigger;
$:
  Object.assign(builder, attrs);
</script>

{#if asChild}
	<slot {builder} />
{:else}
	<button
		bind:this={el}
		{...builder} use:builder.action
		type="button"
		{...$$restProps}
		on:m-blur={dispatch}
		on:m-focus={dispatch}
		on:m-keydown={dispatch}
		on:m-pointerdown={dispatch}
		on:m-pointerenter={dispatch}
		on:m-pointerleave={dispatch}
	>
		<slot {builder} />
	</button>
{/if}
