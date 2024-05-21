import { SvelteComponent } from "svelte";
import type { ThumbProps } from "../types.js";
declare const __propDef: {
    props: ThumbProps;
    events: {
        [evt: string]: CustomEvent<any>;
    };
    slots: {
        default: {
            builder: {
                style: string;
                'data-state': string;
            } & {
                [x: `data-melt-${string}`]: "";
            } & {
                action: (node: HTMLElement) => import("@melt-ui/svelte/internal/types").MeltActionReturn<"pointerdown" | "pointerup">;
            };
        };
    };
};
export type ScrollAreaThumbYProps = typeof __propDef.props;
export type ScrollAreaThumbYEvents = typeof __propDef.events;
export type ScrollAreaThumbYSlots = typeof __propDef.slots;
export default class ScrollAreaThumbY extends SvelteComponent<ScrollAreaThumbYProps, ScrollAreaThumbYEvents, ScrollAreaThumbYSlots> {
}
export {};
