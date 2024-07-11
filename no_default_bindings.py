from textual.app import App, ComposeResult
from textual.events import Key
from textual.widgets import Footer, RichLog, TextArea


class NoBindingsInput(TextArea, inherit_bindings=False):
    BINDINGS = [("enter", "do_the_thing", "DoTheThing")]

    def action_do_the_thing(self) -> None:
        self.app.query_one(RichLog).write("[bold red]I did the thing![/]")

    def on_key(self, event: Key) -> None:
        self.app.query_one(RichLog).write(f"{event=}")
        if event.key == "enter":
            event.prevent_default()
            # event.stop()


class NoBindingsApp(App[None]):
    def compose(self) -> ComposeResult:
        yield Footer()
        yield NoBindingsInput("You can't touch me!")
        yield RichLog(markup=True)


NoBindingsApp().run()
