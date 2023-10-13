import random

from textual import on
from textual.app import App, ComposeResult
from textual.events import Mount
from textual.screen import Screen
from textual.reactive import var
from textual.widgets import Label, ListItem, ListView


class FlashCards(Screen):

    CSS = """
    .good {
        background: $success;
    }
    """

    counter: var[int] = var(0)
    confirming: var[bool] = var(False)

    def compose(self) -> ComposeResult:
        yield Label(id="counter")
        yield ListView()

    def watch_counter(self) -> None:
        self.query_one("#counter", Label).update(str(self.counter))

    def new_card(self) -> list[ListItem]:
        return [
            ListItem(Label(text)) for
            text in random.sample(("one", "two", "three", "four"), k=4)
        ]

    @on(Mount)
    async def next_card(self) -> None:
        self.confirming = False
        self.counter += 1
        card = self.query_one(ListView)
        await card.clear()
        await card.extend(self.new_card())

    @on(ListView.Selected)
    def chosen(self, event: ListView.Selected) -> None:
        if not self.confirming:
            self.confirming = True
            event.item.add_class("good")
            self.set_timer(5.0, self.next_card)

class FlashCardApp(App[None]):

    def on_mount(self) -> None:
        self.push_screen(FlashCards())

if __name__ == "__main__":
    FlashCardApp().run()
