declare const _default: {
    error: () => Promise<typeof import("./plugins/error.js")>;
    "import-npm": () => Promise<any>;
    "py-terminal": () => Promise<typeof import("./plugins/py-terminal.js")>;
};
export default _default;
