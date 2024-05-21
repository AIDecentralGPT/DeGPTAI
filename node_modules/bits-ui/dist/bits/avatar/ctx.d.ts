/// <reference types="svelte" />
import { type CreateAvatarProps, type Avatar as AvatarReturn } from "@melt-ui/svelte";
export declare function getAvatarData(): {
    NAME: "avatar";
    PARTS: readonly ["root", "image", "fallback"];
};
type GetReturn = Omit<ReturnType<typeof setCtx>, "updateOption">;
export declare function setCtx(props: CreateAvatarProps): {
    updateOption: <K extends string, V extends unknown>(key: K, value: V | undefined) => void;
    getAttrs: (part: "image" | "root" | "fallback") => Record<string, string>;
    elements: {
        image: import("@melt-ui/svelte/internal/helpers").MeltElement<[import("@melt-ui/svelte/internal/helpers").WithGet<import("svelte/store").Writable<string>>, {
            update: (updater: import("svelte/store").Updater<"loading" | "loaded" | "error">, sideEffect?: ((newValue: "loading" | "loaded" | "error") => void) | undefined) => void;
            set: (this: void, value: "loading" | "loaded" | "error") => void;
            subscribe(this: void, run: import("svelte/store").Subscriber<"loading" | "loaded" | "error">, invalidate?: import("svelte/store").Invalidator<"loading" | "loaded" | "error"> | undefined): import("svelte/store").Unsubscriber;
            get: () => "loading" | "loaded" | "error";
            destroy?: (() => void) | undefined;
        }], import("svelte/action").Action<any, any, Record<never, any>>, ([$src, $loadingStatus]: [string, "loading" | "loaded" | "error"]) => {
            src: string;
            style: string;
        }, "avatar-image">;
        fallback: import("@melt-ui/svelte/internal/helpers").MeltElement<[{
            update: (updater: import("svelte/store").Updater<"loading" | "loaded" | "error">, sideEffect?: ((newValue: "loading" | "loaded" | "error") => void) | undefined) => void;
            set: (this: void, value: "loading" | "loaded" | "error") => void;
            subscribe(this: void, run: import("svelte/store").Subscriber<"loading" | "loaded" | "error">, invalidate?: import("svelte/store").Invalidator<"loading" | "loaded" | "error"> | undefined): import("svelte/store").Unsubscriber;
            get: () => "loading" | "loaded" | "error";
            destroy?: (() => void) | undefined;
        }], import("svelte/action").Action<any, any, Record<never, any>>, ([$loadingStatus]: ["loading" | "loaded" | "error"]) => {
            style: string | undefined;
            hidden: boolean | undefined;
        }, "avatar-fallback">;
    };
    states: {
        loadingStatus: {
            update: (updater: import("svelte/store").Updater<"loading" | "loaded" | "error">, sideEffect?: ((newValue: "loading" | "loaded" | "error") => void) | undefined) => void;
            set: (this: void, value: "loading" | "loaded" | "error") => void;
            subscribe(this: void, run: import("svelte/store").Subscriber<"loading" | "loaded" | "error">, invalidate?: import("svelte/store").Invalidator<"loading" | "loaded" | "error"> | undefined): import("svelte/store").Unsubscriber;
            get: () => "loading" | "loaded" | "error";
            destroy?: (() => void) | undefined;
        };
    };
    options: import("@melt-ui/svelte/internal/helpers").ToWritableStores<Omit<{
        src: string;
        delayMs: number;
        loadingStatus?: import("svelte/store").Writable<"loading" | "loaded" | "error"> | undefined;
        onLoadingStatusChange: import("@melt-ui/svelte/internal/helpers").ChangeFn<"loading" | "loaded" | "error"> | undefined;
    }, "onLoadingStatusChange" | "loadingStatus">>;
};
export declare function getImage(src?: string | undefined | null): AvatarReturn;
export declare function getCtx(): GetReturn;
export {};
