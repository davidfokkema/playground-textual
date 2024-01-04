from textual import on
from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.widgets import Button, RichLog


class LoggingApp(App[None]):
    CSS = """
        Horizontal {
            height: auto;
            align: center top;
        }

        Button, RichLog {
            margin: 1 2;
        }
    """

    def compose(self) -> ComposeResult:
        with Horizontal():
            yield Button("Green", id="green", variant="primary")
            yield Button("Red", id="red", variant="primary")
            yield Button("Blue", id="blue", variant="primary")
        yield RichLog(markup=True)

    @on(Button.Pressed)
    def log_text(self, event: Button.Pressed) -> None:
        color = event.button.id
        self.query_one("RichLog").write(f"Hi, I'm [bold {color}]{color}![/] :wink:")


if __name__ == "__main__":
    LoggingApp().run()
