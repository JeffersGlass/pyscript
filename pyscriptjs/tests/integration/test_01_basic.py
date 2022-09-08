import re
import time

from .support import PyScriptTest


class TestBasic(PyScriptTest):
    def test_pyscript_hello(self):
        self.pyscript_run(
            """
            <py-script>
                print('hello pyscript')
            </py-script>
        """
        )
        # this is a very ugly way of checking the content of the DOM. If we
        # find ourselves to write a lot of code in this style, we will
        # probably want to write a nicer API for it.
        inner_html = self.page.locator("py-script").inner_html()
        pattern = r'<div id="py-.*">hello pyscript</div>'
        assert re.search(pattern, inner_html)

    def test_execution_in_order(self):
        """
        Check that they py-script tags are executed in the same order they are
        defined
        """
        self.pyscript_run(
            """
            <py-script>import js; js.console.log('one')</py-script>
            <py-script>js.console.log('two')</py-script>
            <py-script>js.console.log('three')</py-script>
            <py-script>js.console.log('four')</py-script>
        """
        )
        assert self.console.log.lines == [
            self.PY_COMPLETE,
            "one",
            "two",
            "three",
            "four",
        ]

    def test_escaping_of_angle_brackets(self):
        """
        Check that py-script tags escape angle brackets
        """
        self.pyscript_run(
            """
            <py-script>import js; js.console.log(1<2, 1>2)</py-script>
            <py-script>js.console.log("<div></div>")</py-script>
        """
        )
        assert self.console.log.lines == [self.PY_COMPLETE, "true false", "<div></div>"]

    def test_async_nonblocking(self):
        """
        Check that py-script tags that execute asynchronously do not block
        execution while awaiting
        """
        self.pyscript_run(
            """
            <py-script>import js; import asyncio; js.console.log("one")</py-script>
            <py-script>await asyncio.sleep(2); js.console.log("two")</py-script>
            <py-script>js.console.log("three")</py-script>
        """
        )
        #time.sleep(3)
        #assert True
        assert self.console.log.lines == ["one", "three", "two", self.PY_COMPLETE]