import textual.containers as containers
import textual.widgets as widgets
from textual import events
from textual.app import App, ComposeResult

welcome_text = """Welcome to your Grist cloud setup.

Please fill in the following information so that we can setup your new Grist instance.
"""

class GristSetupApp(App):
    def compose(self) -> ComposeResult:
        yield widgets.Static(welcome_text)

        with containers.Horizontal():
            yield widgets.Label("Email:")
            self.email = widgets.Input(placeholder="you@example.com")
            yield self.email

        with containers.Horizontal():
            yield widgets.Label("Hostname:")
            self.hostname = widgets.Input(placeholder="grist.location")
            yield self.hostname

        with containers.Horizontal():
            yield widgets.Label("Enable automatic HTTPS via Let's Encrypt?")
            self.lets_encrypt_toggle = widgets.Switch(value=False)
            yield self.lets_encrypt_toggle
            
            self.submit_button = widgets.Button("Submit", id="submit-btn")
        yield self.submit_button
        
        self.focused_field = 0
        self.fields = [self.email, self.hostname, self.lets_encrypt_toggle, self.submit_button]

    def on_mount(self):
        self.fields[self.focused_field].focus()

    def focus_next(self):
        self.focused_field = (self.focused_field + 1) % len(self.fields)
        self.fields[self.focused_field].focus()

    def focus_previous(self):
        self.focused_field = (self.focused_field - 1) % len(self.fields)
        self.fields[self.focused_field].focus()

    async def on_key(self, event: events.Key):
        if event.key == "down":
            self.focus_next()
        elif event.key == "up":
            self.focus_previous()
        elif event.key == "enter" and self.focused_field == len(self.fields):
            # If Enter is pressed on the button, submit the form
            self.submit()

    def on_button_pressed(self, event: widgets.Button.Pressed) -> None:
        if event.button.id == "submit-btn":
            self.submit()

    def submit(self):
        """Process the form data."""
        app.exit({
            'email': self.email.value,
            'domain': self.hostname.value,
            'tls': self.lets_encrypt_toggle.value
        })

# Run the application
app = GristSetupApp()
print(app.run())