import { SvelteComponent } from "svelte";
import type { NextButtonProps } from "../types.js";
declare const __propDef: {
    props: NextButtonProps;
    slots: {
        default: {
            builder: {
                role: string;
                type: "button";
                'aria-label': string;
                'aria-disabled': "true" | undefined;
                'data-disabled': string | undefined;
                disabled: boolean | undefined;
            } & {
                [x: `data-melt-${string}`]: "";
            } & {
                action: (node: HTMLElement) => import("@melt-ui/svelte/internal/types").MeltActionReturn<"click">;
            };
        };
    };
    events: {
        click: import("../../../index.js").CustomEventHandler<MouseEvent, HTMLButtonElement>;
    };
};
export type CalendarNextButtonProps = typeof __propDef.props;
export type CalendarNextButtonEvents = typeof __propDef.events;
export type CalendarNextButtonSlots = typeof __propDef.slots;
export default class CalendarNextButton extends SvelteComponent<CalendarNextButtonProps, CalendarNextButtonEvents, CalendarNextButtonSlots> {
}
export {};
