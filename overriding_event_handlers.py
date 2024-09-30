from textual import on
from textual.app import App, ComposeResult
from textual.widgets import Button


class FancyButton(Button):
    @on(Button.Pressed)
    def first_method(self, event: Button.Pressed) -> None:
        self.notify("First method.")

    @on(Button.Pressed)
    def second_method(self, event: Button.Pressed) -> None:
        self.notify("Second method.")


class FancierButton(FancyButton):
    @on(Button.Pressed)
    def second_method(self, event: Button.Pressed) -> None:
        event.prevent_default()
        self.notify("Fancier second method")


class MyApp(App[None]):
    def compose(self) -> ComposeResult:
        yield FancyButton("Fancy")
        yield FancierButton("Even fancier")


MyApp().run()
