from textual.app import App, ComposeResult
from textual.widgets import Label

TEXT = "A quick brown [dark_goldenrod]fox[/] jumps over the lazy dog."


class HatchLabelApp(App[None]):
    CSS = """
        Screen {
            align: center middle;
        }

        Label {
            hatch: horizontal white;
        }
    """

    def compose(self) -> ComposeResult:
        # replace space with non-breaking space to prevent the hatched
        # background from showing through.
        yield Label(TEXT.replace(" ", " "))
        yield Label(TEXT)


HatchLabelApp().run()
