# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "faker",
#     "textual",
# ]
# ///

from faker import Faker
from textual import on, work
from textual.app import App, ComposeResult
from textual.containers import HorizontalGroup
from textual.widgets import Button, SelectionList
from textual.widgets.selection_list import Selection
from textual.worker import Worker, WorkerState, get_current_worker


class CustomSelectionList(SelectionList):
    @work(thread=True, exclusive=True)
    def scan_and_mount(self) -> list[Selection] | None:
        worker = get_current_worker()
        fake = Faker()
        texts = fake.texts(nb_texts=100_000, max_nb_chars=30)
        if not worker.is_cancelled:
            return [Selection(text, idx) for idx, text in enumerate(texts)]
        else:
            self.notify("I'm being cancelled")
            return

    @on(Worker.StateChanged)
    def load_options(self, event: Worker.StateChanged) -> None:
        match event.state:
            case WorkerState.PENDING:
                self.loading = True
                self.clear_options()
            case WorkerState.SUCCESS:
                assert isinstance(event.worker.result, list)
                self.add_options(event.worker.result)
                self.loading = False


class SlowLoadingApp(App[None]):
    CSS = """
        CustomSelectionList {
            height: 1fr;
        }
    """

    def compose(self) -> ComposeResult:
        yield CustomSelectionList()
        with HorizontalGroup():
            yield Button("Reload", id="reload", variant="primary")
            yield Button("Press me", id="pressme")

    def on_mount(self) -> None:
        self.query_one(CustomSelectionList).scan_and_mount()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        match event.button.id:
            case "reload":
                self.query_one(CustomSelectionList).scan_and_mount()
            case "pressme":
                self.notify("I'm still responsive")


SlowLoadingApp().run()
