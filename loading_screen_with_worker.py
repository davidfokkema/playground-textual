"""Demo of an app with a loading screen.

If you have to do some work on startup, this is how you could do it. The default
screen is the loading screen and on startup, a worker runs which can do all the
work that is required before running the app proper. When the tasks are
finished, the worker posts a FinishedLoading message which is picked up by the
App. The event handler for that message pushes the main app screen.
"""

import time

from textual import on, work
from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.message import Message
from textual.screen import ModalScreen, Screen
from textual.widgets import Footer, Header, Label, LoadingIndicator, Placeholder


class LoadingScreen(ModalScreen):
    DEFAULT_CSS = """
        LoadingScreen {
            align: center middle;
            hatch: right $primary-background;

            Vertical {
                background: $surface;
                border: hkey $accent;
                width: auto;
                height: auto;
                padding: 0 5;

                Label {
                    width: auto;
                    padding: 0;
                    margin-bottom: 1;
                }

                LoadingIndicator {
                    height: 1;
                }
            }
        }
    """

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Label("Loading data...")
            yield LoadingIndicator()


class MainScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield Placeholder("Main App Screen")


class AppWithLoadingScreen(App[None]):
    class FinishedLoading(Message): ...

    def get_default_screen(self) -> Screen:
        return LoadingScreen()

    def on_mount(self) -> None:
        self.run_startup_tasks()

    @work(thread=True)
    def run_startup_tasks(self) -> None:
        # doing some important work, either async or threaded
        time.sleep(5)
        self.post_message(self.FinishedLoading())

    @on(FinishedLoading)
    def push_app_screen(self) -> None:
        self.push_screen(MainScreen())


AppWithLoadingScreen().run()
