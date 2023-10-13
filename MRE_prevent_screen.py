import asyncio

from textual.app import App, ComposeResult
from textual.reactive import reactive
from textual.screen import Screen
from textual.widgets import Button, Label


class MyScreen(Screen):
    N = reactive(0)

    def compose(self) -> ComposeResult:
        yield Label(id="counter")
        yield Button("Click me")

    def watch_N(self, _, N: int) -> None:
        self.query_one("#counter").update(f"{N=}")

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        with event.control.prevent(Button.Pressed):
            await asyncio.sleep(1)
            self.N += 1


class ChoiceFeedbackApp(App[None]):
    def on_mount(self):
        self.push_screen(MyScreen())


if __name__ == "__main__":
    ChoiceFeedbackApp().run()
