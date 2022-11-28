import js
from js import cytoscape
from pyodide.ffi import to_js


def jsobj(d):
    return to_js(d, dict_converter=js.Object.fromEntries)


cy = cytoscape.new(
    jsobj(
        {
            "container": js.document.getElementById("cnv"),
            "elements": [
                jsobj({"data": {"id": "a"}}),  # node a
                jsobj({"data": {"id": "b"}}),  # node b
                jsobj(
                    {"data": {"id": "ab", "source": "a", "target": "b"}}  # // edge ab
                ),
            ],
            "style": [  # the stylesheet for the graph
                jsobj(
                    {
                        "selector": "node",
                        "style": jsobj(
                            {"background-color": "#666", "label": "data(id)"}
                        ),
                    }
                ),
                {
                    "selector": "edge",
                    "style": jsobj(
                        {
                            "width": 3,
                            "line-color": "#ccc",
                            "target-arrow-color": "#ccc",
                            "target-arrow-shape": "triangle",
                            "curve-style": "bezier",
                        }
                    ),
                },
            ],
            "layout": jsobj({"name": "grid", "rows": 1}),
        }
    )
)
