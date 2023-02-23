import type { Interpreter } from '../interpreter';
import { make_PyRepl } from './pyrepl';
import { make_PyWidget } from './pywidget';
import { getLogger } from '../logger';

const logger = getLogger('element');


function createCustomElements(interpreter: Interpreter) {
    const PyWidget = make_PyWidget(interpreter);
    const PyRepl = make_PyRepl(interpreter);

    /* eslint-disable @typescript-eslint/no-unused-vars */
    const xPyRepl = customElements.define('py-repl', PyRepl);
    const xPyWidget = customElements.define('py-register-widget', PyWidget);
    logger.info("pyWidget and pyRepl registered")
    
    /* eslint-enable @typescript-eslint/no-unused-vars */
}

export { createCustomElements };
