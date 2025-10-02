from textual import on
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Label


class AutoClosingPopup(ModalScreen[bool]):
    def __init__(
        self, message: str, timeout: float | None = None, *args, **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self.message = message
        self.timeout = timeout

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Label(self.message)
            with Horizontal():
                yield Button(f"Yes [{self.timeout}]", id="yes")
                yield Button("No", id="no")

    def on_mount(self) -> None:
        if self.timeout is not None:
            self.set_interval(1.0, self.decrement_timeout)

    def decrement_timeout(self) -> None:
        assert self.timeout is not None
        self.timeout -= 1
        yes_button = self.query_one("#yes", Button)
        if self.timeout > 0:
            yes_button.label = f"Yes [{self.timeout}]"
        else:
            self.dismiss(True)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "yes":
            self.dismiss(True)
        else:
            self.dismiss(False)


class PopupApp(App[None]):
    def compose(self) -> ComposeResult:
        yield Button("Confirm", id="confirm")

    @on(Button.Pressed, "#confirm")
    def ask_confirmation(self) -> None:
        def callback(result: bool | None) -> None:
            self.notify(f"User selected: {'Yes' if result else 'No'}")

        self.push_screen(
            AutoClosingPopup("Are you sure?", timeout=3.0), callback=callback
        )


PopupApp().run()
