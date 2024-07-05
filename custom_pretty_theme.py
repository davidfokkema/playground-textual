# code is mostly from davep, I edited it for theming pretty-printing
from rich.theme import Theme
from textual.app import App, ComposeResult
from textual.widgets import Pretty


class CustomThemeApp(App[None]):
    def on_mount(self) -> None:
        self.console.push_theme(Theme({"repr.str": "bold italic blue"}))

    def compose(self) -> ComposeResult:
        yield Pretty({"username": "david", "userid": 12345, "type": float})


if __name__ == "__main__":
    CustomThemeApp().run()
