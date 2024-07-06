from textual.app import App, ComposeResult
from textual.events import Key
from textual.widget import Widget
from textual.widgets import Button, Static


class TestWidget(Widget):
    def compose(self):
        yield Static("Hello, world!\n")
        # yield Button("Hi")

    def on_key(self, event: Key) -> None:
        self.app.bell()


class TestApp(App):
    CSS = """
        Widget:focus {
            border: solid $secondary;
        }
    """

    def compose(self) -> ComposeResult:
        yield TestWidget()


if __name__ == "__main__":
    TestApp().run()
