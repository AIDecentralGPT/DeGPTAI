export function createBitAttrs(bit, parts) {
    const attrs = {};
    parts.forEach((part) => {
        attrs[part] = {
            [`data-${bit}-${part}`]: "",
        };
    });
    return (part) => attrs[part];
}
export function disabledAttrs(disabled) {
    return disabled
        ? { "aria-disabled": "true", "data-disabled": "" }
        : { "aria-disabled": undefined, "data-disabled": undefined };
}
