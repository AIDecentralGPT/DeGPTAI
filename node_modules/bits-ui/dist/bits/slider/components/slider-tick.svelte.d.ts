import { SvelteComponent } from "svelte";
import type { TickProps } from "../types.js";
declare const __propDef: {
    props: TickProps;
    events: {
        [evt: string]: CustomEvent<any>;
    };
    slots: {
        default: {
            builder: {
                'data-bounded': boolean | undefined;
                'data-value': number;
                style: string;
            } & {
                [x: `data-melt-${string}`]: "";
            } & {
                action: import("svelte/action").Action<any, any, Record<never, any>>;
            };
        };
    };
};
export type SliderTickProps = typeof __propDef.props;
export type SliderTickEvents = typeof __propDef.events;
export type SliderTickSlots = typeof __propDef.slots;
export default class SliderTick extends SvelteComponent<SliderTickProps, SliderTickEvents, SliderTickSlots> {
}
export {};
