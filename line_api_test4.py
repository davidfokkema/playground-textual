import itertools

from rich.segment import Segment
from textual.app import App, ComposeResult
from textual.geometry import Region
from textual.strip import Strip
from textual.widget import Widget

CHARS = itertools.cycle(["x", "o", ".", ",", "/", "-", "|", "\\"])


class LineWidget(Widget):
    def refresh(self, *regions, repaint=True, layout=False, recompose=False):
        self._char = next(CHARS)
        return super().refresh(
            *regions, repaint=repaint, layout=layout, recompose=recompose
        )

    def render_line(self, y):
        return Strip([Segment(self._char * self.size.width)])

    def redraw_square(self) -> None:
        self.refresh(Region(40, 10, 5, 5))


class TestApp(App[None]):
    def compose(self) -> ComposeResult:
        yield LineWidget()

    def on_mount(self) -> None:
        self.set_interval(1 / 2, self.refresh_widget)

    def refresh_widget(self) -> None:
        self.query_one(LineWidget).redraw_square()


TestApp().run()
