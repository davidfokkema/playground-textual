import time

from textual import on, work
from textual.app import App, ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Button, LoadingIndicator, Static
from textual.worker import Worker, WorkerState


class TaskButton(Button):
    @on(Button.Pressed)
    def execute(self):
        self.loading = True
        self.run_task()

    @work(thread=True)
    def run_task(self):
        time.sleep(1)

    @on(Worker.StateChanged)
    def exit_task(self, event: Worker.StateChanged):
        if event.state == WorkerState.SUCCESS:
            self.loading = False


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
            yield TaskButton(f"Task {i}", id=f"task{i}")
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
