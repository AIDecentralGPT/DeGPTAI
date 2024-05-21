import { SvelteComponent } from "svelte";
import type { CancelEvents } from "../types.js";
declare const __propDef: {
    props: import("../types.js").TriggerProps;
    slots: {
        default: {
            builder: {
                readonly type: "button";
            } & {
                [x: `data-melt-${string}`]: "";
            } & {
                action: (node: HTMLElement) => import("@melt-ui/svelte/internal/types").MeltActionReturn<"keydown" | "click">;
            };
        };
    };
    events: CancelEvents;
};
export type AlertDialogCancelProps = typeof __propDef.props;
export type AlertDialogCancelEvents = typeof __propDef.events;
export type AlertDialogCancelSlots = typeof __propDef.slots;
export default class AlertDialogCancel extends SvelteComponent<AlertDialogCancelProps, AlertDialogCancelEvents, AlertDialogCancelSlots> {
}
export {};
