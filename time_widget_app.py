# copy / paste from discord, with changes
import requests
from rich.console import RenderableType
from textual.app import App, ComposeResult
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Footer, Static


class TimeWidget(Static):
    react_response = reactive(str)

    def render(self) -> RenderableType:
        return str(self.react_response)

    def update_time(self) -> None:
        self.react_response = str(
            requests.get(
                "https://www.timeapi.io/api/Time/current/zone?timeZone=Europe/Amsterdam"
            ).json()
        )

    def on_mount(self) -> None:
        self.update_time()


class AutoReact(App):
    BINDINGS = [("r", "refresh", "Refresh"), ("q", "quit", "Quit")]

    def compose(self) -> ComposeResult:
        yield TimeWidget()
        yield Footer()

    def action_refresh(self) -> None:
        self.query_one(TimeWidget).update_time()

    def action_quit(self) -> None:
        self.exit()


if __name__ == "__main__":
    AutoReact().run()
