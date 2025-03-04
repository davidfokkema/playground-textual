from functools import partial

from textual import work
from textual.app import App, ComposeResult
from textual.widgets import Log

from long_running_process_with_print import perform_work


class LongRunningUI(App):
    CSS = """
        Log {
            border: solid $primary;
        }
    """

    def compose(self) -> ComposeResult:
        yield Log()

    def on_mount(self) -> None:
        self.perform_work()

    @work(thread=True)
    def perform_work(self) -> None:
        perform_work(partial(self.call_from_thread, self.write_to_log))

    def write_to_log(self, text: str) -> None:
        self.query_one(Log).write_line(text)


if __name__ == "__main__":
    LongRunningUI().run()
