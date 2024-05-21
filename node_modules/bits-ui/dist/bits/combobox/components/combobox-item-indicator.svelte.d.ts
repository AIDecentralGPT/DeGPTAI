import { SvelteComponent } from "svelte";
import type { IndicatorProps } from "../types.js";
declare const __propDef: {
    props: IndicatorProps;
    events: {
        [evt: string]: CustomEvent<any>;
    };
    slots: {
        default: {
            attrs: Record<string, string>;
            isSelected: boolean;
        };
    };
};
export type ComboboxItemIndicatorProps = typeof __propDef.props;
export type ComboboxItemIndicatorEvents = typeof __propDef.events;
export type ComboboxItemIndicatorSlots = typeof __propDef.slots;
export default class ComboboxItemIndicator extends SvelteComponent<ComboboxItemIndicatorProps, ComboboxItemIndicatorEvents, ComboboxItemIndicatorSlots> {
}
export {};
