import asyncio

from textual import work
from textual.app import App, ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import LoadingIndicator, Placeholder


class MinimalApp(App[None]):
    CSS = """
        Placeholder, LoadingIndicator {
            height: 5;
        }
    """

    def compose(self) -> ComposeResult:
        with VerticalScroll(id="widget_list"):
            yield LoadingIndicator(id="loading_widgets")

    def on_mount(self) -> None:
        self.load_slow_widgets()

    @work
    async def load_slow_widgets(self) -> None:
        for _ in range(20):
            await self.query_one("#widget_list").mount(
                Placeholder(), before="#loading_widgets"
            )
            self.query_one("#loading_widgets").scroll_visible()
            await asyncio.sleep(0.4)
        self.query_one("#loading_widgets").remove()


MinimalApp().run()
