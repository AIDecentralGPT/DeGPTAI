import type { DOMEl, HTMLDivAttributes } from "../../internal/index.js";
import type { CustomEventHandler } from "../../index.js";
import type { HTMLButtonAttributes, HTMLInputAttributes } from "svelte/elements";
import type * as I from "./_types.js";
type Props = I.Props & HTMLButtonAttributes;
type IndicatorProps = I.IndicatorProps & HTMLDivAttributes;
type InputProps = Omit<HTMLInputAttributes, "value"> & DOMEl<HTMLInputElement>;
type Events = {
    click: CustomEventHandler<MouseEvent, HTMLButtonElement>;
    keydown: CustomEventHandler<KeyboardEvent, HTMLButtonElement>;
};
export type { Props, IndicatorProps, InputProps, Events, };
