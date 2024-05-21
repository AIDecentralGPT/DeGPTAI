import { SvelteComponent } from "svelte";
import type { InputProps } from "../types.js";
declare const __propDef: {
    props: InputProps;
    events: {
        [evt: string]: CustomEvent<any>;
    };
    slots: {};
};
export type SwitchInputProps = typeof __propDef.props;
export type SwitchInputEvents = typeof __propDef.events;
export type SwitchInputSlots = typeof __propDef.slots;
export default class SwitchInput extends SvelteComponent<SwitchInputProps, SwitchInputEvents, SwitchInputSlots> {
}
export {};
