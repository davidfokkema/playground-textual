import pathlib

from textual.app import App, ComposeResult
from textual.containers import Grid, Horizontal, Vertical
from textual.widgets import Button, Checkbox, Input, Label, Static, TextArea


class SidebarApp(App[None]):
    CSS = """
        #sidebar {
            background: $panel;
            border: vkey $primary;
            width: 35;
            height: auto;
            & #sidebar_label {
                width: 100%;
                text-align: center;
                text-style: bold;
                margin-bottom: 1;
            }    
        }

        #settings {
            height: auto;
            grid-size: 2;
            grid-columns: 5 2fr;
            & Label {
                height: 100%;
                width: 100%;
                content-align: right middle;

            }
        }

        #buttons {
            align: center middle;
        }
    """

    def compose(self) -> ComposeResult:
        with Horizontal():
            with Vertical(id="sidebar"):
                yield Label("Sidebar", id="sidebar_label")
                with Grid(id="settings"):
                    yield Label("Name:")
                    yield Input(pathlib.Path(__file__).name)
                    yield Label()
                    yield Checkbox(label="BasicFeature", value=True)
                    yield Label()
                    yield Checkbox(label="ProFeature", value=False)
                with Horizontal(id="buttons"):
                    yield Button("Reset Settings", id="reset_button")
                yield Static("Here you can change some settings. It is a nice sidebar!")
            yield TextArea(pathlib.Path(__file__).read_text(), language="python")

    def on_mount(self) -> None:
        self.query_one("TextArea").focus()


SidebarApp().run()
