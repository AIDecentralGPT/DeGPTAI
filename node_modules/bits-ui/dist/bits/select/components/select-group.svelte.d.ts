import { SvelteComponent } from "svelte";
import type { GroupProps } from "../types.js";
declare const __propDef: {
    props: GroupProps;
    events: {
        [evt: string]: CustomEvent<any>;
    };
    slots: {
        default: {
            builder: {
                role: string;
                'aria-labelledby': string;
            } & {
                [x: `data-melt-${string}`]: "";
            } & {
                action: import("svelte/action").Action<any, any, Record<never, any>>;
            };
        };
    };
};
export type SelectGroupProps = typeof __propDef.props;
export type SelectGroupEvents = typeof __propDef.events;
export type SelectGroupSlots = typeof __propDef.slots;
export default class SelectGroup extends SvelteComponent<SelectGroupProps, SelectGroupEvents, SelectGroupSlots> {
}
export {};
