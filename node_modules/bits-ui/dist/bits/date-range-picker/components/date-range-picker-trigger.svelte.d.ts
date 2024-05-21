import { SvelteComponent } from "svelte";
import type { TriggerEvents, TriggerProps } from "../types.js";
declare const __propDef: {
    props: TriggerProps;
    slots: {
        default: {
            builder: {
                'aria-label': string;
                'data-segment': string;
                disabled: boolean | undefined;
                'data-state': "open" | "closed";
                'aria-expanded': "false" | "true";
                'aria-controls': string;
                role: "button";
                id: string;
                'aria-haspopup': "dialog";
            } & {
                "data-melt-popover-trigger": "";
            } & {
                action: (node: HTMLElement) => import("@melt-ui/svelte/internal/types").MeltActionReturn<"keydown" | "click">;
            };
        };
    };
    events: TriggerEvents;
};
export type DateRangePickerTriggerProps = typeof __propDef.props;
export type DateRangePickerTriggerEvents = typeof __propDef.events;
export type DateRangePickerTriggerSlots = typeof __propDef.slots;
export default class DateRangePickerTrigger extends SvelteComponent<DateRangePickerTriggerProps, DateRangePickerTriggerEvents, DateRangePickerTriggerSlots> {
}
export {};
