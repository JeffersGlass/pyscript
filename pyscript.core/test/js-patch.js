import { hooks } from "@pyscript/core";

hooks.codeBeforeRunWorker.add(`
    print("Starting codeBeforeRunWorker")
    import pyscript
    import js
    import sys

    class Wrapper(object):
        def __init__(self, obj):
            setattr(self, "_wrapped_obj", obj)
        def __getattribute__(self, attr):
            print(attr)
            if attr == "document": return pyscript.document
            if attr == "devicePixelRatio": return 1
            print(f"About to try to lookup {attr}")

            # Equivalent to return 
            #return object.__getattribute__(self._wrapped_obj, attr)

    sys.modules['js'] = Wrapper(js)
    print("js is wrapped?")
    `
)

hooks.codeAfterRunWorker.add(`
sys.modules['js'] = js
`)
