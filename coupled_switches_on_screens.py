from textual import on
from textual.app import App, ComposeResult
from textual.message import Message
from textual.screen import Screen
from textual.widgets import Footer, Header, Switch


class MasterScreen(Screen):
    TITLE = "Master Screen"

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield Switch(value=False, id="master-switch")


class SlaveScreen(Screen):
    class MasterSwitchChanged(Message):
        def __init__(self, value: bool) -> None:
            super().__init__()
            self.value = value

    TITLE = "Slave Screen"

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield Switch(value=False, id="slave-switch")

    @on(MasterSwitchChanged)
    def set_slave_from_master(self, event: MasterSwitchChanged) -> None:
        self.query_one("#slave-switch").value = event.value


class CoupledSwitchesApp(App[None]):
    CSS = """
        Screen {
            align: center top;
        }
    """
    SCREENS = {"master": MasterScreen(), "slave": SlaveScreen()}

    BINDINGS = [
        ("m", "app.switch_screen('master')", "Switch to Master"),
        ("s", "app.switch_screen('slave')", "Switch to Slave"),
        ("q", "quit", "Quit"),
    ]

    def on_mount(self) -> None:
        self.push_screen("master")

    @on(Switch.Changed, "#master-switch")
    def store_master_switch_value(self, event: Switch.Changed) -> None:
        self.SCREENS["slave"].post_message(
            SlaveScreen.MasterSwitchChanged(value=event.value)
        )


CoupledSwitchesApp().run()
