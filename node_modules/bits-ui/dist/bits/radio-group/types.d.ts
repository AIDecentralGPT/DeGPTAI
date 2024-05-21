import type { HTMLDivAttributes } from "../../internal/index.js";
import type { CustomEventHandler } from "../../index.js";
import type { HTMLButtonAttributes, HTMLInputAttributes } from "svelte/elements";
import type * as I from "./_types.js";
type Props = I.Props & HTMLDivAttributes;
type InputProps = I.InputProps & HTMLInputAttributes;
type ItemProps = I.ItemProps & HTMLButtonAttributes;
type ItemIndicatorProps = I.ItemIndicatorProps & HTMLDivAttributes;
type ItemEvents<T extends Element = HTMLButtonElement> = {
    click: CustomEventHandler<MouseEvent, T>;
    keydown: CustomEventHandler<KeyboardEvent, T>;
    focus: CustomEventHandler<FocusEvent, T>;
};
export type { Props, InputProps, ItemProps, ItemIndicatorProps, ItemEvents, };
