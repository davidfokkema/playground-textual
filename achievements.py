from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Footer, Header, Label


class AchievementsBoard(App[None]):
    CSS = """
        Screen {
            align: center middle;
            hatch: right $secondary-background;
        }

        Horizontal, Vertical {
            width: auto;
            height: auto;
        }

        #panel {
            border: round $primary;
            background: $surface;
            padding: 1 2;

            #achievements {
                margin: 1 0;

                .medal {
                    width: 2;
                }
            }
        }
    """

    def compose(self) -> ComposeResult:
        yield Header(icon="🥇")
        yield Footer()
        with Vertical(id="panel"):
            yield Label(
                "Hi [bold]Codey McBugface[/bold], you've done well!\nHere are your achievements:"
            )
            achievements = "🥇🥇◌🥇🥇◌🥇🥇◌◌◌◌"
            with Horizontal(id="achievements"):
                for c in achievements:
                    yield Label(c, classes="medal")
            yield Label("[italic]Write some code[/italic] and earn even more!")


AchievementsBoard().run()
