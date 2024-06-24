from textual.app import App, ComposeResult
from textual.containers import Center, Vertical
from textual.widgets import Label


class Icon(Vertical):

    DEFAULT_CSS = """
    Icon {
        visibility: hidden;
        width: 10;
        height: 10;
        border: solid $primary;

        Center {
            margin-bottom: 1;
        }

        Label {
            visibility: visible;
        }
    }
    """

    def __init__(self, label: str) -> None:
        super().__init__()
        self._label = label

    def compose(self) -> ComposeResult:
        with Center():
            yield Label("▉▉▉▉\n▉▉▉▉\n▉▉▉▉\n▉▉▉▉", classes="image")
        yield Label(self._label)


class IconLikeApp(App[None]):

    CSS = """
    Screen {
        layers: background foreground;
        layout: horizontal;
    }

    #background {
        width: 100%;
        height: 100%;
        color: #444;
        overflow: hidden;
        layer: background;
    }

    Icon {
        layer: foreground;
    }
    """

    def compose(self) -> ComposeResult:
        yield Label(
            "All these worlds are yours, except Europa. " * 1000, id="background"
        )
        for n in range(10):
            yield Icon(f"Icon {n}")


if __name__ == "__main__":
    IconLikeApp().run()
