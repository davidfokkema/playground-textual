from textual.app import App, ComposeResult, RenderResult
from textual.widgets import Button


class TransparentButton(Button):
    DEFAULT_CSS = """
        TransparentButton {
            border: none;
            width: auto;
            min-width: 0;
            padding: 0;

            &:hover {
                border: none;
            }
        }
    """

    def render(self) -> RenderResult:
        background = self.styles.background.hex
        parent_background = self.colors[0].hex
        return (
            f"[{background} on {parent_background}]\ue0b6[/] "
            + str(self.label)
            + f" [{background} on {parent_background}]\ue0b4[/]"
        )

    def get_content_width(self, container, viewport):
        width = super().get_content_width(container, viewport)
        # The original button already pads the text with one space on each side
        # so we only need to add the width of the rounded borders on each side.
        return width + 2


class MinimalApp(App[None]):
    CSS = """
        Screen {
            background: $primary-muted;
            align: center middle;
            layout: horizontal;
        }

        TransparentButton {
            background: $accent;
            margin: 2;
        }
    """

    def compose(self) -> ComposeResult:
        yield TransparentButton("Button 1")
        yield TransparentButton("Button 2")


MinimalApp().run()
