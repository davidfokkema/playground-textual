from threading import Condition

from textual import on, work
from textual.app import App, ComposeResult
from textual.containers import Center, Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Label
from textual.worker import Worker, WorkerState


class ConfirmationDialog(ModalScreen):
    def compose(self) -> ComposeResult:
        with Horizontal():
            yield Button("Yes", id="yes")
            yield Button("No", id="no")

    @on(Button.Pressed)
    def confirm(self, event: Button.Pressed) -> None:
        if event.button.id == "yes":
            self.dismiss(True)
        else:
            self.dismiss(False)
        print("DONE")


class ConfirmApp(App):
    CSS = """
        Screen, ConfirmationDialog {
            align: center middle;
        }

        Screen > Vertical {
            width: auto;
            height: auto;
        }

        ConfirmationDialog > Horizontal {
            width: auto;
            height: auto;
        }

        #my_button .success {
            border: solid green;
        }
    """

    def compose(self) -> ComposeResult:
        with Vertical():
            with Center():
                yield Label("Click to start the action!")
            with Center():
                yield Button("Click", id="mybutton")

    @on(Button.Pressed)
    def confirm(self):
        self.run_task()

    @on(Worker.StateChanged)
    def worker_state(self, event: Worker.StateChanged) -> None:
        if event.state == WorkerState.SUCCESS:
            print("SUCCESS")

    @work(thread=True)
    def run_task(self):
        confirmed = Condition()
        confirmation = None

        def callback(value: bool) -> None:
            nonlocal confirmation
            with confirmed:
                confirmation = value
                confirmed.notify()

        self.call_from_thread(self.push_screen, ConfirmationDialog(), callback)

        print("WAITING...")
        with confirmed:
            confirmed.wait()
            print(f"Confirmation is {confirmation}")
            if confirmation is True:
                print("Clicked YES")
            elif confirmation is False:
                print("Clicked NO")
            else:
                print("WTF?")


if __name__ == "__main__":
    app = ConfirmApp()
    app.run()
