from textual import on
from textual.app import App, ComposeResult
from textual.widgets import Input, RadioButton, RadioSet


class RadioApp(App[None]):
    CSS = """
        .error {
            border: tall $error;
        }
    """

    def compose(self) -> ComposeResult:
        with RadioSet(id="radio_group"):
            yield RadioButton("Some option")
            yield RadioButton("Disable input", id="radiobutton_disable_input")
            yield RadioButton("Unrelated option")
        yield Input()

    @on(RadioSet.Changed, "#radio_group")
    def disable_input(self, event: RadioSet.Changed) -> None:
        if event.pressed.id == "radiobutton_disable_input":
            (input := self.query_one(Input)).disabled = True
            input.add_class("error")
        else:
            (input := self.query_one(Input)).disabled = False
            input.remove_class("error")


RadioApp().run()
