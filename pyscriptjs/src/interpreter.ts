import { getLastPath } from './utils';

let pyodideReadyPromise;
let pyodide;

const loadInterpreter = async function (): Promise<any> {
    console.log('creating pyodide runtime');
    // eslint-disable-next-line
    // @ts-ignore
    pyodide = await loadPyodide({
        stdout: console.log,
        stderr: console.log,
        fullStdLib: false
    });

    // now that we loaded, add additional convenience functions
    console.log('loading micropip');
    await pyodide.loadPackage('micropip');

    console.log('loading pyscript...');

    // let's get the full path of where PyScript is running from so we can load the pyscript.py
    // file from the same location
    const loadedScript: HTMLScriptElement = document.querySelector(`script[src$='pyscript.js']`);
    const scriptPath = loadedScript.src.substr(0, loadedScript.src.lastIndexOf('/'));
    await pyodide.runPythonAsync(await (await fetch(`${scriptPath}/pyscript.py`)).text());

    console.log(scriptPath);

    //create dict for non-default namespaces
    let namespace_dict = pyodide.globals.get("dict")();
    pyodide.globals.set("namespaces", namespace_dict)

    console.log('done setting up environment');
    return pyodide;
};

const loadPackage = async function (package_name: string[] | string, runtime: any): Promise<any> {
    const micropip = pyodide.globals.get('micropip');
    await micropip.install(package_name);
    micropip.destroy();
};

const loadFromFile = async function (s: string, runtime: any): Promise<any> {
    const filename = getLastPath(s);
    await runtime.runPythonAsync(
        `
        from pyodide.http import pyfetch
        from js import console
        response = await pyfetch("` +
            s +
            `")
        content = await response.bytes()
        with open("` +
            filename +
            `", "wb") as f:
            f.write(content)
    `,
    );
};

export { loadInterpreter, pyodideReadyPromise, loadPackage, loadFromFile };
