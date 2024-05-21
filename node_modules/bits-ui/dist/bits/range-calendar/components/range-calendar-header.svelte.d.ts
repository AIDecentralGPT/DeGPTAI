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
export type RangeCalendarHeaderProps = typeof __propDef.props;
export type RangeCalendarHeaderEvents = typeof __propDef.events;
export type RangeCalendarHeaderSlots = typeof __propDef.slots;
export default class RangeCalendarHeader extends SvelteComponent<RangeCalendarHeaderProps, RangeCalendarHeaderEvents, RangeCalendarHeaderSlots> {
}
export {};
