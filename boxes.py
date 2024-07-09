from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal
from textual.widgets import Label


class BorderApp(App[None]):
    CSS_PATH = "boxes.tcss"

    def compose(self) -> ComposeResult:
        with Horizontal():
            with Container(id="box1"):
                yield Label("Box 1")
            yield Container(id="spacing")
            with Container(id="box2"):
                yield Label("Box 2")


BorderApp().run()
