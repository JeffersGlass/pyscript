import type { PyScriptApp } from '../main';
import type { Interpreter } from '../interpreter';
import { make_PyRepl } from './pyrepl';
import { make_PyWidget } from './pywidget';

function createCustomElements(runtime: Interpreter, app: PyScriptApp) {
    const PyWidget = make_PyWidget(runtime);
    const PyRepl = make_PyRepl(runtime, app);

    /* eslint-disable @typescript-eslint/no-unused-vars */
    const xPyRepl = customElements.define('py-repl', PyRepl);
    const xPyWidget = customElements.define('py-register-widget', PyWidget);
    /* eslint-enable @typescript-eslint/no-unused-vars */
}

export { createCustomElements };
