from textual.app import App, ComposeResult
from textual.widgets import Checkbox


class StyledCheckboxApp(App[None]):
    CSS = """
        Screen {
            align: center middle;
        }

        Checkbox {
            background: green;
        }
        # Checkbox > .toggle--button {
        #     color: blue;
        # }

        Checkbox.-on > .toggle--button {
            color: red;
        }
    """

    def compose(self) -> ComposeResult:
        yield Checkbox("You can style me")


StyledCheckboxApp().run()
