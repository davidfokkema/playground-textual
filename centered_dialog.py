from textual.app import App, ComposeResult
from textual.containers import Center, Horizontal, Vertical
from textual.widgets import Button, Label


class CenteredDialogApp(App[None]):
    CSS = """
        Screen {
            align: center middle;
        }

        Horizontal, Vertical {
            width: auto;
            height: auto;
        }

        Center {
            width: 100%;
        }
    """

    def compose(self) -> ComposeResult:
        with Vertical():
            with Center():
                yield Label("¿Exit without save?", id="message")
            with Horizontal():
                yield Button.success("Accept", id="accept")
                yield Button.error("Cancel", id="cancel")


CenteredDialogApp().run()
