import pyscript

def make_variable_row(var_name):
    return f"""<div class="grid grid-cols-3 px-2 py-1 vardisplay">
        <div class='text-center'>{pyscript.html.escape(str(var_name))}</div>
        <div class='text-center'>{pyscript.html.escape(str(globals()[var_name]))}</div>
        <div class='text-center'>{pyscript.html.escape(str(id(globals()[var_name])))}</div>
        </div>
        """

def make_variable_display():
    return "<div class='grid grid-cols-1'>" + \
            ''.join([make_variable_row(var)
                    for var in sorted(set(globals()).difference((initial_globals,)) - initial_globals) 
                    if var != 'initial_globals']
                ) +\
            "</div>"

initial_globals = frozenset(globals())