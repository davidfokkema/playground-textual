import itertools
import math
import random
import time

from textual import on, work
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Label, ProgressBar
from textual.worker import Worker, WorkerState

N_ITEMS = 100
N_WORKERS = 3


class WorkersApp(App[None]):
    CSS = """
        Vertical {
            border: round $primary;
        }

        Horizontal {
            height: auto;
        }

        ProgressBar {
            width: 1fr;
            & > Bar {
                width: 1fr;
            }
        }
    """

    def compose(self) -> ComposeResult:
        with Horizontal():
            with Vertical() as container:
                container.border_title = "Overal Progress"
                yield ProgressBar(id="overall_progress")
            with Vertical() as container:
                container.border_title = "Jobs"
                for num in range(N_WORKERS):
                    with Horizontal():
                        yield Label(f"Worker {num+1}: ")
                        yield ProgressBar(id=f"worker-{num}", total=100)

    def on_mount(self) -> None:
        """Generate a list of items and check them in batches."""
        items = [random.random() for _ in range(N_ITEMS)]
        self.query_one("#overall_progress").total = N_ITEMS

        # batch items and start workers
        batch_size = math.ceil(N_ITEMS / N_WORKERS)
        for idx, (first, last) in enumerate(
            itertools.pairwise(range(0, N_ITEMS + batch_size, batch_size))
        ):
            self.check_items(idx, items[first:last])

    @work(thread=True)
    def check_items(self, worker_idx: int, items: list[float]) -> None:
        """Check items one by one."""
        overal_progress: ProgressBar = self.query_one("#overall_progress")
        worker_progress: ProgressBar = self.query_one(f"#worker-{worker_idx}")
        worker_progress.total = len(items)
        for item in items:
            # simulating doing some work on item
            time.sleep(random.uniform(0, 0.3))
            # update progress bars
            self.call_from_thread(overal_progress.advance, 1)
            self.call_from_thread(worker_progress.advance, 1)

    @on(Worker.StateChanged)
    def exit_if_work_is_done(self) -> None:
        """Exit if all workers have completed."""
        for worker in self.workers:
            if worker.state in (WorkerState.PENDING, WorkerState.RUNNING):
                return
        else:
            self.exit()


WorkersApp().run()
