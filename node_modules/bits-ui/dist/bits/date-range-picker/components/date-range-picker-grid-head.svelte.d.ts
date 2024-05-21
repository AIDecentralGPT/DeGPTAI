import { SvelteComponent } from "svelte";
import type { GridHeadProps } from "../types.js";
declare const __propDef: {
    props: GridHeadProps;
    events: {
        [evt: string]: CustomEvent<any>;
    };
    slots: {
        default: {};
    };
};
export type DateRangePickerGridHeadProps = typeof __propDef.props;
export type DateRangePickerGridHeadEvents = typeof __propDef.events;
export type DateRangePickerGridHeadSlots = typeof __propDef.slots;
export default class DateRangePickerGridHead extends SvelteComponent<DateRangePickerGridHeadProps, DateRangePickerGridHeadEvents, DateRangePickerGridHeadSlots> {
}
export {};
