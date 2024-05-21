import { SvelteComponent } from "svelte";
import type { CloseEvents } from "../types.js";
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
    events: CloseEvents;
};
export type DialogCloseProps = typeof __propDef.props;
export type DialogCloseEvents = typeof __propDef.events;
export type DialogCloseSlots = typeof __propDef.slots;
export default class DialogClose extends SvelteComponent<DialogCloseProps, DialogCloseEvents, DialogCloseSlots> {
}
export {};
