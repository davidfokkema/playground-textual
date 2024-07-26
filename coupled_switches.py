from textual.app import App, ComposeResult
from textual.widgets import Switch


class CoupledSwitchesApp(App[None]):
    def compose(self) -> ComposeResult:
        yield Switch(value=True, id="switch-0")
        yield Switch(value=True, id="switch-1")

    def on_switch_changed(self, event: Switch.Changed) -> None:
        if event.switch.id == "switch-0":
            self.query_one("#switch-1").value = event.value


CoupledSwitchesApp().run()
