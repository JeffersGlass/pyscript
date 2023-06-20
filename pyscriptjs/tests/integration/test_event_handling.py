from .support import PyScriptTest, skip_worker


class TestEventHandler(PyScriptTest):
    @skip_worker(reason="FIXME: js.document (@when decorator)")
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

    @skip_worker(reason="FIXME: js.document (@when decorator)")
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

    @skip_worker(reason="FIXME: js.document (@when decorator)")
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

    @skip_worker(reason="FIXME: js.document (@when decorator)")
    def test_two_when_decorators(self):
        """When decorating a function twice, both should function"""
        self.pyscript_run(
            """
            <button id="foo_id">foo_button</button>
            <button class="bar_class">bar_button</button>
            <py-script>
                from pyscript import when
                @when("click", selector="#foo_id")
                @when("mouseover", selector=".bar_class")
                def foo(evt):
                    print(f"An event of type {evt.type} happened")
            </py-script>
        """
        )
        self.page.locator("text=bar_button").hover()
        self.page.locator("text=foo_button").click()
        self.wait_for_console("An event of type click happened")
        assert "An event of type mouseover happened" in self.console.log.lines
        assert "An event of type click happened" in self.console.log.lines
        self.assert_no_banners()

    @skip_worker(reason="FIXME: js.document (@when decorator)")
    def test_two_when_decorators_same_element(self):
        """When decorating a function twice *on the same DOM element*, both should function"""
        self.pyscript_run(
            """
            <button id="foo_id">foo_button</button>
            <py-script>
                from pyscript import when
                @when("click", selector="#foo_id")
                @when("mouseover", selector="#foo_id")
                def foo(evt):
                    print(f"An event of type {evt.type} happened")
            </py-script>
        """
        )
        self.page.locator("text=foo_button").hover()
        self.page.locator("text=foo_button").click()
        self.wait_for_console("An event of type click happened")
        assert "An event of type mouseover happened" in self.console.log.lines
        assert "An event of type click happened" in self.console.log.lines
        self.assert_no_banners()

    @skip_worker(reason="FIXME: js.document (@when decorator)")
    def test_when_decorator_multiple_elements(self):
        """The @when decorator's selector should successfully select multiple
        DOM elements
        """
        self.pyscript_run(
            """
            <button class="bar_class">button1</button>
            <button class="bar_class">button2</button>
            <py-script>
                from pyscript import when
                @when("click", selector=".bar_class")
                def foo(evt):
                    print(f"{evt.target.innerText} was clicked")
            </py-script>
        """
        )
        self.page.locator("text=button1").click()
        self.page.locator("text=button2").click()
        self.wait_for_console("button2 was clicked")
        assert "button1 was clicked" in self.console.log.lines
        assert "button2 was clicked" in self.console.log.lines
        self.assert_no_banners()

    @skip_worker(reason="FIXME: js.document (@when decorator)")
    def test_when_decorator_duplicate_selectors(self):
        """ """
        self.pyscript_run(
            """
            <button id="foo_id">foo_button</button>
            <py-script>
                from pyscript import when
                @when("click", selector="#foo_id")
                @when("click", selector="#foo_id")
                def foo(evt):
                    print(f"I've clicked {evt.target} with id {evt.target.id}")
            </py-script>
        """
        )
        self.page.locator("text=foo_button").click()
        console_text = self.console.all.lines
        self.wait_for_console("I've clicked [object HTMLButtonElement] with id foo_id")
        assert (
            console_text.count("I've clicked [object HTMLButtonElement] with id foo_id")
            == 2
        )
        self.assert_no_banners()

    @skip_worker(reason="FIXME: js.document (@when decorator)")
    def test_when_decorator_invalid_selector(self):
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

        assert msg in self.console.error.lines[-1]
        self.check_py_errors(msg)

    @skip_worker(reason="FIXME: js.document (@when decorator)")
    def test_remove_when(self):
        self.pyscript_run(
            """
            <button id="one" class="foo">One</button>
            <button id="two" class="foo bar">Two</button>
            <button id="three" class="foo bar">Three</button>

            <button id="remove-one" py-click="foo.remove_when('#one'); print('removed_one')">remove_one</button>
            <button id="remove-bar" py-click="foo.remove_when('.bar'); print('removed_two')">remove_bar</button>

            <button id="done" py-click="print("DONE")>Done</button>
            
            <py-script>
                from pyscript import when
                @when("click", selector=".foo")
                def foo(evt):
                    print(evt.target.innerText * 2)

            </py-script>
        """
        )

        #Make sure all buttons actually work
        self.page.locator("#one").click()
        self.page.locator("#two").click()
        self.page.locator("#three").click()
        self.page.locator("text='ThreeThree'").wait_for()
        assert self.console.log.lines.count("OneOne") == 1
        assert self.console.log.lines.count("TwoTwo") == 1
        assert self.console.log.lines.count("ThreeThree") == 1

        #Remove listeners from #one
        self.page.locator("#remove-one").click()
        self.page.locator("text='remove_one'").wait_for()
        
        self.page.locator("#one").click()
        self.page.locator("#two").click()
        self.page.locator("#three").click()
        self.page.locator("text='ThreeThree'").wait_for()
        assert self.console.log.lines.count("OneOne") == 1 # Not incremented
        assert self.console.log.lines.count("TwoTwo") == 2 # Incremented
        assert self.console.log.lines.count("ThreeThree") == 2 # Incremented

        #Remove listeners from .bar
        self.page.locator("#remove-bar").click()
        self.page.locator("text='remove_bar'").wait_for()

        self.page.locator("#one").click()
        self.page.locator("#two").click()
        self.page.locator("#three").click()
        self.page.locator("text='DNE'").wait_for()
        assert self.console.log.lines.count("OneOne") == 1 # Not incremented
        assert self.console.log.lines.count("TwoTwo") == 2 # Not incremented
        assert self.console.log.lines.count("ThreeThree") == 2 # Not incremented

    @skip_worker(reason="FIXME: js.document (@when decorator)")
    def test_remove_all_when(self):
        self.pyscript_run(
            """
            <button>button</button>
            <div>div</div>
            <p>paragraph</p>

            <span py-click="foo.remove_when(); print('removed')">Remove</span>
            <h1 id="done">DONE</h1>

            <py-script>
                from pyscript import when

                @when("click", selector="button")
                @when("click", selector="div")
                @when("click", selector="p")
                def foo(evt):
                    print(evt.target.innerText * 2)
            </py-script>
            """
        )

        self.page.locator("button").click()
        self.page.locator("div").click()
        self.page.locator("p").click()
        self.page.locator("text='paragraphparagraph'").wait_for()
        assert self.console.log.lines.count("buttonbutton") == 1
        assert self.console.log.lines.count("divdiv") == 1
        assert self.console.log.lines.count("paragraphparagraph") == 1

        self.page.locator('span').click()
        self.page.locator("button").click()
        self.page.locator("div").click()
        self.page.locator("p").click()
        self.page.locator("text='DONE'").wait_for()
        assert self.console.log.lines.count("buttonbutton") == 1
        assert self.console.log.lines.count("divdiv") == 1
        assert self.console.log.lines.count("paragraphparagraph") == 1