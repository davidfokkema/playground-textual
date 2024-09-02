from textual import work
from textual.app import App
from textual.widgets import Footer, Header, TabbedContent, TabPane


class MyTabPane(TabPane):
    def __init__(self):
        super().__init__("table")
        self.data = [1] * 10_000_000


class Explorer(App):
    BINDINGS = [
        ("ctrl+o", "add_table", "add table"),
    ]

    def __init__(self):
        super().__init__()

    def compose(self):
        yield Header(show_clock=False)
        yield TabbedContent()
        yield Footer()

    @work
    async def action_add_table(self):
        tabs = self.query_one(TabbedContent)
        tabs.loading = True
        for tab in tabs.query(MyTabPane):
            # this deletes the data in the tab panes
            del tab.data
        await tabs.clear_panes()
        await tabs.add_pane(MyTabPane())
        tabs.loading = False


if __name__ == "__main__":
    app = Explorer()
    app.run()
