import { SvelteComponent } from "svelte";
import type { HeaderProps } from "../types.js";
declare const __propDef: {
    props: HeaderProps;
    events: {
        [evt: string]: CustomEvent<any>;
    };
    slots: {
        default: {
            attrs: Record<string, string>;
        };
    };
};
export type DateRangePickerHeaderProps = typeof __propDef.props;
export type DateRangePickerHeaderEvents = typeof __propDef.events;
export type DateRangePickerHeaderSlots = typeof __propDef.slots;
export default class DateRangePickerHeader extends SvelteComponent<DateRangePickerHeaderProps, DateRangePickerHeaderEvents, DateRangePickerHeaderSlots> {
}
export {};
