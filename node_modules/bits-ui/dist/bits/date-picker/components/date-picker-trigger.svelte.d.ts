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
export type DatePickerTriggerProps = typeof __propDef.props;
export type DatePickerTriggerEvents = typeof __propDef.events;
export type DatePickerTriggerSlots = typeof __propDef.slots;
export default class DatePickerTrigger extends SvelteComponent<DatePickerTriggerProps, DatePickerTriggerEvents, DatePickerTriggerSlots> {
}
export {};
