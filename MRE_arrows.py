from textual.app import App, ComposeResult
from textual.widgets import Label


class ArrowApp(App[None]):
    CSS = """
        Screen {
            align: center middle;
        }
        
        Label {
            border: solid;
        }
    """

    def compose(self) -> ComposeResult:
        yield Label("▶")


ArrowApp().run()
