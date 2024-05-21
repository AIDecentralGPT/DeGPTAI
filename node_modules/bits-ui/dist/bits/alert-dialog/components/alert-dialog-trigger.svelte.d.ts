import { SvelteComponent } from "svelte";
import type { TriggerEvents, TriggerProps } from "../types.js";
declare const __propDef: {
    props: TriggerProps;
    slots: {
        default: {
            builder: {
                readonly 'aria-haspopup': "dialog";
                readonly 'aria-expanded': boolean;
                readonly type: "button";
            } & {
                [x: `data-melt-${string}`]: "";
            } & {
                action: (node: HTMLElement) => import("@melt-ui/svelte/internal/types").MeltActionReturn<"keydown" | "click">;
            };
        };
    };
    events: TriggerEvents;
};
export type AlertDialogTriggerProps = typeof __propDef.props;
export type AlertDialogTriggerEvents = typeof __propDef.events;
export type AlertDialogTriggerSlots = typeof __propDef.slots;
export default class AlertDialogTrigger extends SvelteComponent<AlertDialogTriggerProps, AlertDialogTriggerEvents, AlertDialogTriggerSlots> {
}
export {};
