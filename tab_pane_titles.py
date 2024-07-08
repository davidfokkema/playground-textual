from textual.app import App, ComposeResult
from textual.widgets import Label, TabbedContent, TabPane


class MyApp(App[None]):
    def compose(self) -> ComposeResult:
        with TabbedContent():
            with TabPane("Leto", id="tab-leto"):
                yield Label("Leto")
            with TabPane("Jessica"):
                yield Label("Jessica")
            with TabPane("Paul"):
                yield Label("Paul")

    def on_mount(self) -> None:
        tab: TabPane = self.query_one(TabbedContent).get_tab("tab-leto")
        tab.label = "Duke of Atreides"


MyApp().run()
