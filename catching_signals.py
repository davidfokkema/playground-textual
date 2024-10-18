import pathlib
import signal
import time

from textual.app import App, ComposeResult
from textual.widgets import Placeholder


class MinimalApp(App[None]):
    _signal = None

    def on_mount(self) -> None:
        signal.signal(signalnum=signal.SIGHUP, handler=self.catch_signal)
        signal.signal(signalnum=signal.SIGTERM, handler=self.catch_signal)

    def compose(self) -> ComposeResult:
        yield Placeholder("This is a minimal app.")

    def catch_signal(self, signum, frame) -> None:
        self._signal = signum
        self.exit()


app = MinimalApp()
app.run()

pathlib.Path("signal.txt").write_text(
    f"{time.monotonic()}: Received signal: {app._signal}"
)
print("Done")
print(f"Received signal: {app._signal}")
