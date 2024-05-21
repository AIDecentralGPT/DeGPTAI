import { SvelteComponent } from "svelte";
import { type Transition } from "../../../internal/index.js";
import type { SubContentEvents, SubContentProps } from "../types.js";
declare class __sveltets_Render<T extends Transition, In extends Transition, Out extends Transition> {
    props(): SubContentProps<T, In, Out>;
    events(): SubContentEvents;
    slots(): {
        default: {
            builder: {
                readonly role: "menu";
                readonly hidden: true | undefined;
                readonly style: string;
                readonly id: string;
                readonly 'aria-labelledby': string;
                readonly 'data-state': "open" | "closed";
                readonly 'data-id': string;
                readonly tabindex: -1;
            } & {
                [x: `data-melt-${string}`]: "";
            } & {
                action: (node: HTMLElement) => import("@melt-ui/svelte/internal/types").MeltActionReturn<"keydown" | "focusout" | "pointermove">;
            };
        };
    };
}
export type MenuSubContentProps<T extends Transition, In extends Transition, Out extends Transition> = ReturnType<__sveltets_Render<T, In, Out>['props']>;
export type MenuSubContentEvents<T extends Transition, In extends Transition, Out extends Transition> = ReturnType<__sveltets_Render<T, In, Out>['events']>;
export type MenuSubContentSlots<T extends Transition, In extends Transition, Out extends Transition> = ReturnType<__sveltets_Render<T, In, Out>['slots']>;
export default class MenuSubContent<T extends Transition, In extends Transition, Out extends Transition> extends SvelteComponent<MenuSubContentProps<T, In, Out>, MenuSubContentEvents<T, In, Out>, MenuSubContentSlots<T, In, Out>> {
}
export {};
