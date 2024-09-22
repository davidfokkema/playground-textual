from textual import on
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Label, Switch


class SwitchesScreen(Screen):
    app: "MyApp"

    CSS = """
        #switches {
            & Horizontal {
                height: auto;
            }

            & Label {
                padding: 1 2;
                width: 20;
            }
        }
    """

    def compose(self) -> ComposeResult:
        with Vertical(id="switches"):
            with Horizontal():
                yield Label("Use numbers:")
                yield Switch(id="use_numbers")
            with Horizontal():
                yield Label("Use symbols:")
                yield Switch(id="use_symbols")

    def on_mount(self) -> None:
        for setting, value in self.app.settings.items():
            self.query_one(f"#{setting}", Switch).value = value

    @on(Switch.Changed)
    def change_setting(self, event: Switch.Changed) -> None:
        self.app.settings[event.switch.id] = event.value


class MyApp(App[None]):
    SCREENS = {"switches": SwitchesScreen}

    def __init__(self, settings: dict[str, bool]) -> None:
        super().__init__()
        self.settings = settings

    def on_mount(self) -> None:
        self.push_screen("switches")


app = MyApp(settings={"use_numbers": True, "use_symbols": False})
app.run()

print("Current settings:")
print(app.settings)
