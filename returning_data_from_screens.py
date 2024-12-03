from textual import on, work
from textual.app import App, ComposeResult
from textual.containers import Grid, Horizontal, Vertical
from textual.screen import ModalScreen, Screen
from textual.widgets import Button, Input, Label


class LoginScreen(Screen):
    DEFAULT_CSS = """
        LoginScreen {
            align: center middle;
            hatch: right $primary-background;
        
            & Grid {
                border: round $secondary;
                background: $panel;
                padding: 1 2;
                height: auto;
                width: auto;
                grid-size: 2 2;
                grid-columns: auto 40;
                grid-rows: auto;
                grid-gutter: 1;

                & Label {
                    height: 3;
                    width: 100%;
                    content-align: left middle;
                }
            }
        }
    """
    attempts = 0

    def compose(self) -> ComposeResult:
        with Grid():
            yield Label("Username:")
            yield Input(id="username")
            yield Label("Password:")
            yield Input(id="password", password=True)
        yield Label(id="failed")

    @on(Input.Submitted, "#password")
    def check_auth(self, event: Input.Submitted) -> None:
        self.attempts += 1
        if (
            username := self.query_one("#username").value
        ) == "John" and event.value == "Doe":
            self.dismiss((True, username))
        else:
            self.query_one("#failed").update("[red]Login failed.")
            if self.attempts >= 3:
                self.dismiss((False, username))


class ConfirmationDialog(ModalScreen):
    DEFAULT_CSS = """
        ConfirmationDialog {
            align: center middle;

            & Vertical {
                border: round $secondary;
                padding: 1 2;
                width: auto;
                height: auto;

                & Label {
                    margin-bottom: 2;
                    width: 100%;
                    text-align: center;
                }
                & Horizontal {
                    height: auto;
                    width: auto;

                    & Button {
                        margin: 0 2;
                    }
                }
            }
        }
    """

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Label("Do you want to exit?")
            with Horizontal():
                yield Button("Yes", id="yes")
                yield Button("No", id="no")

    @on(Button.Pressed)
    def confirm(self, event: Button.Pressed) -> None:
        if event.button.id == "yes":
            self.dismiss(True)
        else:
            self.dismiss(False)


class Dashboard(Screen):
    def __init__(self, username: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.username = username

    def compose(self) -> ComposeResult:
        yield Label(f"User {self.username} has logged in.")
        yield Button("Exit", variant="primary", id="exit-button")

    @on(Button.Pressed, "#exit-button")
    def exit_button_pressed(self, event: Button.Pressed) -> None:
        self.confirm_exit()

    @work
    async def confirm_exit(self) -> None:
        # show how to use a worker for returning data from screens
        confirmed = await self.app.push_screen_wait(ConfirmationDialog())
        if confirmed:
            self.app.exit()


class AppWithLogin(App[None]):
    def on_mount(self) -> None:
        # show how to use a handler for returning data from screens
        def login_handler(return_values):
            is_successful, username = return_values
            if is_successful:
                self.push_screen(Dashboard(username))
            else:
                self.exit()

        self.push_screen(LoginScreen(), callback=login_handler)


AppWithLogin().run()
