/// <reference types="svelte" />
import { type CreateLinkPreviewProps } from "@melt-ui/svelte";
import type { FloatingProps } from "../floating/_types.js";
import type { Writable } from "svelte/store";
export declare function getLinkPreviewData(): {
    NAME: "link-preview";
    PARTS: string[];
};
type GetReturn = Omit<ReturnType<typeof setCtx>, "updateOption">;
export declare function setCtx(props: CreateLinkPreviewProps): {
    updateOption: <K extends string, V extends unknown>(key: K, value: V | undefined) => void;
    getAttrs: (part: string) => Record<string, string>;
    ids: import("@melt-ui/svelte/internal/helpers").ToWritableStores<{
        content: string;
        trigger: string;
    }>;
    elements: {
        trigger: import("@melt-ui/svelte/internal/helpers").MeltElement<[{
            update: (updater: import("svelte/store").Updater<boolean>, sideEffect?: ((newValue: boolean) => void) | undefined) => void;
            set: (this: void, value: boolean) => void;
            subscribe(this: void, run: import("svelte/store").Subscriber<boolean>, invalidate?: import("svelte/store").Invalidator<boolean> | undefined): import("svelte/store").Unsubscriber;
            get: () => boolean;
            destroy?: (() => void) | undefined;
        }, import("@melt-ui/svelte/internal/helpers").WithGet<Writable<string>>, import("@melt-ui/svelte/internal/helpers").WithGet<Writable<string>>], (node: HTMLElement) => import("@melt-ui/svelte/internal/types").MeltActionReturn<"blur" | "focus" | "pointerenter" | "pointerleave">, ([$open, $triggerId, $contentId]: [boolean, string, string]) => {
            role: "button";
            'aria-haspopup': "dialog";
            'aria-expanded': boolean;
            'data-state': string;
            'aria-controls': string;
            id: string;
        }, string>;
        content: import("@melt-ui/svelte/internal/helpers").MeltElement<[import("svelte/store").Readable<boolean>, import("@melt-ui/svelte/internal/helpers").WithGet<Writable<string | HTMLElement | null | undefined>>, import("@melt-ui/svelte/internal/helpers").WithGet<Writable<string>>], (node: HTMLElement) => import("@melt-ui/svelte/internal/types").MeltActionReturn<"focusout" | "pointerdown" | "pointerenter" | "pointerleave">, ([$isVisible, $portal, $contentId]: [boolean, string | HTMLElement | null | undefined, string]) => {
            hidden: boolean | undefined;
            tabindex: number;
            style: string;
            id: string;
            'data-state': string;
            'data-portal': string | undefined;
        }, string>;
        arrow: import("@melt-ui/svelte/internal/helpers").MeltElement<import("@melt-ui/svelte/internal/helpers").WithGet<Writable<number>>, import("svelte/action").Action<any, any, Record<never, any>>, ($arrowSize: number) => {
            'data-arrow': boolean;
            style: string;
        }, string>;
    };
    states: {
        open: {
            update: (updater: import("svelte/store").Updater<boolean>, sideEffect?: ((newValue: boolean) => void) | undefined) => void;
            set: (this: void, value: boolean) => void;
            subscribe(this: void, run: import("svelte/store").Subscriber<boolean>, invalidate?: import("svelte/store").Invalidator<boolean> | undefined): import("svelte/store").Unsubscriber;
            get: () => boolean;
            destroy?: (() => void) | undefined;
        };
    };
    options: import("@melt-ui/svelte/internal/helpers").ToWritableStores<Omit<{
        positioning: import("@melt-ui/svelte/internal/actions").FloatingConfig | {
            placement: "bottom";
        };
        defaultOpen: boolean;
        open?: Writable<boolean> | undefined;
        onOpenChange?: import("@melt-ui/svelte/internal/helpers").ChangeFn<boolean> | undefined;
        openDelay: number;
        closeDelay: number;
        closeOnOutsideClick: boolean;
        onOutsideClick: ((event: import("@melt-ui/svelte/index.js").InteractOutsideEvent) => void) | undefined;
        closeOnEscape: boolean;
        arrowSize: number;
        forceVisible: boolean;
        portal: string | HTMLElement | null | undefined;
        ids?: Partial<{
            content: string;
            trigger: string;
        }> | undefined;
    }, "ids">>;
};
export declare function getCtx(): GetReturn;
export declare function setArrow(size?: number): GetReturn;
export declare function updatePositioning(props: FloatingProps): void;
export {};
