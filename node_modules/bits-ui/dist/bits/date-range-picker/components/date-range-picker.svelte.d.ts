import { SvelteComponent } from "svelte";
declare const __propDef: {
    props: {
        disabled?: boolean | undefined;
        preventScroll?: boolean | undefined;
        closeOnEscape?: boolean | undefined;
        closeOnOutsideClick?: boolean | undefined;
        onOutsideClick?: ((event: import("@melt-ui/svelte/index.js").InteractOutsideEvent) => void) | undefined;
        portal?: string | HTMLElement | null | undefined;
        openFocus?: import("@melt-ui/svelte/index.js").FocusProp | undefined;
        closeFocus?: import("@melt-ui/svelte/index.js").FocusProp | undefined;
        preventDeselect?: boolean | undefined;
        minValue?: import("@internationalized/date").DateValue | undefined;
        maxValue?: import("@internationalized/date").DateValue | undefined;
        pagedNavigation?: boolean | undefined;
        weekStartsOn?: 0 | 1 | 2 | 3 | 4 | 5 | 6 | undefined;
        weekdayFormat?: "narrow" | "short" | "long" | undefined;
        isDateDisabled?: import("@melt-ui/svelte/index.js").Matcher | undefined;
        isDateUnavailable?: import("@melt-ui/svelte/index.js").Matcher | undefined;
        fixedWeeks?: boolean | undefined;
        numberOfMonths?: number | undefined;
        calendarLabel?: string | undefined;
        locale?: string | undefined;
        readonly?: boolean | undefined;
        hourCycle?: 12 | 24 | undefined;
        granularity?: import("@melt-ui/svelte/index.js").Granularity | undefined;
        hideTimeZone?: boolean | undefined;
        disableFocusTrap?: boolean | undefined;
        open?: boolean | undefined;
        onOpenChange?: import("../../../internal/types.js").OnChangeFn<boolean> | undefined;
        value?: import("../../../index.js").DateRange | undefined;
        onValueChange?: import("../../../internal/types.js").OnChangeFn<import("../../../index.js").DateRange | undefined> | undefined;
        placeholder?: import("@internationalized/date").DateValue | undefined;
        onPlaceholderChange?: import("../../../internal/types.js").OnChangeFn<import("@internationalized/date").DateValue> | undefined;
        validationId?: string | undefined;
        descriptionId?: string | undefined;
        startValue?: import("@internationalized/date").DateValue | undefined;
    };
    events: {
        [evt: string]: CustomEvent<any>;
    };
    slots: {
        default: {
            ids: {
                field: string;
                description: string;
                label: string;
                validation: string;
                calendar: string;
                content: string;
                trigger: string;
                startField: {
                    day: string;
                    dayPeriod: string;
                    hour: string;
                    minute: string;
                    month: string;
                    second: string;
                    year: string;
                    timeZoneName: string;
                };
                endField: {
                    day: string;
                    dayPeriod: string;
                    hour: string;
                    minute: string;
                    month: string;
                    second: string;
                    year: string;
                    timeZoneName: string;
                };
            };
            isInvalid: boolean;
            startValue: import("@internationalized/date").DateValue | undefined;
            endValue: import("@internationalized/date").DateValue | undefined;
        };
    };
};
export type DateRangePickerProps = typeof __propDef.props;
export type DateRangePickerEvents = typeof __propDef.events;
export type DateRangePickerSlots = typeof __propDef.slots;
export default class DateRangePicker extends SvelteComponent<DateRangePickerProps, DateRangePickerEvents, DateRangePickerSlots> {
}
export {};
