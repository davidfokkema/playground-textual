import textual.widgets._progress_bar
from rich.text import Text
from textual.app import App, ComposeResult
from textual.widgets import ProgressBar


def modify_progressbar(method):
    def wrapper(*args, **kwargs):
        result = method(*args, **kwargs)
        for segment in result:
            text = segment.plain
            new_text = text.replace("╸", "▌").replace("╺", "▐").replace("━", "█")
            new_segment = Text(new_text)
            new_segment.copy_styles(segment)
            yield new_segment

    return wrapper


class MinimalApp(App[None]):
    def compose(self) -> ComposeResult:
        yield ProgressBar()

    def on_mount(self) -> None:
        textual.widgets._progress_bar.BarRenderable.__rich_console__ = (
            modify_progressbar(
                textual.widgets._progress_bar.BarRenderable.__rich_console__
            )
        )
        self.progress_timer = self.set_interval(1 / 10, self.make_progress, pause=True)
        self.set_timer(5.0, self.start_progress)

    def start_progress(self) -> None:
        for bar in self.query(ProgressBar):
            bar.update(total=100)
        self.progress_timer.resume()

    def make_progress(self) -> None:
        for bar in self.query(ProgressBar):
            bar.advance(1)


MinimalApp().run()
