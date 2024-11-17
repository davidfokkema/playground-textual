"""Run a worker and provide UI callbacks.

This code demonstrates how to run a regular synchronous Python function from a
Textual app. The complication is that that function requires user input from
time to time. So we must provide a way for that function to call back to the
Textual app to ask for input. A further complication is that we do not want that
function to know that it is called from Textual. The callback could just as
easily be provide by a small script. Since Textual is a full application
framework running async code, this is quite different. This code shows how that
could work.
"""

import datetime
import random
import time
from collections.abc import Callable

from textual import on, work
from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, DataTable, Footer, Input, Label
from textual.worker import Worker, WorkerState

ITEMS = ["Socks", "Book: Web Scraping", "Book: Intermediate Python", "Pencils"]


class TransactionScraper:
    """A (fake) transaction scraper.

    This class simulates a web scraper which knows nothing about asyncio or
    front-ends.
    """

    def search_transactions(
        self,
        new_data_callback: Callable[[tuple], None],
        user_input_callback: Callable[[str], str],
    ) -> None:
        """Search for (fake) transactions.

        This method will find between 5 and 15 transactions. Fetching each
        transaction takes a random amount of time, but never more than 3
        seconds. It has a 20% chance of requiring user input. You must provide
        it with two callbacks: one to let the caller know it has new data, and
        one to ask the user for input.

        Args:
            new_data_callback (Callable[[tuple], None]): callback to pass a new
                transaction to the caller.
            user_input_callback (Callable[[str], str]): callback to request
                input from the user. Should accept a prompt and return a
                response.
        """
        for _ in range(random.randint(5, 15)):
            # wait for a bit, fetching takes time
            time.sleep(min(3, random.expovariate(lambd=1 / 0.5)))
            if random.random() < 0.2:
                # 20% chance we need user input
                response = user_input_callback("I need your input!")
                # record the response as new data, just to show we got it.
                new_data_callback(("", f"[bold green]{response}", ""))
            else:
                # 80% chance we got the transaction without issues.
                # Date's today, the item is a random choice and we got between 1
                # and 5 items.
                new_data_callback(
                    (datetime.date.today(), random.choice(ITEMS), random.randint(1, 5))
                )


class AskInput(ModalScreen):
    """A simple modal screen which asks for user input."""

    def __init__(self, prompt: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.prompt = prompt

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Label(self.prompt)
            yield Input()

    @on(Input.Submitted)
    def return_response(self, event: Input.Submitted) -> None:
        self.dismiss(event.value)


class MyApp(App[None]):
    """A simple app which records transactions fetched from an API.

    This class provides two callback functions to record transactions and to ask
    the user for input, if needed. The search for transactions runs in a
    threaded worker.
    """

    CSS = """
        DataTable {
            height: 1fr;
            margin-bottom: 1;
        }

        #table_title {
            margin: 1 0;
            background: $panel;
            width: 100%;
            text-align: center;
            border: hkey $primary;
            text-style: bold;
        }

        AskInput {
            align: center middle;

            & Vertical {
                border: tall $accent;
                width: 90%;
                background: $panel;
                height: auto;

                & Label {
                    width: 100%;
                    margin-bottom: 1;
                    text-align: center;
                    text-style: bold;
                }
            }
        }
    """

    def compose(self) -> ComposeResult:
        yield Footer()
        yield Label("Transactions", id="table_title")
        yield DataTable()
        yield Button("Start Scraping", variant="primary", id="start-button")

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns("Date", "Item", "Quantity")

    @on(Button.Pressed)
    @work(thread=True)
    def start_scraping(self) -> None:
        """Start scraping transactions.

        Disables the start button.
        """
        self.query_one("#start-button", Button).disabled = True
        TransactionScraper().search_transactions(
            new_data_callback=self.log_new_transaction,
            user_input_callback=self.ask_for_input,
        )

    @on(Worker.StateChanged)
    def enable_start_button(self, event: Worker.StateChanged) -> None:
        """Enable start button if the worker has finished.

        Args:
            event (Worker.StateChanged): the event to be handled.
        """
        if event.state not in (WorkerState.PENDING, WorkerState.RUNNING):
            self.query_one("#start-button").disabled = False

    def log_new_transaction(self, transaction) -> None:
        """Log a new transaction.

        Args:
            transaction (tuple): the transaction to record in the data table.
        """
        (table := self.query_one(DataTable)).add_row(*transaction)
        table.action_scroll_bottom()

    def ask_for_input(self, prompt: str) -> str:
        """Aks the user for input and return the response.

        This method expects to be called from a threaded worker, so has to use
        `call_from_thread()` to call the async method which actually does the
        work.

        Args:
            prompt (str): the prompt to display to the user.

        Returns:
            str: the user's response.
        """
        return self.call_from_thread(self._ask_for_input, prompt)

    async def _ask_for_input(self, prompt: str) -> str:
        """Ask the user for input and return the response.

        Push the AskInput screen and await the response.

        Args:
            prompt (str): the prompt to display to the user.

        Returns:
            str: the user's response.
        """
        return await self.push_screen_wait(AskInput(prompt))


MyApp().run()
