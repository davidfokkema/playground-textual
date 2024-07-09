from rich.text import Text
from textual import on
from textual.app import App, ComposeResult, RenderResult
from textual.events import Resize
from textual.widgets import Label, Static

TEXT = "A quick brown fox jumps over the lazy dog."
STEP = 2


class MyLabel(Label):
    def __init__(self, label: str, *args, **kwargs) -> None:
        super().__init__(label, *args, **kwargs)
        self.label = label

    def render(self) -> RenderResult:
        text = Text(self.label)
        text.truncate(self.size.width, overflow="ellipsis")
        return text


class SmallLabelApp(App[None]):
    CSS = """
        MyLabel {
            height: 3;
            border: solid $primary;
        }
    """

    def compose(self) -> ComposeResult:
        for width in range(STEP, len(TEXT) + STEP + 2, STEP):
            (label := MyLabel(TEXT)).styles.width = width
            yield label


SmallLabelApp().run()
