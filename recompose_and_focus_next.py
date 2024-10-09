import itertools

from textual.app import App, ComposeResult
from textual.reactive import reactive
from textual.widgets import Input, Label


class MyApp(App[None]):
    some_reactive = reactive(dict[str, str], recompose=True)
    label_text = itertools.cycle(["Something", "Something else"])
    current_text = None

    def compose(self) -> ComposeResult:
        self.current_text = next(self.label_text)
        yield Label(
            f"{self.current_text}, previous value: {self.some_reactive.get(self.current_text)}"
        )
        yield Input(id="my-input-field")

    def on_input_submitted(self, event: Input.Submitted) -> None:
        self.some_reactive[self.current_text] = event.value
        self.call_later(self.focus_input)
        self.mutate_reactive(MyApp.some_reactive)

    def focus_input(self) -> None:
        self.query_one("#my-input-field").focus()


MyApp().run()
