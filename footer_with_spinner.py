from textual.widgets import Footer, Static
from rich.console import RenderableType
from textual.app import App, ComposeResult
from textual.binding import Binding
import rich.spinner
from rich.text import Text

class FooterWithSpinner(Footer):

    def render(self):
        return self.renderable

    def on_mount(self):
        if self._key_text is None:
            self._key_text = self._make_key_text()
        self.renderable = rich.spinner.Spinner("point", text=self._key_text)
        self.interval_update = self.set_interval(1 / 60, self.update_rendering)

    def pause(self):
        self.interval_update.pause()

    def resume(self):
        self.interval_update.resume()

    def update_rendering(self):
        self.refresh(layout=True)

    def render(self):
        return self.renderable

class ExampleApp(App):

    BINDINGS = [
        Binding(key="q", action="quit", description="Quit the app"),
        Binding(
            key="question_mark",
            action="help",
            description="Show help screen",
            key_display="?",
        ),
        Binding(key="delete", action="delete", description="Delete the thing"),
        Binding(key="j", action="down", description="Scroll down", show=False),
    ]

    def compose(self) -> ComposeResult:
        yield FooterWithSpinner()

if __name__ == "__main__":
    ExampleApp().run()
