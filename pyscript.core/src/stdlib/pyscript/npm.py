from pyscript import document
from pyodide.http import pyfetch

async def npm_package(package_name: str, default_name, *objects) :
    script = document.createElement('script')
    script.setAttribute("type", "module")
    if default_name:
        script_text = f"import {default_name} from '{package_name}'"
        script_text += f"\nglobalThis.{default_name} = {default_name}"
    else:
        script_text = f"import {{ {','.join(objects)} }} from '{package_name}'"
        for obj in objects:
            script_text += f"\nglobalThis.{obj} = {obj}"

    script_text += """
const scriptDone = new Event("load-done");
document.dispatchEvent(scriptDone);

"""

    script.textContent = script_text

    document.body.append(script)
    await 
    return script
