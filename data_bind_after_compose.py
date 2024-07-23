from textual import on
from textual.app import App, ComposeResult
from textual.message import Message
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Button, Label


class L3(Widget):
    animal_sound = reactive("Meow")

    def compose(self) -> ComposeResult:
        yield Label(id="label3")

    def watch_animal_sound(self, value: str) -> None:
        self.query_one("#label3").update(self.animal_sound * 3)


class L2(Widget):
    class MountAnimalWidget(Message):
        def __init__(self, widget: Widget) -> None:
            super().__init__()
            self.widget = widget

    animal_sound = reactive("Woof")

    def compose(self) -> ComposeResult:
        yield Label(id="label2")

    def watch_animal_sound(self, value: str) -> None:
        self.query_one("#label2").update(self.animal_sound * 2)

    @on(MountAnimalWidget)
    def mount_animal_widget(self, event: MountAnimalWidget) -> None:
        self.mount(event.widget.data_bind(L2.animal_sound))


class MainApp(App):
    CSS = """
        Widget {
            height: auto;
        }
    """
    animal_sound = reactive("Meh")

    def compose(self) -> ComposeResult:
        yield L2().data_bind(MainApp.animal_sound)
        yield Button("Mount L3")

    def on_button_pressed(self) -> None:
        self.query_one(L2).post_message(L2.MountAnimalWidget(L3()))


MainApp().run()
