from textual.app import App, ComposeResult
from textual.containers import HorizontalScroll
from textual.widgets import Label, ListItem, ListView


class MyApp(App[None]):
    CSS = """
        ListView, ListItem {
            width: auto;
        }
    """

    def compose(self) -> ComposeResult:
        with HorizontalScroll():
            with ListView():
                yield ListItem(Label("This is a very long item" * 10))
                yield ListItem(Label("Another very long item" * 10))


MyApp().run()
