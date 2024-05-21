import { SvelteComponent } from "svelte";
import type { GridBodyProps } from "../types.js";
declare const __propDef: {
    props: GridBodyProps;
    events: {
        [evt: string]: CustomEvent<any>;
    };
    slots: {
        default: {};
    };
};
export type RangeCalendarGridBodyProps = typeof __propDef.props;
export type RangeCalendarGridBodyEvents = typeof __propDef.events;
export type RangeCalendarGridBodySlots = typeof __propDef.slots;
export default class RangeCalendarGridBody extends SvelteComponent<RangeCalendarGridBodyProps, RangeCalendarGridBodyEvents, RangeCalendarGridBodySlots> {
}
export {};
