import inspect

import js
from pyodide.ffi.wrappers import add_event_listener
from functools import partial


def when(event_type=None, selector=None):
    """
    Decorates a function and passes py-* events to the decorated function
    The events might or not be an argument of the decorated function
    """

    def decorator(func):
        elements = js.document.querySelectorAll(selector)
        sig = inspect.signature(func)

        # Set to track JS elements
        if not hasattr(func, "_when_elements"): func._when_elements = list()
        func._when_elements.extend(el for el in elements if el not in func._when_elements)

        # Public property 'when_elements' for acessing remaining elements on page
        if not hasattr(func, "when_elements"): func.when_elements = property(
                fget=lambda self: [el for el in self._when_elements if js.document.contains(el)],
                )
            
        func.remove_when = partial(_remove_when, func)
        
        # Function doesn't receive events
        if not sig.parameters:

            def wrapper(*args, **kwargs):
                func()

            for el in elements:
                add_event_listener(el, event_type, wrapper)
        else:
            for el in elements:
                add_event_listener(el, event_type, func)
        return func

    return decorator

def _remove_when(func, selector=None):
    if selector:
        # TODO actually remove event listeners
        func._when_elements = [el for el in func._when_elements if not el in js.document.querySelectorAll(selector)]
    else:
        # TODO actually remove event listeners
        func._when_elements = list()