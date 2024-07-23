from textual.app import App, ComposeResult
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Label


class L3(Widget):
    animal_sound = reactive("Meow")

    def compose(self) -> ComposeResult:
        yield Label(id="label3")

    def watch_animal_sound(self, value: str) -> None:
        self.query_one("#label3").update(self.animal_sound * 3)


class L2(Widget):
    animal_sound = reactive("Woof")

    def compose(self) -> ComposeResult:
        yield Label(id="label2")
        yield L3().data_bind(L2.animal_sound)

    def watch_animal_sound(self, value: str) -> None:
        self.query_one("#label2").update(self.animal_sound * 2)


class MainApp(App):
    animal_sound = reactive("Meh")

    def compose(self) -> ComposeResult:
        yield L2().data_bind(MainApp.animal_sound)


MainApp().run()
