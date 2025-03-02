import itertools
import random

from rich.segment import Segment
from textual.app import App, ComposeResult
from textual.geometry import Region
from textual.strip import Strip
from textual.widget import Widget

CHARS = itertools.cycle(["x", "o", ".", ",", "/", "-", "|", "\\"])


class LineWidget(Widget):
    def refresh(self, *regions, repaint=True, layout=False, recompose=False):
        char = next(CHARS)
        self._buffer = [
            [char for _ in range(self.size.width)] for _ in range(self.size.height)
        ]
        return super().refresh(
            *regions, repaint=repaint, layout=layout, recompose=recompose
        )

    def render_line(self, y):
        return Strip([Segment(char) for char in self._buffer[y]])

    def replot(self) -> None:
        regions = [
            Region(
                random.randint(0, self.size.width - 1),
                random.randint(0, self.size.height - 1),
                1,
                1,
            )
            for _ in range(20)
        ]
        self.refresh(*regions)


class TestApp(App[None]):
    def compose(self) -> ComposeResult:
        yield LineWidget()

    def on_mount(self) -> None:
        self.set_interval(1 / 24, self.refresh_widget)

    def refresh_widget(self) -> None:
        self.query_one(LineWidget).replot()


TestApp().run()
