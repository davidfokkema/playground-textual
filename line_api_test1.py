import random

from rich.segment import Segment
from textual.app import App, ComposeResult
from textual.strip import Strip
from textual.widget import Widget

CHARS = ["x", "o", ".", ",", "/", "-", "|", "\\"]


class LineWidget(Widget):
    def refresh(self, *regions, repaint=True, layout=False, recompose=False):
        self._buffer = [
            [random.choice(CHARS) for _ in range(self.size.width)]
            for _ in range(self.size.height)
        ]
        return super().refresh(
            *regions, repaint=repaint, layout=layout, recompose=recompose
        )

    def render_line(self, y):
        return Strip([Segment(char) for char in self._buffer[y]])


class TestApp(App[None]):
    def compose(self) -> ComposeResult:
        yield LineWidget()

    def on_mount(self) -> None:
        self.set_interval(1 / 24, self.refresh_widget)

    def refresh_widget(self) -> None:
        self.query_one(LineWidget).refresh()


TestApp().run()
