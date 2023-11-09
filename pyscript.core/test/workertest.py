import polyscript
from pyodide.ffi import to_js

f = polyscript.xworker.window.aFunc
print(f(to_js([1,2])))