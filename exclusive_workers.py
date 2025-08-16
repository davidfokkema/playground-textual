import time
from asyncio import sleep

from textual import on, work
from textual.app import App, ComposeResult
from textual.containers import HorizontalGroup
from textual.widgets import Button, RichLog
from textual.worker import get_current_worker


class Application(App):
    def compose(self) -> ComposeResult:
        self.richlog = RichLog()
        yield self.richlog
        with HorizontalGroup():
            yield Button("Run worker", id="worker")
            yield Button("Run worker THREAD", id="thread")

    def on_button_pressed(self, event: Button.Pressed):
        self.richlog.write(event.button.id)

    @on(Button.Pressed, "#worker")
    @work(exclusive=True, thread=False)
    async def worker_runner(self, event: Button.Pressed):
        await sleep(1)  # simulate process intensive thing
        self.richlog.write("Worker completed!")

    @on(Button.Pressed, "#thread")
    @work(exclusive=True, thread=True)
    def thread_runner(self, event: Button.Pressed):
        time.sleep(1)  # simulate process intensive thing
        if get_current_worker().is_cancelled:
            self.richlog.write("Thread was cancelled!")
            return
        else:
            self.richlog.write("Thread completed!")


Application().run()
