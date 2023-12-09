import time

from textual import on, work
from textual.app import App, ComposeResult
from textual.events import ScreenResume
from textual.message import Message
from textual.screen import ModalScreen
from textual.widgets import Button, LoadingIndicator, Static
from textual.worker import Worker, WorkerState


class MyTask(ModalScreen):
    def compose(self) -> ComposeResult:
        yield Button("Close")
        yield LoadingIndicator(id="loading_indicator")

    @on(Button.Pressed)
    def close(self, event: Button.Pressed) -> None:
        # bug: if you do not return a value, await push_screen will hang and
        # subsequent tasks will not be performed in speedrun
        self.dismiss()

    @on(ScreenResume)
    def resume(self) -> None:
        self.run_task()

    @work(thread=True)
    def run_task(self):
        time.sleep(1)

    @on(Worker.StateChanged)
    def exit_task(self, event: Worker.StateChanged):
        if event.state == WorkerState.SUCCESS:
            self.query_one("#loading_indicator").remove()


class TaskButton(Button):
    def __init__(
        self, task_class: type[MyTask], label: str | None = None, *args, **kwargs
    ) -> None:
        super().__init__(label, *args, **kwargs)
        self.task_class = task_class

    @on(Button.Pressed)
    def execute(self):
        task = self.task_class()
        self.app.push_screen(task)


class SpeedRunApp(App[None]):
    # CSS = """
    #     Screen, ModalScreen {
    #         height: 100%;
    #         align: center middle;
    #     }

    #     Static {
    #         text-align: center;
    #     }

    #     LoadingIndicator {
    #         height: auto;
    #     }
    # """

    def compose(self) -> ComposeResult:
        for i in range(1, 4):
            yield TaskButton(MyTask, f"Task {i}", id=f"task{i}")
        yield Button("Run all", id="speedrun")

    @on(Button.Pressed, "#speedrun")
    def execute_speedrun(self, event: Button.Pressed):
        self.speedrun()

    @work()
    async def speedrun(self):
        print("Starting tasks...")
        for i in range(3):
            print(f"Running task {i}")
            task = MyTask()
            await self.push_screen(task, wait_for_dismiss=True)
            print(f"Finished task {i}")
        print("All tasks done!")


app = SpeedRunApp()
if __name__ == "__main__":
    app.run()
