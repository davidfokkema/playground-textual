"""A (fake) file manager for professional use.

While playing with menus and workers for background tasks I needed a
confirmation dialog. Returning data from modal screens involves callbacks which
require you to push a screen, wrap up your task and pick it up inside a
callback. This broke my brain because maybe I'm in a long-running task and need
to ask for confirmation repeatedly, as in copying a batch of files of which
multiple files may already exist at the destination. How do I wrap up, and pick
up the work in a new callback repeatedly? I'm looking for a nice, elegant
solution which fits the callback / asyncio nature of Textual.

This is not that solution. It is, however, _a_ solution. I opted for writing
something that _does_ fit my brain which involves synchronisation primitives.

To make the example interesting, the code is not as small as I would have liked.
The interesting things happen in the worker CopyDialog.copy_files and the
confirmation dialog handler CopyDialog.ask_overwrite_confirmation.
"""

import asyncio
import enum
import itertools
import random
import threading
import time
from pathlib import Path
from threading import Condition
from typing import Iterator

from faker import Faker
from textual import on, work
from textual.app import App, ComposeResult
from textual.containers import Center, Horizontal, Vertical
from textual.events import Mount
from textual.reactive import reactive
from textual.screen import ModalScreen
from textual.widgets import Button, Footer, Header, Label, ProgressBar, Static
from textual.worker import Worker, WorkerState


class FileReplaceChoice(enum.Enum):
    REPLACE = enum.auto()
    SKIP = enum.auto()
    CANCEL = enum.auto()


def generate_file_names() -> Iterator[Path]:
    faker = Faker()
    while True:
        yield faker.file_path(depth=random.randint(1, 5))


class FileReplaceDialog(ModalScreen):
    def __init__(self, file: Path) -> None:
        super().__init__()
        self.file = file

    def compose(self) -> ComposeResult:
        with Vertical(classes="dialog"):
            with Center():
                yield Label(
                    f"File {self.file} already exists at destination.", classes="msg"
                )
            with Center():
                with Horizontal():
                    yield Button("Skip", id="skip", variant="primary")
                    yield Button("Replace", id="replace", variant="warning")
                    yield Button("Cancel", id="cancel", variant="error")

    @on(Button.Pressed)
    def make_choice(self, event: Button.Pressed):
        match event.button.id:
            case "replace":
                self.dismiss(FileReplaceChoice.REPLACE)
            case "skip":
                self.dismiss(FileReplaceChoice.SKIP)
            case _:
                self.dismiss(FileReplaceChoice.CANCEL)


class CopyDialog(ModalScreen):
    current_file = reactive("")

    def __init__(self, files: list[Path]) -> None:
        super().__init__()
        self.files = files
        self.cancel = threading.Event()

    def compose(self) -> ComposeResult:
        with Vertical(classes="dialog"):
            with Center():
                yield Static(id="current_file")
            with Center():
                yield ProgressBar(id="progress")
            with Center():
                yield Button("Cancel", id="cancel", variant="error")

    @on(Mount)
    def start_worker(self) -> None:
        self.worker = self.copy_files()

    def watch_current_file(self, file: Path) -> None:
        if not file:
            copy_msg = "Preparing files..."
        else:
            copy_msg = f"Copying {file}..."
        self.query_one("#current_file").update(copy_msg)
        self.query_one("#progress").update(
            progress=self.worker.completed_steps, total=self.worker.total_steps
        )

    @work(thread=True)
    def copy_files(self) -> None:
        # simulate preflight
        time.sleep(1)

        self.worker.update(total_steps=len(self.files))
        for file in self.files:
            if self.cancel.is_set():
                # we want to have the CANCELLED WorkerState
                self.worker.cancel()
                break

            self.current_file = file
            if random.random() < 0.05:
                # some files already exist
                match self.app.call_from_thread(self.ask_overwrite_confirmation, file):
                    case FileReplaceChoice.CANCEL:
                        self.cancel.set()
                    case FileReplaceChoice.REPLACE:
                        self.copy_file(file)
                    case FileReplaceChoice.SKIP:
                        continue
            else:
                self.copy_file(file)
            self.worker.advance()

    def copy_file(self, file: Path) -> None:
        # simulate copy
        time.sleep(min(random.expovariate(1.0 / 0.2), 1.0))

    async def ask_overwrite_confirmation(self, file: Path) -> FileReplaceChoice:
        def callback(value: FileReplaceChoice) -> None:
            future_choice.set_result(value)

        self.log("Asking for confirmation...")
        loop = asyncio.get_running_loop()
        future_choice = loop.create_future()

        self.app.push_screen(FileReplaceDialog(file), callback)

        return await future_choice

    def on_worker_state_changed(self, event: Worker.StateChanged) -> None:
        if event.state in (
            WorkerState.SUCCESS,
            WorkerState.ERROR,
            WorkerState.CANCELLED,
        ):
            print(event.state)
            self.dismiss()

    @on(Button.Pressed, "#cancel")
    def cancel_copy(self, event: Button.Pressed) -> None:
        self.cancel.set()


class FileManagerWidget(Static):
    def compose(self) -> ComposeResult:
        with Vertical():
            with Center():
                yield Label("Start Recursive Copy Procedure Pro™️")
            with Center():
                yield Button("Start", id="start")

    @on(Button.Pressed, "#start")
    def start_copy(self) -> None:
        files = list(itertools.islice(generate_file_names(), 200))
        self.app.push_screen(CopyDialog(files=files))


class FileManagerPro(App):
    BINDINGS = [("q", "quit", "Quit")]

    CSS = """
        Screen {
            align: center middle;
        }

        Vertical {
            height: auto;
        }

        Horizontal {
            width: auto;
            height: auto;
        }

        #current_file, .msg {
            width: 100%;
            padding: 1 2;
            text-align: center;
        }

        .dialog {
            width: 90%;
            border: heavy $primary;
            background: $panel;
        }

        Button {
            margin: 1 2;
        }
    """

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield FileManagerWidget()


if __name__ == "__main__":
    Faker.seed(2)
    random.seed(1)
    app = FileManagerPro()
    app.run()
