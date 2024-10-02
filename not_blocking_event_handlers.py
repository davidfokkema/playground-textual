import asyncio

from textual import on, work
from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.widgets import Button, Label


class MyApp(App):
    def compose(self) -> ComposeResult:
        # Run button
        self.runbutton = Button(label="Run", variant="success", id="button")
        self.text = Label("Not Running")

        # Assemble the UI
        yield Vertical(self.runbutton, self.text)

    @on(Button.Pressed, "#button")
    def can_be_any_name(self, event: Button.Pressed) -> None:
        # Call the long-running function
        self.my_function()

    @work
    async def my_function(self):
        self.query_one("#button").disabled = True
        self.text.update("Running!")
        await asyncio.sleep(5)
        self.text.update("Not Running")
        self.query_one("#button").disabled = False


# Start the application
if __name__ == "__main__":
    MyApp().run()
