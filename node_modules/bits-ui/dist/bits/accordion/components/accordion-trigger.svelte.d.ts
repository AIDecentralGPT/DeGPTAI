import { SvelteComponent } from "svelte";
import type { TriggerEvents, TriggerProps } from "../types.js";
declare const __propDef: {
    props: TriggerProps;
    slots: {
        default: {
            builder: {
                disabled: boolean | undefined;
                'aria-expanded': boolean;
                'aria-disabled': boolean;
                'data-disabled': boolean | undefined;
                'data-value': string;
                'data-state': string;
            } & {
                [x: `data-melt-${string}`]: "";
            } & {
                action: (node: HTMLElement) => import("@melt-ui/svelte/internal/types").MeltActionReturn<"keydown" | "click">;
            };
        };
    };
    events: TriggerEvents;
};
export type AccordionTriggerProps = typeof __propDef.props;
export type AccordionTriggerEvents = typeof __propDef.events;
export type AccordionTriggerSlots = typeof __propDef.slots;
export default class AccordionTrigger extends SvelteComponent<AccordionTriggerProps, AccordionTriggerEvents, AccordionTriggerSlots> {
}
export {};
