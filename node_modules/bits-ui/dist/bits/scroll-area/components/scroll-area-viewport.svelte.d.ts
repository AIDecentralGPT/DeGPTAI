import { SvelteComponent } from "svelte";
import type { ViewportProps } from "../types.js";
declare const __propDef: {
    props: ViewportProps;
    events: {
        [evt: string]: CustomEvent<any>;
    };
    slots: {
        default: {
            builder: {
                style: string;
                id: string;
            } & {
                [x: `data-melt-${string}`]: "";
            } & {
                action: <Node_2 extends unknown>(node: HTMLElement) => {
                    destroy(): void;
                };
            };
        };
    };
};
export type ScrollAreaViewportProps = typeof __propDef.props;
export type ScrollAreaViewportEvents = typeof __propDef.events;
export type ScrollAreaViewportSlots = typeof __propDef.slots;
export default class ScrollAreaViewport extends SvelteComponent<ScrollAreaViewportProps, ScrollAreaViewportEvents, ScrollAreaViewportSlots> {
}
export {};
