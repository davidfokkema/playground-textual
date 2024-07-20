import asyncio

from textual import on, work
from textual.app import App, ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Button, OptionList


class ItemGroup(VerticalScroll):
    def compose(self) -> ComposeResult:
        yield OptionList()

    def on_mount(self) -> None:
        option_list = self.query_one(OptionList)
        self.add_items(option_list)

    @work
    async def add_items(self, option_list: OptionList) -> None:
        s = 0
        for i in range(1_000_000):
            option_list.add_option(f"Item {s}")
            option_list.scroll_end()
            await asyncio.sleep(0.01)
            s += i


class TestApp(App[None]):
    def compose(self) -> ComposeResult:
        yield Button("Call again")
        yield ItemGroup()

    @on(Button.Pressed)
    def renew_option_list(self) -> None:
        self.query_one(ItemGroup).remove()
        self.mount(ItemGroup())


if __name__ == "__main__":
    TestApp().run()
