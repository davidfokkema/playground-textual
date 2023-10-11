from textual.app import App, ComposeResult
from textual.widgets import Label


class WrapTextApp(App[None]):
    CSS = """
        Label {
            width: 100%;
        }
    """

    def compose(self) -> ComposeResult:
        yield Label(
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed consectetur vestibulum nulla, ut consequat felis iaculis vitae. Duis fringilla ex bibendum nulla posuere venenatis. Cras bibendum dui et lorem feugiat eleifend. Suspendisse ultricies suscipit volutpat. Sed id elementum libero, sit amet dignissim dui. Pellentesque sem orci, pharetra vitae placerat non."
        )


if __name__ == "__main__":
    WrapTextApp().run()
