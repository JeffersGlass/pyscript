function betterTrim(snippetEl) {
    // Helper functions
    function trimLeft(val) {
        // Adapted from https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/Trim#Polyfill
        return val.replace(/^[\s\uFEFF\xA0]+/g, "");
    }
    function trimLineBreaks(input) {
        var lines = input.split("\n");

        // Trim line-breaks from the beginning
        for (var i = 0; i < lines.length; i++) {
            if (lines[i].trim() === "") {
                lines.splice(i--, 1);
            } else break;
        }

        // Trim line-breaks from the end
        for (var i = lines.length - 1; i >= 0; i--) {
            if (lines[i].trim() === "") {
                lines.splice(i, 1);
            } else break;
        }

        return lines.join("\n");
    }

    // Main function for betterTrim()
    return (function (snippetEl) {
        var content = trimLineBreaks(snippetEl.innerHTML);
        var lines = content.split("\n");
        // Calculate the minimum amount to remove on each line start of the snippet (can be 0)
        var pad = lines.reduce(function (acc, line) {
            if (
                line.length > 0 &&
                trimLeft(line).length > 0 &&
                acc > line.length - trimLeft(line).length
            ) {
                return line.length - trimLeft(line).length;
            }
            return acc;
        }, Number.POSITIVE_INFINITY);
        // Slice each line with this amount
        return lines
            .map(function (line, index) {
                return line.slice(pad);
            })
            .join("\n");
    })(snippetEl);
}
