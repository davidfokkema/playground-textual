import time

from textual import on, work
from textual.app import App, ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Button, LoadingIndicator, Static
from textual.worker import Worker, WorkerState


class TaskDialog(ModalScreen):
    def compose(self) -> ComposeResult:
        yield Static(self.name)
        yield LoadingIndicator()


class TaskButton(Button):
    @on(Button.Pressed)
    def execute(self):
        self._task_screen = TaskDialog(self.label)
        self.app.push_screen(self._task_screen)
        self.run_task()

    @work(thread=True)
    def run_task(self):
        time.sleep(1)

    @on(Worker.StateChanged)
    def exit_task(self, event: Worker.StateChanged):
        if event.state in [
            WorkerState.CANCELLED,
            WorkerState.ERROR,
            WorkerState.SUCCESS,
        ]:
            self._task_screen.dismiss()


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
        for i in range(3):
            yield TaskButton(f"Task {i}")
        yield Button("Run all", id="speedrun")

    @on(Button.Pressed, "#speedrun")
    def speedrun(self) -> None:
        task = TaskButton("Task 0")
        task.execute()


app = SpeedRunApp()
if __name__ == "__main__":
    app.run()
