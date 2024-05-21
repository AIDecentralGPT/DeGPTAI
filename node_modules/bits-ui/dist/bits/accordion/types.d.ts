import type { HTMLDivAttributes, Transition } from "../../internal/index.js";
import type { CustomEventHandler } from "../../index.js";
import type { HTMLButtonAttributes } from "svelte/elements";
import type * as I from "./_types.js";
type Props<Multiple extends boolean> = I.Props<Multiple> & HTMLDivAttributes;
type ItemProps = I.ItemProps & HTMLDivAttributes;
type HeaderProps = I.HeaderProps & HTMLDivAttributes;
type TriggerProps = I.TriggerProps & HTMLButtonAttributes;
type ContentProps<T extends Transition = Transition, In extends Transition = Transition, Out extends Transition = Transition> = I.ContentProps<T, In, Out> & HTMLDivAttributes;
type TriggerEvents = {
    click: CustomEventHandler<MouseEvent, HTMLButtonElement>;
    keydown: CustomEventHandler<KeyboardEvent, HTMLButtonElement>;
};
export type { Props, ItemProps, HeaderProps, TriggerProps, ContentProps, TriggerEvents, };
