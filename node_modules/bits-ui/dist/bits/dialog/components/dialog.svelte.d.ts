import { SvelteComponent } from "svelte";
declare const __propDef: {
    props: {
        preventScroll?: boolean | undefined;
        closeOnEscape?: boolean | undefined;
        closeOnOutsideClick?: boolean | undefined;
        onOutsideClick?: ((event: MouseEvent | TouchEvent | PointerEvent) => void) | undefined;
        portal?: string | HTMLElement | null | undefined;
        open?: boolean | undefined;
        onOpenChange?: import("../../../internal/types.js").OnChangeFn<boolean> | undefined;
        openFocus?: import("../../../index.js").FocusProp | undefined;
        closeFocus?: import("../../../index.js").FocusProp | undefined;
    };
    events: {
        [evt: string]: CustomEvent<any>;
    };
    slots: {
        default: {
            ids: {
                content: string;
                description: string;
                title: string;
            };
        };
    };
};
export type DialogProps = typeof __propDef.props;
export type DialogEvents = typeof __propDef.events;
export type DialogSlots = typeof __propDef.slots;
export default class Dialog extends SvelteComponent<DialogProps, DialogEvents, DialogSlots> {
}
export {};
