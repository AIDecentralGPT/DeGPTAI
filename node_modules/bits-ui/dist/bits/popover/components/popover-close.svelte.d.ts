import { SvelteComponent } from "svelte";
import type { CloseProps, CloseEvents } from "../types.js";
declare const __propDef: {
    props: CloseProps;
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
export type PopoverCloseProps = typeof __propDef.props;
export type PopoverCloseEvents = typeof __propDef.events;
export type PopoverCloseSlots = typeof __propDef.slots;
export default class PopoverClose extends SvelteComponent<PopoverCloseProps, PopoverCloseEvents, PopoverCloseSlots> {
}
export {};
