from rich.text import Text
from textual.app import App, ComposeResult
from textual.widgets import Button, SelectionList
from textual.widgets.selection_list import Selection


class MyApp(App):
    def compose(self) -> ComposeResult:
        self.selections = [
            Selection(Text("one", style="bold green"), 1),
            Selection("two", 2),
        ]
        yield SelectionList(*self.selections)
        yield Button("Update Text", id="update")
        yield Button("Disable One", id="disable_one")
        yield Button("Disable Two", id="disable_two")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        selection_one = self.selections[0]
        selection_two = self.selections[1]
        button_id = event.button.id

        if button_id == "update":
            selection_one.set_prompt("new value")
        elif button_id == "disabled_one":
            selection_one.disabled = not selection_one.disabled
        elif button_id == "disable_two":
            selection_two.disabled = not selection_two.disabled


MyApp().run()
