import { SvelteComponent } from "svelte";
import type { InputProps } from "../types.js";
declare const __propDef: {
    props: InputProps;
    events: {
        [evt: string]: CustomEvent<any>;
    };
    slots: {
        default: {
            builder: {
                role: string;
                id: string;
                'aria-labelledby': string;
                'aria-describedby': string;
                'data-invalid': string | undefined;
            } & {
                [x: `data-melt-${string}`]: "";
            } & {
                action: <Node_1 extends unknown>() => {
                    destroy(): void;
                };
            };
            segments: {
                start: {
                    part: import("@melt-ui/svelte/index.js").SegmentPart;
                    value: string;
                }[];
                end: {
                    part: import("@melt-ui/svelte/index.js").SegmentPart;
                    value: string;
                }[];
            };
        };
    };
};
export type DateRangeFieldInputProps = typeof __propDef.props;
export type DateRangeFieldInputEvents = typeof __propDef.events;
export type DateRangeFieldInputSlots = typeof __propDef.slots;
export default class DateRangeFieldInput extends SvelteComponent<DateRangeFieldInputProps, DateRangeFieldInputEvents, DateRangeFieldInputSlots> {
}
export {};
