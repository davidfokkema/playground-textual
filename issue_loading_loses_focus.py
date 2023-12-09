from textual.app import App, ComposeResult
from textual.widgets import Button


class SpeedRunApp(App[None]):
    def compose(self) -> ComposeResult:
        for idx in range(1, 6):
            yield Button(f"Button {idx}")

    def on_button_pressed(self, event: Button.Pressed):
        event.button.loading = True


app = SpeedRunApp()
if __name__ == "__main__":
    app.run()
