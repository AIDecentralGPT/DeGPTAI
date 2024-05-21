import type { HTMLDivAttributes } from "../../internal/index.js";
import type { CustomEventHandler } from "../../index.js";
import type { HTMLButtonAttributes } from "svelte/elements";
import type * as I from "./_types.js";
import type { ContentProps } from "../floating/types.js";
type Props = I.Props;
type TriggerProps = I.TriggerProps & HTMLButtonAttributes;
type CloseProps = I.CloseProps & HTMLButtonAttributes;
type ArrowProps = I.ArrowProps & HTMLDivAttributes;
type TriggerEvents<T extends Element = HTMLButtonElement> = {
    click: CustomEventHandler<MouseEvent, T>;
    keydown: CustomEventHandler<KeyboardEvent, T>;
};
type CloseEvents = TriggerEvents;
export type { Props, CloseProps, ArrowProps, ContentProps, TriggerProps, TriggerEvents, CloseEvents, };
