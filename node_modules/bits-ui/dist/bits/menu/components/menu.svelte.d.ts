import { SvelteComponent } from "svelte";
declare const __propDef: {
    props: {
        preventScroll?: boolean | undefined;
        closeOnEscape?: boolean | undefined;
        closeOnOutsideClick?: boolean | undefined;
        onOutsideClick?: ((event: import("@melt-ui/svelte/index.js").InteractOutsideEvent) => void) | undefined;
        portal?: string | HTMLElement | null | undefined;
        closeFocus?: import("@melt-ui/svelte/index.js").FocusProp | undefined;
        typeahead?: boolean | undefined;
        loop?: boolean | undefined;
        dir?: import("@melt-ui/svelte/internal/types").TextDirection | undefined;
        closeOnItemClick?: boolean | undefined;
        disableFocusFirstItem?: boolean | undefined;
        open?: boolean | undefined;
        onOpenChange?: import("../../../internal/types.js").OnChangeFn<boolean> | undefined;
    };
    events: {
        [evt: string]: CustomEvent<any>;
    };
    slots: {
        default: {
            ids: {
                menu: string;
                trigger: string;
            };
        };
    };
};
export type MenuProps = typeof __propDef.props;
export type MenuEvents = typeof __propDef.events;
export type MenuSlots = typeof __propDef.slots;
export default class Menu extends SvelteComponent<MenuProps, MenuEvents, MenuSlots> {
}
export {};
