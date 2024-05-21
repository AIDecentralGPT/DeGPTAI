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
export type CalendarGridRowProps = typeof __propDef.props;
export type CalendarGridRowEvents = typeof __propDef.events;
export type CalendarGridRowSlots = typeof __propDef.slots;
export default class CalendarGridRow extends SvelteComponent<CalendarGridRowProps, CalendarGridRowEvents, CalendarGridRowSlots> {
}
export {};
