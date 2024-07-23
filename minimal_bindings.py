import time

from textual.app import App, ComposeResult
from textual.widgets import Footer, Log


class NoBindingsApp(App[None]):
    BINDINGS = [("q", "quit", "Quit"), ("a", "add_text", "Add Log Entry")]

    def compose(self) -> ComposeResult:
        yield Footer()
        yield Log()

    def action_add_text(self) -> None:
        self.query_one(Log).write_line(
            f"Captains Log, stardate {time.monotonic():.1f}."
        )


NoBindingsApp().run()
