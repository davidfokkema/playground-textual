from textual import on
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal
from textual.events import Show
from textual.reactive import reactive
from textual.widgets import Button, Label


class AnimalLabel(Container):
    animal: reactive[str | None] = reactive(None, recompose=True)

    def compose(self) -> ComposeResult:
        if self.animal is None:
            yield Label("No animal selected")
        else:
            with Horizontal(id="animal-display"):
                yield Label(f"Animal: {self.animal}")
                yield Button("Reset", variant="warning", id="reset-button")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "reset-button":
            self.animal = None


class ReactiveRecomposeApp(App[None]):
    CSS = """
        Button {
            margin: 1 2;
        }

        AnimalLabel {
            height: auto;

            & #animal-display {
                height: auto;
            }
        }
    """

    def compose(self) -> ComposeResult:
        yield AnimalLabel()
        with Horizontal():
            yield Button("Dog person", id="animal-dog-button")
            yield Button("Cat person", id="animal-cat-button")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id.startswith("animal-"):
            animal = event.button.id.split("-")[1]
            self.query_one(AnimalLabel).animal = animal


ReactiveRecomposeApp().run()
