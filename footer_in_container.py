from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.widgets import Footer, Label, Placeholder


class UndockedFooter(Footer, inherit_css=False):
    DEFAULT_CSS = """
        UndockedFooter {
            layout: grid;
            grid-columns: auto;
            background: $panel;
            color: $text;
            # dock: bottom;
            height: 1;
            scrollbar-size: 0 0;
            &.-compact {
                grid-gutter: 1;
            }
            FooterKey.-command-palette  {
                dock: right;                        
                padding-right: 1;
                border-left: vkey $foreground 20%;                
            }
        }
    """


class ContainerizedFooter(App[None]):
    CSS = """
        Horizontal {
            dock: bottom;
            height: 1;

            & Footer {
                width: 1fr;
            }

            & Label {
                width: auto;
                border-left: solid $panel-lighten-3;
                padding: 0 1;
                background: $panel;
                text-style: bold;
            }
        }
    """

    BINDINGS = [("q", "quit", "Quit")]

    def compose(self) -> ComposeResult:
        with Horizontal():
            yield Footer()
            yield Label("Some important piece of text")
        yield Placeholder("This is a minimal app.")

    def on_mount(self) -> None:
        footer = self.query_one(Footer)
        footer.styles.dock = ""
        footer.styles.width = "1fr"


ContainerizedFooter().run()
