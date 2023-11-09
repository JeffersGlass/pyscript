import pyscript
canvas = pyscript.document.createElement("canvas")
context = canvas.getContext("2d")
context.setLineDash([2, 2]) # This breaks