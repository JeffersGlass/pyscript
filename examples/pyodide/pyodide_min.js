async function main(){
    let pyodide = await loadPyodide();
    pyodide.pyodide_py.eval_code(`
    from js import console, document
    from pyodide import create_proxy, to_js
  
    my_local_dict = {'x': 42} #Create a rudimentary namespace dict

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
  pyodide.globals); //globals argument to eval_code
  
  //This code will use my_local_dict as its local dictionary
  pyodide.pyodide_py.eval_code(`
    console.log(f"Hey, the value of x at the start of this block is {x}") #Outputs 42

    x = 0
    
    def x_value( _ ):
        console.log(f"The value of x is {x}") # Should be 42... but instead raises NameError when executed by event
        
    x_value(None)

    def getvars(_):
        import inspect
        variables = inspect.getclosurevars(globals()['my_local_dict']['x_value'])
        console.log(repr(variables))
  
    document.getElementById("btn-x-1").addEventListener('click', create_proxy(x_value))
    document.getElementById("btn-free").addEventListener('click', create_proxy(getvars))

    `, //pyodide.globals, //globals argument to eval_code
  pyodide.globals.get('my_local_dict')); //locals argument to eval_code
  }
  main();