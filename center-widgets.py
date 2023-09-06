from textual.app import App, ComposeResult
from textual.containers import Center, Vertical
from textual.widgets import Label


class CenterApp(App):
    CSS = """
        Screen {
            align: center middle;
        }

        Vertical {
            # width: auto;
            width: 15;
            border: solid;
            height: auto;
            align: center middle;
        }

        Center {
            width: 1fr;
            border: round;
        }

        Label {
            width: auto;
            border: solid;
        }
    """

    def compose(self) -> ComposeResult:
        yield Vertical(Center(Label("Short")), Center(Label("Loooooong")))


if __name__ == "__main__":
    app = CenterApp()
    app.run()
