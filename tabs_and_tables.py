import datetime
import random

from textual import on
from textual.app import App, ComposeResult
from textual.widgets import Button, DataTable, Label, TabbedContent, TabPane


class TabsAndTablesApp(App[None]):
    CSS = """
        #order_book {
            border: round $primary-lighten-2;

            & DataTable {
                height: 1fr;
            }

            & #order-button {
                border: hkey $secondary;
            }
        }
    """

    def compose(self) -> ComposeResult:
        with TabbedContent(initial="order_book"):
            with TabPane("Limits", id="limits"):
                yield Label("Some limits")
            with TabPane("Positions", id="positions"):
                yield DataTable()
            with TabPane("Order Book", id="order_book"):
                yield DataTable(cursor_type="row")
                yield Button("Place Order", id="order-button")
            with TabPane("Trade Book", id="trade_book"):
                yield DataTable()
            with TabPane("User Details", id="user_details"):
                yield Label("Some Details")

    def on_mount(self) -> None:
        self.query_one("#order_book > DataTable").add_columns(
            "Item", "Qty", "Expected", "Status"
        )
        table: DataTable = self.query_one("#positions > DataTable")
        table.add_columns(*"Some positions I hold".split())
        table.add_rows([[1, 2, 3, 4], [5, 6, 7, 8]])
        table: DataTable = self.query_one("#trade_book > DataTable")
        table.add_columns(*"Trades in some empty table".split())
        table.add_rows([[1, 2, 3, 4, 5], [6, 7, 8, 9, 10]])

    @on(Button.Pressed, "#order-button")
    def place_order(self, event: Button.Pressed) -> None:
        self.query_one("#order_book > DataTable").add_row(
            f"Pencils HB (color code 1{random.randint(1, 19) * 5})",
            random.randint(1, 10) * 10,
            datetime.date.today() + datetime.timedelta(days=random.randint(2, 14)),
            "In Progress",
        )


TabsAndTablesApp().run()
