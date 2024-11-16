from textual.app import App, ComposeResult
from textual.widgets import Placeholder


class MinimalApp(App[None]):
    CSS = """
        Screen {
            overflow: auto auto;
        }
        Placeholder {
            min-width: 40;
        }
    """

    def compose(self) -> ComposeResult:
        yield Placeholder("This is a minimal app.")


MinimalApp().run()
