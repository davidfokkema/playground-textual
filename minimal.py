from textual.app import App, ComposeResult
from textual.widgets import Placeholder


class MinimalApp(App[None]):
    def compose(self) -> ComposeResult:
        yield Placeholder("This is a minimal app.")


MinimalApp().run()
