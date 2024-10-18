from textual.app import App, ComposeResult
from textual.containers import ScrollableContainer, Vertical
from textual.widgets import Markdown, Static, TabbedContent, TabPane


class NothingToShow(Vertical):
    def __init__(self, action_name: str) -> None:
        super().__init__()
        self.action_name = action_name

    def compose(self) -> ComposeResult:
        yield Static("Noting to show!")
        yield Static(
            f"[b]To generate [i]expressions[/i] go to [@click={self.action_name}]Terms[/][/b]"
        )


class MyApp(App):
    def compose(self) -> ComposeResult:
        with TabbedContent():
            with TabPane("Leto", id="leto"):
                yield Markdown("LETO")
            with TabPane("Jessica", id="jessica"):
                yield Markdown("JESSICA")
            with TabPane("Paul", id="paul"):
                yield Markdown("PAUL")
            with TabPane("Terms", id="terms"):
                yield Markdown("Terms and Conditions")
        with ScrollableContainer(id="exp-body"):
            yield NothingToShow("app.go_to_terms")

    def action_go_to_terms(self) -> None:
        self.notify("Hello")
        self.query_exactly_one(TabbedContent).active = "terms"


MyApp().run()
