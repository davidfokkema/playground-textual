import subprocess

from textual import work
from textual.app import App, ComposeResult
from textual.widgets import Log


class MyLog(Log):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.border_title = "Console"


class ConsoleApp(App):
    CSS = """
        #console {
            border: double lightgreen;
        }
    """

    def compose(self) -> ComposeResult:
        yield MyLog(id="console")

    async def on_mount(self) -> None:
        self.run_process()

    @work(thread=True)
    def run_process(self) -> None:
        console: MyLog = self.query_one("#console")
        with subprocess.Popen(
            "python -m rich.progress",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            encoding="utf-8",
        ) as proc:
            while True:
                output = proc.stdout.readline()
                if output == "" and proc.poll() is not None:
                    break
                self.call_from_thread(console.write, output)


if __name__ == "__main__":
    app = ConsoleApp()
    app.run()
