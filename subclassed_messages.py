from textual.app import App, ComposeResult
from textual.message import Message
from textual.widgets import Placeholder


class LowLevel(Placeholder):
    class PostIt(Message):
        def __init__(self) -> None:
            super().__init__()
            self.msg = "This is basically still the low-level message."

    def on_click(self) -> None:
        self.post_message(self.PostIt())


# class HighLevel(LowLevel): ...


class HighLevel(LowLevel):
    class PostIt(LowLevel.PostIt): ...


class MinimalApp(App[None]):
    CSS = """
        Placeholder {
            height: 5;
        }
    """

    def compose(self) -> ComposeResult:
        yield Placeholder("This is a minimal app.")
        yield LowLevel("Some low-level widget.")
        yield HighLevel("Some high-level widget.")

    def on_low_level_post_it(self, event: LowLevel.PostIt) -> None:
        self.notify(f"Low-level post-it: {event.msg}")

    def on_high_level_post_it(self, event: HighLevel.PostIt) -> None:
        self.notify(f"High-level post-it: {event.msg}")


MinimalApp().run()
