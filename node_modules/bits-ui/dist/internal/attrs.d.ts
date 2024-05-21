import type { Bit } from "@/content/api-reference/index.js";
export declare function createBitAttrs<T extends readonly string[]>(bit: Bit | "menu", parts: T): (part: T[number]) => Record<string, string>;
export declare function disabledAttrs(disabled: boolean | undefined | null): {
    "aria-disabled": string;
    "data-disabled": string;
} | {
    "aria-disabled": undefined;
    "data-disabled": undefined;
};
