from textual import work
from textual.app import App, ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Button, Footer, Placeholder, TextArea


class EditPost(ModalScreen):
    def __init__(self, text="", *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.text = text

    def compose(self) -> ComposeResult:
        yield TextArea(text=self.text)
        yield Button("OK")

    def on_button_pressed(self) -> None:
        text_area = self.query_one(TextArea)
        self.dismiss(text_area.text)


class MinimalApp(App[None]):
    BINDINGS = [("n", "new_post", "New Post"), ("e", "edit_post", "Edit Post")]

    def compose(self) -> ComposeResult:
        yield Placeholder("This is a minimal app.")
        yield Footer()

    @work
    async def action_new_post(self) -> None:
        text = await self.push_screen_wait(EditPost())
        self.notify(f"New post with text: {text}")

    @work
    async def action_edit_post(self) -> None:
        text = await self.push_screen_wait(EditPost("You can edit your old post"))
        self.notify(f"Edited post with final text: {text}")


MinimalApp().run()
