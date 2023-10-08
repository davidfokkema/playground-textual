import time

from textual import work
from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.message import Message
from textual.screen import Screen
from textual.widgets import Label


class MyLabel(Label):
    class UpdateMsg(Message):
        def __init__(self, msg: str) -> None:
            super().__init__()
            self.msg = msg


class MyScreen(Screen):
    def compose(self) -> ComposeResult:
        with Vertical():
            yield MyLabel("First!")

    # doesn't work
    def on_my_label_update_msg(self, message: MyLabel.UpdateMsg) -> None:
        self.query_one("MyLabel").update(message.msg)


class CustomMessageApp(App[None]):
    CSS = """
        Vertical {
            align: center middle;
        }
        Label {
            padding: 1 2;
            border: solid $secondary;
            color: $text;
        }
    """

    def on_mount(self):
        self.push_screen(MyScreen())
        self.update()

    @work(thread=True)
    def update(self) -> None:
        time.sleep(1)
        self.post_message(MyLabel.UpdateMsg("First post!"))
        time.sleep(1)
        self.call_from_thread(self.app.pop_screen)

    # does work
    # def on_my_label_update_msg(self, message: MyLabel.UpdateMsg) -> None:
    #     self.query_one("MyLabel").update(message.msg)


if __name__ == "__main__":
    CustomMessageApp().run()
