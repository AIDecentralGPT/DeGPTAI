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
export type SelectItemIndicatorProps = typeof __propDef.props;
export type SelectItemIndicatorEvents = typeof __propDef.events;
export type SelectItemIndicatorSlots = typeof __propDef.slots;
export default class SelectItemIndicator extends SvelteComponent<SelectItemIndicatorProps, SelectItemIndicatorEvents, SelectItemIndicatorSlots> {
}
export {};
