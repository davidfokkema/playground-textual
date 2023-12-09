import time

from textual import on, work
from textual.app import App, ComposeResult
from textual.events import ScreenResume
from textual.screen import ModalScreen
from textual.widgets import Button, LoadingIndicator, Static
from textual.worker import Worker, WorkerState


class Task(ModalScreen):
    def __init__(self, title: str) -> None:
        super().__init__()
        self.title = title

    def compose(self) -> ComposeResult:
        yield Button("Close")
        yield LoadingIndicator()

    @on(Button.Pressed)
    def close(self, event: Button.Pressed) -> None:
        self.dismiss()


class TaskButton(Button):
    def __init__(self, task: Task) -> None:
        super().__init__()
        self.task_ = task
        self.label = task.title

    @on(Button.Pressed)
    def execute(self):
        self.app.push_screen(self.task_)


class SpeedRunApp(App[None]):
    CSS = """
        Screen, ModalScreen {
            height: 100%;
            align: center middle;
        }

        Static {
            text-align: center;
        }

        LoadingIndicator {
            height: auto;
        }
    """

    def compose(self) -> ComposeResult:
        for i in range(1, 4):
            yield TaskButton(Task(f"Task {i}"))
        yield Button("Run all", id="speedrun")

    @on(Button.Pressed, "#speedrun")
    def execute(self):
        # task = self.query_one("#task0")
        task = TaskButton("Speedrun")
        self.mount(task)
        task.loading = True
        task.run_task()


app = SpeedRunApp()
if __name__ == "__main__":
    app.run()
