import { SvelteComponent } from "svelte";
import type { TriggerEvents, TriggerProps } from "../types.js";
declare const __propDef: {
    props: TriggerProps;
    slots: {
        default: {
            builder: {
                role: "button";
                'aria-haspopup': "dialog";
                'aria-expanded': boolean;
                'data-state': string;
                'aria-controls': string;
                id: string;
            } & {
                [x: `data-melt-${string}`]: "";
            } & {
                action: (node: HTMLElement) => import("@melt-ui/svelte/internal/types").MeltActionReturn<"blur" | "focus" | "pointerenter" | "pointerleave">;
            };
        };
    };
    events: TriggerEvents;
};
export type LinkPreviewTriggerProps = typeof __propDef.props;
export type LinkPreviewTriggerEvents = typeof __propDef.events;
export type LinkPreviewTriggerSlots = typeof __propDef.slots;
export default class LinkPreviewTrigger extends SvelteComponent<LinkPreviewTriggerProps, LinkPreviewTriggerEvents, LinkPreviewTriggerSlots> {
}
export {};
