import subprocess

from rich.text import Text
from textual import work
from textual.app import App, ComposeResult
from textual.widgets import RichLog


class MyLog(RichLog):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.border_title = "Console"
        self.clear_next_line = False

    def mywrite(self, text: Text):
        if self.clear_next_line:
            del self.lines[-1]
            self.clear_next_line = False
        self.write(repr(text))
        if text.plain and text.plain[-1] == "\n":
            self.clear_next_line = True


class ConsoleApp(App):
    CSS = """
        #console {
            border: double lightgreen;
        }
    """

    def compose(self) -> ComposeResult:
        yield MyLog(id="console", auto_scroll=False)

    async def on_mount(self) -> None:
        self.run_process()

    @work(thread=True)
    def run_process(self) -> None:
        console: MyLog = self.query_one("#console")
        with subprocess.Popen(
            "FORCE_COLOR=yes python -m rich.progress",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            encoding="utf-8",
        ) as proc:
            while True:
                output = proc.stdout.readline()
                if output == "" and proc.poll() is not None:
                    break
                self.call_from_thread(console.mywrite, Text.from_ansi(output))


if __name__ == "__main__":
    app = ConsoleApp()
    app.run()
