import math

from textual.app import App, ComposeResult
from textual.color import Color
from textual.widgets import Label


class HeartbeatLabel(Label):
    DEFAULT_CSS = """
        HeartbeatLabel {
            padding: 1 2;
        }
    """

    t = 0

    def on_mount(self) -> None:
        self.set_interval(interval=1 / 30, callback=self.modulate_color)
        # start with a color
        self.modulate_color()

    def modulate_color(self) -> None:
        # green, fully saturated, lightness varying smoothly between 0.1 and 0.6
        self.styles.background = Color.from_hsl(
            h=120 / 360, s=1.0, l=0.1 + 0.25 * (1 + math.cos(self.t))
        )
        self.t += math.pi / 30


class MyApp(App[None]):
    CSS = """
        Screen {
            align: center middle;
        }
    """

    def compose(self) -> ComposeResult:
        yield HeartbeatLabel("I'm fancy!")


MyApp().run()
