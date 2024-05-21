import { SvelteComponent } from "svelte";
import type { Props } from "../types.js";
declare const __propDef: {
    props: Props;
    events: {
        [evt: string]: CustomEvent<any>;
    };
    slots: {
        default: {
            builder: {
                role: string;
                'data-orientation': import("@melt-ui/svelte/internal/types").Orientation;
            } & {
                [x: `data-melt-${string}`]: "";
            } & {
                action: import("svelte/action").Action<any, any, Record<never, any>>;
            };
        };
    };
};
export type ToolbarProps = typeof __propDef.props;
export type ToolbarEvents = typeof __propDef.events;
export type ToolbarSlots = typeof __propDef.slots;
export default class Toolbar extends SvelteComponent<ToolbarProps, ToolbarEvents, ToolbarSlots> {
}
export {};
