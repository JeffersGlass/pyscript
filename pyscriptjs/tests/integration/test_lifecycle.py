# This file tests quite a lot of the PyScript project,
# and covers Python execution, the App lifecycle, and the
# plugin lifecycle hooks.
# As such, the tests try to touch as many parts of the lifecycle
# as possible in a simple way (console.log), as opposed to testing
# a single aspect of PyScript in a detailed way.

from .support import PyScriptTest
from .test_plugins import prepare_test, HTML_TEMPLATE_WITH_TAG, HOOKS_PLUGIN_CODE

JS_PLUGIN_CODE = """
export default class TestPlugin{
    //external plugins cannot get configure
    //external plugins cannot get beforeLaunch

    afterSetup(interpreter){
        console.info("afterSetup called")
    }

    afterStartup(interpreter){
        console.info("afterStartup called")
    }

    beforePyScriptExec(){
        console.info("beforePyscriptExec called")
    }

    afterPyScriptExec(){
        console.info("afterPyScriptExec called")
    }
}
"""

class TestLifecycle(PyScriptTest):
    @prepare_test('testplugin', JS_PLUGIN_CODE, extension="js", tagname='py-script', html="print('Hello')",)
    def test_lifecycle(self):
        log_order = [
            "[pyscript/main] PyScript main() running", # in _realmain (1)
            "[pyscript/main] searching for <py-config>", # in loadconfig (2)
            "[py-config] Loading config from py-config element", # in loadConfigFromElement
            "[py-splashscreen] configuring py-splashscreen", #plugins.configure()
            "[py-splashscreen] add py-splashscreen", #plugins.beforeLaunch()
            "[pyscript/main] Initializing interpreter", # start of loadInterpreter (4)
            "[pyscript/main] Python startup...", # prior to await this.interpreter.loadInterpreter() (5)
            "[pyscript/pyodide] Loading pyodide", # start of interface.loadInterpreter()
            "[pyscript/pyodide] pyodide loaded and initialized", # end of interface.loadInterpreter()
            "Python initialization complete", # Output using the Python interpreter in interface.loadInterpreter(), to prove the interface is ready to run some Python
            "[pyscript/main] Python ready!", # after loadInterpreter() completes
            "[pyscript/main] Setting up virtual environment...", # prior to calling setupVirtualEnv
            "[pyscript/main] importing pyscript", # inside setupVirtualEnv() (6)
            "[py-script] Mounting py-mount elements", # inside mountElements()
            "afterSetup called", #plugins.afterSetup()
            "[pyscript/main] Executing <py-script> tags...", # prior to main.executeScripts()
            # "beforePyscriptExec called", #plugins.beforePyScriptExec()
            # "Hello", # Uncommenting this will break the test; but this is where it should be; uncomment when ready! (7)
            # "afterPyScriptExec": Something for afterPyScriptExec()
            "[pyscript/main] Initializing web components...", # Following completion of py-script tags
            "[element] pyWidget and pyRepl registered", #Inside createCustomElements() (8)
            "[py-script] Initializing py-* event handlers...", #Inside initHandlers()
            "[pyscript/main] Startup complete", #Following handler initialization
            "[py-splashscreen] Closing", #plugins.afterStartup
            "[pyscript/main] PyScript page fully initialized" #final step in main
            ]
        lines = self.console.all.lines
        print("\n".join(lines))

        for previous, current in zip(log_order, log_order[1:]):
            assert lines.index(previous) < lines.index(current)
