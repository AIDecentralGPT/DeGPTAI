<script>import { melt } from "@melt-ui/svelte";
import { getCtx } from "../ctx.js";
import { createDispatcher } from "../../../internal/events.js";
export let asChild = false;
export let el = void 0;
const {
  elements: { link },
  getAttrs
} = getCtx();
const dispatch = createDispatcher();
const attrs = getAttrs("link");
$:
  builder = $link;
$:
  Object.assign(builder, attrs);
</script>

{#if asChild}
	<slot {builder} />
{:else}
	<!-- svelte-ignore a11y-no-static-element-interactions -->
	<svelte:element
		this={"a"}
		bind:this={el}
		{...builder} use:builder.action
		{...$$restProps}
		on:click
		on:m-keydown={dispatch}
	>
		<slot {builder} />
	</svelte:element>
{/if}
