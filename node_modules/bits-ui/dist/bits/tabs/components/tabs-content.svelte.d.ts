import { SvelteComponent } from "svelte";
import type { ContentProps } from "../types.js";
declare const __propDef: {
    props: ContentProps;
    events: {
        [evt: string]: CustomEvent<any>;
    };
    slots: {
        default: {
            builder: {
                role: string;
                'aria-labelledby': string;
                hidden: boolean | undefined;
                tabindex: number;
            } & {
                [x: `data-melt-${string}`]: "";
            } & {
                action: import("svelte/action").Action<any, any, Record<never, any>>;
            };
        };
    };
};
export type TabsContentProps = typeof __propDef.props;
export type TabsContentEvents = typeof __propDef.events;
export type TabsContentSlots = typeof __propDef.slots;
export default class TabsContent extends SvelteComponent<TabsContentProps, TabsContentEvents, TabsContentSlots> {
}
export {};
