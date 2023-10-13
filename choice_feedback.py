import asyncio
import random

from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widgets import Label, ListItem, ListView


class MyScreen(Screen):
    # class ChoiceFeedbackApp(App[None]):
    CSS = """   
        .feedback {background: $success;}
    """

    N = 0

    def compose(self) -> ComposeResult:
        yield Label(f"{self.N=}", id="counter")
        yield ListView()

    def on_mount(self) -> None:
        self.next_items()

    def next_items(self) -> None:
        self.N += 1
        self.query_one("#counter").update(f"{self.N=}")
        list_view = self.query_one("ListView")
        list_view.clear()
        list_view.extend(self.create_items())

    def create_items(self) -> list[ListItem]:
        return [
            ListItem(Label(text))
            for text in random.sample(["one", "two", "three", "four"], k=4)
        ]

    async def on_list_view_selected(self, event: ListView.Selected) -> None:
        with event.control.prevent(ListView.Selected):
            event.item.add_class("feedback")
            # self.refresh_css()
            self.app.refresh_css()
            await asyncio.sleep(1)
            self.next_items()


class ChoiceFeedbackApp(App[None]):
    def on_mount(self):
        self.push_screen(MyScreen())


if __name__ == "__main__":
    ChoiceFeedbackApp().run()
