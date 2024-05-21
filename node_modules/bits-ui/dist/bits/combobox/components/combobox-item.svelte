<script>import { melt } from "@melt-ui/svelte";
import { setItemCtx } from "../ctx.js";
import { createDispatcher } from "../../../internal/events.js";
export let value;
export let disabled = void 0;
export let label = void 0;
export let asChild = false;
export let el = void 0;
const {
  elements: { option: item },
  helpers: { isSelected: isSelectedStore },
  getAttrs
} = setItemCtx(value);
const dispatch = createDispatcher();
const attrs = getAttrs("item");
$:
  if (!label && typeof value === "string")
    label = value;
$:
  builder = $item({ value, disabled, label });
$:
  Object.assign(builder, attrs);
$:
  isSelected = $isSelectedStore(value);
</script>

<!-- svelte-ignore a11y-no-static-element-interactions / applied by melt's builder-->

{#if asChild}
	<slot {builder} {isSelected} />
{:else}
	<div
		bind:this={el}
		{...builder} use:builder.action
		{...$$restProps}
		on:m-click={dispatch}
		on:m-pointermove={dispatch}
		on:focusin
		on:keydown
		on:focusout
		on:pointerleave
	>
		<slot {builder} {isSelected}>
			{label ? label : value}
		</slot>
	</div>
{/if}
