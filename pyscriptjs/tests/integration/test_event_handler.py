from .support import PyScriptTest


class TestEventHandler(PyScriptTest):
    def test_decorator_click_event(self):
        self.pyscript_run(
            """
            <button id="foo_id">foo_button</button>
            <py-script>
                for d in list(dir()):
                    print(d)
                from pyscript import when
                @when("click", id="foo_id")
                def foo(evt):
                    print(f"I've clicked {evt.target} with id {evt.target.id}")
            </py-script>
        """
        )
        self.page.locator("text=foo_button").click()
        console_text = self.console.all.lines
        assert "I've clicked [object HTMLButtonElement] with id foo_id" in console_text

    def test_decorator_without_event(self):
        self.pyscript_run(
            """
            <button id="foo_id">foo_button</button>
            <py-script>
                from pyscript import when
                @when(id="foo_id")
                def foo():
                    print("This will fail")
            </py-script>
        """
        )
        self.page.locator("text=foo_button").click()
        console_text = self.console.all.lines
        assert "This will fail" not in console_text

    def test_multiple_decorators_click_event(self):
        self.pyscript_run(
            """
            <button id="foo_id">foo_button</button>
            <button id="bar_id">bar_button</button>
            <py-script>
                from pyscript import when
                @when("click", id="foo_id")
                def foo(evt):
                    print(f"I've clicked {evt.target} with id {evt.target.id}")
                @when("click", id="bar_id")
                def foo(evt):
                    print(f"I've clicked {evt.target} with id {evt.target.id}")
            </py-script>
        """
        )
        self.page.locator("text=foo_button").click()
        console_text = self.console.all.lines
        assert "I've clicked [object HTMLButtonElement] with id foo_id" in console_text

        self.page.locator("text=bar_button").click()
        console_text = self.console.all.lines
        assert "I've clicked [object HTMLButtonElement] with id bar_id" in console_text

    # TODO Printing Logging the actual event 
    # print(f"Reacting to event {evt}")
    # "TypeError: __str__ returned non-string (type pyodide.JsProxy)"
    def test_py_click_no_decorator(self):
        self.pyscript_run(
            """
            <button py-click="reacts_to_py_click">no_when</button><br><br>
            <py-script>
            def reacts_to_py_click(evt):
                print(f"Reacting to event")
            </py-script>
            """
        )
        self.page.locator("text=no_when").click()
        self.wait_for_console("Reacting to event")
        console_text = self.console.all.lines
        assert "Reacting to event" in console_text

    def test_py_click_two_args_no_decorator(self):
        self.pyscript_run(
            """
            <button py-click="multiple_args">two_args_button</button><br><br>
            <py-script>
            def multiple_args(first, second):
                print(f"I got {first=}, {second=}")
            </py-script>
            """
        )
        self.page.locator("text=two_args_button").click()
        self.wait_for_console("[event]", match_substring=True)
        assert any("UserError: (PY0000): 'py-[event]' take 0 or 1 arguments" in line for line in self.console.error.lines)

    # TODO Printing or logging the actual event here gives 
    # print(f"Got event with target {evt}")
    # "TypeError: __str__ returned non-string (type pyodide.JsProxy)"
    # TODO Inspect is incorrectly identifying the 'self' parameter as a second parameter.
    # 'params.length' is identified as 2 in JS though the direct inspection sees only 
    # the 1 non-self paramter
    def test_py_click_method_no_decorator(self):
        self.pyscript_run(
            """
            <button py-click="instance.someEventFunc">instance_method</button>
            <py-script>
                import inspect
                class Instance():
                    def someEventFunc(self, evt):
                        print(f"Got event on Method")
                instance = Instance()
                print(f"{len(inspect.signature(instance.someEventFunc).parameters)= }")
            </py-script>
            """
        )
        self.page.locator("text=instance_method").click()
        self.wait_for_console("Method", match_substring=True, timeout=5000)
        console_text = self.console.all.lines
        assert "Got event on Method" in console_text

    def test_run_code_in_py_click(self):
        self.pyscript_run(
            """
                <button py-click="print('a hack!')">misuse_py_event</button>
            """
        )
        self.page.locator("text=misuse_py_event").click()
        self.wait_for_console("[event]", match_substring=True)
        assert any("UserError: (PY0000): The code provided to 'py-[event]' should be the name of a function or Callable. To run an expression as code, use 'py-[event]-code'" in line for line in self.console.error.lines)

    def test_run_code_in_py_click_code(self):
        self.pyscript_run(
            """
                <button py-click-code="print('printed code from code tag')">correct_use_py_event_code</button>
            """
        )
        self.page.locator("text=correct_use_py_event_code").click()
        self.wait_for_console('code tag', match_substring=True)
        console_text = self.console.all.lines
        assert "printed code from code tag" in console_text

    def test_run_callable_in_py_click_code(self):
        self.pyscript_run(
            """
                <button id="foo" py-click-code="callable_fun">misuse_py_event_code</button>
                <py-script>
                    def callable_fun():
                        print('This should fail')
                </py-script>
            """
        )
        self.page.locator("text=misuse_py_event").click()
        self.wait_for_console('Callable', match_substring=True)
        tb_lines = self.console.error.lines[-1].splitlines()
        assert (
            tb_lines[1]
            == "UserError: (PY0000): The code provided to 'py-[event]-code' was the name of a Callable. Did you mean to use 'py-[event]?"
        )
