from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.widgets import Button, Label


class AddChildrenApp(App[None]):
    def compose(self) -> ComposeResult:
        yield Button("Add Label")
        with Vertical():
            for idx in range(1, 4):
                yield Label(f"Label {idx}")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        container = self.query_one(Vertical)
        idx = len(container.children) + 1
        self.query_one(Vertical).mount(Label(f"Label {idx}"), before=0)


AddChildrenApp().run()
