import itertools

from textual.app import App, ComposeResult
from textual.widgets import Label


class HeartbeatLabel(Label):
    DEFAULT_CSS = """
        HeartbeatLabel {
            padding: 1 2;
        }
    """

    COLORS = itertools.cycle(["red", "blue", "green"])

    def on_mount(self) -> None:
        self.set_interval(interval=0.5, callback=self.blink)
        # start with a color
        self.blink()

    def blink(self) -> None:
        self.styles.background = next(self.COLORS)


class MyApp(App[None]):
    CSS = """
        Screen {
            align: center middle;
        }
    """

    def compose(self) -> ComposeResult:
        yield HeartbeatLabel("I'm fancy!")


MyApp().run()
