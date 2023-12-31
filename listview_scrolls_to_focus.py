from textual.app import App, ComposeResult
from textual.widgets import ListItem, ListView, Static


class ListViewScrollApp(App[None]):
    BINDINGS = [("h", "scroll()", "Home")]
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

    def on_mount(self) -> None:
        self.screen.scroll_to_widget(self.query_one("#banner"))

    def action_scroll(self) -> None:
        # self.screen.scroll_home()
        self.screen.scroll_to_widget(self.query_one("#banner"))

    def on_list_view_highlighted(self, event: ListView.Highlighted) -> None:
        self.screen.scroll_to_widget(event.item)


if __name__ == "__main__":
    ListViewScrollApp().run()
