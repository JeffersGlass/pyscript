async function main(){
  let pyodide = await loadPyodide();
  pyodide.pyodide_py.eval_code(`
    from js import console, document
    from pyodide import create_proxy, to_js

    def runFunctionInNamespace(func, namespace, *args, **kwargs):
      console.warn(f"Running function {func.__name__} in namespace {namespace}")
      old_vars = dict()
      new_vars = set()
      for key, value in globals()['pyscript_namespaces'][namespace].items():
        console.log(f"Examining {key}:{value}")
        if key in globals():
          old_value = globals()[key]
          console.log(f"Saving old value of {key} as {old_value}")
          old_vars[key] = old_value
        else: new_vars.add(key)
        
        globals()[key] = value

      result = func(*args, **kwargs)

      for key, value in old_vars.items():
        console.log(f"Restoring previous version of variable {key} to {value}")
        globals()[key] = value
      for key in new_vars:
        del globals()[key]
      
      return result

    pyscript_namespaces = {
      'button_1': {
        'x': 1
      },
      'button_2': {
        'x': 2
      }
    }

    x = 10000

    def show_globals(_):
      from js import console
      from pyodide import to_js
      console.log(to_js(globals()))

    def show_locals(_):
      from js import console
      from pyodide import to_js
      console.log(to_js(locals()))

    document.getElementById("btn-globals").addEventListener('click', create_proxy(show_globals))
    document.getElementById("btn-locals").addEventListener('click', create_proxy(show_locals))
    `,
  pyodide.globals);

  pyodide.pyodide_py.eval_code(`
    from functools import partial
    console.log(f"Hey, the value of x at the start of this block is {x}")
    console.log(to_js(globals()))
    
    def _x_value(_):
      console.log("Loading x value in function")
      console.log(f"The value of x is {x}") #should be 1 or 2
      console.log(to_js(globals()))
      console.log(to_js(locals()))
    
    x_value_1 = partial(globals()['runFunctionInNamespace'], _x_value, 'button_1')
    x_value_2 = partial(globals()['runFunctionInNamespace'], _x_value, 'button_2')
    
    document.getElementById("btn-x-1").addEventListener('click', create_proxy(x_value_1))
    document.getElementById("btn-x-2").addEventListener('click', create_proxy(x_value_2))
    `,
  pyodide.globals,
  pyodide.globals.get('pyscript_namespaces').get('button_1'));
}
main();