from textual import events
from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.widgets import Button, Input, Label, Switch

welcome_text = """Welcome to your Grist cloud setup.

Please fill in the following information so that we can setup your new Grist instance.
"""


class GristSetupApp(App):
    def compose(self) -> ComposeResult:
        yield Label(welcome_text)

        with Horizontal():
            yield Label("Email:")
            yield Input(placeholder="you@example.com", id="email")

        with Horizontal():
            yield Label("Hostname:")
            yield Input(placeholder="grist.location", id="hostname")

        with Horizontal():
            yield Label("Enable automatic HTTPS via Let's Encrypt?")
            yield Switch(value=False, id="use_lets_encrypt")

        yield Button("Submit", id="submit-btn")

    def on_key(self, event: events.Key):
        if event.key == "down":
            self.screen.focus_next()
        elif event.key == "up":
            self.screen.focus_previous()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "submit-btn":
            self.submit()

    def submit(self):
        """Process the form data."""
        app.exit(
            {
                "email": self.query_one("#email").value,
                "hostname": self.query_one("#hostname").value,
                "tls": self.query_one("#use_lets_encrypt").value,
            }
        )


# Run the application
app = GristSetupApp()
print(app.run())
