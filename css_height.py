import asyncio

from textual import work
from textual.app import App, ComposeResult
from textual.widgets import (
    DataTable,
    Footer,
    Header,
    Log,
    Static,
    TabbedContent,
    TabPane,
)
from textual.worker import Worker, WorkerState
from typing_extensions import override


class SubTabContent(Static):
    @override
    def compose(self) -> ComposeResult:
        yield DataTable()
        yield Log()

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns(
            "Col 1",
            "Col 2",
            "Col 3",
        )

        self.set_interval(1, self._run_command)

    @work(exclusive=True)
    async def _run_command(self) -> None:
        table = self.query_one(DataTable)

        table.add_row(
            "cell 1",
            "cell 2",
            "cell 3",
        )
        table.action_scroll_bottom()

    def on_worker_state_changed(self, event: Worker.StateChanged) -> None:
        log = self.query_one(Log)
        if event.state == WorkerState.PENDING:
            log.clear()
        log.write_line(f"Worker state changed: {event.state}")


class SubTabs(Static):
    @override
    def compose(self) -> ComposeResult:
        with TabbedContent():
            with TabPane("Sub Tab 1"):
                yield SubTabContent()
            with TabPane("Sub Tab 2"):
                yield SubTabContent()
            with TabPane("Sub Tab 3"):
                yield SubTabContent()


class MainTabs(Static):
    @override
    def compose(self) -> ComposeResult:
        with TabbedContent():
            with TabPane("Tab 1"):
                yield SubTabs()
            with TabPane("Tab 2"):
                yield SubTabs()
            with TabPane("Tab 3"):
                yield SubTabs()


class MyApp(App[None]):
    CSS = """
        SubTabContent {
            border: solid $primary;
            height: 1fr;
        }

        DataTable {
            border: solid $secondary;
            max-height: 75%;
        }
        Log {
            border: solid $secondary;
            min-height: 25%;
        }
    """

    @override
    def compose(self) -> ComposeResult:
        yield Header()
        yield MainTabs()
        yield Footer()


if __name__ == "__main__":
    app = MyApp()
    app.run()
