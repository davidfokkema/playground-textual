from pathlib import Path

from rich.syntax import Syntax
from textual.app import App, ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Static


class ShowThyselfApp(App):
    def compose(self) -> ComposeResult:
        with VerticalScroll():
            yield Static(id="code")

    def on_mount(self) -> None:
        code = Path(__file__).read_text()
        highlighted_code = Syntax(code, "python")
        self.query_one("#code").update(highlighted_code)


if __name__ == "__main__":
    ShowThyselfApp().run()
