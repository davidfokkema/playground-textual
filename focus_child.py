from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.widgets import Button


class ContentSwitcher(Vertical):
    def compose(self) -> ComposeResult:
        self.border_title = "ContentSwitcher"
        yield Button("only child")

    def on_mount(self) -> None:
        self.query().first().focus()


class FocusApp(App):
    CSS = """
        Vertical {
            padding: 1 2;
            border: heavy $primary;
        }
    """

    def compose(self) -> ComposeResult:
        with Vertical() as v:
            v.border_title = "Outer"
            yield Button("button 1")
            yield ContentSwitcher()


if __name__ == "__main__":
    app = FocusApp()
    app.run()
