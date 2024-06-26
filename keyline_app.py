from textual.app import App, ComposeResult
from textual.containers import Grid, Horizontal
from textual.widgets import Placeholder


class KeylinApp(App):
    CSS_PATH = "keyline.tcss"

    def compose(self) -> ComposeResult:
        with Horizontal():
            with Grid():
                yield Placeholder("a")
                yield Placeholder("b")
                yield Placeholder("c")
                yield Placeholder("d")
                yield Placeholder("e")
                yield Placeholder("f")
                yield Placeholder("g")
                yield Placeholder("h")
                yield Placeholder("i")


if __name__ == "__main__":
    KeylinApp().run()
