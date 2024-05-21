import { SvelteComponent } from "svelte";
import type { RadioIndicatorProps } from "../types.js";
declare const __propDef: {
    props: RadioIndicatorProps;
    events: {
        [evt: string]: CustomEvent<any>;
    };
    slots: {
        default: {
            attrs: Record<string, string>;
            checked: boolean;
        };
    };
};
export type MenuRadioIndicatorProps = typeof __propDef.props;
export type MenuRadioIndicatorEvents = typeof __propDef.events;
export type MenuRadioIndicatorSlots = typeof __propDef.slots;
export default class MenuRadioIndicator extends SvelteComponent<MenuRadioIndicatorProps, MenuRadioIndicatorEvents, MenuRadioIndicatorSlots> {
}
export {};
