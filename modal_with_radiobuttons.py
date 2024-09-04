from textual.app import App, ComposeResult
from textual.containers import Grid, Horizontal, Vertical
from textual.widgets import Button, Input, Label, RadioButton, RadioSet


class RadioGridApp(App[None]):
    CSS = """
        Screen {
            align: center middle;

            & Horizontal, Vertical {
                height: auto;
            }

            & #header-text {
                text-align: center;
                text-style: bold;
                width: 100%;
                padding: 1 2;
            }

            & #container {
                width: 80%;
                border: solid $secondary;
            }

            & RadioSet {
                layout: horizontal;
                & RadioButton {
                    width: 1fr;
                }
            }

            & #buttons {
                & Button {
                    width: 1fr;
                    margin: 1 2;
                }
            }
        }
    """

    def compose(self) -> ComposeResult:
        with Vertical(id="container"):
            yield Label("Enter workload or select PID", id="header-text")
            with RadioSet():
                yield RadioButton("Enter workload")
                yield RadioButton("Select PID")
            with Horizontal(id="inputs"):
                with Vertical():
                    yield Input()
                    yield Input()
                    yield Input()
                    yield Input()
                with Vertical():
                    yield Input()
            with Horizontal(id="buttons"):
                yield Button("Save", variant="primary")
                yield Button("Cancel", variant="error")


RadioGridApp().run()
