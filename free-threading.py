import sys

from textual import work
from textual.app import App, ComposeResult
from textual.containers import HorizontalGroup
from textual.widgets import Footer, Header, Label, ProgressBar


class Calculator(HorizontalGroup):
    N = 1_000
    M = 10_000_000

    DEFAULT_CSS = """
        Calculator {
            &> Label {
                margin-right: 2;
            }
        }
    """

    def __init__(self, title: str) -> None:
        super().__init__()
        self.title = title

    def compose(self) -> ComposeResult:
        yield Label(self.title)
        yield ProgressBar(total=self.N)

    def on_mount(self) -> None:
        self.do_work()

    @work(thread=True)
    def do_work(self) -> None:
        for n in range(self.N):
            _ = 0
            for m in range(1, self.M):
                _ += 1 / m
            self.app.call_from_thread(self.query_one(ProgressBar).advance)


class CalculatorApp(App[None]):
    BINDINGS = [("a", "add_calculator", "Add another calculator")]

    count = 1

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield Label(
            f"Is the GIL enabled? -- {'Yes.' if sys._is_gil_enabled() else 'No.'}"
        )

    async def on_mount(self) -> None:
        await self.run_action("add_calculator")

    def action_add_calculator(self) -> None:
        self.mount(Calculator(f"Calculator #{self.count}"))
        self.count += 1


CalculatorApp().run()
