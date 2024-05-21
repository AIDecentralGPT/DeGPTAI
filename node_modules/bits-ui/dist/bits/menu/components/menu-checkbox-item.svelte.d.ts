import { SvelteComponent } from "svelte";
import type { CheckboxItemEvents, CheckboxItemProps } from "../types.js";
declare const __propDef: {
    props: CheckboxItemProps;
    slots: {
        default: {
            builder: {
                readonly role: "menuitemcheckbox";
                readonly tabindex: -1;
                readonly 'data-orientation': "vertical";
                readonly 'aria-checked': "false" | "true" | "mixed";
                readonly 'data-disabled': true | undefined;
                readonly 'data-state': "checked" | "unchecked" | "indeterminate";
            } & {
                [x: `data-melt-${string}`]: "";
            } & {
                action: (node: HTMLElement) => import("@melt-ui/svelte/internal/types").MeltActionReturn<"keydown" | "click" | "focusin" | "focusout" | "pointerdown" | "pointerleave" | "pointermove">;
            };
        };
    };
    events: CheckboxItemEvents;
};
export type MenuCheckboxItemProps = typeof __propDef.props;
export type MenuCheckboxItemEvents = typeof __propDef.events;
export type MenuCheckboxItemSlots = typeof __propDef.slots;
export default class MenuCheckboxItem extends SvelteComponent<MenuCheckboxItemProps, MenuCheckboxItemEvents, MenuCheckboxItemSlots> {
}
export {};
