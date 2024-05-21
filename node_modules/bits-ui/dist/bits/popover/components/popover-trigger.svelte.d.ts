import { SvelteComponent } from "svelte";
import type { TriggerEvents, TriggerProps } from "../types.js";
declare const __propDef: {
    props: TriggerProps;
    slots: {
        default: {
            builder: {
                readonly role: "button";
                readonly 'aria-haspopup': "dialog";
                readonly 'aria-expanded': "false" | "true";
                readonly 'data-state': "open" | "closed";
                readonly 'aria-controls': string;
                readonly id: string;
            } & {
                [x: `data-melt-${string}`]: "";
            } & {
                action: (node: HTMLElement) => import("@melt-ui/svelte/internal/types").MeltActionReturn<"keydown" | "click">;
            };
        };
    };
    events: TriggerEvents;
};
export type PopoverTriggerProps = typeof __propDef.props;
export type PopoverTriggerEvents = typeof __propDef.events;
export type PopoverTriggerSlots = typeof __propDef.slots;
export default class PopoverTrigger extends SvelteComponent<PopoverTriggerProps, PopoverTriggerEvents, PopoverTriggerSlots> {
}
export {};
