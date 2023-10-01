from textual import on
from textual.app import App, ComposeResult
from textual.widgets import ListView, ListItem, Label

class ArrowItem(ListItem):

    DEFAULT_CSS = """
    ArrowItem {
        layout: horizontal;
    }

    ArrowItem .chevron {
        visibility: hidden;
    }

    ArrowItem.--highlight .chevron {
        visibility: visible;
    }
    """

    def __init__(self, text: str, id: str) -> None:
        super().__init__(id=id)
        self._text = text

    def compose(self) -> ComposeResult:
        yield Label("> ", classes="chevron")
        yield Label(self._text)
        yield Label(" <", classes="chevron")

class ListViewMessageExampleApp(App[None]):

    def compose(self) -> ComposeResult:
        yield Label("Chosen item will appear here", id="chosen")
        yield ListView(
            ArrowItem("Mal", id="mal"),
            ArrowItem("Zoe", id="zoe"),
            ArrowItem("Wash", id="wash"),
            ArrowItem("Jayne", id="jayne"),
            ArrowItem("Book", id="book"),
            ArrowItem("Simon", id="simon"),
            ArrowItem("River", id="river"),
        )

    @on(ListView.Selected)
    def show_chosen(self, event: ListView.Selected) -> None:
        self.query_one("#chosen", Label).update(f"{event.item}")

if __name__ == "__main__":
    ListViewMessageExampleApp().run()
