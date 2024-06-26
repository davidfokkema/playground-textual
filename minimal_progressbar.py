from textual.app import App, ComposeResult
from textual.widgets import ProgressBar


class MinimalApp(App[None]):
    def compose(self) -> ComposeResult:
        yield ProgressBar()

    def on_mount(self) -> None:
        self.query_one(ProgressBar).query_one("Bar").styles.width = "1fr"


MinimalApp().run()
