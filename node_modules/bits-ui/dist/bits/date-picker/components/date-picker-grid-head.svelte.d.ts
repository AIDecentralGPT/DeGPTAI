import { SvelteComponent } from "svelte";
import type { GridHeadProps } from "../types.js";
declare const __propDef: {
    props: GridHeadProps;
    events: {
        [evt: string]: CustomEvent<any>;
    };
    slots: {
        default: {
            attrs: {
                "aria-hidden": boolean;
            };
        };
    };
};
export type DatePickerGridHeadProps = typeof __propDef.props;
export type DatePickerGridHeadEvents = typeof __propDef.events;
export type DatePickerGridHeadSlots = typeof __propDef.slots;
export default class DatePickerGridHead extends SvelteComponent<DatePickerGridHeadProps, DatePickerGridHeadEvents, DatePickerGridHeadSlots> {
}
export {};
