from textual import on
from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.screen import Screen
from textual.widgets import Button, Label


class ChoiceScreen(Screen):
    def compose(self) -> ComposeResult:
        with Horizontal():
            yield Button("Screen A", id="choose-A")
            yield Button("Screen B", id="choose-B")

    @on(Button.Pressed)
    def return_choice(self, event: Button.Pressed) -> None:
        self.dismiss(event.button.id)


class ScreenA(Screen):
    def compose(self) -> ComposeResult:
        yield Label("Thank you for choosing option A")


class ScreenB(Screen):
    def compose(self) -> ComposeResult:
        yield Label("Thank you for choosing option B")


class ChoiceApp(App[None]):
    def on_mount(self) -> None:
        def process_choice(choice_id: str) -> None:
            if choice_id == "choose-A":
                self.push_screen(ScreenA())
            else:
                self.push_screen(ScreenB())

        self.push_screen(ChoiceScreen(), callback=process_choice)


ChoiceApp().run()
