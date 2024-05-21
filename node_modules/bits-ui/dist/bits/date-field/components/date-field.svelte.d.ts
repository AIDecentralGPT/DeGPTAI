import { SvelteComponent } from "svelte";
declare const __propDef: {
    props: {
        disabled?: boolean | undefined;
        minValue?: import("@internationalized/date").DateValue | undefined;
        maxValue?: import("@internationalized/date").DateValue | undefined;
        isDateUnavailable?: import("@melt-ui/svelte/index.js").Matcher | undefined;
        locale?: string | undefined;
        readonly?: boolean | undefined;
        readonlySegments?: ("month" | "day" | "year" | "hour" | "minute" | "second" | "dayPeriod")[] | undefined;
        hourCycle?: 12 | 24 | undefined;
        granularity?: import("@melt-ui/svelte/index.js").Granularity | undefined;
        hideTimeZone?: boolean | undefined;
        value?: import("@internationalized/date").DateValue | undefined;
        onValueChange?: import("../../../internal/types.js").OnChangeFn<import("@internationalized/date").DateValue | undefined> | undefined;
        placeholder?: import("@internationalized/date").DateValue | undefined;
        onPlaceholderChange?: import("../../../internal/types.js").OnChangeFn<import("@internationalized/date").DateValue> | undefined;
        validationId?: string | undefined;
        descriptionId?: string | undefined;
    };
    events: {
        [evt: string]: CustomEvent<any>;
    };
    slots: {
        default: {
            isInvalid: boolean;
            ids: {
                day: string;
                description: string;
                dayPeriod: string;
                field: string;
                hour: string;
                minute: string;
                month: string;
                second: string;
                year: string;
                validation: string;
                label: string;
                timeZoneName: string;
            };
        };
    };
};
export type DateFieldProps = typeof __propDef.props;
export type DateFieldEvents = typeof __propDef.events;
export type DateFieldSlots = typeof __propDef.slots;
export default class DateField extends SvelteComponent<DateFieldProps, DateFieldEvents, DateFieldSlots> {
}
export {};
