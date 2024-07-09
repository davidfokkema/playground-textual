from rich.text import Text
from textual.app import App, ComposeResult
from textual.widgets import Label


class NoEmojiApp(App[None]):
    def compose(self) -> ComposeResult:
        yield Label(Text(":car:"))


NoEmojiApp().run()
