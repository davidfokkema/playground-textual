from rich.text import Text
from textual.app import App, ComposeResult, RenderResult
from textual.containers import Container, Horizontal
from textual.widgets import Label

TEXT = "A quick brown [dark_goldenrod]fox[/] jumps over the lazy dog."
STEP = 2


class MyLabel(Label):
    def __init__(self, label: str, *args, **kwargs) -> None:
        super().__init__(label, *args, **kwargs)
        self.label = label

    def render(self) -> RenderResult:
        text = Text.from_markup(self.label)
        text.truncate(self.size.width, overflow="ellipsis")
        return text


class SmallLabelApp(App[None]):
    CSS = """
        Horizontal, Container {
            height: auto;
        }

        Label, MyLabel {
            height: 3;
            border: solid $primary;
        }
    """

    def compose(self) -> ComposeResult:
        for width in range(STEP, len(TEXT) + STEP + 2, STEP):
            with Horizontal():
                with Container():
                    (label := Label(TEXT)).styles.width = width
                    yield label
                with Container():
                    (label := MyLabel(TEXT)).styles.width = width
                    yield label


SmallLabelApp().run()
