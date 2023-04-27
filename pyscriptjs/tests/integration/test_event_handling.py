from .support import PyScriptTest, skip_worker


class TestEventHandler(PyScriptTest):
    @skip_worker(reason="FIXME: js.document")
    def test_when_decorator_with_event(self):
        """When the decorated function takes a single parameter,
        it should be passed the event object
        """
        self.pyscript_run(
            """
            <button id="foo_id">foo_button</button>
            <py-script>
                from pyscript import when
                @when("click", selector="#foo_id")
                def foo(evt):
                    print(f"I've clicked {evt.target} with id {evt.target.id}")
            </py-script>
        """
        )
        self.page.locator("text=foo_button").click()
        console_text = self.console.all.lines
        self.wait_for_console("I've clicked [object HTMLButtonElement] with id foo_id")
        assert "I've clicked [object HTMLButtonElement] with id foo_id" in console_text
        self.assert_no_banners()

    @skip_worker(reason="FIXME: js.document")
    def test_when_decorator_without_event(self):
        """When the decorated function takes no parameters (not including 'self'),
        it should be called without the event object
        """
        self.pyscript_run(
            """
            <button id="foo_id">foo_button</button>
            <py-script>
                from pyscript import when
                @when("click", selector="#foo_id")
                def foo():
                    print("The button was clicked")
            </py-script>
        """
        )
        self.page.locator("text=foo_button").click()
        self.wait_for_console("The button was clicked")
        assert "The button was clicked" in self.console.log.lines
        self.assert_no_banners()

    @skip_worker(reason="FIXME: js.document")
    def test_multiple_when_decorators_with_event(self):
        self.pyscript_run(
            """
            <button id="foo_id">foo_button</button>
            <button id="bar_id">bar_button</button>
            <py-script>
                from pyscript import when
                @when("click", selector="#foo_id")
                def foo(evt):
                    print(f"I've clicked {evt.target} with id {evt.target.id}")
                @when("click", selector="#bar_id")
                def foo(evt):
                    print(f"I've clicked {evt.target} with id {evt.target.id}")
            </py-script>
        """
        )
        self.page.locator("text=foo_button").click()
        console_text = self.console.all.lines
        self.wait_for_console("I've clicked [object HTMLButtonElement] with id foo_id")
        assert "I've clicked [object HTMLButtonElement] with id foo_id" in console_text

        self.page.locator("text=bar_button").click()
        console_text = self.console.all.lines
        self.wait_for_console("I've clicked [object HTMLButtonElement] with id bar_id")
        assert "I've clicked [object HTMLButtonElement] with id bar_id" in console_text
        self.assert_no_banners()

    @skip_worker(reason="FIXME: js.document")
    def test_invalid_selector(self):
        """When the selector parameter of @when is invalid, it should show an error"""
        self.pyscript_run(
            """
            <button id="foo_id">foo_button</button>
            <py-script>
                from pyscript import when
                @when("click", selector="#.bad")
                def foo(evt):
                    ...
            </py-script>
        """
        )
        self.page.locator("text=foo_button").click()
        msg = "Failed to execute 'querySelectorAll' on 'Document': '#.bad' is not a valid selector."
        error = self.page.wait_for_selector(".py-error")
        banner_text = error.inner_text()

        if msg not in banner_text:
            raise AssertionError(
                f"Expected message '{msg}' does not "
                f"match banner text '{banner_text}'"
            )

        assert any(msg in line for line in self.console.error.lines)
