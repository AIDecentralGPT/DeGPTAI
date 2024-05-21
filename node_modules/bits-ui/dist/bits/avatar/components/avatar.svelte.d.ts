import { SvelteComponent } from "svelte";
import type { Props } from "../types.js";
declare const __propDef: {
    props: Props;
    events: {
        [evt: string]: CustomEvent<any>;
    };
    slots: {
        default: {
            attrs: Record<string, string>;
        };
    };
};
export type AvatarProps = typeof __propDef.props;
export type AvatarEvents = typeof __propDef.events;
export type AvatarSlots = typeof __propDef.slots;
export default class Avatar extends SvelteComponent<AvatarProps, AvatarEvents, AvatarSlots> {
}
export {};
