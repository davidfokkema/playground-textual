from textual.app import App, ComposeResult
from textual.widgets import Label, Select


class MinimalApp(App[None]):
    CSS = """
        Select {
            width: 40;

            &:focus > SelectCurrent {
                border: tall yellow;
            }

            &.-expanded > SelectCurrent {
                border: round $secondary;
            }
        }
    """

    def compose(self) -> ComposeResult:
        yield Select.from_values(
            ["Option 1", "Option 2", "Option 3"], prompt="Select 1"
        )
        yield Select.from_values(
            ["Option 1", "Option 2", "Option 3"], prompt="Select 2"
        )
        yield Label()

    def on_mount(self) -> None:
        self.query_one(Label).update(self.query_one(Select).DEFAULT_CSS)
        self.log(self.css_tree)


MinimalApp().run()
