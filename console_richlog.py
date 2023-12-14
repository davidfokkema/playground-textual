"""A test with RichLog.

This example shows capturing output from a console script which runs using the
subprocess module, in a threaded worker. The problem it hasn't solved is that in
a terminal, three progressbars are displayed at the bottom of the screen while
text is occassionally printed above it the progress bars, while in RichLog, each
screen update writes three new lines to the log. The result is that the log is
flooded with hundreds of lines of progress bars slowly building up to
completion.
"""

import subprocess

from rich.text import Text
from textual import work
from textual.app import App, ComposeResult
from textual.widgets import RichLog


class MyLog(RichLog):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.border_title = "Console"
        self.auto_scroll = True

    def mywrite(self, text: Text):
        self.write(text)


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
