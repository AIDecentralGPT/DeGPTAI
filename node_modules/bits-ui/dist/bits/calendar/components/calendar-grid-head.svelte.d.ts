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
export type CalendarGridHeadProps = typeof __propDef.props;
export type CalendarGridHeadEvents = typeof __propDef.events;
export type CalendarGridHeadSlots = typeof __propDef.slots;
export default class CalendarGridHead extends SvelteComponent<CalendarGridHeadProps, CalendarGridHeadEvents, CalendarGridHeadSlots> {
}
export {};
