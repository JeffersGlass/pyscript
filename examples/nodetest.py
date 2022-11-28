import itertools

import js
from js import cytoscape
from pyodide.ffi import to_js


def jsobj(d):
    return to_js(d, dict_converter=js.Object.fromEntries)


options = jsobj({"name": "cose", "randomize": True})

js.console.log(options)

cy = cytoscape.new(container=js.document.getElementById("cnv"), layout=options)

stringStylesheet = (
    "node { background-color: green; } edge {line-color: black; width: 3} "
)
cy.style(stringStylesheet)

# cy.style().selector('edge').style("line-color", "black").style("width", 3).update()

ele1 = to_js(
    {
        "group": "nodes",
        "data": jsobj({"id": "a", "weight": 75}),
    },
    dict_converter=js.Object.fromEntries,
)

ele2 = to_js(
    {
        "group": "nodes",
        "data": jsobj({"id": "b", "weight": 75}),
    },
    dict_converter=js.Object.fromEntries,
)

ele3 = to_js(
    {
        "group": "nodes",
        "data": jsobj({"id": "c", "weight": 75}),
    },
    dict_converter=js.Object.fromEntries,
)

cy.add(ele1)
cy.add(ele2)
cy.add(ele3)

for combo in itertools.combinations(["a", "b", "c"], 2):
    edge = to_js(
        {
            "group": "edges",
            "data": jsobj({"source": combo[0], "target": combo[1]}),
        },
        dict_converter=js.Object.fromEntries,
    )
    cy.add(edge)
