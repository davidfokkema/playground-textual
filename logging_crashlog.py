import logging

from textual.app import App, ComposeResult
from textual.widgets import Label


class CrashApp(App[None]):
    def compose(self) -> ComposeResult:
        yield Label("Don't crash me")

    def on_mount(self) -> None:
        self.query_one(Labelx).update("crash")


logging.basicConfig(filename="example.log", encoding="utf-8", level=logging.DEBUG)
try:
    CrashApp().run()
except Exception as exc:
    logging.ERROR(exc)
else:
    print("No error?!")
