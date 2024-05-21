import { SvelteComponent } from "svelte";
import type { HeadCellProps } from "../types.js";
declare const __propDef: {
    props: HeadCellProps;
    events: {
        [evt: string]: CustomEvent<any>;
    };
    slots: {
        default: {};
    };
};
export type RangeCalendarHeadCellProps = typeof __propDef.props;
export type RangeCalendarHeadCellEvents = typeof __propDef.events;
export type RangeCalendarHeadCellSlots = typeof __propDef.slots;
export default class RangeCalendarHeadCell extends SvelteComponent<RangeCalendarHeadCellProps, RangeCalendarHeadCellEvents, RangeCalendarHeadCellSlots> {
}
export {};
