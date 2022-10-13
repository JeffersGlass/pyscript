## >> pyscript
from dataclasses import dataclass

import js
from pyodide.ffi import create_proxy


def handler(_func=None, *, event=None, element=js.document, options=None):
    if not js.hasOwnProperty("handlers"):
        js.handlers = js.Object.new()

    def decorator(func):
        proxy = create_proxy(func)
        js.set_value(js.handlers, func.__name__, proxy)
        if event:
            element.addEventListener(event, proxy, options)
        return func

    # just @handler( None, **kargs )
    if _func is None:
        return decorator

    # just @handler
    else:
        js.set_value(js.handlers, _func.__name__, create_proxy(_func))
        return _func


## << in pyscript


@handler
def foo():
    js.console.log("foo called")


@handler
def boo(e):
    js.console.log("boo called with event")
    js.console.log(e)


@handler
def loo(*e):
    js.console.log("loo called with *event")
    js.console.log(e[0])
    js.console.log(e[1])


@handler(event="click")
def doc_click(*e):
    js.console.log("doc_click called with *event")
    js.console.log(e[0])


@handler(event="mousemove", element=Element("empty_button").element)
def button_mousemove(*e):
    js.console.log("button_mousemove called with *event")
    js.console.log(e[0])


@dataclass
class Person:
    first: str
    last: str


jg = Person(first="Jeff", last="Glass")


@handler
def set_first_name(*e):
    js.console.log(e)
    # jg.first = e.target.firstName.value
    # js.console.log(e.target.firstName.value)
