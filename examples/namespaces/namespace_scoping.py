import sys
import types

class PyScriptModule(types.ModuleType):
    pass

def eval_pyscript_block(src, modname='__main__'):
    mod = sys.modules.get(modname)
    if mod:
        if not isinstance(mod, PyScriptModule):
            raise Exception(f'Cannot mix <py-script> with regular modules; {modname} already exists')
    else:
        mod = PyScriptModule(modname)
        sys.modules[modname] = mod
    exec(src, mod.__dict__)

### example of usage
if __name__ == "__main__":
    eval_pyscript_block('x = 42', modname='module_a')
    
    import module_a
    print(f"In namespace {__name__} we print {module_a.x= }")

    eval_pyscript_block("""
import module_a
print(f"In namespace {__name__} we print {module_a.x= }")""" , modname='module_b')

    eval_pyscript_block('y = 1000', modname='module_a')

    eval_pyscript_block("print(f'In namespace {__name__} we print {module_a.__dict__= }')" , modname='module_b')
    