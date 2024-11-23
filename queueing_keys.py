import time

from textual import work
from textual.app import App, ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Footer, Label, ListItem, ListView
from textual.worker import Worker, WorkerState


class RunningTaskModal(ModalScreen):
    def compose(self) -> ComposeResult:
        yield Label(f"Working on task {self.name}...")


class Task(ListItem):
    def compose(self) -> ComposeResult:
        yield Label(f"Task {self.id}")

    def execute(self) -> Worker:
        self.app.push_screen(RunningTaskModal(name=self.id))
        return self.run_task()

    @work(thread=True)
    def run_task(self) -> None:
        time.sleep(2)

    def on_worker_state_changed(self, event: Worker.StateChanged) -> None:
        if event.state == WorkerState.SUCCESS:
            self.app.pop_screen()


class QueuingKeysApp(App[None]):
    CSS = """
        ModalScreen {
            hatch: left $primary-background;
            align: center middle;

            & Label {
                border: $primary;
                padding: 1 2;
            }
        }
    """
    BINDINGS = [("a", "task_a", "Run task A"), ("b", "task_b", "Run task B")]

    def compose(self) -> ComposeResult:
        yield Footer()
        with ListView():
            yield Task(id="A")
            yield Task(id="B")

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        event.item.execute()

    async def action_task_a(self) -> None:
        await self.query_one("#A").execute().wait()

    def action_task_b(self) -> None:
        self.query_one("#B").execute()


QueuingKeysApp().run()
