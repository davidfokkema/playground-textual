from textual.app import App, ComposeResult, on
from textual.widgets import Button, ProgressBar


class MinimalApp(App[None]):
    CSS = """
        Bar {
            width: 1fr;
        }

        .fancy .bar--indeterminate {
            color: white;
        }
    """

    def compose(self) -> ComposeResult:
        yield ProgressBar()
        yield Button("Add", id="add")
        yield Button("Remove", id="remove")

    @on(Button.Pressed, "#add")
    def set_fancy(self) -> None:
        self.query_one(ProgressBar).add_class("fancy")

    @on(Button.Pressed, "#remove")
    def remove_fancy(self) -> None:
        self.query_one(ProgressBar).remove_class("fancy")


MinimalApp().run()
