import pyodide_js
await pyodide_js.loadPackage('micropip')

import micropip
micropip.add_mock_package("tree-sitter-languages", "1.9")
micropip.add_mock_package("tree-sitter", "0.20.1")
await micropip.install("textual", keep_going=True)

from textual.app import App, ComposeResult
from textual.widgets import Header, Footer


class StopwatchApp(App):
    """A Textual app to manage stopwatches."""

    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Footer()

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark


if __name__ == "__main__":
    app = StopwatchApp()
    app.run()
    