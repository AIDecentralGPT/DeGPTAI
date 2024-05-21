import { SvelteComponent } from "svelte";
declare const __propDef: {
    props: {
        preventScroll?: boolean | undefined;
        closeOnEscape?: boolean | undefined;
        closeOnOutsideClick?: boolean | undefined;
        onOutsideClick?: ((event: MouseEvent | TouchEvent | PointerEvent) => void) | undefined;
        portal?: string | HTMLElement | null | undefined;
        openFocus?: import("@melt-ui/svelte/index.js").FocusProp | undefined;
        closeFocus?: import("@melt-ui/svelte/index.js").FocusProp | undefined;
        open?: boolean | undefined;
        onOpenChange?: import("../../../internal/types.js").OnChangeFn<boolean> | undefined;
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
export type AlertDialogProps = typeof __propDef.props;
export type AlertDialogEvents = typeof __propDef.events;
export type AlertDialogSlots = typeof __propDef.slots;
export default class AlertDialog extends SvelteComponent<AlertDialogProps, AlertDialogEvents, AlertDialogSlots> {
}
export {};
