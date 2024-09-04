from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Label


class HoverContainer(Container):
    def on_enter(self) -> None:
        self.add_class("hover-within")

    def on_leave(self) -> None:
        self.remove_class("hover-within")


class HoverWithinApp(App[None]):
    CSS = """
        Screen {
            align: center middle;
        }

        Container, Label {
            width: auto;
            height: auto;
            border: solid $secondary;
            margin: 1 2;
        }

        .hover-within {
            border: thick $secondary;
        }
    """

    def compose(self) -> ComposeResult:
        with HoverContainer(id="outer"):
            with Container(id="inner"):
                yield Label("Within", id="innermost")


HoverWithinApp().run()
