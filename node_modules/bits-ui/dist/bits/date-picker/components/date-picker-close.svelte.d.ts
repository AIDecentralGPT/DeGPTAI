import { SvelteComponent } from "svelte";
import type { CloseProps, CloseEvents } from "../types.js";
declare const __propDef: {
    props: CloseProps;
    slots: {
        default: {
            builder: {
                readonly type: "button";
            } & {
                [x: `data-melt-${string}`]: "";
            } & {
                action: (node: HTMLElement) => import("@melt-ui/svelte/internal/types").MeltActionReturn<"keydown" | "click">;
            };
        };
    };
    events: CloseEvents;
};
export type DatePickerCloseProps = typeof __propDef.props;
export type DatePickerCloseEvents = typeof __propDef.events;
export type DatePickerCloseSlots = typeof __propDef.slots;
export default class DatePickerClose extends SvelteComponent<DatePickerCloseProps, DatePickerCloseEvents, DatePickerCloseSlots> {
}
export {};
