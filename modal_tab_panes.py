from textual import work
from textual.app import App, ComposeResult
from textual.screen import ModalScreen, Screen
from textual.widgets import Button, Label, TabbedContent, TabPane


class AskToAddTabModal(ModalScreen):
    def compose(self) -> ComposeResult:
        yield Label("Add a tab?")
        yield Button("Yes", id="yes-button")
        yield Button("No", id="no-button")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "yes-button":
            self.dismiss(True)
        else:
            self.dismiss(False)


class TabsScreen(Screen):
    def compose(self) -> ComposeResult:
        yield TabbedContent()
        yield Button("Push Modal")

    def on_button_pressed(self) -> None:
        self.ask_to_add_tab()

    @work
    async def ask_to_add_tab(self) -> None:
        should_add_tab = await self.app.push_screen_wait(AskToAddTabModal())
        if should_add_tab:
            self.query_one(TabbedContent).add_pane(
                TabPane("Tab", Label("Some content."))
            )


class ModelTabsApp(App[None]):
    def on_mount(self) -> None:
        self.push_screen(TabsScreen())


ModelTabsApp().run()
