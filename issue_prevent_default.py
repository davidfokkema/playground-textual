from textual.app import App, ComposeResult
from textual.widgets import Button, Label


class MyButton(Button):
    def _on_button_pressed(self, event: Button.Pressed) -> None:
        event.prevent_default()


class PreventApp(App[None]):
    def compose(self) -> ComposeResult:
        yield MyButton("Press me")
        yield Label("No pressure")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.query_one(Label).update("Ouch!")


PreventApp().run()
