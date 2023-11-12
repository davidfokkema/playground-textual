from textual.app import App, ComposeResult
from textual.widgets import ListItem, ListView, Static


class ListViewScrollApp(App[None]):
    CSS = """
        ListItem {
            padding: 1 2;
        }
    """

    def compose(self) -> ComposeResult:
        items = [ListItem(Static(f"Item {i}")) for i in range(1, 21)]
        yield ListView(*items)


if __name__ == "__main__":
    ListViewScrollApp().run()
