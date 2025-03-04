import logging

from textual import work
from textual.app import App, ComposeResult
from textual.widgets import Log

from long_running_process import perform_work


class LogStream:
    def write(self, text: str) -> None:
        print(text)


class LongRunningUI(App):
    CSS = """
        Log {
            border: solid $primary;
        }
    """

    def compose(self) -> ComposeResult:
        yield Log()

    def on_mount(self) -> None:
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler(self.query_one(Log))
        handler.setFormatter(
            logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        )
        logger.addHandler(handler)

        self.perform_work()

    @work(thread=True)
    def perform_work(self) -> None:
        perform_work()


if __name__ == "__main__":
    LongRunningUI().run()
