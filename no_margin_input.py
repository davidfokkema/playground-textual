from textual.app import App, ComposeResult
from textual.widgets import Input, Label


class SmallInputApp(App[None]):
    CSS = """
        Input {
            padding: 1;
            border: wide $primary;
            height: 5;
        }
    """

    def compose(self) -> ComposeResult:
        yield Label("Top")
        yield Input()
        yield Label("Bottom")


SmallInputApp().run()
