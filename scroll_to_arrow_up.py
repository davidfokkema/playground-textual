from textual import on
from textual.app import App, ComposeResult
from textual.events import MouseScrollDown, MouseScrollUp
from textual.widgets import Footer, Label, ListItem, ListView


class MyListView(ListView):
    @on(MouseScrollUp)
    def move_up(self) -> None:
        self.action_cursor_up()

    @on(MouseScrollDown)
    def move_down(self) -> None:
        self.action_cursor_down()


class ListViewExample(App):
    CSS = """
        Screen {
            align: center middle;
        }

        ListView {
            width: 30;
            height: auto;
            margin: 2 2;
        }

        Label {
            padding: 1 2;
        }
    """

    def compose(self) -> ComposeResult:
        yield MyListView(
            *[ListItem(Label(f"Item {idx}")) for idx in range(10)],
        )
        yield Footer()


if __name__ == "__main__":
    app = ListViewExample()
    app.run()
