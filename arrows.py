from textual.app import App, ComposeResult
from textual.widgets import Label


class ArrowApp(App[None]):
    CSS = """
        Screen {
            align: center middle;
        }
        
        Label {
            margin: 1 0;
        }
    """

    def compose(self) -> ComposeResult:
        yield Label("->")
        yield Label("→")
        yield Label("⎯⎯⎯⎯→")
        yield Label("      ╲\n▔▔▔▔▔▔╱")
        yield Label("⎯⎯⎯⎯▶︎")
        yield Label("───────▶︎")


ArrowApp().run()
