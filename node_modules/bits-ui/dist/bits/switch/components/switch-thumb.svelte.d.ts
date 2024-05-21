import { SvelteComponent } from "svelte";
import type { ThumbProps } from "../types.js";
declare const __propDef: {
    props: ThumbProps;
    events: {
        [evt: string]: CustomEvent<any>;
    };
    slots: {
        default: {
            attrs: {
                "data-state": string;
                "data-checked": string | undefined;
            };
            checked: boolean;
        };
    };
};
export type SwitchThumbProps = typeof __propDef.props;
export type SwitchThumbEvents = typeof __propDef.events;
export type SwitchThumbSlots = typeof __propDef.slots;
export default class SwitchThumb extends SvelteComponent<SwitchThumbProps, SwitchThumbEvents, SwitchThumbSlots> {
}
export {};
