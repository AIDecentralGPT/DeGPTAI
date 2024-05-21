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
export type CalendarHeaderProps = typeof __propDef.props;
export type CalendarHeaderEvents = typeof __propDef.events;
export type CalendarHeaderSlots = typeof __propDef.slots;
export default class CalendarHeader extends SvelteComponent<CalendarHeaderProps, CalendarHeaderEvents, CalendarHeaderSlots> {
}
export {};
