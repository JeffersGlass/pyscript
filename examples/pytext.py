from pyscript import Plugin
import pyscript
import js

class PyTextPlguin(Plugin):
    def afterPyReplExec(*args, **kwargs):
        js.console.log("REPL was executed")
        py_texts = js.document.getElementsByTagName("py-text")
        for p in py_texts:
            p.pyPluginInstance.refresh(kwargs['interpreter'])

    def afterPyScriptExec(self, interpreter, src, pyscriptTag, result):
        js.console.log("REPL was executed")
        py_texts = js.document.getElementsByTagName("py-text")
        for p in py_texts:
            p.pyPluginInstance.refresh(interpreter)

    #afterPyScriptExec = afterPyReplExec

plugin = PyTextPlguin(name = "pytext")
pyscript.refresh_pytext = plugin.afterPyReplExec

@plugin.register_custom_element("py-text")
class PyText():
    def __init__(self, element):
        self.element = element

    def connect(self):
        ...
        
    def refresh(self, interpreter):
        obj_attrib: str = self.element.getAttribute("code")
        if obj_attrib: 
            try:
                obj_result = eval(str(obj_attrib), interpreter.globals)
                self.element.innerHTML = str(obj_result)
            except Exception as err:
                fallback_attrib: str = self.element.getAttribute("fallback")
                if fallback_attrib:
                    try:
                        obj_result = eval(str(fallback_attrib))
                    except Exception as err:
                        js.console.warn(f"Could not evaluate py-text source {obj_attrib}")        
                    self.element.innerHTML = str(obj_result)
                js.console.warn(f"Could not evaluate py-text source {obj_attrib}")
                raise err

        

        