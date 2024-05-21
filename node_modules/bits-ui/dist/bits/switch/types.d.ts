import type { DOMEl, HTMLSpanAttributes } from "../../internal/index.js";
import type { HTMLButtonAttributes, HTMLInputAttributes } from "svelte/elements";
import type { CustomEventHandler } from "../../index.js";
import type * as I from "./_types.js";
type Props = I.Props & HTMLButtonAttributes;
type ThumbProps = I.ThumbProps & HTMLSpanAttributes;
type InputProps = HTMLInputAttributes & DOMEl<HTMLInputElement>;
type Events<T extends Element = HTMLButtonElement> = {
    click: CustomEventHandler<MouseEvent, T>;
    keydown: CustomEventHandler<KeyboardEvent, T>;
};
export type { Props, ThumbProps, InputProps, Events, };
