from textual.app import App, ComposeResult
from textual.widgets import Button, Label


class AppendTextLabel(Label):
    def __init__(self, text: str, *args, **kwargs) -> None:
        self.text = text
        super().__init__(text, *args, **kwargs)

    def append(self, text: str) -> None:
        self.text += text
        self.update(self.text)


class AppendTextApp(App[None]):
    def compose(self) -> ComposeResult:
        yield AppendTextLabel("Foo")
        yield Button("Add text")

    def on_button_pressed(self) -> None:
        self.query_one(AppendTextLabel).append("\nThis too")


AppendTextApp().run()
