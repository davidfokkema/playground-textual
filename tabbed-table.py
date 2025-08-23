from textual.app import App, ComposeResult
from textual.widgets import Button, DataTable, Footer, Static, TabbedContent, TabPane


class TabbedTableApp(App):
    BINDINGS = [
        ("1", "switch_tab('tab1')", "Switch to Tab 1"),
        ("2", "switch_tab('tab2')", "Switch to Tab 2"),
    ]
    CSS = """
        DataTable {
            height: 1fr; # comment out this line and it works fine
        }
    """

    def compose(self) -> ComposeResult:
        yield Footer()
        with TabbedContent(initial="tab1"):
            with TabPane("Tab 1", id="tab1"):
                yield DataTable()  # comment out this line and it works fine
                yield Button("Switch")  # comment out this line and it works fine
            with TabPane("Tab 2", id="tab2"):
                yield Static("Hi there")

    def action_switch_tab(self, tab_id: str) -> None:
        self.query_one(TabbedContent).active = tab_id


if __name__ == "__main__":
    app = TabbedTableApp()
    app.run()
