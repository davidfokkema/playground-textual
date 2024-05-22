from textual.app import App, ComposeResult
from textual.widgets import Label


class IndicatorApp(App):
    CSS = """
        Screen {
            align: center middle;
        }

        Label {
            border: solid $primary;
        }
    """

    def compose(self) -> ComposeResult:
        yield Label("Server status of the most important server", id="status")

    def on_mount(self) -> None:
        self.query_one("#status").border_subtitle = "[green]●green"


app = IndicatorApp()

if __name__ == "__main__":
    app.run()
