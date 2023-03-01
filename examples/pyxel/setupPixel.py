import pyodide.code

pyodide.code.run_js(
    """
    pyscript.interpreter.interface._module.canvas = document.querySelector("canvas#canvas");

    _virtualGamepadStates = [
        false, // Up
        false, // Down
        false, // Left
        false, // Right
        false, // A
        false, // B
        false, // X
        false, // Y
    ];
    """
)