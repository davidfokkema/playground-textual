from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.widgets import Label


class StatusApp(App):
    CSS = """
    Label {
        padding: 1 2;
        margin: 1 2;
        background: $primary-background;
    }

    .success {
        background: $success;
    }

    .error {
        background: $error;
    }

    .warning {
        background: $warning;
    }
    """

    def compose(self) -> ComposeResult:
        with Horizontal():
            yield Label("Communication Protocol", id="protocol")
            yield Label("Database", id="database")
            yield Label("Visualisation", id="visualisation")
            yield Label("Something else", id="else")

    def on_mount(self) -> None:
        # do some work
        self.query_one("#protocol").add_class("success")
        self.query_one("#database").add_class("warning")
        self.query_one("#visualisation").add_class("error")


if __name__ == "__main__":
    StatusApp().run()
