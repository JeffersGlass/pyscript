import types
from random import randint

from pyscript import HTML, display
from pyscript.js_modules.JSTurtle import Graphic

SVG = (
    Graphic.new()
    .moveTo(10, 10)
    .draw(10)
    .curveRight(randint(20, 360), 10)
    .draw(50)
    .asSVG()
)
display(HTML(SVG))

# This is straight from the TurtleThreadDocs

from pyembroidery import JUMP, STITCH, TRIM
from turtlethread import Turtle
from turtlethread.visualise import centered_cross, centered_dot, centered_line


def _visualise_pattern(
    pattern, turtle=None, width=800, height=800, scale=1, done=True, bye=True
):
    """Use the builtin ``turtle`` library to visualise an embroidery pattern.

    Parameters
    ----------
    pattern : pyembroidery.EmbPattern
        Embroidery pattern to visualise
    turtle : turtle.Turtle (optional)
        Python turtle object to use for drawing. If not specified, then the default turtle
        is used.
    width : int
        Canvas width
    height : int
        Canvas height
    scale : int
        Factor the embroidery length's are scaled by.
    done : bool
        If True, then ``turtle.done()`` will be called after drawing.
    bye : bool
        If True, then ``turtle.bye()`` will be called after drawing.
    """
    ##if USE_SPHINX_GALLERY:
    ##    return

    # Lazy import of 'turtle' module just for visualization so that the rest of
    # the library can be used on Python installs where the GUI libraries are not
    # available.
    #
    # (This looks like it would conflict with the 'turtle' variable but it does not)
    ##from turtle import Screen, Turtle

    ##if turtle is None:
    ##    # If turtle is None, grab the default turtle and set its speed to fastest
    ##    if Turtle._pen is None:
    ##        Turtle._pen = Turtle()
    ##    turtle = Turtle._pen
    ##
    ##    turtle.speed("fastest")
    ##screen = Screen()
    ##screen.setup(width, height)

    turtle = Graphic.new()

    if len(pattern.stitches) == 0:
        _finish_visualise(done=done, bye=bye)
        return

    turtle.penup()
    turtle.goto(pattern.stitches[0][0], pattern.stitches[0][1])
    turtle.pendown()

    turtle._tracer = lambda *args, **kwargs: None
    turtle._delay = lambda *args, **kwargs: None

    raise_error = False
    for x, y, command in pattern.stitches:
        x = scale * x
        y = scale * y
        if command == JUMP:
            print("JUMP")
            turtle.color("red")
            turtle.goto(x, y)

            speed = turtle.speed()
            turtle.speed("fastest")
            centered_dot(turtle, 25 * scale)
            turtle.speed(speed)
        elif command == TRIM:
            print("TRIM")
            turtle.penup()
            turtle.goto(x, y)
            turtle.pendown()

            turtle.color("black")
            speed = turtle.speed()
            turtle.speed("fastest")
            centered_cross(turtle, 25 * scale)
            turtle.speed(speed)
        elif command == STITCH:
            print("STITCH")
            turtle.setheading(turtle.towards(x, y))
            print(f"{turtle.towards(x, y)}")
            turtle.pendown()
            turtle.color("blue")
            turtle.goto(x, y)
            speed = turtle.speed()
            turtle.speed("fastest")
            centered_line(turtle, 10 * scale)
            turtle.speed(speed)
        else:
            raise_error = True
            break

    _finish_visualise(done=done, bye=bye)

    display(HTML(turtle.asSVG()))

    if raise_error:
        ValueError(f"Command not supported: {command}")


def _finish_visualise(done, bye):
    pass


def visualise(self, turtle=None, width=800, height=800, scale=1, done=True, bye=True):
    _visualise_pattern(
        self.pattern.to_pyembroidery(),
        turtle=turtle,
        width=width,
        height=height,
        scale=scale,
        done=done,
        bye=bye,
    )


needle = Turtle()
with needle.running_stitch(30):
    needle.forward(300)
    print(dir(needle))
    needle.turn(90)
    needle.forward(30)

needle.visualise = types.MethodType(visualise, needle)
needle.visualise()

display(randint(1, 1000000))
