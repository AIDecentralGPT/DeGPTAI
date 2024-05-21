/** @typedef {typeof __propDef.props}  ConfettiProps */
/** @typedef {typeof __propDef.events}  ConfettiEvents */
/** @typedef {typeof __propDef.slots}  ConfettiSlots */
export default class Confetti extends SvelteComponent<{
    size?: number;
    x?: number[];
    y?: number[];
    duration?: number;
    infinite?: boolean;
    delay?: number[];
    colorRange?: number[];
    colorArray?: any[];
    amount?: number;
    iterationCount?: number;
    fallDistance?: string;
    rounded?: boolean;
    cone?: boolean;
    noGravity?: boolean;
    xSpread?: number;
    destroyOnComplete?: boolean;
}, {
    [evt: string]: CustomEvent<any>;
}, {}> {
}
export type ConfettiProps = typeof __propDef.props;
export type ConfettiEvents = typeof __propDef.events;
export type ConfettiSlots = typeof __propDef.slots;
import { SvelteComponent } from "svelte";
declare const __propDef: {
    props: {
        size?: number;
        x?: number[];
        y?: number[];
        duration?: number;
        infinite?: boolean;
        delay?: number[];
        colorRange?: number[];
        colorArray?: any[];
        amount?: number;
        iterationCount?: number;
        fallDistance?: string;
        rounded?: boolean;
        cone?: boolean;
        noGravity?: boolean;
        xSpread?: number;
        destroyOnComplete?: boolean;
    };
    events: {
        [evt: string]: CustomEvent<any>;
    };
    slots: {};
};
export {};
