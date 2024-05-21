import { SvelteComponent } from "svelte";
import type { ItemIndicatorProps } from "../types.js";
declare const __propDef: {
    props: ItemIndicatorProps;
    events: {
        [evt: string]: CustomEvent<any>;
    };
    slots: {
        default: {
            checked: boolean;
            attrs: Record<string, string>;
        };
    };
};
export type RadioGroupItemIndicatorProps = typeof __propDef.props;
export type RadioGroupItemIndicatorEvents = typeof __propDef.events;
export type RadioGroupItemIndicatorSlots = typeof __propDef.slots;
export default class RadioGroupItemIndicator extends SvelteComponent<RadioGroupItemIndicatorProps, RadioGroupItemIndicatorEvents, RadioGroupItemIndicatorSlots> {
}
export {};
