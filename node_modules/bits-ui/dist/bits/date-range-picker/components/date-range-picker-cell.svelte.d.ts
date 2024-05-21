import { SvelteComponent } from "svelte";
import type { CellProps } from "../types.js";
declare const __propDef: {
    props: CellProps;
    events: {
        [evt: string]: CustomEvent<any>;
    };
    slots: {
        default: {
            attrs: {
                "aria-disabled": boolean;
                "data-disabled": string | undefined;
                role: string;
            };
        };
    };
};
export type DateRangePickerCellProps = typeof __propDef.props;
export type DateRangePickerCellEvents = typeof __propDef.events;
export type DateRangePickerCellSlots = typeof __propDef.slots;
export default class DateRangePickerCell extends SvelteComponent<DateRangePickerCellProps, DateRangePickerCellEvents, DateRangePickerCellSlots> {
}
export {};
