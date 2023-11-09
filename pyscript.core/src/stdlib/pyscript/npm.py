from pyscript import document, window
from pyodide.http import pyfetch
import asyncio

async def npm_package(package_name: str, *, default_export=None, objects=None) :
    if not default_export and not objects:
        raise ValueError("One of default_export or objects must not be None")
    if default_export and objects:
        raise ValueError("Only one of default_export and objects may be given")
    
    script = document.createElement('script')
    script.setAttribute("type", "module")
    if default_export:
        script_text = f"import {default_export} from '{default_export}'"
        script_text += f"\nglobalThis.{default_export} = {default_export}"
    else:
        script_text = f"import {{ {','.join(objects)} }} from '{package_name}'"
        for obj in objects:
            script_text += f"\nglobalThis.{obj} = {obj}"

    script.textContent = script_text

    document.body.append(script)

    # TODO fix this with some Promise magic
    await asyncio.sleep(1)
    
    if default_export:
        return getattr(window, default_export)
    elif objects:
        return tuple(getattr(window, obj) for obj in objects)
