from textual.app import App, ComposeResult
from textual.widgets import Footer, Label, SelectionList, TabbedContent, TabPane, Tabs


class SampleApp(App):
    BINDINGS = [
        ("a", "previous_tab", "change left"),
        ("d", "next_tab", "change right"),
    ]

    def compose(self) -> ComposeResult:
        yield Footer()
        with TabbedContent(id="main") as t:
            with TabPane("random", id="random-tab"):
                yield Label("Some tab content 1")
            with TabPane("random1", id="random2-tab"):
                yield Label("Some tab content 2")
            with TabPane("random", id="random3-tab"):
                yield Label("Some tab content 3")
        yield SelectionList[int](
            ("Falken's Maze", 0, True),
            ("Black Jack", 1),
            ("Gin Rummy", 2),
            ("Hearts", 3),
            ("Bridge", 4),
            ("Checkers", 5),
            ("Chess", 6, True),
            ("Poker", 7),
            ("Fighter Combat", 8, True),
        )

    def action_next_tab(self) -> None:
        self.query_one(Tabs).action_next_tab()

    def action_previous_tab(self) -> None:
        self.query_one(Tabs).action_previous_tab()


SampleApp().run()
