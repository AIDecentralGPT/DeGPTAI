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
export type DateRangePickerGridRowProps = typeof __propDef.props;
export type DateRangePickerGridRowEvents = typeof __propDef.events;
export type DateRangePickerGridRowSlots = typeof __propDef.slots;
export default class DateRangePickerGridRow extends SvelteComponent<DateRangePickerGridRowProps, DateRangePickerGridRowEvents, DateRangePickerGridRowSlots> {
}
export {};
