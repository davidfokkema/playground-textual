from textual.app import App, ComposeResult
from textual.widgets import Button, Footer, Header, SelectionList


class SelectionListApp(App[None]):
    CSS = """
        Screen {
            align: center middle;
        }

        SelectionList {
            padding: 1;
            border: solid $accent;
            width: 80%;
            height: 80%;
        }

        SelectionList {
            & > .option-list--option-highlighted {
                background: $surface;
                text-style: none;
            }

            & :focus {
                & > .option-list--option-highlighted {
                    background-tint: $foreground 5%;
                }
            }   
        }
    """

    def compose(self) -> ComposeResult:
        yield Header()
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
        yield Footer()
        yield Button("Don't press")

    def on_mount(self) -> None:
        self.query_one(SelectionList).border_title = "Shall we play some games?"
        for class_ in SelectionList.__mro__:
            if css := getattr(class_, "DEFAULT_CSS", None):
                self.log(css)


if __name__ == "__main__":
    SelectionListApp().run()
