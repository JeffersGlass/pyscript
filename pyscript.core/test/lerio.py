from pyscript import display, when, document
from pyscript import HTML
from matplotlib import pyplot as plt
from random import randint
from js import console
from pyodide.ffi import create_proxy

IMAGES = [
    "https://plus.unsplash.com/premium_photo-1665296634241-6669aaa1a133?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2338&q=80",
    "https://images.unsplash.com/photo-1546527868-ccb7ee7dfa6a?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2340&q=80"
    "https://images.unsplash.com/photo-1510337550647-e84f83e341ca?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2231&q=80"
]

# the following will work as expected
fig = plt.figure()
plt.plot(range(5), range(5))
# Adding some textNode as first content
display("RANGE 5 plot displayed first (will be replaced by RANGE 10 Plot and then by a puppy dog)", target="target_10")

# append=False here is intentionally omitted as this plot is exepcted to be replaced!
display(fig, target="target_10")

fig = plt.figure()
plt.plot(range(10), range(10))
# this will replace previous plt
display(fig, target="target_10", append=False)
# this should replace previous plot image, but instead shows that as it was append=True
display("Hello world!", "FOOOOOO", HTML(f"<img src='{IMAGES[0]}' width='30%' />"), target="target_10", append=False)
display("hello")
display("world")



