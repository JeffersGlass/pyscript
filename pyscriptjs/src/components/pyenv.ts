import * as jsyaml from 'js-yaml';

import { pyodideLoaded, addInitializer } from '../stores';
import { loadPackage, loadFromFile } from '../interpreter';
import { faWarning } from '@fortawesome/free-solid-svg-icons';

// Premise used to connect to the first available pyodide interpreter
let pyodideReadyPromise;
let runtime;

pyodideLoaded.subscribe(value => {
    runtime = value;
    console.log('RUNTIME READY');
});

export class PyEnv extends HTMLElement {
    shadow: ShadowRoot;
    wrapper: HTMLElement;
    code: string;
    environment: any;
    runtime: any;
    env: string[];
    paths: string[];

    constructor() {
        super();

        this.shadow = this.attachShadow({ mode: 'open' });
        this.wrapper = document.createElement('slot');
    }

    connectedCallback() {
        this.code = this.innerHTML;
        this.innerHTML = '';

        const env = [];
        const paths: string[] = [];

        this.environment = jsyaml.load(this.code);
        if (this.environment === undefined) return;

        for (const entry of this.environment) {
            if (typeof entry == 'string') {
                env.push(entry);
            } else if (entry.hasOwnProperty('paths')) {
                for (const path of entry.paths) {
                    paths.push(path);
                }
            }
        }

        async function loadEnv() {
            await loadPackage(env, runtime);
            console.log('environment loaded');
        }

        async function loadPaths() {
            var self = this;
            for (const singleFile of paths) {
                console.log(`loading ${singleFile}`);
                try {
                    await loadFromFile(singleFile, runtime);
                }
                catch (e) {
                    console.warn("Caught an error in loadPaths\r\n" + e);

                    let warning = document.createElement("p")
                    warning.style.backgroundColor = "LightCoral";
                    warning.style.alignContent = "center";
                    warning.style.margin = "4px";
                    warning.innerHTML = '<p>PyScript: Access to local files (using "Paths:" in &lt;py-env&gt;) is not available when directly opening a HTML file; you must use a webserver to serve the additional files. See <a style="text-decoration: underline;" href="https://github.com/pyscript/pyscript/issues/257#issuecomment-1119595062">this reference</a> on starting a simple webserver with Python.</p>';
                    document.body.prepend(warning);
                }
            }
            console.log('paths loaded');
        }

        addInitializer(loadEnv);
        addInitializer(loadPaths);
        console.log('environment loading...', this.env);
    }
}
