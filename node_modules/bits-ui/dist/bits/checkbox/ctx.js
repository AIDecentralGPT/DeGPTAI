import { createCheckbox } from "@melt-ui/svelte";
import { getContext, setContext } from "svelte";
import { removeUndefined, getOptionUpdater, createBitAttrs } from "../../internal/index.js";
export function getCheckboxData() {
    const NAME = "checkbox";
    const PARTS = ["root", "input", "indicator"];
    return {
        NAME,
        PARTS,
    };
}
export function setCtx(props) {
    const { NAME, PARTS } = getCheckboxData();
    const getAttrs = createBitAttrs(NAME, PARTS);
    const checkbox = { ...createCheckbox(removeUndefined(props)), getAttrs };
    setContext(NAME, checkbox);
    return {
        ...checkbox,
        updateOption: getOptionUpdater(checkbox.options),
    };
}
export function getCtx() {
    const { NAME } = getCheckboxData();
    return getContext(NAME);
}
