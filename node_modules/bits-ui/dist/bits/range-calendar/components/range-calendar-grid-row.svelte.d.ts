import { SvelteComponent } from "svelte";
import type { GridRowProps } from "../types.js";
declare const __propDef: {
    props: GridRowProps;
    events: {
        [evt: string]: CustomEvent<any>;
    };
    slots: {
        default: {
            attrs: Record<string, string>;
        };
    };
};
export type RangeCalendarGridRowProps = typeof __propDef.props;
export type RangeCalendarGridRowEvents = typeof __propDef.events;
export type RangeCalendarGridRowSlots = typeof __propDef.slots;
export default class RangeCalendarGridRow extends SvelteComponent<RangeCalendarGridRowProps, RangeCalendarGridRowEvents, RangeCalendarGridRowSlots> {
}
export {};
