from textual.app import App, ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Label


class ScrollApp(App[None]):
    CSS = """
        Label {
            margin: 1 2;
        }
    """

    def compose(self) -> ComposeResult:
        with VerticalScroll():
            for idx in range(20):
                yield Label(f"Label {idx}.")


if __name__ == "__main__":
    ScrollApp().run()
