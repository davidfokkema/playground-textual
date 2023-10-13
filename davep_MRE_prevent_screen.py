from asyncio import sleep
from dataclasses import dataclass

from textual import on
from textual.app import App, ComposeResult
from textual.message import Message
from textual.reactive import var
from textual.screen import Screen
from textual.widgets import Label, Log


class PreventionTestScreen(Screen):
    @dataclass
    class Preventable(Message):
        count: int

    count: var[int] = var(0)

    def compose(self) -> ComposeResult:
        yield Label("Not prevented")
        yield Log()

    @on(Preventable)
    def log_leak(self, event: Preventable) -> None:
        self.query_one(Log).write_line(f"{event}")

    def ping(self) -> None:
        self.post_message(self.Preventable(self.count))
        self.count += 1

    def on_mount(self) -> None:
        self.set_interval(1.0, self.ping)
        self.set_timer(5.0, self.unping)

    async def unping(self) -> None:
        self.query_one(Label).update("Prevented")
        with self.prevent(self.Preventable):
            await sleep(5)
        self.set_timer(5.0, self.unping)
        self.query_one(Label).update("Not prevented")


class PreventiontestApp(App[None]):
    def on_mount(self) -> None:
        self.push_screen(PreventionTestScreen())


if __name__ == "__main__":
    PreventiontestApp().run()
