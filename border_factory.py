from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widget import Widget
from textual.widgets import Input


def create_widget_with_title(widget: Widget, title: str) -> Widget:
    widget.border_title = title
    return widget


class WidgetWithTitle(Container):
    DEFAULT_CSS = """
        WidgetWithTitle {
            border: solid $primary;
            height: auto;
        }
    """

    def __init__(self, widget: Widget, title: str) -> None:
        super().__init__()
        self._widget = widget
        self.border_title = title

    def compose(self) -> ComposeResult:
        yield self._widget


class MyApp(App[None]):
    def compose(self) -> ComposeResult:
        yield create_widget_with_title(
            Input(placeholder="Type here"), title="My first Input widget"
        )
        yield WidgetWithTitle(
            Input(placeholder="...or here"), title="My second Input widget"
        )


MyApp().run()
