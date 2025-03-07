import rich.spinner
from textual.app import App, ComposeResult
from textual.widgets import Static


class WidgetSpinner(Static):
    def on_mount(self):
        self.spinner = rich.spinner.Spinner("dots", text="working...")
        self.interval_update = self.set_interval(
            1 / 60, lambda: self.update(self.spinner)
        )


class ExampleApp(App):
    def compose(self) -> ComposeResult:
        yield WidgetSpinner()


if __name__ == "__main__":
    ExampleApp().run()
