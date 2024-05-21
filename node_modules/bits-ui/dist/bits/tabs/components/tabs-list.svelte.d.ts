import { SvelteComponent } from "svelte";
import type { ListProps } from "../types.js";
declare const __propDef: {
    props: ListProps;
    events: {
        [evt: string]: CustomEvent<any>;
    };
    slots: {
        default: {
            builder: {
                role: string;
                'aria-orientation': import("@melt-ui/svelte/internal/types").Orientation;
                'data-orientation': import("@melt-ui/svelte/internal/types").Orientation;
            } & {
                [x: `data-melt-${string}`]: "";
            } & {
                action: import("svelte/action").Action<any, any, Record<never, any>>;
            };
        };
    };
};
export type TabsListProps = typeof __propDef.props;
export type TabsListEvents = typeof __propDef.events;
export type TabsListSlots = typeof __propDef.slots;
export default class TabsList extends SvelteComponent<TabsListProps, TabsListEvents, TabsListSlots> {
}
export {};
