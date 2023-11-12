from textual.app import App, ComposeResult
from textual.widgets import ListItem, ListView, Static


class ListViewScrollApp(App[None]):
    CSS = """
        #banner {
            text-align: center;
            text-style: bold;
            padding: 1 2;
        }

        ListView {
            height: auto;
        }

        ListItem {
            padding: 1 2;
        }
    """

    def compose(self) -> ComposeResult:
        yield Static("ACME Scrolling Test!", id="banner")
        items = [ListItem(Static(f"Item {i}")) for i in range(1, 21)]
        yield ListView(*items)


if __name__ == "__main__":
    ListViewScrollApp().run()
