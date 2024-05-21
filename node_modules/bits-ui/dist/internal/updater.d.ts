/// <reference types="svelte" />
import type { Writable } from "svelte/store";
type Options = Record<string, Writable<unknown>>;
export declare function getOptionUpdater(options: Options): <K extends string, V extends unknown>(key: K, value: V | undefined) => void;
export {};
