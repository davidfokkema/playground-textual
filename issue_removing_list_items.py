import hashlib

import rich
from textual import on, work
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.message import Message
from textual.widgets import Footer, Header, Label, ListItem, ListView


class MyListItem(ListItem):
    def __init__(self, my_item_name: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.my_item_name = my_item_name

    def compose(self) -> ComposeResult:
        yield Label(self.my_item_name)


class MyListItemList(ListView):
    BINDINGS = [
        ("r", "reload", "Reload"),
        ("a", "add", "Add"),
        ("r", "remove", "Remove"),
    ]
    idx = 0

    class MyListItemMessage(Message):
        __slots__ = ["my_item_name"]

        def __init__(self, name: str) -> None:
            super().__init__()
            self.my_item_name = name

        def __rich_repr__(self) -> rich.repr.Result:
            yield "my_item_name", self.my_item_name

    class NewMyListItem(MyListItemMessage):
        """New MyListItem found."""

    class RemovedMyListItem(MyListItemMessage):
        """MyListItem must be removed."""

    def action_add(self) -> None:
        self.idx += 1
        self._last_name = f"foo_{self.idx}"
        self.add_MyListItem(MyListItemList.NewMyListItem(self._last_name))

    def action_remove(self) -> None:
        self.remove_MyListItem(MyListItemList.RemovedMyListItem(self._last_name))

    @on(NewMyListItem)
    def add_MyListItem(self, event: NewMyListItem) -> None:
        self.append(MyListItem(event.my_item_name, id=event.my_item_name))

    @on(RemovedMyListItem)
    def remove_MyListItem(self, event: RemovedMyListItem) -> None:
        print(f"REMOVING {event}")
        widget = self.query_one("#" + event.my_item_name)
        print(f"REMOVING WIDGET {widget}")
        widget.remove()

    @on(ListView.Selected)
    @work()
    async def fix_MyListItem_name(self, event: ListView.Selected) -> None:
        self.post_message(self.RemovedMyListItem(event.item.my_item_name))

    async def action_reload(self) -> None:
        self.clear()
        self.idx = 0


class FixCanonNameApp(App[None]):
    BINDINGS = [Binding("q", "quit", "Quit", priority=True)]

    CSS = """
        MyListItem {
            padding: 1 2;
        }

        PinCodeScreen {
            align: center middle;

            & Input {
                max-width: 40;
            }
        }
    """

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield MyListItemList()

    def action_quit(self) -> None:
        self.exit()


app = FixCanonNameApp()


def main():
    app.run()


if __name__ == "__main__":
    main()
