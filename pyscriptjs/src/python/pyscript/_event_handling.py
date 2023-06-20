import inspect

import js
from pyodide.ffi.wrappers import add_event_listener, remove_event_listener
from functools import partial
from collections import namedtuple

EventPair = namedtuple("EventPair", ('event_type', 'element'))

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
        func._when_elements.extend(EventPair(event_type, el) for pair in elements if pair not in func._when_elements)

        # Public property 'when_elements' for acessing remaining elements on page
        if not hasattr(func, "when_elements"): func.when_elements = property(
                fget=lambda self: [pair for pair in self._when_elements if js.document.contains(pair.element)],
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

def _remove_when(func, *, event=None, selector=None):
    if event:
        if selector:
            all_matches = js.document.querySelectorAll(selector)
            for pair in (pair for pair in func._when_elements if pair.element in all_matches):
                remove_event_listener(pair.element, pair.event_type, func)
            func._when_elements = [pair for pair in func._when_elements if not pair.element in all_matches]
        else: # Remove all matched events
            for pair in (pair for pair in func._when_elements if pair.event_type == event):
                remove_event_listener(pair.element, event, func)
            func._when_elements = list()
    else: # No event provided
        # TODO this part
        pass
