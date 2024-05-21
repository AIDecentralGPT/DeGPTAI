<script>import { createDispatcher } from "../../../internal/events.js";
import { getCtx } from "../ctx.js";
import { melt } from "@melt-ui/svelte";
export let asChild = void 0;
export let page;
export let el = void 0;
const {
  elements: { pageTrigger },
  getAttrs
} = getCtx();
const attrs = getAttrs("page");
$:
  builder = $pageTrigger(page);
$:
  Object.assign(builder, attrs);
const dispatch = createDispatcher();
</script>

{#if asChild}
	<slot {builder} />
{:else}
	<button bind:this={el} type="button" {...builder} use:builder.action on:m-click={dispatch} {...$$restProps}>
		<slot {builder}>
			{page.value}
		</slot>
	</button>
{/if}
