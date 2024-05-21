import { SvelteComponent } from "svelte";
import type { Props, Events } from "../types.js";
declare const __propDef: {
    props: Props;
    slots: {
        default: {};
    };
    events: Events;
};
export type ButtonProps = typeof __propDef.props;
export type ButtonEvents = typeof __propDef.events;
export type ButtonSlots = typeof __propDef.slots;
export default class Button extends SvelteComponent<ButtonProps, ButtonEvents, ButtonSlots> {
}
export {};
